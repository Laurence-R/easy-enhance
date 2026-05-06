import os
import uuid
import time
from dataclasses import dataclass, field
from enum import Enum
from threading import Thread, Lock
from queue import Queue

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class Job:
    job_id: str
    method_id: str
    dataset_id: str
    input_path: str
    output_path: str
    status: JobStatus = JobStatus.PENDING
    runtime: float = 0.0
    error_message: str = ""
    metrics: dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    finished_at: float | None = None

class JobManager:
    def __init__(self, workspace_dir: str):
        self.workspace_dir = workspace_dir
        self.output_dir = os.path.join(workspace_dir, "outputs")
        self.jobs = {} # job_id -> Job
        self.queue = Queue()
        self.is_running = False
        self.lock = Lock()
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_jobs(self, method_id: str, dataset_id: str, input_images: list[str]) -> list[str]:
        """
        建立批次任務。
        """
        new_job_ids = []
        method_output_dir = os.path.join(self.output_dir, f"{method_id}_{dataset_id}")
        if not os.path.exists(method_output_dir):
            os.makedirs(method_output_dir)
            
        for img_path in input_images:
            job_id = str(uuid.uuid4())
            filename = os.path.basename(img_path)
            output_path = os.path.join(method_output_dir, filename)
            
            job = Job(
                job_id=job_id,
                method_id=method_id,
                dataset_id=dataset_id,
                input_path=img_path,
                output_path=output_path
            )
            
            with self.lock:
                self.jobs[job_id] = job
                self.queue.put(job_id)
                new_job_ids.append(job_id)
        
        return new_job_ids

    def start_processing(self, runner_func, on_job_complete_cb=None):
        """
        啟動背景執行執行緒。
        runner_func: (input_path, output_path) -> dict
        """
        if self.is_running:
            return
        
        self.is_running = True
        thread = Thread(target=self._worker, args=(runner_func, on_job_complete_cb), daemon=True)
        thread.start()

    def _worker(self, runner_func, on_job_complete_cb):
        while self.is_running and not self.queue.empty():
            try:
                job_id = self.queue.get(timeout=1)
                job = self.jobs[job_id]
                
                with self.lock:
                    job.status = JobStatus.RUNNING
                
                start_time = time.time()
                try:
                    # 執行影像增強
                    result = runner_func(job.input_path, job.output_path)
                    
                    with self.lock:
                        if result.get("status") == "success":
                            job.status = JobStatus.SUCCESS
                        else:
                            job.status = JobStatus.FAILED
                            job.error_message = result.get("message", "Unknown error")
                        
                        job.runtime = time.time() - start_time
                        job.finished_at = time.time()
                except Exception as e:
                    with self.lock:
                        job.status = JobStatus.FAILED
                        job.error_message = str(e)
                        job.runtime = time.time() - start_time
                        job.finished_at = time.time()
                
                if on_job_complete_cb:
                    on_job_complete_cb(job)
                    
                self.queue.task_done()
            except Exception:
                continue
        
        self.is_running = False

    def stop_processing(self):
        self.is_running = False
        with self.lock:
            # 清空剩餘隊列
            while not self.queue.empty():
                try:
                    job_id = self.queue.get_nowait()
                    job = self.jobs[job_id]
                    job.status = JobStatus.FAILED
                    job.error_message = "Cancelled by user"
                    self.queue.task_done()
                except:
                    break
