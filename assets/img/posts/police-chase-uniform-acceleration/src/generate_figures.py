#!/usr/bin/env python3
"""Generate the SVG figures for the police-chase (追趕問題) post.

Styled with the Notes C2 tokens (see _sass/kakau-c2.scss): neutral surface card with a
hairline border and 14px radius, blue-teal accent for the protagonist (警車), neutral grey
for the other car, brand ink for text, and gold only as a small decorative mark.
An <img> SVG cannot read page CSS variables, so the values are copied here; keep them in
sync with kakau-c2.scss if the palette changes.

    python3 assets/img/posts/police-chase-uniform-acceleration/src/generate_figures.py
"""

from __future__ import annotations

import html
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]

THEMES = {
    "light": {
        "raised": "#ffffff",
        "border": "#d8d9dc",        # --c2-border over white
        "grid": "#ececee",
        "axis": "#6b7280",          # --c2-border-control
        "ink": "#0b1730",           # --c2-brand-ink
        "text": "#1f232b",          # --c2-text
        "muted": "#555b66",         # --c2-muted
        "accent": "#216e84",        # --c2-accent
        "accent_wash": "#eef6f7",   # --c2-accent-wash
        "accent_fill": "#216e8433",
        "on_accent": "#ffffff",
        "other": "#6b7280",         # neutral grey for 賊車
        "on_other": "#ffffff",
        "point": "#d8951d",         # --c2-point (decoration only)
    },
    "dark": {
        "raised": "#1a1c21",
        "border": "#33353a",
        "grid": "#25272c",
        "axis": "#8a909c",
        "ink": "#b7c6e6",
        "text": "#d4d7dd",
        "muted": "#a5aab4",
        "accent": "#9bd7dd",
        "accent_wash": "#1a2c32",
        "accent_fill": "#9bd7dd33",
        "on_accent": "#101114",
        "other": "#a5aab4",
        "on_other": "#101114",
        "point": "#e3a93a",
    },
}

SANS = '"Source Sans Pro", "PingFang TC", "Microsoft JhengHei", "Noto Sans TC", "Noto Sans CJK TC", sans-serif'
SERIF = '"STIX Two Text", "Latin Modern Roman", "Times New Roman", serif'


VARS = {"x", "t", "v"}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def rich(s: str) -> str:
    """Variables x, t, v -> italic serif; '^n' -> superscript; units (m, s) and CJK stay upright."""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == "^" and i + 1 < len(s):
            out.append(f'<tspan baseline-shift="super" font-size="70%">{esc(s[i + 1])}</tspan>')
            i += 2
            continue
        if ch in VARS:
            out.append(f'<tspan font-family=\'{SERIF}\' font-style="italic">{esc(ch)}</tspan>')
        else:
            out.append(esc(ch))
        i += 1
    return "".join(out)


