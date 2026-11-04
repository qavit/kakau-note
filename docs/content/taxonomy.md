# Taxonomy — normative source

This is the single normative owner of `categories`/taxonomy rules for
`notes.kakau.tw`. `AGENTS.md` only points here — if you're an agent and
`AGENTS.md`'s summary and this file ever seem to disagree, this file is
correct; update `AGENTS.md`'s pointer text, not this file, to match.

## Rule

Every post's `categories` front matter uses exactly two levels: a top-level
subject area, then a sub-area. Only five top-level values exist for Chinese
content:

`國中理化`、`高中數學`、`高中物理`、`大學數學`、`大學物理`

`國中理化` was added 2026-11-04 by owner decision, for junior-high
physics/chemistry (國中自然・理化) posts, starting with the chase-problem post
(2026-10-10). Junior-high content goes there by education level, even when the
same topic also appears under `高中物理`; it is not filed under a high-school
category with a `國中理化` tag.

Do not invent another top-level category for a new post. If a topic doesn't
fit one of the five, that's a signal to pick the closest existing one and
use `tags` for the more specific term, not to add a new top-level category
unilaterally.

## Current top-level → sub-area mapping

| 文章類型 | categories |
|---|---|
| 高中物理—力學 | `[高中物理, 力學]` |
| 高中物理—靜力學 | `[高中物理, 靜力學]` |
| 高中物理—波動 | `[高中物理, 波動]` |
| 高中物理—電磁學 | `[高中物理, 電磁學]` |
| 高中物理—近代物理 | `[高中物理, 近代物理]` |
| 高中物理—核物理 | `[高中物理, 核物理]` |
| 大學數學—微積分 | `[大學數學, 微積分]` |
| 大學數學—線性代數 | `[大學數學, 線性代數]` |
| 大學數學—常微分方程 | `[大學數學, 常微分方程]` |
| 大學物理—電磁學 | `[大學物理, 電磁學]` |
| 大學物理—電路學 | `[大學物理, 電路學]` |
| 大學物理—力學 | `[大學物理, 力學]` |
| 大學物理—古典場論 | `[大學物理, 古典場論]` |
| 大學物理—量子場論 | `[大學物理, 量子場論]` |
| 大學物理—天文物理 | `[大學物理, 天文物理]` |
| 大學物理—熱學 | `[大學物理, 熱學]` |
| 高中數學—三角函數 | `[高中數學, 三角函數]` |
| 高中數學—幾何 | `[高中數學, 幾何]` |
| 高中數學—代數 | `[高中數學, 代數]` |
| 國中理化—力與運動 | `[國中理化, 力與運動]` |

New sub-areas under an existing top-level value are fine to add as content
needs them (this table isn't a closed set at the second level — only the
five top-level values are closed).

## Same-named sub-areas under different top-levels

`力學` and `電磁學` each appear under both `高中物理` and `大學物理`. That's
a deliberate distinction by education level, not an accidental duplicate —
**do not** batch-rename or merge them into one, even though Chirpy's category
archive page may visually aggregate same-named sub-categories. Doing so would
change existing post permalinks. (Confirmed by audit:
[`docs/audits/2026-09-06-taxonomy-audit.md`](../audits/2026-09-06-taxonomy-audit.md).)

## English-language posts

An English translation page may use an English-language category (e.g.
`High School Math`) instead of the Chinese taxonomy above, but only if it
has all three of:

- `lang: en` in front matter
- its own independent `permalink` (e.g. `/en/posts/...`)
- a `translation_id` pairing it to its Chinese counterpart

Putting an English post under a Chinese category would send English readers
into a Chinese-language archive page — worse than a separate English island.
If a full English-language site is ever built, categories will need a
locale-aware redesign at that point; don't try to solve that preemptively in
a single post's front matter.

## Changing this file

This file describes current policy. If a rule here needs to change (new
top-level category, retiring one, changing the English-page contract),
that's a content-policy decision, not a mechanical edit — make the change
here, and if it affects an audit's prior conclusions, note it in a new dated
audit entry rather than editing the old one.
