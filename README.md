# Easy-Enhance

影像增強評估工作檯 (Image Enhancement Evaluation Workbench)

## 專案簡介
Easy-Enhance 是一個專為影像增強研究設計的桌面工具，旨在提供一個標準化的流程來匯入增強方法、執行批次測試並自動計算品質指標。

## 核心功能
- **Plugin 架構**: 透過 ZIP 匯入自定義的影像增強方法。
- **批次處理**: 自動化執行影像增強任務，支援暫停/停止。
- **指標引擎**: 內建 PSNR, SSIM, LPIPS, NIQE, EME, BRISQUE 六種指標。
- **結果視覺化**: 即時顯示指標表格與動態趨勢圖 (Matplotlib)。
- **報告匯出**: 一鍵匯出 CSV 數據與趨勢圖表。

## 使用方式
1. **啟動程式**: 執行 `uv run python main.py`。
2. **匯入方法**: 點擊「匯入 Method ZIP」，選擇符合規範的插件壓縮檔。
3. **匯入資料集**: 點擊「匯入 Dataset ZIP」，選擇包含影像檔案的壓縮檔。
4. **執行測試**: 點擊「啟動批次任務」開始處理。
5. **檢視結果**: 在右側表格查看數據，或切換至「Trend Charts」查看指標趨勢。
6. **匯出報告**: 任務完成後，點擊「匯出評估報告」選擇儲存目錄。

## 檔案結構說明
```text
easy_enhance/
├── app/                # 程式核心邏輯 (GUI, Controller, Core)
├── plugins/            # [自動產生] 已解壓的增強方法插件
├── workspace/          # [自動產生] 包含 datasets (解壓後) 與 outputs (處理後影像)
├── .docs/              # 專案文件與開發進度表
├── dummy_brightener.zip # [範例] 用於測試的插件
├── sample_dataset.zip  # [範例] 用於測試的資料集
└── main.py             # 程式入口
```

## 插件開發規範 (Plugin Spec)
請參考 `.docs/spec.md` 以了解如何封裝您自己的影像增強方法。
