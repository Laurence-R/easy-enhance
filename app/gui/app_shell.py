import customtkinter as ctk
from tkinter import ttk

class InputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label = ctk.CTkLabel(self, text="輸入與設定", font=("Arial", 16, "bold"))
        self.label.pack(pady=10, padx=10)

        # Method ZIP
        self.method_btn = ctk.CTkButton(self, text="匯入 Method ZIP")
        self.method_btn.pack(pady=5, padx=10, fill="x")
        self.method_path_label = ctk.CTkLabel(self, text="未選擇方法", font=("Arial", 10))
        self.method_path_label.pack(pady=2, padx=10)

        # Dataset ZIP
        self.dataset_btn = ctk.CTkButton(self, text="匯入 Dataset ZIP")
        self.dataset_btn.pack(pady=5, padx=10, fill="x")
        self.dataset_path_label = ctk.CTkLabel(self, text="未選擇資料集", font=("Arial", 10))
        self.dataset_path_label.pack(pady=2, padx=10)

        # Run Button
        self.run_btn = ctk.CTkButton(self, text="啟動批次任務", fg_color="green", hover_color="darkgreen")
        self.run_btn.pack(pady=10, padx=10, fill="x")

        # Stop Button
        self.stop_btn = ctk.CTkButton(self, text="停止任務", fg_color="red", hover_color="darkred", state="disabled")
        self.stop_btn.pack(pady=5, padx=10, fill="x")

        # Export Button
        self.export_btn = ctk.CTkButton(self, text="匯出評估報告", fg_color="gray", state="disabled")
        self.export_btn.pack(pady=10, padx=10, fill="x")

class QueueFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label = ctk.CTkLabel(self, text="任務排程與進度", font=("Arial", 16, "bold"))
        self.label.pack(pady=10, padx=10)

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=5, padx=10, fill="x")
        self.progress_bar.set(0)

        self.queue_list = ctk.CTkScrollableFrame(self, label_text="Job Queue")
        self.queue_list.pack(pady=5, padx=10, fill="both", expand=True)

class ResultsTableFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label = ctk.CTkLabel(self, text="Metrics Table", font=("Arial", 16, "bold"))
        self.label.pack(pady=5, padx=10)

        # Treeview for results
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=5, padx=10, fill="both", expand=True)

        columns = ("ID", "Image", "PSNR", "SSIM", "LPIPS", "NIQE", "EME", "BRISQUE", "Status")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class TabsFrame(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.add("Trend Charts")
        self.add("Execution Log")
        
        # Sub-tabs for metrics within Trend Charts
        self.charts_tabview = ctk.CTkTabview(self.tab("Trend Charts"))
        self.charts_tabview.pack(fill="both", expand=True)
        
        self.metric_names = ["PSNR", "SSIM", "LPIPS", "NIQE", "EME", "BRISQUE"]
        self.chart_containers = {}
        
        for name in self.metric_names:
            self.charts_tabview.add(name)
            # Container for Matplotlib canvas
            container = ctk.CTkFrame(self.charts_tabview.tab(name))
            container.pack(fill="both", expand=True)
            self.chart_containers[name] = container
        
        # Log Panel
        self.log_text = ctk.CTkTextbox(self.tab("Execution Log"), state="disabled")
        self.log_text.pack(fill="both", expand=True)

class AppShell(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Easy-Enhance - 影像增強評估工作檯")
        self.geometry("1300x900")

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Layout
        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.queue_frame = QueueFrame(self)
        self.queue_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.table_frame = ResultsTableFrame(self)
        self.table_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.tabs_frame = TabsFrame(self)
        self.tabs_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    app = AppShell()
    app.mainloop()
