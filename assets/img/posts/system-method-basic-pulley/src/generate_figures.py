#!/usr/bin/env python3
"""Figures for 「整體法是什麼？從最基本的滑車問題…」 (system-method-basic-pulley).

Mobile-first: canvases are ~460 units wide so the 16–19px text stays readable at ~288px.

    python3 assets/img/posts/system-method-basic-pulley/src/generate_figures.py
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OUT.parent / "_figlib"))
from figlib import *  # noqa: E402,F401,F403

W = 460


def fig_setup(c):
    h = 350
    p = []
    ty = 200
    p.append(f'<rect x="16" y="{ty}" width="276" height="20" fill="{c["other_wash"]}" stroke="{c["axis"]}" stroke-width="2"/>')
    p.append(text(154, ty + 15, "光滑桌面", "small", "middle", c["muted"]))
    px, r = 312, 20
    rope_y = ty - 28
    py = rope_y + r
    p.append(line(292, ty + 10, px, py, c["axis"], 3))
    p.append(pulley(c, px, py, r))
    p.append(block(c, 140, ty - 28, 104, 56, "A  5 kg", "a"))
    p.append(line(192, rope_y, px, rope_y, c["ink"], 2.4))
    p.append(f'<path d="M {px} {rope_y} A {r} {r} 0 0 1 {px + r} {py}" fill="none" stroke="{c["ink"]}" stroke-width="2.4"/>')
    bx = px + r
    p.append(line(bx, py, bx, 252, c["ink"], 2.4))
    p.append(block(c, bx, 252 + 36, 96, 72, "B 10 kg", "b"))
    p.append(arrow(96, 112, 184, 112, c["accent"]))
    p.append(text(140, 76, "*x*_A = *q*", "", "middle", c["accent"]))
    p.append(text(140, 98, "朝滑輪為正", "small", "middle", c["accent"]))
    ax_ = 262
    p.append(arrow(ax_, 262, ax_, 330, c["accent"]))
    p.append(text(ax_ - 10, 290, "*y*_B = *q*", "", "end", c["accent"]))
    p.append(text(ax_ - 10, 312, "向下為正", "small", "end", c["accent"]))
    return shell(c, W, h, "滑車問題示意圖",
                 "光滑水平桌面上的物體 A（5 公斤）以輕繩跨過桌邊定滑輪，連接垂掛的物體 B（10 公斤）。A 朝滑輪前進的位移與 B 下降的位移相同，都記為 q。",
                 "\n".join("  " + s for s in p))


def fig_fbd(c):
    h = 700
    p = []
    L = 1.0
    T = 100 / 3
    # panel A
    cx, cy = 230, 150
    p.append(text(cx, 34, "對 A（朝滑輪為正）", "strong", "middle", c["ink"]))
    p.append(block(c, cx, cy, 104, 60, "A", "a"))
    p.append(arrow(cx, cy - 30, cx, cy - 30 - 50 * L, c["ink"]))
    p.append(text(cx + 10, cy - 30 - 50 * L + 8, "*N*", "", "start"))
    p.append(arrow(cx, cy + 30, cx, cy + 30 + 50 * L, c["ink"]))
    p.append(text(cx + 10, cy + 30 + 50 * L, "*m*_A *g*", "", "start"))
    p.append(arrow(cx + 52, cy, cx + 52 + T * 1.9, cy, c["accent"], 3.2))
    p.append(text(cx + 52 + T * 1.9 + 8, cy + 7, "*T*", "strong", "start", c["accent"]))
    p.append(arrow(36, cy, 100, cy, c["muted"], 2))
    p.append(text(68, cy - 12, "正方向", "small", "middle", c["muted"]))
    p.append(text(cx, 278, "*T* = *m*_A *a*", "strong", "middle", c["accent"]))
    p.append(text(cx, 304, "鉛直方向 *N* 與 *m*_A *g* 平衡", "small", "middle", c["muted"]))
    # panel B
    oy = 340
    cx, cy = 230, oy + 150
    p.append(text(cx, oy + 34, "對 B（向下為正）", "strong", "middle", c["ink"]))
    p.append(block(c, cx, cy, 92, 76, "B", "b"))
    p.append(arrow(cx, cy - 38, cx, cy - 38 - T * 1.9, c["accent"], 3.2))
    p.append(text(cx + 10, cy - 38 - T * 1.9 + 10, "*T*", "strong", "start", c["accent"]))
    p.append(arrow(cx, cy + 38, cx, cy + 38 + 100 * 0.9, c["ink"]))
    p.append(text(cx + 10, cy + 38 + 100 * 0.9, "*m*_B *g*", "", "start"))
    p.append(arrow(400, cy - 40, 400, cy + 30, c["muted"], 2))
    p.append(text(400, cy - 52, "正方向", "small", "middle", c["muted"]))
    p.append(text(cx, oy + 322, "*m*_B *g* − *T* = *m*_B *a*", "strong", "middle", c["accent"]))
    p.append(text(cx, oy + 348, "箭頭長度依本題數值大致按比例繪製", "small", "middle", c["muted"]))
    return shell(c, W, h, "A、B 的自由體圖",
                 "A 受重力、正向力與水平向右的張力；B 受向下的重力與向上的張力。A 以朝滑輪為正，B 以向下為正，分別寫出 T = m_A a 與 m_B g − T = m_B a。",
                 "\n".join("  " + s for s in p))


if __name__ == "__main__":
    write(OUT, "setup", fig_setup, W, 350)
    write(OUT, "fbd", fig_fbd, W, 700)
