"""Shared helpers for the 整體法 (system-method) series figures.

Same Notes C2 palette as pursuit-problem-uniform-acceleration/src/generate_figures.py
(an <img> SVG cannot read page CSS variables, so values are copied; keep in sync with
_sass/kakau-c2.scss). The leading underscore keeps this folder out of the built site.

Label markup for text(): *x* = italic serif variable, _x or _{xy} = subscript.
"""

from __future__ import annotations

import html
import math

THEMES = {
    "light": {
        "raised": "#ffffff", "border": "#d8d9dc", "grid": "#ececee", "axis": "#6b7280",
        "ink": "#0b1730", "text": "#1f232b", "muted": "#555b66",
        "accent": "#216e84", "accent_wash": "#eef6f7", "other": "#6b7280", "other_wash": "#f1f2f4",
        "point": "#d8951d",
    },
    "dark": {
        "raised": "#1a1c21", "border": "#33353a", "grid": "#25272c", "axis": "#8a909c",
        "ink": "#b7c6e6", "text": "#d4d7dd", "muted": "#a5aab4",
        "accent": "#9bd7dd", "accent_wash": "#1a2c32", "other": "#a5aab4", "other_wash": "#25272c",
        "point": "#e3a93a",
    },
}

SANS = '"Source Sans Pro", "PingFang TC", "Microsoft JhengHei", "Noto Sans TC", "Noto Sans CJK TC", sans-serif'
SERIF = '"STIX Two Text", "Latin Modern Roman", "Times New Roman", serif'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def rich(s: str) -> str:
    out, i, ital = [], 0, False
    while i < len(s):
        ch = s[i]
        if ch == "*":
            ital = not ital
            i += 1
            continue
        if ch == "_":
            if i + 1 < len(s) and s[i + 1] == "{":
                j = s.index("}", i)
                sub = s[i + 2:j]
                i = j + 1
            else:
                sub = s[i + 1]
                i += 2
            fam = f" font-family='{SERIF}' font-style='italic'" if ital else ""
            out.append(f'<tspan baseline-shift="sub" font-size="72%"{fam}>{esc(sub)}</tspan>')
            continue
        if ital:
            out.append(f"<tspan font-family='{SERIF}' font-style='italic'>{esc(ch)}</tspan>")
        else:
            out.append(esc(ch))
        i += 1
    return "".join(out)


def shell(c, w, h, title, desc, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(desc)}</desc>
  <style>
    text {{ font-family: {SANS}; fill: {c['text']}; font-size: 19px; }}
    .strong {{ font-weight: 700; }}
    .small {{ font-size: 16px; }}
    .muted {{ fill: {c['muted']}; }}
  </style>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{c['raised']}" stroke="{c['border']}"/>
{body}
</svg>
"""


def text(x, y, s, cls="", anchor="start", color=None):
    st = f' style="fill:{color}"' if color else ""
    cl = f' class="{cls}"' if cls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}"{cl} text-anchor="{anchor}"{st}>{rich(s)}</text>'


def line(x1, y1, x2, y2, color, width=1.8, dash=False):
    d = ' stroke-dasharray="5 5"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>'


def arrow(x1, y1, x2, y2, color, width=2.6, head=11):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    px, py = -math.sin(ang) * head * 0.42, math.cos(ang) * head * 0.42
    pts = f"{x2:.1f},{y2:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}"
    return (line(x1, y1, bx, by, color, width) +
            f'<polygon points="{pts}" fill="{color}"/>')


def block(c, cx, cy, w, h, label, kind="a", angle=0, lab_dy=6):
    fill, stroke = (c["accent_wash"], c["accent"]) if kind == "a" else (c["other_wash"], c["other"])
    rect = (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({angle})">'
            f'<rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="2.4"/></g>')
    return rect + text(cx, cy + lab_dy, label, "strong", "middle", stroke)


def pulley(c, cx, cy, r=22):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{c["raised"]}" stroke="{c["axis"]}" stroke-width="2.4"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{c["axis"]}"/>')


def hatch(c, x1, x2, y, depth=12, step=14):
    p = [line(x1, y, x2, y, c["axis"], 2.4)]
    x = x1
    while x < x2:
        p.append(line(x, y, x - depth, y - depth, c["axis"], 1.2))
        x += step
    return "".join(p)


def write(out, name, fn, w, h):
    for mode, c in THEMES.items():
        path = out / f"{name}-zh-{mode}.svg"
        path.write_text(fn(c), encoding="utf-8")
        print(path)
