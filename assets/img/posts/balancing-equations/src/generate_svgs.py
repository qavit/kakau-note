#!/usr/bin/env python3
"""Generate the static SVG figures for the balancing-equations series.

Two figures, each exported as light / dark (zh only):

* nitrogen-ladder   — part 2: oxidation numbers of N from +5 to -3, and how far
                      nitric acid is reduced in four reactions.
* no2-solution-line — part 3: every balanced form of NO2 + NH3 + O2 -> N2 + H2O
                      lies on one segment between two independent reactions.

Colours follow C2 (Notion D-053): neutral ink and surfaces, the ratified
Blue-Teal accent for emphasis, no gold (decoration only, never meaning).
Emphasis is never colour-only: highlighted items also change weight, shape or
line style.

Run: python3 -I assets/img/posts/balancing-equations/src/generate_svgs.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]

THEMES = {
    "light": {
        "bg": "#ffffff",
        "ink": "#1f232b",
        "muted": "#555b66",
        "rule": "#c9ccd2",
        "faint": "#ebebed",
        "accent": "#216e84",
        "accent_soft": "#e4f1f3",
    },
    "dark": {
        "bg": "#1a1c21",
        "ink": "#d4d7dd",
        "muted": "#a5aab4",
        "rule": "#4a4e57",
        "faint": "#24272d",
        "accent": "#9bd7dd",
        "accent_soft": "#173139",
    },
}

FONT = "'PingFang TC','Noto Sans TC','Microsoft JhengHei',system-ui,sans-serif"


def chem(formula: str) -> str:
    """Formula -> SVG tspans: digits after an element or ')' become subscripts,
    a trailing ^+ / ^- / ^2- becomes a superscript charge."""
    charge = ""
    m = re.search(r"\^(\d*[+-])$", formula)
    if m:
        charge = m.group(1).replace("-", "−")
        formula = formula[: m.start()]
    out = []
    for i, ch in enumerate(formula):
        if ch.isdigit() and i > 0 and (formula[i - 1].isalpha() or formula[i - 1] in ")" or formula[i - 1].isdigit() and out and out[-1][0] == "sub"):
            out.append(("sub", ch))
        else:
            out.append(("n", ch))
    # merge runs
    runs: list[list[str]] = []
    for kind, ch in out:
        if runs and runs[-1][0] == kind:
            runs[-1][1] += ch
        else:
            runs.append([kind, ch])
    parts = []
    for kind, text in runs:
        t = html.escape(text)
        if kind == "sub":
            parts.append(f'<tspan dy="0.28em" font-size="72%">{t}</tspan><tspan dy="-0.28em"></tspan>')
        else:
            parts.append(t)
    if charge:
        parts.append(f'<tspan dy="-0.45em" font-size="72%">{html.escape(charge)}</tspan><tspan dy="0.45em"></tspan>')
    return "".join(parts)


def shell(w: int, h: int, c: dict[str, str], title: str, desc: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-labelledby="t d" font-family="{FONT}">\n'
        f"<title id=\"t\">{html.escape(title)}</title>\n<desc id=\"d\">{html.escape(desc)}</desc>\n"
        f'<rect width="{w}" height="{h}" rx="12" fill="{c["bg"]}"/>\n{body}</svg>\n'
    )


def arrow_marker(c: dict[str, str], mid: str) -> str:
    return (
        f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c["accent"]}"/></marker></defs>\n'
    )


# ---------------------------------------------------------------- figure 1

LEVELS = [
    (5, ["HNO3", "NO3^-"]),
    (4, ["NO2"]),
    (3, ["HNO2", "NO2^-"]),
    (2, ["NO"]),
    (1, ["N2O"]),
    (0, ["N2"]),
    (-1, ["NH2OH"]),
    (-2, ["N2H4"]),
    (-3, ["NH4^+", "NH3"]),
]

# (target oxidation number, electrons per N, label line 1, label line 2)
REACTIONS = [
    (4, 1, "Cu＋濃硝酸", "→ NO2"),
    (2, 3, "Cu＋稀硝酸", "→ NO"),
    (1, 4, "活性大的金屬", "→ N2O"),
    (-3, 8, "Zn＋極稀硝酸", "→ NH4^+"),
]


def nitrogen_ladder(mode: str) -> str:
    c = THEMES[mode]
    W, H = 760, 680
    top, step = 128, 56
    y = {ox: top + (5 - ox) * step for ox, _ in LEVELS}
    targets = {t for t, *_ in REACTIONS} | {5}
    b = [arrow_marker(c, "ah")]
    b.append(f'<text x="32" y="40" font-size="20" font-weight="700" fill="{c["ink"]}">氮的氧化數階梯</text>\n')
    b.append(f'<text x="32" y="70" font-size="14" fill="{c["muted"]}">箭頭長度＝每個 N 得到的電子數</text>\n')
    # axis
    b.append(f'<line x1="92" y1="{y[5]}" x2="92" y2="{y[-3]}" stroke="{c["rule"]}" stroke-width="2"/>\n')
    for ox, species in LEVELS:
        yy = y[ox]
        hit = ox in targets
        if hit:
            b.append(f'<rect x="100" y="{yy - 19}" width="230" height="38" rx="6" fill="{c["accent_soft"]}"/>\n')
        b.append(f'<line x1="84" y1="{yy}" x2="100" y2="{yy}" stroke="{c["rule"]}" stroke-width="2"/>\n')
        label = f"+{ox}" if ox > 0 else ("0" if ox == 0 else f"−{-ox}")
        b.append(f'<text x="70" y="{yy + 6}" text-anchor="end" font-size="17" font-weight="700" fill="{c["ink"]}">{label}</text>\n')
        names = "<tspan>、</tspan>".join(chem(s) for s in species)
        weight = "700" if hit else "400"
        col = c["ink"] if hit else c["muted"]
        b.append(f'<text x="116" y="{yy + 6}" font-size="18" font-weight="{weight}" fill="{col}">{names}</text>\n')
    # arrows
    x0 = 370
    for i, (t, e, l1, l2) in enumerate(REACTIONS):
        x = x0 + i * 96
        b.append(f'<circle cx="{x}" cy="{y[5]}" r="5" fill="{c["accent"]}"/>\n')
        b.append(
            f'<line x1="{x}" y1="{y[5]}" x2="{x}" y2="{y[t] - 4}" stroke="{c["accent"]}" stroke-width="3" marker-end="url(#ah)"/>\n'
        )
        # electron count and reaction label stacked under the arrowhead
        ty = y[t] + 28
        b.append(f'<text x="{x}" y="{ty}" text-anchor="middle" font-size="17" font-weight="700" fill="{c["ink"]}">{e} e<tspan dy="-0.45em" font-size="72%">−</tspan></text>\n')
        b.append(f'<text x="{x}" y="{ty + 22}" text-anchor="middle" font-size="13" fill="{c["muted"]}">{html.escape(l1)}</text>\n')
        b.append(f'<text x="{x}" y="{ty + 40}" text-anchor="middle" font-size="13" fill="{c["muted"]}">{chem(l2)}</text>\n')
    b.append(f'<text x="{x0 - 6}" y="{y[5] - 26}" font-size="13" fill="{c["muted"]}">起點：{chem("HNO3")} 的 N（+5）</text>\n')
    return shell(
        W, H, c,
        "氮的氧化數階梯",
        "氮的氧化數從 +5 到 −3 的代表物質；四個箭頭從硝酸的 +5 往下，分別到 NO2（1 個電子）、NO（3 個）、N2O（4 個）、NH4+（8 個）。",
        "".join(b),
    )


# ---------------------------------------------------------------- figure 2

def solution_line(mode: str) -> str:
    c = THEMES[mode]
    W, H = 760, 420
    x_of = lambda d: 110 + (d - 4) * 180  # d from 4 to 7
    ly = 200
    b = []
    b.append(f'<text x="32" y="40" font-size="20" font-weight="700" fill="{c["ink"]}">{chem("NO2")} ＋ {chem("NH3")} ＋ {chem("O2")} → {chem("N2")} ＋ {chem("H2O")} 的所有平衡式</text>\n')
    b.append(f'<text x="32" y="72" font-size="14" fill="{c["muted"]}">固定 {chem("NH3")} ＝ 8、{chem("H2O")} ＝ 12，橫軸是 {chem("N2")} 的係數 d；線段上每一點都原子守恆</text>\n')
    # the segment
    b.append(f'<line x1="{x_of(4)}" y1="{ly}" x2="{x_of(7)}" y2="{ly}" stroke="{c["accent"]}" stroke-width="5" stroke-linecap="round"/>\n')
    pts = [
        (4, "0 : 8 : 6 : 4 : 12", "R₁：沒有 NO₂", "end"),
        (5, "2 : 8 : 4 : 5 : 12", "係數和 31", "mid"),
        (6, "4 : 8 : 2 : 6 : 12", "÷2 → 2 : 4 : 1 : 3 : 6，係數和 16", "exam"),
        (7, "6 : 8 : 0 : 7 : 12", "R₂：沒有 O₂", "end"),
    ]
    for d, tup, note, kind in pts:
        x = x_of(d)
        if kind == "end":
            b.append(f'<circle cx="{x}" cy="{ly}" r="9" fill="{c["bg"]}" stroke="{c["ink"]}" stroke-width="2.5"/>\n')
        else:
            b.append(f'<circle cx="{x}" cy="{ly}" r="8" fill="{c["ink"]}"/>\n')
        if kind == "exam":
            b.append(f'<circle cx="{x}" cy="{ly}" r="15" fill="none" stroke="{c["accent"]}" stroke-width="2.5" stroke-dasharray="4 3"/>\n')
        b.append(f'<text x="{x}" y="{ly + 42}" text-anchor="middle" font-size="16" font-weight="700" fill="{c["ink"]}">d ＝ {d}</text>\n')
        b.append(f'<text x="{x}" y="{ly - 52}" text-anchor="middle" font-size="15" fill="{c["ink"]}" font-weight="{700 if kind == "exam" else 400}">{tup}</text>\n')
        anchor = "middle"
        b.append(f'<text x="{x}" y="{ly - 30}" text-anchor="{anchor}" font-size="13" fill="{c["muted"]}">{html.escape(note)}</text>\n')
    b.append(f'<text x="{x_of(6)}" y="{ly - 76}" text-anchor="middle" font-size="13" font-weight="700" fill="{c["accent"]}">段考答案 (A)</text>\n')
    b.append(f'<text x="32" y="{H - 24}" font-size="13" fill="{c["muted"]}">係數順序 a : b : c : d : e ＝ {chem("NO2")} : {chem("NH3")} : {chem("O2")} : {chem("N2")} : {chem("H2O")}</text>\n')
    # trade-off arrows
    b.append(arrow_marker(c, "ah2"))
    ay = ly + 90
    b.append(f'<line x1="{x_of(4.6)}" y1="{ay}" x2="{x_of(6.9)}" y2="{ay}" stroke="{c["accent"]}" stroke-width="2" marker-end="url(#ah2)"/>\n')
    b.append(f'<text x="{x_of(4.6) - 10}" y="{ay + 5}" text-anchor="end" font-size="14" fill="{c["ink"]}">{chem("NO2")} 份量 a ＝ 2d − 8 增加</text>\n')
    ay2 = ay + 36
    b.append(f'<line x1="{x_of(6.4)}" y1="{ay2}" x2="{x_of(4.1)}" y2="{ay2}" stroke="{c["accent"]}" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ah2)"/>\n')
    b.append(f'<text x="{x_of(6.4) + 10}" y="{ay2 + 5}" font-size="14" fill="{c["ink"]}">{chem("O2")} 份量 c ＝ 14 − 2d 增加</text>\n')
    return shell(
        W, H, c,
        "NO2 + NH3 + O2 → N2 + H2O 的解集合",
        "固定 NH3 為 8、H2O 為 12 時，N2 的係數 d 可以是 4 到 7 之間任何值。兩端是只用 O2（R1）與只用 NO2（R2）的反應；d = 6 化簡後為 2:4:1:3:6，係數和 16，是段考答案；d = 5 得 2:8:4:5:12，係數和 31。",
        "".join(b),
    )


def main() -> None:
    for mode in THEMES:
        (OUT / f"nitrogen-ladder-zh-{mode}.svg").write_text(nitrogen_ladder(mode), encoding="utf-8")
        (OUT / f"no2-solution-line-zh-{mode}.svg").write_text(solution_line(mode), encoding="utf-8")
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
