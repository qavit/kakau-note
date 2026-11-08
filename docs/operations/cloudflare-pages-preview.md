# Cloudflare Pages 預覽管線（私有原始碼／公開部署分離，Gate 2）

> 狀態：**預覽管線的程式碼已就緒、本機驗證通過；Cloudflare 端尚未建立**（2026-11-09 撰寫）。
> 正式站仍是 `pages.yml` → GitHub Pages。本文件與 `cloudflare-preview.yml` 不改變 production。
> 現況的網域／DNS 事實仍以 [`domain-dns.md`](domain-dns.md) 為準。

## 選定的架構（方案 B）

```
Private GitHub repo ──► GitHub Actions（建置＋全部既有測試）──► Cloudflare Pages Direct Upload
                              ▲ 測試失敗 → deploy job 不會執行
```

選方案 B（Actions 建置＋Direct Upload）而非 A（Cloudflare Git integration）的理由：

1. 既有品質 Gate（attribution、GoatCounter、整合檢查、htmlproofer）已在 Actions 裡；方案 A 要在
   Cloudflare 建置環境重寫一份，且 Cloudflare 即使建置成功也不會等 GitHub 測試——**測試失敗仍可能上線**，
   違反專案硬條件，除非另外把 Cloudflare 的 build command 變成「測試＋建置」並與 Actions 重複維護。
2. 建置環境（Ruby 3.4、Bundler、Node）與 `pages.yml` 完全相同，不必處理 Cloudflare build image 的差異。
3. 不需把 Cloudflare 的 GitHub App 授權到 private repo；只需 Actions Secrets 兩個值。

代價：Direct Upload 專案**之後不能改成 Git integration**（Cloudflare 官方文件）；要改就得新建專案。

## 預覽與 production 的隔離

`_config.preview.yml` 只被 `cloudflare-preview.yml` 疊加載入；`pages.yml` 從不讀它。它關掉
GoatCounter（`analytics.goatcounter.id`、`pageviews.provider`）與 giscus（`comments.provider`）。
這裡必須用 `false`：空值不會覆蓋、空字串在 Liquid 是 truthy 且會讓 Chirpy 的 include 路徑壞掉。
`url` 於建置時由 workflow 以 `PREVIEW_URL` 疊加，使 canonical／sitemap／feed／robots 指向預覽網域。
部署前另寫入 `_headers`（`X-Robots-Tag: noindex, nofollow`），且「Assert preview isolation」步驟會在
預覽仍載入 `count.js`／giscus 或 sitemap 含 production URL 時讓 job 失敗。

## 擁有者需要做的帳戶端設定（agent 無 Cloudflare 憑證，未代為執行）

1. Cloudflare Dashboard → Workers & Pages → Create → Pages → **Direct Upload**，專案名
   `kakau-notes-preview`（若改名，同步改 workflow 的 `CF_PAGES_PROJECT`／`PREVIEW_URL`）。
   Production branch 不必設定；此管線只用非 production 的 `--branch` alias。
2. 建立 API token（My Profile → API Tokens → Custom）：權限 **Account › Cloudflare Pages › Edit**，
   Account Resources 限定本帳戶。不要給 Zone／DNS 權限。
3. GitHub → repo Settings → Secrets and variables → Actions，新增 `CLOUDFLARE_API_TOKEN`、
   `CLOUDFLARE_ACCOUNT_ID`。未設定時，workflow 仍會建置與測試，僅跳過 deploy 並顯示 notice。
4. 對本分支的 PR 或手動 `workflow_dispatch` 觸發後，部署網址會出現在 wrangler 輸出與
   Cloudflare 專案的 Deployments 頁。

Gate 3（正式網域切換）會另需一個 production 專案或把此專案指定 production branch，並綁定
`notes.kakau.tw`——該決定尚未做，不在本文件範圍。

## Rollback

- **本管線**：刪除 `kakau-notes-preview` 專案或移除 workflow 即可；對 production 無影響。
- **Gate 3 之後（預擬）**：切換前記錄 Cloudflare DNS 中 `notes` CNAME 現值（`qavit.github.io`）；
  GitHub Pages 與 `pages.yml` 在 Gate 4 前保持啟用，回復＝把 CNAME 改回 `qavit.github.io`
  （DNS 在 Cloudflare，TTL 可事先調低），並確認 GitHub Pages 的 custom domain／HTTPS 仍為 approved。
  Gate 4 把 repo 設為 Private 前，必須先確認 GitHub Free 下 Private repo 無法繼續提供 Pages，
  因此那一步之後 GitHub Pages 路徑即失效，回復只剩 Cloudflare 的前一個 deployment（Pages 可回滾到舊部署）。

## 已知需另案處理

- `_site/AGENTS.md` 目前會被 Jekyll 發布到公開網站（`_config.yml` 的 `exclude` 未列入）。
  這和「內部工程資產不公開」的目標衝突，屬 Gate 3 前應處理的獨立小修，本分支未動。
- `.ruby-version` 為 3.3.6，CI 用 3.4；本管線與 `pages.yml` 對齊 3.4。
