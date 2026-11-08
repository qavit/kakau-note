#!/usr/bin/env bash

set -eu

failures=0

if command -v rg >/dev/null 2>&1; then
  search() { rg -n -i "$@"; }
  search_quiet() { rg -q "$@"; }
  list_matching() { rg -l "$@"; }
else
  search() { grep -R -n -i -E -- "$@"; }
  search_quiet() { grep -q -E -- "$@"; }
  list_matching() { grep -R -l -E -- "$@"; }
fi

check_forbidden() {
  label="$1"
  pattern="$2"
  shift 2
  if search "$pattern" "$@"; then
    echo "ERROR: found forbidden ${label}" >&2
    failures=1
  fi
}

check_forbidden "legacy production domain" 'kakau-tutor\.vercel\.app' _config.yml index.html _tabs _includes _posts _data
check_forbidden "legacy Google inquiry form" 'forms\.gle/R38gD1b9SecEbufq8' _config.yml index.html _tabs _includes _posts _data
check_forbidden "legacy tutoring CTA" '歡迎預約家教課|需要家教或預約諮詢' _config.yml index.html _tabs _includes _posts _data
check_forbidden "placeholder social account" 'threads\.net/@placeholder' _config.yml index.html _tabs _includes _posts _data

# The theme's own analytics/goatcounter.html loads count.js with no settings, which sends the
# full query string twice (inside `p`, and again as `q`). `_includes/analytics/goatcounter.html`
# overrides it. If that override is deleted the theme's version silently takes over again and
# `fbclid` starts reaching zgo.at, with nothing failing -- so pin the three parts that matter.
# Behaviour is covered by tools/test_goatcounter.mjs; this only catches the file vanishing.
if [ ! -f _includes/analytics/goatcounter.html ]; then
  echo "ERROR: the GoatCounter override is gone; the theme default would send the query string" >&2
  failures=1
else
  for pin in 'no_onload: true' 'location.pathname' "data.q = ''"; do
    if ! grep -qF -- "$pin" _includes/analytics/goatcounter.html; then
      echo "ERROR: GoatCounter override lost \"$pin\"; see docs/operations/analytics.md" >&2
      failures=1
    fi
  done
fi
# 非台灣用詞的檢查搬到 tools/check_terminology.rb。有幾個詞需要前後文守衛才不會誤判
# 合法的繁體寫法，而 grep -E 的 [^…] 在不同 grep 實作與 locale 下可能以位元組而非字元
# 比對，中文一個字三個位元組，守衛會在某些平台悄悄失效。理由詳見該檔開頭。
if ! ruby tools/check_terminology.rb; then
  failures=1
fi

if search '/tutoring-plans/' _tabs _includes index.html _data; then
  echo "ERROR: /tutoring-plans/ remains a primary navigation destination" >&2
  failures=1
fi

if [[ ! -f _tabs/academy.md ]] || ! search_quiet '^permalink: /academy/$' _tabs/academy.md; then
  echo "ERROR: /academy/ bridge page is missing" >&2
  failures=1
fi

if [[ ! -f tutoring-plans/index.html ]] || ! search_quiet "canonical.*academy" tutoring-plans/index.html; then
  echo "ERROR: legacy /tutoring-plans/ compatibility redirect is missing" >&2
  failures=1
fi

if [[ $(list_matching '<div class="cta-box">|\{% include cta\.html %\}' _posts | wc -l | tr -d ' ') != "0" ]]; then
  echo "ERROR: post-level legacy CTA markup remains" >&2
  failures=1
fi

if [[ $(find _posts -type f -name '*.md' | wc -l | tr -d ' ') -lt 1 ]]; then
  echo "ERROR: no posts found" >&2
  failures=1
fi

# Cross-site identity contract. Articles here are authored by a person whose canonical profile
# lives on kakau.tw; that @id is what lets a crawler merge the two sites into one author instead
# of inventing a second one. See _data/authors.yml and _plugins/author_identity.rb.
if ! search_quiet 'id: https://kakau\.tw/about/#person' _data/authors.yml; then
  echo "ERROR: _data/authors.yml no longer points at the canonical Person @id on kakau.tw" >&2
  failures=1
fi

if ! search_quiet '^      author: sin-iu-ho$' _config.yml; then
  echo "ERROR: posts no longer default to the named author; the byline falls back to the brand" >&2
  failures=1
fi

# `social.name` describes the site/brand. Turning it into the person's name would collapse the
# Organization and the Person into one entity, so it must stay as the brand.
if ! search_quiet '^  name: Kakau$' _config.yml; then
  echo "ERROR: social.name must stay the brand name, not the author's name" >&2
  failures=1
