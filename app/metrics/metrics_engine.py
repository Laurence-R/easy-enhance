import cv2
import numpy as np
import os
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import torch

try:
    import pyiqa
except ImportError:
    pyiqa = None

class MetricsEngine:
    def __init__(self):
        self.device = None
        self.iqa_metrics = {}
        self.metric_names = ["lpips", "niqe", "brisque"]

    def _ensure_torch(self):
        if self.device is None:
            import torch
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"MetricsEngine initialized on {self.device}")

    def _load_metric(self, name):
        self._ensure_torch()
        if pyiqa and name not in self.iqa_metrics:
            try:
                # 某些指標在第一次執行時會下載權重
                self.iqa_metrics[name] = pyiqa.create_metric(name, device=self.device)
            except Exception as e:
                print(f"Failed to load metric {name}: {e}")
                return None
        return self.iqa_metrics.get(name)

    def calculate_eme(self, img):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        img = img.astype(np.float32) + 1e-5
        h, w = img.shape
        block_size = 8
        
        eme = 0
        blocks_h = h // block_size
        blocks_w = w // block_size
        
        for i in range(blocks_h):
            for j in range(blocks_w):
                block = img[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size]
                m1 = np.max(block)
                m2 = np.min(block)
                if m2 > 0:
                    val = m1 / m2
                    if val > 1:
                        eme += 20 * np.log(val)
        
        return eme / (blocks_h * blocks_w + 1e-5)

    def calculate_all(self, ref_path, enhanced_path):
        results = {}
        
        if not os.path.exists(enhanced_path):
            return {"error": f"檔案不存在: {enhanced_path}"}
            
        img_enhanced = cv2.imread(enhanced_path)
        if img_enhanced is None:
            return {"error": "無法讀取增強後的影像"}
            
        # Non-reference metrics
        results["eme"] = self.calculate_eme(img_enhanced)
        
        niqe_model = self._load_metric("niqe")
        if niqe_model:
            try:
                results["niqe"] = float(niqe_model(enhanced_path))
            except: pass
            
        brisque_model = self._load_metric("brisque")
        if brisque_model:
            try:
                results["brisque"] = float(brisque_model(enhanced_path))
            except: pass
            
        # Reference metrics
        if ref_path and os.path.exists(ref_path):
            img_ref = cv2.imread(ref_path)
            if img_ref is not None:
                if img_ref.shape != img_enhanced.shape:
                    img_ref = cv2.resize(img_ref, (img_enhanced.shape[1], img_enhanced.shape[0]))
                
                results["psnr"] = psnr(img_ref, img_enhanced)
                results["ssim"] = ssim(img_ref, img_enhanced, channel_axis=2)
                
                lpips_model = self._load_metric("lpips")
                if lpips_model:
                    try:
                        results["lpips"] = float(lpips_model(enhanced_path, ref_path))
                    except: pass
        
        return results
