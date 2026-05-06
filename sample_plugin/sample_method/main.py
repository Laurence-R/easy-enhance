import cv2
import os
import time

def run(input_path: str, output_path: str, config: dict | None = None) -> dict:
    """
    Dummy Enhancement: Just brighten the image slightly.
    """
    start_time = time.time()
    try:
        img = cv2.imread(input_path)
        if img is None:
            return {"status": "failed", "message": f"Could not read image {input_path}"}
            
        # Brighten
        enhanced = cv2.convertScaleAbs(img, alpha=1.2, beta=10)
        
        cv2.imwrite(output_path, enhanced)
        
        return {
            "status": "success",
            "runtime": time.time() - start_time,
            "message": "done"
        }
    except Exception as e:
        return {"status": "failed", "message": str(e)}
