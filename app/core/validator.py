import os
import zipfile
import json

class ImportValidator:
    @staticmethod
    def validate_method_zip(zip_path: str) -> tuple[bool, str, dict | None]:
        """
        驗證 Enhancement Method ZIP。
        必須包含: main.py, manifest.json
        """
        try:
            if not zipfile.is_zipfile(zip_path):
                return False, "檔案並非有效的 ZIP 格式", None

            with zipfile.ZipFile(zip_path, 'r') as z:
                file_list = [f.filename for f in z.infolist()]
                
                # 尋找根目錄名稱 (假設 ZIP 內有一個與 ZIP 檔名相同的資料夾，或是直接在根目錄)
                # 我們支持直接在根目錄或在單一層級資料夾內
                
                required_files = ["main.py", "manifest.json"]
                base_dir = ""
                
                # 檢查是否所有檔案都在一個子資料夾中
                first_file = file_list[0]
                if "/" in first_file:
                    potential_base = first_file.split("/")[0]
                    # 驗證是否所有檔案都有這個 prefix
                    if all(f.startswith(potential_base + "/") for f in file_list if not f.endswith("/")):
                        base_dir = potential_base + "/"

                # 檢查必要檔案
                found_files = []
                for req in required_files:
                    if (base_dir + req) in file_list:
                        found_files.append(req)
                
                if len(found_files) != len(required_files):
                    missing = set(required_files) - set(found_files)
                    return False, f"缺少必要檔案: {', '.join(missing)}", None

                # 讀取並驗證 manifest.json
                with z.open(base_dir + "manifest.json") as f:
                    manifest = json.load(f)
                    
                required_manifest_keys = ["method_name", "entry_file", "entry_function"]
                for key in required_manifest_keys:
                    if key not in manifest:
                        return False, f"manifest.json 缺少必要欄位: {key}", None
                
                return True, "驗證成功", manifest

        except Exception as e:
            return False, f"驗證過程發生錯誤: {str(e)}", None

    @staticmethod
    def validate_dataset_zip(zip_path: str) -> tuple[bool, str]:
        """
        驗證 Dataset ZIP。
        簡易版：檢查是否包含影像資料夾 (images/)
        """
        try:
            if not zipfile.is_zipfile(zip_path):
                return False, "檔案並非有效的 ZIP 格式"

            with zipfile.ZipFile(zip_path, 'r') as z:
                file_list = [f.filename for f in z.infolist()]
                
                # 檢查是否存在影像資料夾或任何影像檔案
                image_exts = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]
                has_images = any(any(f.lower().endswith(ext) for ext in image_exts) for f in file_list)
                
                if not has_images:
                    return False, "ZIP 內未發現有效的影像檔案"
                
                return True, "驗證成功"

        except Exception as e:
            return False, f"驗證過程發生錯誤: {str(e)}"