fi

if ! search_quiet '何信佑' _tabs/about.md; then
  echo "ERROR: /about/ no longer names the author in human-readable text" >&2
  failures=1
fi

# Canonical domain. See docs/operations/domain-dns.md. Pinned as a positive assertion (not a
# banned-string search) because the old GitHub Pages hostname is legitimately mentioned in
# historical prose (README.md, AGENTS.md, docs/history/) -- what must never drift is the actual
# canonical URL in _config.yml, which is what actually gets built into the site. (The repo-root
# CNAME file is NOT checked here: this repo deploys via a custom GitHub Actions workflow, and in
# that mode GitHub Pages ignores a root CNAME file entirely -- the real custom-domain setting
# lives in GitHub repository Settings -> Pages, which this repo can't assert against in CI. See
# docs/operations/domain-dns.md for the full model.)
if ! search_quiet '^url: "https://notes\.kakau\.tw"$' _config.yml; then
  echo "ERROR: _config.yml's canonical url is no longer https://notes.kakau.tw; see docs/operations/domain-dns.md" >&2
  failures=1
fi

# GoatCounter site id is an analytics identifier, independent of the GitHub owner/repo name --
# renaming the repo (as happened 2026-09-28) must never be "helpfully" followed by renaming this,
# or historical analytics data stops lining up with new data. See docs/history/domain-and-repository-migrations.md.
if ! search_quiet '^    id: g4kakau ' _config.yml; then
  echo "ERROR: GoatCounter site id drifted from g4kakau; it must stay independent of the GitHub owner" >&2
  failures=1
fi

# Cross-subdomain first-touch attribution contract. The record is one first-party cookie on the
# registrable parent domain, written by BOTH properties and read back by the Academy when an
# application is submitted. `qavit/kakau-front` `src/lib/attribution.ts` is the source of truth;
# the constants below are the part that silently breaks the shared record if the two drift apart
# — a renamed cookie or a bumped version simply produces two records that never meet.
attr='_includes/kakau-attribution.html'
if [[ ! -f "$attr" ]]; then
  echo "ERROR: the Notes-side attribution capture is missing; first touches that start on an article are lost" >&2
  failures=1
else
  while IFS= read -r pin; do
    if ! search_quiet "$pin" "$attr"; then
      echo "ERROR: attribution contract drifted from the Academy: expected ${pin}" >&2
      failures=1
    fi
  done <<'PINS'
var VERSION = 1;
var COOKIE = 'kakau_attr';
var MAX_AGE_SECONDS = 30 \* 24 \* 60 \* 60;
var INTERNAL_SOURCES = \['kakau_academy', 'kakau_notes'\];
var OWNED_DOMAIN = 'kakau.tw';
PINS

  # The eight-field whitelist. Anything else in the record is data the Academy drops on read and
  # data we promised not to collect, so an extra field is a silent one-sided change, not a feature.
  unexpected=$(
    grep -oE 'record\.[a-z_]+ =' "$attr" | sed -E 's/^record\.//; s/ =$//' | sort -u |
      grep -vxE 'utm_source|utm_medium|utm_campaign|utm_content|landing_path|referrer_host|first_seen_at|attribution_version' || true
  )
  if [[ -n "$unexpected" ]]; then
    echo "ERROR: the attribution record grew fields outside the shared whitelist: ${unexpected}" >&2
    failures=1
  fi

  # `//` comments do not survive `compress_html`, which collapses every newline inside an inline
  # <script> into a single space and would take the rest of the file with the comment.
  if grep -qE '^[[:space:]]*//' "$attr"; then
    echo "ERROR: // comments in the attribution script are destroyed by compress_html" >&2
    failures=1
  fi

  # Capture has to run on every page, and on the one redirect stub the footer never reaches.
  if ! search_quiet 'include kakau-attribution\.html' _includes/footer.html; then
    echo "ERROR: attribution capture is no longer included site-wide from the footer" >&2
    failures=1
  fi
  if ! search_quiet 'include kakau-attribution\.html' tutoring-plans/index.html; then
    echo "ERROR: the legacy /tutoring-plans/ ingress no longer captures attribution" >&2
    failures=1
  fi
fi

# Internal repo files must never be published (AGENTS.md was served from production until 2026-11-09).
if [ -d _site ]; then
  for f in AGENTS.md DEV_NOTES.md; do
    if [ -e "_site/$f" ]; then
      echo "ERROR: internal file $f is published in _site" >&2
      failures=1
    fi
  done
fi

exit "$failures"
