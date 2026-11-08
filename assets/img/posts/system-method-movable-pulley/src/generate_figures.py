#!/usr/bin/env python3
"""Figures for 「動滑輪問題：為什麼不能直接用合力除以總質量？」 (system-method-movable-pulley).

Mobile-first: ~460-unit-wide canvases, free-body panels stacked vertically.

    python3 assets/img/posts/system-method-movable-pulley/src/generate_figures.py
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OUT.parent / "_figlib"))
from figlib import *  # noqa: E402,F401,F403

W = 460


def fig_setup(c):
    h = 490
    p = []
    cy = 44
    p.append(hatch(c, 60, 400, cy))
    r1, r2 = 24, 22
    mx, my = 190, 215
    lx, fx = mx - r1, mx + r1
    fcx, fcy = fx + r2, 96
    bx = fcx + r2
    p.append(line(lx, cy, lx, my, c["ink"], 2.6))
    p.append(f'<circle cx="{lx}" cy="{cy}" r="5" fill="{c["ink"]}"/>')
    p.append(line(fx, my, fx, fcy, c["ink"], 2.6))
    p.append(f'<path d="M {lx} {my} A {r1} {r1} 0 0 0 {fx} {my}" fill="none" stroke="{c["ink"]}" stroke-width="2.6"/>')
    p.append(line(fcx, cy, fcx, fcy, c["axis"], 3))
    p.append(f'<path d="M {fx} {fcy} A {r2} {r2} 0 0 1 {fcx + r2} {fcy}" fill="none" stroke="{c["ink"]}" stroke-width="2.6"/>')
    p.append(pulley(c, fcx, fcy, r2))
    p.append(pulley(c, mx, my, r1))
    by = 300
    p.append(line(bx, fcy, bx, by, c["ink"], 2.6))
    p.append(block(c, bx, by + 30, 60, 60, "2 kg", "b"))
    p.append(line(mx, my, mx, 290, c["axis"], 3))
    p.append(block(c, mx, 290 + 32, 76, 64, "3 kg", "a"))
    # labels
    p.append(text(lx - 12, 130, "繩端固定", "small", "end", c["muted"]))
    p.append(text(lx - 12, 232, "動滑輪", "small", "end", c["muted"]))
    p.append(text(fcx + r2 + 12, fcy + 6, "定滑輪", "small", "start", c["muted"]))
    # displacement arrows: q (50) and 2q (100)
    ax_ = 70
    p.append(arrow(ax_, 372, ax_, 322, c["accent"]))
    p.append(text(ax_, 396, "*q*", "strong", "middle", c["accent"]))
    p.append(text(ax_, 418, "向上", "small", "middle", c["accent"]))
    ax2 = bx + 62
    p.append(arrow(ax2, 300, ax2, 400, c["accent"]))
    p.append(text(ax2, 424, "2*q*", "strong", "middle", c["accent"]))
    p.append(text(ax2, 446, "向下", "small", "middle", c["accent"]))
    p.append(text(W / 2, 478, "動滑輪下有兩股繩：2*d*_3 + *d*_2 = 常數", "small", "middle", c["muted"]))
    return shell(c, W, h, "動滑輪系統示意圖",
                 "繩的一端固定在天花板，向下繞過掛有 3 公斤物體的動滑輪，再向上繞過定滑輪，自由端垂下掛 2 公斤物體。動滑輪下有兩股繩，所以動滑輪上升 q 時，2 公斤物體下降 2q。",
                 "\n".join("  " + s for s in p))


def fig_fbd(c):
    h = 750
    p = []
    k = 3.5
    T = 180 / 11
    cx, cy = 230, 170
    p.append(text(cx, 30, "對 3 kg（向上為正）", "strong", "middle", c["ink"]))
    p.append(block(c, cx, cy, 96, 70, "3 kg", "a"))
    for dx in (-20, 20):
        p.append(arrow(cx + dx, cy - 35, cx + dx, cy - 35 - T * k, c["accent"], 3.2))
    p.append(text(cx - 30, cy - 35 - T * k + 8, "*T*", "strong", "end", c["accent"]))
    p.append(text(cx + 30, cy - 35 - T * k + 8, "*T*", "strong", "start", c["accent"]))
    p.append(text(cx, cy - 35 - T * k - 12, "共 2*T*", "small", "middle", c["accent"]))
    p.append(arrow(cx, cy + 35, cx, cy + 35 + 30 * k, c["ink"]))
    p.append(text(cx + 12, cy + 35 + 30 * k, "3*g*", "", "start"))
    p.append(arrow(400, cy + 30, 400, cy - 30, c["muted"], 2))
    p.append(text(400, cy - 42, "正方向", "small", "middle", c["muted"]))
    p.append(text(cx, 354, "2*T* − 3*g* = 3*a*", "strong", "middle", c["accent"]))
    oy = 385
    cy = oy + 150
    p.append(text(cx, oy + 30, "對 2 kg（向下為正）", "strong", "middle", c["ink"]))
    p.append(block(c, cx, cy, 80, 70, "2 kg", "b"))
    p.append(arrow(cx, cy - 35, cx, cy - 35 - T * k, c["accent"], 3.2))
    p.append(text(cx + 12, cy - 35 - T * k + 8, "*T*", "strong", "start", c["accent"]))
    p.append(arrow(cx, cy + 35, cx, cy + 35 + 20 * k, c["ink"]))
    p.append(text(cx + 12, cy + 35 + 20 * k, "2*g*", "", "start"))
    p.append(arrow(400, cy - 30, 400, cy + 30, c["muted"], 2))
    p.append(text(400, cy - 42, "正方向", "small", "middle", c["muted"]))
    p.append(text(cx, oy + 290, "2*g* − *T* = 2·(2*a*) = 4*a*", "strong", "middle", c["accent"]))
    p.append(text(cx, oy + 316, "這個物體的加速度是 2*a*，不是 *a*", "small", "middle", c["muted"]))
    p.append(text(cx, oy + 344, "箭頭長度依本題數值按比例繪製", "small", "middle", c["muted"]))
    return shell(c, W, h, "動滑輪兩物體的自由體圖",
                 "3 公斤物體由動滑輪兩側各一股張力向上拉，共 2T，重力 3g 向下，向上為正；2 公斤物體受向上的張力 T 與向下的重力 2g，向下為正，加速度為 2a。",
                 "\n".join("  " + s for s in p))


if __name__ == "__main__":
    write(OUT, "setup", fig_setup, W, 490)
    write(OUT, "fbd", fig_fbd, W, 750)
