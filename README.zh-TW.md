# ui-design — Codex UI 設計與審查 Skill

[English](README.md)

**整合設計、施工、審查、修正與驗證五種模式的 Codex Skill。** 優先考慮產品需求、既有 Design System、使用體驗與證據，不把「看起來像 AI 做的」直接當成缺陷。

> **版本狀態：** `v0.2.1`（Skill V2.1 未正式發行候選版）。[Repository 已公開](https://github.com/YihongTools/ui-design-skill)；截至 2026-10-14 尚無版本 tag 或 GitHub Release。單一 VERIFY smoke 的修正後驗收結果為 **PASS**，不代表 V2.1 整體品質或產品功能都通過。詳見[證據紀錄](evals/evidence.md)，評分僅供參考。

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

V2.1 強化參考優先方向（無人可答時有明確三方向備援）與 **Render → Critique → Revise**：無人回覆或「你決定」時寫三個實質不同方向並標記模型自行選擇；整頁預設替換表涵蓋主色系、字型、主要區域版型，只有使用者要求或其提供的需求文件明確固定且能逐字引用原句的列才能標示「由需求決定」；所有適用的設計選擇須在施工前回覆；被批評為樣板化的項目都要「已修改」或「刻意保留，因為……」逐項收尾。新畫面／大幅改版使用方向與預設表，局部微調沿用既有程式慣例；真正的既有 Design System 可讓受管轄列簡化，但未客製的 Material 3、Tailwind、shadcn 預設不算治理中的 Design System。若整個畫面已完整受 Design System 管轄，可跳過參考／三方向選擇，只留下精簡的受管轄列。字型使用系統字型組合或已核准的本機打包字型；無人可批准字型檔時，實作系統字型並把偏好字型記成建議。新增畫面或修改整頁版型、主色系、字體才算大幅改版。PLAN 依相同範圍輸出決策紀錄。完整操作契約在 [`ui-design/SKILL.md`](ui-design/SKILL.md)。規則不是硬性禁止特定字型、配色、卡片或設計風格。

## 雙語 Skill 文件

- [`ui-design/SKILL.md`](ui-design/SKILL.md)：V2.1 候選版英文主檔，**Codex 執行的唯一權威規格**。
- [`docs/SKILL.zh-TW.md`](docs/SKILL.zh-TW.md)：V2.1 繁體中文閱讀參考，放在 Skill 目錄外，若有差異以英文版為準。
- GitHub 更新不代表本機已同步。已安裝的 Codex 使用者可從獨立 Codex ZIP 將英文 `SKILL.md` 與同步後的中文閱讀檔更新到原本的 `ui-design` 資料夾，然後重啟 Codex 或建立新對話，不必重裝 Codex。英文主檔才是 Skill 執行入口，Repository 中的中文版則放在 `docs/`。

## 審查與評分

- 證據層：原始碼觀察、實際畫面、產品脈絡判斷（各自標示是否已驗證）。
- 可信度：`Confirmed`、`Probable`、`Candidate`、`Exempted`。
- 嚴重性：`High`、`Medium`、`Low`，以使用影響為主，而非「AI 味」強弱。
- **無內建數值評分器**。外部掃描結果只作輔助指標，不作 CI 通過門檻；不能宣稱它能衡量 UX 品質。

## 既有實測結果

V2 單組探索性視覺 A/B 的回報結論為 **INCONCLUSIVE**。V2.1 A/B 的該次案例回報為 **REGRESSED**：重新設計遺失必要的工作階段完成狀態，critique 也未發現。這些結論來自保留的 Owner 報告；本 Repository 未附原始 A/B artifacts，不能宣稱目前 BUILD 已修好該問題。

VERIFY 的歷程則不同：smoke-001 卡在 child 無法 Render；smoke-002 R1 因 installed Skill 不一致而停止，R2 已由 child 成功渲染並辨認 High 缺陷，但未遵守當時要求的輸出詞彙。smoke-003 使用了 exact Status labels；原 evaluator 卻把「顯示目前處理進度」擴成未要求的動態更新行為而判 FAIL。重評確認 evaluator 缺陷，修正後驗收為 **PASS**。這表示 VERIFY 能發現並分類故意保留的缺陷、且保持唯讀；fixture 本身仍缺少「審閱完成」狀態。各次結果與來源分開列於[證據紀錄](evals/evidence.md)。

動態更新、持久化、實體裝置、真人視覺驗收及完整 E2E 仍未驗證。本次回報格式澄清只做靜態檢查，沒有追加 runtime 或 A/B 實測。

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
