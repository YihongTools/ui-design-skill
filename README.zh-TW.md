# ui-design — Codex UI 設計與審查 Skill

[English](README.md)

**整合設計、施工、審查、修正與驗證五種模式的 Codex Skill。** 優先考慮產品需求、既有 Design System、使用體驗與證據，不把「看起來像 AI 做的」直接當成缺陷。

> **版本狀態：** `v0.2.0`（Skill V2）。已建立可發布的 Repository 結構及靜態檢查；**尚未完成真實 Codex 行為測試、瀏覽器／裝置渲染測試或 UI E2E 驗證**。評分僅供參考。

## 五種模式

| 模式 | 功能 | 預設權限 |
| --- | --- | --- |
| `PLAN` | 設計方向、內容層級、Design Tokens、驗收條件 | 唯讀 |
| `BUILD` | 實作已核准的 UI 範圍 | 僅修改授權範圍 |
| `AUDIT` | 檢查 UI 品質與 AI 制式化特徵，提出證據 | 唯讀 |
| `FIX` | 修正已確認、已授權的問題 | 最小且可回復修改 |
| `VERIFY` | 驗證畫面、互動、響應式與適當的回歸測試 | 限界驗證，不擅自重設計 |

## 八大治理規則

1. **Design Authority 優先**：明確 Owner 決策、既有 Design System、品牌、平台慣例和可及性要求優於通用美學偏好。
2. **刻意選擇預設設計**：不要無意識沿用框架外觀；若適合產品，則可保留。
3. **控制裝飾**：漸層、陰影、發光、模糊、圖示和動畫要有可說明的用途。
4. **建立資訊層級**：優先使用字體、間距、對比和對齊，不濫用巢狀卡片。
5. **一致但不僵化**：沿用 Tokens 與元件語意，不強制通用字型、色彩比例或圓角數值。
6. **依內容決定版面**：不預設置中 Hero、三欄卡片或 CTA 套版。
7. **動態效果要有目的**：支援操作回饋與狀態，尊重 reduced-motion。
8. **Audit 必須有證據**：指出位置、觀察、影響、可信度、嚴重程度、最小改善及合理例外。

新版加入參考風格先行的 Greenfield 設計流程，以及最多兩輪修正的 **Render → Critique → Revise** 渲染回饋迴圈。完整操作契約在 [`ui-design/SKILL.md`](ui-design/SKILL.md)。規則不是硬性禁止特定字型、配色、卡片或設計風格。

## 雙語 Skill 文件

- [`ui-design/SKILL.md`](ui-design/SKILL.md)：V2 英文版，**Codex 執行的唯一權威規格**。
- [`ui-design/SKILL.zh-TW.md`](ui-design/SKILL.zh-TW.md)：V2 繁體中文閱讀版，**不是第二個 Skill**，不會取代英文檔；若有差異，以英文版為準。
- GitHub 更新不代表本機已同步。已安裝的 Codex 使用者需將兩個檔案更新到原本的 `ui-design` 資料夾，然後重啟 Codex 或建立新對話，不必重裝 Codex。

## 審查與評分

- 證據層：原始碼觀察、實際畫面、產品脈絡判斷（各自標示是否已驗證）。
- 可信度：`Confirmed`、`Probable`、`Candidate`、`Exempted`。
- 嚴重性：`High`、`Medium`、`Low`，以使用影響為主，而非「AI 味」強弱。
- **無內建數值評分器**。外部掃描結果只作輔助指標，不作 CI 通過門檻；不能宣稱它能衡量 UX 品質。

## 安裝到 Windows Codex

從 **GitHub Repository** 安裝，可在 Codex 使用：

```text
$skill-installer install https://github.com/YihongTools/ui-design-skill/tree/main/ui-design
```

或者下載完整 Repository／從本機目錄安裝（PowerShell 5.1 或 7；在 Repository 根目錄執行）：

```powershell
$source = Join-Path (Get-Location) 'ui-design'
$target = Join-Path $HOME '.agents\skills\ui-design'
if (-not (Test-Path (Join-Path $source 'SKILL.md'))) { throw '請在 Repository 根目錄執行。' }
if (Test-Path $target) { throw 'ui-design 已存在，請先確認，避免覆蓋。' }
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Recurse
Test-Path (Join-Path $target 'SKILL.md')
```

預期輸出 `True`。Skill 應放在使用者層級的 `.agents/skills/ui-design`，不要把整個 GitHub Repository 複製進 Skill 目錄。如果你目前使用的 `$skill-installer` 採 `$CODEX_HOME/skills`（通常為 `.codex/skills`），請依當前 Codex 文件與環境擇一安裝，避免同名 Skill 重複。若安裝後未列出，重新啟動 Codex。

## 使用範例

```text
$ui-design PLAN：依現有 Design System 規劃 Settings 畫面，不修改程式碼。
$ui-design AUDIT：唯讀檢查此畫面的 UI，提供檔案／行號與證據層，禁止修正。
$ui-design BUILD：只實作已核准的畫面，最後回報實際驗證範圍。
$ui-design FIX：只修正已確認的 UI-03，避免無關重設計。
$ui-design VERIFY：檢查修改後的畫面，列出尚未實測的裝置／瀏覽器項目。
```

## 如何檢查與實測

在 Repository 根目錄執行（需 Python 3）：

```sh
python scripts/validate_skill.py
python -m unittest discover -s scripts -p 'test_*.py' -v
```

以上僅檢查 Skill 格式及契約文字，不能證明 Codex 會正確啟動或遵守規則。

完成安裝後，再依 [`evals/README.md`](evals/README.md) 的 **evaluation-first** 規格，在乾淨的測試工作目錄執行 Codex 實測。`evals/cases.json` 是測試案例，不是已通過的測試結果。

## 來源、授權與限制

設計理念參考 [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) 與 [anti-ui-slop](https://github.com/discountry/ritmex-skills/tree/main/skills/anti-ui-slop)。這份 Skill 是獨立撰寫的整合規則，**未附帶上游程式碼或完整規則目錄，也非上游官方認可版本**；請參考 [`ATTRIBUTION.md`](ATTRIBUTION.md)。

此 Repository 的原創內容採用 [MIT](LICENSE)，已於 2026-10-13 取得 Repository Owner 同意。發布、push、建立 Release 及修改他人的 repository 均不屬於 Skill 自動授權範圍。