import os
import zipfile
import shutil
from app.core.validator import ImportValidator

class DatasetManager:
    def __init__(self, workspace_dir: str):
        self.datasets_dir = os.path.join(workspace_dir, "datasets")
        self.datasets = {} # dataset_id -> {image_paths: []}
        
        if not os.path.exists(self.datasets_dir):
            os.makedirs(self.datasets_dir)

    def import_dataset(self, zip_path: str) -> tuple[bool, str, str | None]:
        """
        匯入資料集。
        """
        success, message = ImportValidator.validate_dataset_zip(zip_path)
        if not success:
            return False, message, None
        
        dataset_name = os.path.splitext(os.path.basename(zip_path))[0]
        target_dir = os.path.join(self.datasets_dir, dataset_name)
        
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(target_dir)
            
            # 索引影像
            image_exts = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]
            images = []
            for root, _, files in os.walk(target_dir):
                for f in files:
                    if any(f.lower().endswith(ext) for ext in image_exts):
                        images.append(os.path.join(root, f))
            
            if not images:
                return False, "資料集內未發現影像", None
                
            self.datasets[dataset_name] = {
                "path": target_dir,
                "images": sorted(images)
            }
            
            return True, f"資料集 {dataset_name} 已成功匯入，共 {len(images)} 張影像", dataset_name
            
        except Exception as e:
            return False, f"解壓資料集時發生錯誤: {str(e)}", None

    def get_dataset_images(self, dataset_id: str) -> list[str]:
        if dataset_id in self.datasets:
            return self.datasets[dataset_id]["images"]
        return []