def shell(c: dict[str, str], w: int, h: int, title: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
  <title id="title">{esc(title)}</title>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="{c['axis']}"/>
    </marker>
  </defs>
  <style>
    text {{ font-family: {SANS}; fill: {c['text']}; font-size: 17px; }}
    .strong {{ font-weight: 700; }}
    .small {{ font-size: 14px; }}
    .muted {{ fill: {c['muted']}; }}
  </style>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{c['raised']}" stroke="{c['border']}"/>
{body}
</svg>
"""


def text(x: float, y: float, value: str, cls: str = "", anchor: str = "start", color: str | None = None, raw: bool = False) -> str:
    style = f' style="fill:{color}"' if color else ""
    cls_attr = f' class="{cls}"' if cls else ""
    content = value if raw else rich(value)
    return f'<text x="{x:.1f}" y="{y:.1f}"{cls_attr} text-anchor="{anchor}"{style}>{content}</text>'


def line(x1, y1, x2, y2, color, width=1.5, dash=False, arrow=False) -> str:
    d = ' stroke-dasharray="5 5"' if dash else ""
    a = ' marker-end="url(#arrow)"' if arrow else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}{a}/>'


def car_dot(c, x, y, kind, r=9):
    """警車 = solid accent; 賊車 = ring in neutral grey (shape + colour, not colour alone)."""
    if kind == "police":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c["accent"]}"/>'
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r - 1.5}" fill="{c["raised"]}" stroke="{c["other"]}" stroke-width="3"/>'


def point_mark(c, x, y, r=7):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c["point"]}" stroke="{c["raised"]}" stroke-width="2.5"/>'


def kcolor(c, kind):
    return c["accent"] if kind == "police" else c["muted"]


# 圖 1：重繪的軌跡圖（警車 0, 5, 15, 30 小格；賊車 0, 4, 12, 24 小格）
def fig_trajectory(c):
    w, h = 960, 380
    x0, cell, cells = 150, 22, 34
    top, bottom = 84, 300
    rows = {"賊車": (150, [0, 4, 12, 24], "thief"), "警車": (240, [0, 5, 15, 30], "police")}
    p = []
    for i in range(cells + 1):
        x = x0 + i * cell
        major = i % 5 == 0
        p.append(line(x, top, x, bottom, c["border"] if major else c["grid"], 1.2 if major else 1))
    for name, (y, pos, kind) in rows.items():
        p.append(line(x0, y, x0 + cells * cell, y, c["axis"], 1.2))
        p.append(text(x0 - 24, y + 6, name, "strong", "end", kcolor(c, kind)))
        for t, pp in enumerate(pos):
            x = x0 + pp * cell
            p.append(car_dot(c, x, y, kind))
            p.append(text(x, y - 18, f"{t} s", "small", "middle", kcolor(c, kind)))
    for i in range(0, cells + 1, 5):
        p.append(text(x0 + i * cell, bottom + 24, f"{i}", "small", "middle", c["muted"]))
    p.append(text(x0 - 24, bottom + 24, "小格", "small", "end", c["muted"]))
    p.append(text(x0, 50, "起點", "small", "middle", c["muted"]))
    p.append(text(w - 36, 50, "1 小格 = 2 m", "small", "end", c["muted"]))
    # 結論 pill
    p.append(f'<rect x="{w - 36 - 330}" y="{bottom + 44}" width="330" height="36" rx="10" fill="{c["accent_wash"]}" stroke="{c["border"]}"/>')
    p.append(text(w - 36 - 165, bottom + 68, "每一刻：警車路程 ÷ 賊車路程 = 5/4", "strong", "middle", c["accent"]))
    return shell(c, w, h, "重繪的兩車軌跡圖：每秒一點", "\n".join("  " + s for s in p))


# 圖 2：比例速解的「份數」圖
def fig_parts(c):
    w, h = 1040, 360
    x0, seg = 130, 140
    catch = x0 + 5 * seg
    p = []
    rows = [("警車", 150, 0, "police", "跑 5 份 = 180 m"), ("賊車", 230, 1, "thief", "跑 4 份 = 144 m")]
    for name, y, start, kind, note in rows:
        col = kcolor(c, kind)
        bar = c["accent"] if kind == "police" else c["other"]
        on = c["on_accent"] if kind == "police" else c["on_other"]
        p.append(text(x0 - 22, y + 6, name, "strong", "end", col))
        for k in range(start, 5):
            x = x0 + k * seg
            p.append(f'<rect x="{x + 3:.1f}" y="{y - 20:.1f}" width="{seg - 6}" height="40" rx="8" fill="{bar}"/>')
            p.append(text(x + seg / 2, y + 6, "36 m", "strong", "middle", on))
        p.append(text(catch + 16, y + 6, note, "strong", "start", col))
    p.append(line(x0, 268, x0, 296, c["axis"], 1.5))
    p.append(line(x0 + seg, 268, x0 + seg, 296, c["axis"], 1.5))
    p.append(line(x0, 282, x0 + seg, 282, c["axis"], 1.5))
    p.append(text(x0 + seg / 2, 318, "起始差距 36 m = 1 份", "small", "middle", c["muted"]))
    p.append(line(catch, 104, catch, 296, c["axis"], 1.8, dash=True))
    p.append(point_mark(c, catch, 96, 8))
    p.append(text(catch + 20, 102, "追上", "strong", "start"))
    p.append(text(x0, 80, "起點（警車）", "small", "middle", c["muted"]))
    return shell(c, w, h, "比例速解：多跑的 1 份就是 36 公尺", "\n".join("  " + s for s in p))


class Axes:
    def __init__(self, left, right, top, bottom, tmax, ymax):
        self.left, self.right, self.top, self.bottom = left, right, top, bottom
        self.tmax, self.ymax = tmax, ymax

    def px(self, t):
        return self.left + (self.right - self.left) * t / self.tmax

    def py(self, y):
        return self.bottom - (self.bottom - self.top) * y / self.ymax

    def frame(self, c, tstep, ystep, ylabel, yunit):
        p = []
        t = 0.0
        while t <= self.tmax + 1e-9:
            x = self.px(t)
            p.append(line(x, self.top, x, self.bottom, c["grid"], 1))
            p.append(text(x, self.bottom + 26, f"{t:g}", "small", "middle", c["muted"]))
            t += tstep
        y = 0.0
        while y <= self.ymax + 1e-9:
            py = self.py(y)
            p.append(line(self.left, py, self.right, py, c["grid"], 1))
            p.append(text(self.left - 12, py + 5, f"{y:g}", "small", "end", c["muted"]))
            y += ystep
        p.append(line(self.left, self.bottom, self.right + 26, self.bottom, c["axis"], 1.8, arrow=True))
        p.append(line(self.left, self.bottom, self.left, self.top - 26, c["axis"], 1.8, arrow=True))
        p.append(text(self.right + 34, self.bottom + 6, "t", "", "start"))
        p.append(text(self.right + 34, self.bottom + 26, "(s)", "small", "start", c["muted"]))
        p.append(text(self.left, self.top - 38, ylabel, "", "end"))
        p.append(text(self.left + 6, self.top - 38, f"({yunit})", "small", "start", c["muted"]))
        return p

    def curve(self, f, t1, color, width=3.5, n=80):
        pts = " ".join(f"{self.px(t1 * k / n):.1f},{self.py(f(t1 * k / n)):.1f}" for k in range(n + 1))
        return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


T_CATCH = math.sqrt(18)


# 圖 3：x-t 圖
def fig_xt(c):
    w, h = 960, 560
    ax = Axes(110, 850, 78, 480, 5, 260)
    p = ax.frame(c, 1, 50, "x", "m")
    p.append(ax.curve(lambda t: 36 + 8 * t * t, 5, c["other"], 3))
    p.append(ax.curve(lambda t: 10 * t * t, 5, c["accent"], 3.8))
    xc, yc = ax.px(T_CATCH), ax.py(180)
    p.append(line(xc, yc, xc, ax.bottom, c["axis"], 1.5, dash=True))
    p.append(line(ax.left, yc, xc, yc, c["axis"], 1.5, dash=True))
    p.append(text(ax.left + 12, yc - 9, "180", "small", "start", c["muted"]))
    p.append(point_mark(c, xc, yc, 8))
    p.append(text(xc + 16, ax.py(150), "追上", "strong", "start"))
    p.append(text(xc + 16, ax.py(150) + 24, "t ≈ 4.24 s", "small", "start", c["muted"]))
    p.append(text(xc + 16, ax.py(150) + 46, "x = 180 m", "small", "start", c["muted"]))
    y36 = ax.py(36)
    p.append(line(ax.left + 16, ax.bottom - 2, ax.left + 16, y36 + 2, c["accent"], 2.5))
    p.append(text(ax.left + 28, (ax.bottom + y36) / 2 + 5, "相距 36 m", "small", "start", c["accent"]))
    p.append(text(ax.px(1.0), ax.py(100), "賊車 x = 36 + 8t^2", "strong", "start", c["muted"]))
    p.append(text(ax.px(3.0), ax.py(40), "警車 x = 10t^2", "strong", "start", c["accent"]))
    return shell(c, w, h, "兩車的 x-t 圖：交點就是追上的時刻與位置", "\n".join("  " + s for s in p))


# 圖 4：v-t 圖
def fig_vt(c):
    w, h = 960, 560
    ax = Axes(110, 850, 78, 480, 5, 100)
    p = ax.frame(c, 1, 20, "v", "m/s")
    tc = T_CATCH
    tri = f"{ax.px(0):.1f},{ax.py(0):.1f} {ax.px(tc):.1f},{ax.py(20 * tc):.1f} {ax.px(tc):.1f},{ax.py(16 * tc):.1f}"
    p.append(f'<polygon points="{tri}" fill="{c["accent_fill"]}" stroke="none"/>')
    p.append(ax.curve(lambda t: 16 * t, 5, c["other"], 3, n=2))
    p.append(ax.curve(lambda t: 20 * t, 5, c["accent"], 3.8, n=2))
    xc = ax.px(tc)
    p.append(line(xc, ax.py(20 * tc), xc, ax.bottom, c["axis"], 1.5, dash=True))
    p.append(text(xc, ax.bottom + 50, "4.24", "small", "middle", c["muted"]))
    lx = ax.px(3.3)
    p.append(line(lx, ax.py(36), lx, ax.py(59), c["accent"], 1.5))
    p.append(f'<circle cx="{lx:.1f}" cy="{ax.py(59):.1f}" r="3.5" fill="{c["accent"]}"/>')
    p.append(text(lx, ax.py(36) + 22, "面積 = 36 m", "strong", "middle", c["accent"]))
    p.append(text(lx, ax.py(36) + 44, "（被追回的差距）", "small", "middle", c["accent"]))
    p.append(text(ax.px(4.6), ax.py(20 * 4.6) - 14, "警車 v = 20t", "strong", "end", c["accent"]))
    p.append(text(ax.px(4.95), ax.py(40), "賊車 v = 16t", "strong", "end", c["muted"]))
    return shell(c, w, h, "兩車的 v-t 圖：兩線之間的面積就是被追回的距離", "\n".join("  " + s for s in p))


FIGS = {"trajectory": fig_trajectory, "ratio-parts": fig_parts, "x-t": fig_xt, "v-t": fig_vt}


def main() -> None:
    for name, fn in FIGS.items():
        for mode, c in THEMES.items():
            path = OUT / f"{name}-zh-{mode}.svg"
            path.write_text(fn(c), encoding="utf-8")
            print(path.relative_to(OUT.parents[3]))


if __name__ == "__main__":
    main()
