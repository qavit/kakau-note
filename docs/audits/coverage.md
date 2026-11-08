# Coverage ledger

每篇文章各稽核層最後一次被檢查的日期與報告連結。空格＝未稽核，不代表通過。

本檔案於 2026-09-28 docs 重整時建立。目前只回填了本次稽核涵蓋的 8 篇；既有 87 篇（含 2026-09-08 B1–B12 的 79 篇科學層稽核，見 [`2026-09-08-full-site-fact-audit.md`](2026-09-08-full-site-fact-audit.md)）尚未回填到這張表，是已知缺口，見下方「待辦」。

## 本次涵蓋（2026-09-28 Release Audit）

| Slug | 科學層 (L1) | 渲染層 (L5) | SEO/架構層 (L3) | Funnel 層 (L4) | 報告 | 未結 finding |
|---|---|---|---|---|---|---|
| `logarithm-power-law-loglog-plot` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | [2026-09-28-release-8-new-posts](2026-09-28-release-8-new-posts.md) | 無（R-003 已修） |
| `logarithm-entropy-boltzmann` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | 同上 | 無（R-003 已修） |
| `logarithm-multiplicative-to-additive` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | 同上 | 無（R-003 已修） |
| `logarithm-semilog-exponential-decay` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | 同上 | 無（R-001 經 owner 裁示：修 checker 規則，原文「實驗數據」保留） |
| `logarithm-decibel-richter-magnitude` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | 同上 | 無（R-003 已修） |
| `planck-einstein-qft-photon-energy` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | 同上 | 無（R-003、R-004 已修） |
| `median-theorem-absolute-value-sum` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | 同上 | 無（R-003、R-004 已修） |
| `median-theorem-quadratic-absolute-value` | 2026-09-28 | 2026-09-28 | 2026-09-28 | 2026-09-28 | 同上 | 無（R-002、R-003、R-004 已修） |

## 2026-11-04 Cluster 稽核（平衡化學反應式難題）

| Slug | 科學層 (L1) | 渲染層 (L5) | SEO/架構層 (L3) | Funnel 層 (L4) | 報告 | 未結 finding |
|---|---|---|---|---|---|---|
| `balancing-equations-1-inspection-and-groups` | 2026-11-04 | 2026-11-04 | 2026-11-04 | 2026-11-04 | [2026-11-04-cluster-balancing-equations](2026-11-04-cluster-balancing-equations.md) | A-005、A-006、A-007、A-008（待 owner） |
| `balancing-equations-2-oxidation-numbers` | 2026-11-04 | 2026-11-04 | 2026-11-04 | 2026-11-04 | 同上 | A-007（A-004 已修） |
| `balancing-equations-3-linear-algebra` | 2026-11-04 | 2026-11-04 | 2026-11-04 | 2026-11-04 | 同上 | A-006、A-009（A-001／A-002／A-003 已修） |

## 2026-11-09 單篇稽核（整體法系列第 4 篇）

| Slug | 科學層 (L1) | 渲染層 (L5) | SEO/架構層 (L3) | Funnel 層 (L4) | 報告 | 未結 finding |
|---|---|---|---|---|---|---|
| `system-method-general-formula` | 2026-11-09 | 2026-11-09（本機＋正式站 24 組） | 2026-11-09（只查站內連結） |  | [2026-11-09-single-system-method-general-formula](2026-11-09-single-system-method-general-formula.md) | A-007（P3，接受） |

## 待辦

- 既有 87 篇尚未回填：L1 可從 [`2026-09-08-full-site-fact-audit.md`](2026-09-08-full-site-fact-audit.md)（2026-09-08，B1–B12，79 篇）回填有證據的欄位；其餘 8 篇中有 7 篇（`modular-arithmetic-to-abstract-algebra`、`gram-schmidt`、`resistor-cube-3-symmetry`、`resistor-cube-6-graph-theory`、`constructibility-gauss-wantzel`、`galois-correspondence-abel-ruffini`、`group-ring-field-map`）經 2026-09-28 渲染排查確認有地雷 4 違規（行內 `\{`／`\}` 未雙跳脫，規則見 `docs/content/authoring.md` §2），L1/L5 都留空。
- L3／L4／L5 目前全站幾乎沒有回填紀錄；9/08 那次稽核只做了 L1。
