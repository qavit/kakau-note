# 單篇稽核：整體法系列第 4 篇〈整體法的真正公式：從三物體連結體到廣義座標〉

稽核日期：2026-11-09　對象：`_posts/2026-11-08-system-method-general-formula.md`（commit `08345ae`）

## 1. 範圍

| 項目 | 內容 |
|---|---|
| Scope | Single Asset |
| Population | 1 篇：`2026-11-08-system-method-general-formula`，及其兩組圖 `assets/img/posts/system-method-general-formula/` |
| Layers | L1 科學、L2 教學、L3 架構（連結）、L4 funnel（只查有無手寫 CTA）、L5 本機渲染 |
| 未涵蓋 | Search Console 資料；第 1–3 篇的 L1 內容稽核（只檢查了本篇引用的數值） |
| Decision supported | 本篇能否移除 DRAFT 註解 |
| Baseline | `docs/audits/coverage.md` 無本系列紀錄；本篇是首次稽核 |

## 2. Executive summary

- 無 BLOCKER、無 P1。所有數值與推導重算通過。
- 5 個文字層 finding（P2×3、P3×2），皆已在本次修正（未 commit）。
- 一個發布層風險不在本篇內容：正式站目前回 404（見 §7），因此 L5 只完成本機渲染，不能標為正式站通過。

## 3. Findings register

| ID | Layer | Severity | Finding | Evidence | Recommendation | 狀態 |
|---|---|---|---|---|---|---|
| A-001 | L1 | P2 | 「在四個題目裡把 $\sum c_iR_i$ 算出來每次都是 0」：本篇只對本題寫出此算式，前三題的算式不在本篇中，屬於未在文內支持的主張 | 原 `:219` | 改成只宣稱本題逐項算過，前三題說明為「同樣的加權相加」 | 已修 |
| A-002 | L1 | P2 | 「換成有摩擦的系統，這個規律就不再成立」過度概括：大小已知的動摩擦力可併入已知外力 $F_i$，公式仍適用 | 原 `:227` | 區分「大小與方向未知的約束力（如靜摩擦）」與「已知大小的動摩擦」 | 已修 |
| A-003 | L1 | P3 | 質心加速度寫成「質量加權向量和」，少了除以總質量 | 原 `:195` | 改為「質量加權平均」 | 已修 |
| A-004 | L1 | P3 | 功率推導「消去 $\dot q$」在 $\dot q=0$（靜止瞬間）不成立 | 原 `:250` | 補「在 $\dot q\neq0$ 的時刻」 | 已修 |
| A-005 | L2 | P2 | 「第三篇的延伸也算出同樣的 11 與 g」：本篇是 15 與 g，「同樣」會讓讀者誤以為數字相同 | 原 `:252` | 明寫 11 vs 15，做法相同 | 已修 |
| A-006 | L3 | P2 | 本篇上線時沒有任何站內連入（第 3 篇結尾仍寫「未來」）→ orphan | `grep` 無他篇連到本篇 | 第 3 篇結尾改成 `post_url` 連結 | 已修（第 3 篇已改） |
| A-007 | L5 | P3 | 320 px 下本篇有 3 個表格、約 5 個 display 公式在容器內需橫向捲動；頁面本身沒有橫向溢出 | 本機 dev server，`.table-wrapper`／`mjx-container` 的 `scrollWidth>clientWidth`；頁寬 320=320 | 接受（與站上其他文章行為一致）；若要更好需拆公式 | 保留 |

## 4. 已驗證無誤的關鍵項

獨立重算（Python `fractions.Fraction`，$g=10$）：

- 約束 $2d_A+d_B=$ 常數 ⇒ B 下降 $2q$；繩 2 鉛直＋水平段不變 ⇒ C 前進 $2q$；位移比 $1:2:2$。
- $a=g/15=2/3$ m/s²；$a_B=a_C=4/3$ m/s²；$T_2=2a=4/3$ N；$T_1=(3g+3a)/2=16$ N；(2) 回代 $20-16-\tfrac43=\tfrac83=4a$ ✓。
- 張力係數矩陣的零向量：$2\lambda_A-\lambda_B=0$、$-\lambda_B+\lambda_C=0$ ⇒ $(1,2,2)$ ✓。
- $\sum c_iR_i=1\cdot2T_1+2\cdot(-T_1-T_2)+2\cdot T_2=0$ ✓。
- $Q=1\cdot(-3g)+2\cdot(2g)+2\cdot0=g$；$M_{\text{eff}}=3+8+4=15$；$\tfrac12M_{\text{eff}}$ 與直接算動能一致（$v=1$ 時 $15/2$）。
- 對照表：滑車 $100/15=20/3$；雙斜面 $(54-40)/14=1$；動滑輪 $g/11$（沿用第 3 篇）。
- 總質量 $3+2+1=6$ kg ≠ $M_{\text{eff}}=15$。
- 兩條張力均為正，「繩始終繃緊」自洽。

圖：圖 1 的繩路（繩 1 接 B 左吊鉤、繩 2 接 B 右吊鉤，皆鉛直）與文內約束一致；圖 2 的正方向、$2T_1$、$a_B=a_C=2a$ 標註與文字一致。

## 5. 判定可接受

- 以 $a\equiv\ddot q$ 簡寫，符號與第 3 篇一致。
- 「一般形式」一節的推導僅以 $\sum c_iR_i=0$ 為假設，並在「目前的證據夠嗎」明說未證明；這是刻意的教學結構，且與 Notion 的 Gate B 要求一致（不將虛功證明偷渡為已完成）。

## 6. 待作者決定

- 本篇與第 1–3 篇的 DRAFT 註解何時移除（取決於正式站驗收，見 §7）。
- 第 5、6 篇尚未在 Notion 內容排程確認，因此本篇結尾只寫「未來」。

## 7. 限制與正式站驗收

- 2026-11-09 稽核期間，owner 誤將 repo 改為私有，GitHub 因而下架 Pages 並清除設定（網域對所有路徑回 404）。owner 改回公開後，經 owner 同意以 `gh api` 重新啟用 Pages（`build_type=workflow`，自訂網域 `notes.kakau.tw`，網域驗證狀態 verified），並手動觸發 deploy（run 42508670458，success）。
- 恢復後在正式站（`https://notes.kakau.tw/posts/system-method-{basic-pulley,double-incline,movable-pulley,general-formula}/`）驗收：320／390／1280 px × 淺色／深色，共 24 組。每組皆：頁面無橫向捲動（scrollWidth=clientWidth）、每組只顯示對應主題的 `setup`、`fbd` 兩張圖並成功載入（`naturalWidth=460`，顯示寬度 288／358／480）、無 MathJax 錯誤（`mjx-merror`=0）。16 個 SVG 網址皆 200 `image/svg+xml`。雙斜面自由體圖於 320 px 深色另有截圖，文字可讀。
- 驗收的是 commit `08345ae` 的部署版本；本次稽核修正（A-001～A-006）與移除 DRAFT 註解尚未部署。
- 正式站驗收用 Browser 窗格的模擬視窗，不是實機；A-007 的內部橫向捲動只在本機 dev server 量測。
- L3 搜尋意圖、Search Console、L4 的 `_data/kakau.yml` mapping 是否應納入本系列：未稽核。
