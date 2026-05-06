import os
import zipfile
import shutil
import importlib.util
import sys
from app.core.validator import ImportValidator

class PluginManager:
    def __init__(self, plugins_dir: str):
        self.plugins_dir = plugins_dir
        self.plugins = {} # method_id -> manifest
        
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir)

    def import_plugin(self, zip_path: str) -> tuple[bool, str, str | None]:
        """
        匯入並安裝插件。
        傳回: (成功, 訊息, method_id)
        """
        success, message, manifest = ImportValidator.validate_method_zip(zip_path)
        if not success:
            return False, message, None
        
        method_name = manifest["method_name"]
        target_dir = os.path.join(self.plugins_dir, method_name)
        
        # 如果已存在，先刪除舊的 (或報錯，這裡選擇覆蓋)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # 處理可能是包在資料夾內的 ZIP
                file_list = z.namelist()
                first_file = file_list[0]
                has_subdir = False
                if "/" in first_file:
                    potential_base = first_file.split("/")[0]
                    if all(f.startswith(potential_base + "/") for f in file_list if not f.endswith("/")):
                        has_subdir = True
                        base_prefix = potential_base + "/"
                
                if has_subdir:
                    # 解壓並移動內容
                    temp_extract = target_dir + "_temp"
                    z.extractall(temp_extract)
                    shutil.move(os.path.join(temp_extract, potential_base), target_dir)
                    shutil.rmtree(temp_extract)
                else:
                    z.extractall(target_dir)
            
            self.plugins[method_name] = manifest
            return True, f"插件 {method_name} 已成功匯入", method_name
            
        except Exception as e:
            return False, f"解壓插件時發生錯誤: {str(e)}", None

    def get_plugin_runner(self, method_id: str):
        """
        動態載入插件的入口函式。
        """
        if method_id not in self.plugins:
            return None, "找不到該插件"
        
        manifest = self.plugins[method_id]
        plugin_path = os.path.join(self.plugins_dir, method_id)
        entry_file = manifest["entry_file"]
        entry_func_name = manifest["entry_function"]
        
        module_path = os.path.join(plugin_path, entry_file)
        
        try:
            # 動態載入模組
            spec = importlib.util.spec_from_file_location(f"plugin.{method_id}", module_path)
            module = importlib.util.module_from_spec(spec)
            
            # 加入 plugin 目錄到 sys.path 以便 plugin 內部的相對匯入
            if plugin_path not in sys.path:
                sys.path.insert(0, plugin_path)
                
            spec.loader.exec_module(module)
            
            if hasattr(module, entry_func_name):
                return getattr(module, entry_func_name), None
            else:
                return None, f"模組中找不到入口函式: {entry_func_name}"
        except Exception as e:
            return None, f"載入模組失敗: {str(e)}"
