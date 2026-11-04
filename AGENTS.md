# AGENTS.md — kakau-note AI Agent 操作指引

這個檔案提供給 AI agent（Claude Cowork、Codex 等）使用，說明這個 repo 的架構、規則和慣例。

完整文件索引（architecture／content／operations／audits／history 四層）在 [`docs/README.md`](docs/README.md)；
這裡只放 agent 必須遵守的 hard rules，細節規則一律指向 `docs/` 底下的正式文件。

---

## 基本資訊

| 項目 | 內容 |
|---|---|
| 網站 | https://notes.kakau.tw |
| Repo | `qavit/kakau-note`（2026-09-28 由 `g4kakau/g4kakau.github.io` 轉移並更名而來，repository ID／git history 不變；見 `docs/history/domain-and-repository-migrations.md`） |
| 用途 | 數理家教品牌網站、教學文章、SEO 內容資產 |
| 主題 | [Chirpy](https://github.com/cotes2357/jekyll-theme-chirpy) v7.x |
| Jekyll | 4.4.x |
| Ruby | 3.3.6（rbenv 管理） |
| 部署 | GitHub Pages（Actions workflow），push 到 `main` branch 自動觸發 |

---

## Branch 規則

- **`main` branch** = 唯一 canonical branch、正式線上版本、repo default branch，所有修改都在這裡
- 2026-09-29 起 `theme` branch 已 fast-forward 進 `main` 並刪除（不再存在，本身沒有留存價值——所有內容都完整保留在
  `main` 的 git history 裡）。任何 Kakau repo 的 default branch 原則上都是 `main`；branch 名稱描述「暫時正在做什麼」，
  不是永久產品層級。

**所有新文章、修改、commit 都要在 `main` branch 上進行。**

---

## Git / Commit 身份規範

- 所有 Claude Code、Codex、ChatGPT 或其他 coding agent 在這個 repo 建立的 commit，都必須使用 repo-local 的 `qavit` Git identity（`git config --local`，不是 global）。
- 不得以 `g4kakau`、agent 自己的名字、Claude、ChatGPT、Codex 等身份作為 commit 的 author 或 committer。
- 不得為了這個 repo 去修改 global Git config——只設 `--local`。
- 每次 commit 前，若不確定目前 identity 是什麼，先跑 `git var GIT_AUTHOR_IDENT` 與 `git var GIT_COMMITTER_IDENT` 確認。
- 這條規則從 2026-09-28（`3ee7a18` 之後）生效；`3ee7a18` 以前用 `g4kakau` identity 建立的既有 commit 不回溯修改（不 amend、不 rewrite history）。

---

## 新增文章的規則

### 檔案位置與命名

```
_posts/YYYY-MM-DD-英文-kebab-case-slug.md
```

### Front Matter 模板

```yaml
---
layout: post
title: "文章標題（繁體中文）"
date: YYYY-MM-DD 00:00:00 +0800
categories: [大分類, 小分類]
tags: [tag1, tag2, tag3]
math: true
description: "一句話摘要，約 50–120 字，給 SEO meta description 用"
---
```

**重要規則：**
- `math: true` 是 Chirpy 啟用 MathJax 的開關。有數學式的文章**一定要加**，否則 `$...$` 不會渲染。
- `categories` 採兩層：大分類在前，小分類在後。
- `tags` 用來補充關鍵字，盡量包含使用者會搜尋的詞彙（繁體中文）。
- `layout: post` 不可省略。
- **`date`（與檔名日期）預設對應原始素材筆記的日期**，而不是動工／發布當天。若筆記有 `source_created`（對話實際發生的時間），優先用它；沒有的話退而用筆記的 `created`。同一批動工的多篇文章，日期通常會因此打散在不同天，這是預期行為，不要為了方便而全部改成同一天。純自撰、沒有對應筆記的文章才用動工當天的日期。因為 `_posts/` 檔名必須是 `YYYY-MM-DD-slug.md`，改日期等於要重新命名檔案——同時要記得更新所有指向該檔案的 `{% post_url %}` 引用（否則會直接 build failed）。

### Categories 慣例

Taxonomy 的完整規則（六個 top-level 分類、現有 sub-area 對照表、同名次分類不可合併、英文翻譯頁規則）唯一真本在
[`docs/content/taxonomy.md`](docs/content/taxonomy.md)。新增文章前先讀那份文件，不要憑記憶或猜測選分類。

---

## 數學式寫法

這個網站使用 **MathJax v3**（由 Chirpy 內建，front matter 加 `math: true` 啟用）。完整規則（MathJax／physics
package 巨集、四種 Kramdown 行內地雷、圖片與 caption、跨文章引用）唯一真本在
[`docs/content/authoring.md`](docs/content/authoring.md)——寫文章或修文前先讀那份文件。

這裡只留兩條沒有例外空間的 agent-facing 硬規則：

- 有 `$...$` 或 `$$...$$` 的文章，front matter **一定要加** `math: true`，否則不會渲染。
- 行內絕對值一律用 `\lvert x-1\rvert`，**不要**寫裸 `$|x-1|$`——即使不在表格裡，Kramdown 也可能把它誤判成表格分隔符，導致整段被吞成破碎表格。

---

## 內容風格

### 目標讀者

- **高中生**：選修物理（III、IV）、段考複習、大考衝刺
- **大學生**：微積分、線性代數、普通物理
- **家長**：尋找家教資訊

### 文章結構慣例

1. **開場**：用一個直覺問題或生活場景帶入
2. **直覺說明**：用類比或圖像，不直接丟公式
3. **正式定義/推導**：清楚分節，用 `##`、`###`
4. **應用/例題**：至少一個具體例子
5. **總結**：表格或條列整理重點
6. **延伸閱讀**：優先提供相關文章或學習路徑

### Kakau 整合元件

- 所有文章會由 `_plugins/kakau_integration.rb` 自動加入 ecosystem footer，不要在文章內手動貼招生框。
- 只有與現行課程高度相關的文章才顯示 contextual CTA；slug mapping 集中在 `_data/kakau.yml`。
- 新文章若需要 contextual CTA，更新集中 mapping，不要自行建立不同文案、UTM 或產品敘事。

### 語言

- 繁體中文（台灣用法）
- 術語第一次出現時附英文：`動量（momentum）`
- 避免簡體中文詞彙

---

## SEO 原則

- `title` 盡量包含目標關鍵字（放在句首更好）
- `description` 約 50–120 字，說清楚「讀這篇可以學到什麼」
- 文章內部連結：同系列文章之間互相連結
- 圖片加 `alt` 屬性

---

## 內容來源

原始素材（教學觀察、AI 對話匯出、課程規劃）位於：`~/Documents/Obsidian/TEACHING/` 與
`~/Documents/Obsidian/Archive/`（雜項對話匯出，內含大量數理內容，**每次挖掘素材都要一併掃描**，並非只是備存舊資料）。這是
research／provenance 層，供寫文章時參考，不是選題真本。

**選題、狀態、投資判斷（Create／Refresh／Consolidate／Skip）的真本是 Kakau 的 Notion「內容排程」，不在這個
repo。** 本 repo 只處理已經決定要發布的內容；不要在這裡新建或維護第二份文章待辦清單、候選題排序，或任何形式的
content backlog——那會製造出一份永遠不會跟 Notion 同步的平行真本。

---

## 禁止事項

- 不要直接 rewrite `main` history（`push --force`、`reset --hard` 後強推等）；一般內容修改可直接在 `main` 上進行，較大型或高風險變更改用短期 feature branch
- 不要 push `DEV_NOTES.md`（在 `.gitignore`）
- 不要移除 `math: true`（除非文章真的沒有數學）
- 不要使用 Chirpy 以外的 layout（`home`、`base` 是舊版殘留）
- 不要在文章裡硬寫 MathJax script tag（Chirpy 已內建）

---

_最後更新：2026-09-28_
