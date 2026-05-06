# Easy-Enhance 開發進度追蹤 (Checklist)

## Phase 1: MVP (最小可行性產品) - 進度: 100%

### Task 1: 專案初始化
- [x] 建立專案資料夾結構
- [x] 建立 `main.py`
- [x] 建立 `pyproject.toml`
- [x] 使用 `uv` 套件管理環境
- [x] 建立基礎 README
- [x] 建立虛擬環境與依賴安裝流程

### Task 2: GUI 主框架
- [x] 建立 `AppShell`
- [x] 建立主視窗布局 (Input, Queue, Result, Tab panels)
- [x] 建立輸入區、queue 區、結果區、圖表區、log 區
- [x] 套用 CustomTkinter 主題與外觀模式

### Task 3: ZIP 匯入與驗證
- [x] 實作 method ZIP 選取與載入
- [x] 實作 dataset ZIP 選取與載入
- [x] 實作解壓縮流程
- [x] 實作 validator (檢查必要檔案與 manifest)
- [x] 顯示驗證結果與錯誤訊息

### Task 4: Plugin 管理
- [x] 定義 plugin manifest 規格
- [x] 實作 Plugin Manager (安裝與覆蓋)
- [x] 驗證 `main.py` 與 `entry_function`
- [x] 建立 sample plugin 範例 (Dummy Brightener)
- [x] 建立 plugin 錯誤處理機制

### Task 5: Dataset 管理
- [x] 建立 Dataset Manager
- [x] 實作資料集影像索引 (支援多種格式)
- [x] 解析資料夾結構
- [x] 建立 image list metadata

### Task 6: Job Queue 與 Runner
- [x] 定義 job schema (Job dataclass)
- [x] 建立 Job Builder
- [x] 建立 Queue Manager
- [x] 實作單筆 job 執行流程 (Background Threading)
- [x] 記錄 job status、runtime、error_message
- [x] 加入停止與 retry 機制

### Task 7: Metrics Engine
- [x] 建立 PSNR 模組
- [x] 建立 SSIM 模組
- [x] 建立 LPIPS 模組 (經由 pyiqa)
- [x] 建立 NIQE 模組 (經由 pyiqa)
- [x] 建立 EME 模組 (自定義實作)
- [x] 建立 BRISQUE 模組 (經由 pyiqa)
- [x] 建立 metrics record 格式

### Task 8: 結果輸出
- [x] 產生逐圖 `results.csv`
- [x] 產生 `summary.csv`
- [x] 產生六張指標趨勢圖
- [x] 建立 log 輸出
- [x] 建立匯出按鈕與路徑管理

### Task 9: GUI 結果整合
- [x] 將 queue 狀態同步到 GUI (進度條)
- [x] 將 metrics table 綁定到結果區 (Treeview 更新)
- [x] 將 charts 綁定到 tab view (使用子分頁與 Matplotlib)
- [x] 將 logs 綁定到 log panel
- [x] 補強使用者回饋與例外提示

---

## Phase 2: 穩定化 (待啟動)
- [ ] 補強 queue 狀態管理 (暫停/續傳)
- [ ] 補強 log 系統 (持久化儲存)
- [ ] 補強失敗重試機制
- [ ] 改善資料輸出與匯出流程

## Phase 3: 擴充化 (待啟動)
- [ ] 支援多 methods 比較模式
- [ ] 支援更多 metrics
- [ ] 支援平行處理 (Multiprocessing)
- [ ] 自動生成完整評估報告
