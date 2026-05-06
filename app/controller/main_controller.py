import os
import tkinter as tk
from tkinter import filedialog, messagebox
from app.core.plugin_manager import PluginManager
from app.core.dataset_manager import DatasetManager
from app.core.job_manager import JobManager, JobStatus
from app.metrics.metrics_engine import MetricsEngine
from app.core.report_manager import ReportManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainController:
    def __init__(self, view):
        self.view = view
        
        # Paths
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.plugins_dir = os.path.join(self.base_dir, "plugins")
        self.workspace_dir = os.path.join(self.base_dir, "workspace")
        
        # Services
        self.plugin_manager = PluginManager(self.plugins_dir)
        self.dataset_manager = DatasetManager(self.workspace_dir)
        self.job_manager = JobManager(self.workspace_dir)
        self._metrics_engine = None
        
        # State
        self.selected_method_id = None
        self.selected_dataset_id = None
        self.canvas_map = {} # metric_name -> canvas
        
        # Bind events
        self._bind_events()

    def _bind_events(self):
        self.view.input_frame.method_btn.configure(command=self._on_import_method)
        self.view.input_frame.dataset_btn.configure(command=self._on_import_dataset)
        self.view.input_frame.run_btn.configure(command=self._on_run_batch)
        self.view.input_frame.stop_btn.configure(command=self._on_stop)
        self.view.input_frame.export_btn.configure(command=self._on_export)

    def _on_stop(self):
        if self.job_manager.is_running:
            self._log("正在停止任務...")
            self.job_manager.stop_processing()
            self.view.input_frame.stop_btn.configure(state="disabled")

    def _log(self, message):
        def do_log():
            self.view.tabs_frame.log_text.configure(state="normal")
            self.view.tabs_frame.log_text.insert("end", f"{message}\n")
            self.view.tabs_frame.log_text.see("end")
            self.view.tabs_frame.log_text.configure(state="disabled")
        self.view.after(0, do_log)

    def _on_import_method(self):
        file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if not file_path:
            return
        
        success, message, method_id = self.plugin_manager.import_plugin(file_path)
        if success:
            self.selected_method_id = method_id
            self.view.input_frame.method_path_label.configure(text=method_id)
            self._log(f"成功匯入方法: {method_id}")
        else:
            messagebox.showerror("匯入失敗", message)
            self._log(f"方法匯入失敗: {message}")

    def _on_import_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if not file_path:
            return
        
        success, message, dataset_id = self.dataset_manager.import_dataset(file_path)
        if success:
            self.selected_dataset_id = dataset_id
            self.view.input_frame.dataset_path_label.configure(text=dataset_id)
            self._log(f"成功匯入資料集: {dataset_id}")
        else:
            messagebox.showerror("匯入失敗", message)
            self._log(f"資料集匯入失敗: {message}")

    def _on_run_batch(self):
        if not self.selected_method_id or not self.selected_dataset_id:
            messagebox.showwarning("提示", "請先匯入方法與資料集")
            return
        
        images = self.dataset_manager.get_dataset_images(self.selected_dataset_id)
        if not images:
            messagebox.showwarning("提示", "資料集內無影像")
            return
        
        # 取得插件執行器
        runner_func, error = self.plugin_manager.get_plugin_runner(self.selected_method_id)
        if error:
            messagebox.showerror("錯誤", f"無法啟動插件: {error}")
            return

        # 建立任務
        job_ids = self.job_manager.create_jobs(self.selected_method_id, self.selected_dataset_id, images)
        self._log(f"已建立 {len(job_ids)} 個任務，開始執行...")
        
        # 清空舊表格
        for item in self.view.table_frame.tree.get_children():
            self.view.table_frame.tree.delete(item)
            
        # 清空舊 Queue List
        for widget in self.view.queue_frame.queue_list.winfo_children():
            widget.destroy()
            
        # 初始化表格列
        self.job_labels = {} # job_id -> label
        for job_id in job_ids:
            job = self.job_manager.jobs[job_id]
            self.view.table_frame.tree.insert("", "end", iid=job_id, values=(
                job_id[:8], os.path.basename(job.input_path), "", "", "", "", "", "", "Pending"
            ))
            
            # Add to Queue List
            lbl = tk.Label(self.view.queue_frame.queue_list, text=f"{os.path.basename(job.input_path)}: Pending", fg="white", bg="#2b2b2b")
            lbl.pack(fill="x", padx=5, pady=2)
            self.job_labels[job_id] = lbl

        # 啟動處理
        self.view.input_frame.run_btn.configure(state="disabled")
        self.view.input_frame.stop_btn.configure(state="normal")
        self.view.input_frame.export_btn.configure(state="disabled", fg_color="gray")
        
        self.job_manager.start_processing(
            runner_func=runner_func,
            on_job_complete_cb=self._on_job_complete
        )

    @property
    def metrics_engine(self):
        if self._metrics_engine is None:
            self._metrics_engine = MetricsEngine()
        return self._metrics_engine

    def _on_job_complete(self, job):
        try:
            self._log(f"任務完成: {os.path.basename(job.input_path)} - {job.status.value}")
            
            if job.status == JobStatus.SUCCESS:
                # 計算品質指標
                metrics = self.metrics_engine.calculate_all(job.input_path, job.output_path)
                job.metrics = metrics
        except Exception as e:
            self._log(f"指標計算出錯: {os.path.basename(job.input_path)} - {str(e)}")
            
        # 無論指標是否成功，都要更新表格狀態 (success/failed)
        self.view.after(0, self._update_gui_job_status, job)

    def _update_gui_job_status(self, job):
        try:
            m = job.metrics if job.metrics else {}
            # 更新 Queue List 中的 Label
            if job.job_id in self.job_labels:
                color = "white"
                if job.status == JobStatus.SUCCESS: color = "green"
                elif job.status == JobStatus.FAILED: color = "red"
                self.job_labels[job.job_id].config(text=f"{os.path.basename(job.input_path)}: {job.status.value}", fg=color)

            # 確保 iid 與 job.job_id 一致
            self.view.table_frame.tree.item(job.job_id, values=(
                job.job_id[:8], 
                os.path.basename(job.input_path),
                f"{m.get('psnr', 0):.2f}" if 'psnr' in m else "-",
                f"{m.get('ssim', 0):.4f}" if 'ssim' in m else "-",
                f"{m.get('lpips', 0):.4f}" if 'lpips' in m else "-",
                f"{m.get('niqe', 0):.2f}" if 'niqe' in m else "-",
                f"{m.get('eme', 0):.2f}" if 'eme' in m else "-",
                f"{m.get('brisque', 0):.2f}" if 'brisque' in m else "-",
                job.status.value
            ))
            
            total_jobs = len(self.job_manager.jobs)
            completed_jobs = sum(1 for j in self.job_manager.jobs.values() if j.status in [JobStatus.SUCCESS, JobStatus.FAILED])
            self.view.queue_frame.progress_bar.set(completed_jobs / total_jobs)

            if completed_jobs == total_jobs:
                self._log("所有任務已完成！")
                self.view.input_frame.run_btn.configure(state="normal")
                self.view.input_frame.stop_btn.configure(state="disabled")
                self.view.input_frame.export_btn.configure(state="normal", fg_color="blue")
                self._update_charts()
        except Exception as e:
            print(f"GUI Update Error: {e}")

    def _update_charts(self):
        """
        在 GUI 畫面上更新趨勢圖
        """
        # 整理數據
        data = []
        for job in self.job_manager.jobs.values():
            if job.status == JobStatus.SUCCESS:
                row = {"image": os.path.basename(job.input_path)}
                row.update(job.metrics)
                data.append(row)
        
        if not data:
            return

        import pandas as pd
        df = pd.DataFrame(data)
        
        metrics_map = {
            "PSNR": "psnr", "SSIM": "ssim", "LPIPS": "lpips",
            "NIQE": "niqe", "EME": "eme", "BRISQUE": "brisque"
        }

        for display_name, internal_name in metrics_map.items():
            if internal_name in df.columns:
                container = self.view.tabs_frame.chart_containers[display_name]
                
                # 清除舊的 canvas
                for widget in container.winfo_children():
                    widget.destroy()

                fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
                ax.plot(df["image"], df[internal_name], marker='o', color='b')
                ax.set_title(f"{display_name} Trend")
                ax.tick_params(axis='x', rotation=45)
                fig.tight_layout()

                canvas = FigureCanvasTkAgg(fig, master=container)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                plt.close(fig)

    def _on_export(self):
        export_dir = filedialog.askdirectory(title="選擇匯出目錄")
        if not export_dir:
            return
            
        try:
            # 產生 CSV
            ReportManager.generate_csv(self.job_manager.jobs, export_dir)
            # 產生圖表圖片
            ReportManager.export_charts(self.job_manager.jobs, export_dir)
            
            self._log(f"報告已成功匯出至: {export_dir}")
            messagebox.showinfo("成功", f"報告已匯出至 {export_dir}")
        except Exception as e:
            self._log(f"匯出失敗: {str(e)}")
            messagebox.showerror("錯誤", f"匯出失敗: {str(e)}")
