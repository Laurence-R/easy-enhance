# Easy-Enhance Task Plan

## 開發任務目標

本文件定義 Easy-Enhance 的實作任務拆解、開發階段、優先順序與交付項目，作為開發排程與追蹤依據。

## 任務拆解

### Task 1：專案初始化

- 建立專案資料夾結構
- 建立 `main.py`
- 建立 `pyproject.toml`
- 使用 `uv` 套件管理環境
- 建立基礎 README
- 建立虛擬環境與依賴安裝流程

### Task 2：GUI 主框架

- 建立 `AppShell`
- 建立主視窗布局
- 建立輸入區、queue 區、結果區、圖表區、log 區
- 套用 CustomTkinter 主題與外觀模式

### Task 3：ZIP 匯入與驗證

- 實作 method ZIP 選取與載入
- 實作 dataset ZIP 選取與載入
- 實作解壓縮流程
- 實作 validator
- 顯示驗證結果與錯誤訊息

### Task 4：Plugin 管理

- 定義 plugin manifest 規格
- 實作 Plugin Manager
- 驗證 `main.py` 與 `entry_function`
- 建立 sample plugin 範例
- 建立 plugin 錯誤處理機制

### Task 5：Dataset 管理

- 建立 Dataset Manager
- 實作資料集影像索引
- 解析資料夾結構與描述檔
- 建立 image list metadata

### Task 6：Job Queue 與 Runner

- 定義 job schema
- 建立 Job Builder
- 建立 Queue Manager
- 實作單筆 job 執行流程
- 記錄 job status、runtime、error_message
- 加入停止與 retry 機制

### Task 7：Metrics Engine

- 建立 PSNR 模組
- 建立 SSIM 模組
- 建立 LPIPS 模組
- 建立 NIQE 模組
- 建立 EME 模組
- 建立 BRISQUE 模組
- 建立 metrics record 格式

### Task 8：結果輸出

- 產生逐圖 `results.csv`
- 產生 `summary.csv`
- 產生六張指標趨勢圖
- 建立 log 輸出
- 建立匯出按鈕與路徑管理

### Task 9：GUI 結果整合

- 將 queue 狀態同步到 GUI
- 將 metrics table 綁定到結果區
- 將 charts 綁定到 tab view
- 將 logs 綁定到 log panel
- 補強使用者回饋與例外提示

### Task 10：測試與穩定化

- 單元測試 validator
- 單元測試 plugin manager
- 單元測試 queue manager
- 單元測試 metrics engine
- 整合測試完整流程
- GUI 操作測試
- 錯誤情境測試

## 開發階段規劃

### Phase 1：MVP

交付目標：先跑通完整流程。

- 完成主視窗與基本 GUI
- 完成 ZIP 匯入與解壓
- 完成 plugin 驗證基本版
- 完成單一 method + dataset 的批次執行
- 完成六種 metrics 計算
- 完成逐圖 table 與六張 line charts

### Phase 2：穩定化

交付目標：讓系統更能實際使用。

- 補強 queue 狀態管理
- 補強 log 系統
- 補強失敗重試
- 補強 GUI 響應與錯誤提示
- 改善資料輸出與匯出流程

### Phase 3：擴充化

交付目標：提升研究使用價值。

- 支援多 methods 比較模式
- 支援更多 metrics
- 支援更多 dataset profile
- 支援平行處理
- 支援完整報告輸出

## 優先順序

### 高優先

- GUI 主框架
- ZIP 匯入與驗證
- Plugin Manager
- Job Queue
- Runner
- Metrics Engine
- Result Table
- Trend Charts

### 中優先

- Retry 機制
- 匯出摘要表
- 更完整的 log 系統
- GUI 錯誤提示優化

### 低優先

- 多 methods 同時比較
- 多 worker 平行處理
- 自動生成完整報告
- 主題切換與外觀微調

## 建議里程碑

| 里程碑 | 內容 | 驗收方式 |
|---|---|---|
| M1 | 完成 GUI 骨架與檔案匯入 | 可選取 ZIP 並顯示檔名 |
| M2 | 完成 validator、plugin 載入、dataset 索引 | 可正確驗證與解析輸入 |
| M3 | 完成 job queue 與 runner | 可逐張執行影像增強 |
| M4 | 完成 metrics engine | 可輸出六項指標 |
| M5 | 完成 table 與六張 charts | GUI 可檢視結果 |
| M6 | 完成匯出與 log | 可匯出 CSV 與圖表 |
| M7 | 完成測試與穩定化 | 系統可重複執行且錯誤可追蹤 |

## 驗收標準

- 能成功匯入合法 method ZIP 與 dataset ZIP
- 能拒絕不合法 ZIP
- 能建立 jobs 並逐張執行
- 能計算六種 metrics
- 能顯示逐圖結果表
- 能顯示六張趨勢圖
- 能記錄 log 與錯誤訊息
- 能匯出 CSV 與圖表

## 風險與對策

| 風險 | 說明 | 對策 |
|---|---|---|
| Plugin 規格不一致 | 不同方法輸入輸出差異太大 | 先嚴格定義 manifest 與入口函式 |
| GUI 卡頓 | 執行流程阻塞主執行緒 | 將執行流程與 GUI 更新分離 |
| Metrics 相依複雜 | 某些指標需要額外套件 | 模組化封裝並建立 fallback 處理 |
| 大型資料集耗時 | 批次任務過長 | 先做進度追蹤與中斷機制 |
| 錯誤難追 | 執行中失敗不易定位 | 建立完整 log 與 job status 記錄 |

## 最終交付項目

- 可執行的 Easy-Enhance 桌面程式
- plugin 規格文件
- sample plugin
- 完整原始碼
- 測試程式
- 使用說明文件
- 規格文件（purpose / spec / task）

## 結語

task 文件的目的，是把 Easy-Enhance 從概念與規格，落實成可執行的開發清單。後續實作時，可直接以本文件作為開發追蹤、里程碑驗收與專題進度管理基準。
