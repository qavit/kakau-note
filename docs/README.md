# docs/ — 索引

四個語意分層。知道一份文件屬於哪一層，就知道該把它當指令照做，還是當記錄查閱：

| 分層 | 意義 |
|---|---|
| `architecture/` | 目前系統結構——系統現在實際上是怎麼運作的 |
| `content/`、`operations/` | 目前的規範性契約與操作手冊——照著做 |
| `audits/` | 證據——已提交的稽核報告視為不可變（更正用附加的方式，不回頭改寫）；`coverage.md` 是這一層唯一持續更新的活文件 |
| `history/` | 已完結的事件——是沿革紀錄，不是指令；這裡的內容不會告訴你接下來該做什麼 |

這個 repo 是 `notes.kakau.tw` 的公開知識發布層。它**不是** Kakau 的商業路線圖、內容待辦清單，也不是產品規格庫——完整定位見
`AGENTS.md`。任何真本在 Notion、Obsidian 或 Kakau 其他 repo 的資訊，這裡只引用，不重複建立。

## architecture/

- [`publishing-pipeline.md`](architecture/publishing-pipeline.md)——一篇文章如何從 `_posts/` 變成上線頁面：front
  matter 預設值、自動注入 CTA／footer 的 hook、分析與 attribution 的 include，以及 `pages.yml` 裡的 CI 關卡。

## content/

- [`authoring.md`](content/authoring.md)——MathJax 巨集、Kramdown 地雷、圖片與 caption 慣例、跨文章引用規則的唯一真本。
- [`taxonomy.md`](content/taxonomy.md)——`categories` 規則的唯一真本（四個 top-level 分類、現有 sub-area
  對照表、英文頁規則）。
- [`audit-policy.md`](content/audit-policy.md)——「稽核過」是什麼意思：`audits/` 底下每份稽核報告所依循的
  L1–L5 分層、scope 種類與 pass 語意。

## operations/

- [`analytics.md`](operations/analytics.md)——GoatCounter 契約：資料最小化覆寫、事件名稱、維護規則。
- [`attribution.md`](operations/attribution.md)——跨子網域 first-touch attribution：與 `kakau-front` 共用的
  cookie 契約。
- [`domain-dns.md`](operations/domain-dns.md)——目前的網域／DNS／主機現況（canonical domain、CNAME
  target、HTTPS、Giscus 綁定）。
- [`cloudflare-pages-preview.md`](operations/cloudflare-pages-preview.md)——Cloudflare Pages 預覽管線（Direct Upload）、隔離方式、帳戶端設定與 Rollback。

## audits/

- [`coverage.md`](audits/coverage.md)——持續更新的稽核覆蓋率總表：每篇文章在哪一層被檢查過、何時檢查的。空格代表未稽核，不代表通過。
- [`2026-09-06-taxonomy-audit.md`](audits/2026-09-06-taxonomy-audit.md)——一次性的 79 篇分類統計快照；其中發現的前瞻性規則已抽取進
  `content/taxonomy.md`。
- [`2026-09-08-full-site-fact-audit.md`](audits/2026-09-08-full-site-fact-audit.md)——B1–B12 批次、全站
  L1（科學／數學正確性）稽核，共 79 篇。
- [`2026-09-28-release-8-new-posts.md`](audits/2026-09-28-release-8-new-posts.md)——8
  篇未追蹤文章在首次 commit 前的 release audit；未來 release audit 可依此為範本。

## history/

- [`domain-and-repository-migrations.md`](history/domain-and-repository-migrations.md)——append-only
  沿革紀錄：2026-09-06 的 custom-domain 切換、2026-09-28 的 repository ownership migration，以及同日收尾的
  DNS 改點紀錄。
- [`2026-09-06-two-site-integration-delivery.md`](history/2026-09-06-two-site-integration-delivery.md)——Kakau
  Notes 與物理學苑最初整合的交付紀錄（首批 13 個 contextual CTA、發布前檢查清單）。其中仍然現行的架構事實已抽取進
  `architecture/publishing-pipeline.md`；這份文件維持凍結，作為交付紀錄保存。

## 刻意不放在這裡的內容

選題、brief 與投資判斷（Create／Refresh／Consolidate／Skip）的真本是 Kakau 的 Notion「內容排程」——這個 repo
只承接已經選定要撰寫或發布的內容（包含還在 `_drafts/`、寫作中或稽核中的內容，不只是已經上線的文章）。不要在
`docs/` 底下新增待辦清單、路線圖或規劃草稿；若某份規劃文件是用來得出這裡記錄的決策，保留的是決策本身，不是那份草稿。
