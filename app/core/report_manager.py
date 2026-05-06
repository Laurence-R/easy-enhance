import os
import pandas as pd
import matplotlib.pyplot as plt

class ReportManager:
    @staticmethod
    def generate_csv(jobs_dict, export_dir):
        """
        產生 results.csv 與 summary.csv
        """
        data = []
        for job in jobs_dict.values():
            row = {
                "job_id": job.job_id,
                "image_name": os.path.basename(job.input_path),
                "method_id": job.method_id,
                "dataset_id": job.dataset_id,
                "status": job.status.value,
                "runtime": job.runtime
            }
            # 合併指標
            row.update(job.metrics)
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # 1. Results CSV
        results_path = os.path.join(export_dir, "results.csv")
        df.to_csv(results_path, index=False, encoding='utf-8-sig')
        
        # 2. Summary CSV
        metrics_cols = ["psnr", "ssim", "lpips", "niqe", "eme", "brisque"]
        # 只選取存在的指標列
        existing_metrics = [c for c in metrics_cols if c in df.columns]
        
        if not df.empty and existing_metrics:
            summary_df = df[existing_metrics].agg(['mean', 'std', 'min', 'max']).transpose()
            summary_path = os.path.join(export_dir, "summary.csv")
            summary_df.to_csv(summary_path, encoding='utf-8-sig')
            
        return results_path

    @staticmethod
    def export_charts(jobs_dict, export_dir):
        """
        將六種指標繪製成圖表並儲存
        """
        data = []
        for job in jobs_dict.values():
            if job.status.value == "success":
                row = {"image": os.path.basename(job.input_path)}
                row.update(job.metrics)
                data.append(row)
        
        if not data:
            return
            
        df = pd.DataFrame(data)
        metrics = ["psnr", "ssim", "lpips", "niqe", "eme", "brisque"]
        
        saved_paths = []
        for m in metrics:
            if m in df.columns:
                plt.figure(figsize=(10, 6))
                plt.plot(df["image"], df[m], marker='o', linestyle='-', color='b')
                plt.title(f"Trend of {m.upper()}")
                plt.xlabel("Image")
                plt.ylabel("Value")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                path = os.path.join(export_dir, f"{m}_trend.png")
                plt.savefig(path)
                plt.close()
                saved_paths.append(path)
        
        return saved_paths
