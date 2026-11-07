#!/usr/bin/env python3
"""Figures for 「動滑輪問題：為什麼不能直接用合力除以總質量？」 (system-method-movable-pulley).

    python3 assets/img/posts/system-method-movable-pulley/src/generate_figures.py
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OUT.parent / "_figlib"))
from figlib import *  # noqa: E402,F401,F403


def fig_setup(c):
    w, h = 900, 530
    p = []
    cy = 60                                           # ceiling line
    p.append(hatch(c, 200, 700, cy))
    r1, r2 = 26, 24
    mx, my = 290, 250                                 # movable pulley centre
    fx = mx + r1                                      # right strand x
    fcx, fcy = fx + r2, 110                           # fixed pulley centre
    lx = mx - r1                                      # left strand x
    p.append(line(lx, cy, lx, my, c["ink"], 2.6))     # fixed end -> movable pulley (strand 1)
    p.append(f'<circle cx="{lx}" cy="{cy}" r="5" fill="{c["ink"]}"/>')
    p.append(line(fx, my, fx, fcy, c["ink"], 2.6))    # movable pulley -> fixed pulley (strand 2)
    p.append(f'<path d="M {lx} {my} A {r1} {r1} 0 0 0 {fx} {my}" fill="none" stroke="{c["ink"]}" stroke-width="2.6"/>')
    p.append(line(fcx, cy, fcx, fcy, c["axis"], 3))
    p.append(f'<path d="M {fx} {fcy} A {r2} {r2} 0 0 1 {fcx + r2} {fcy}" fill="none" stroke="{c["ink"]}" stroke-width="2.6"/>')
    p.append(pulley(c, fcx, fcy, r2))
    p.append(pulley(c, mx, my, r1))
    # 2 kg block
    bx = fcx + r2
    by = 340
    p.append(line(bx, fcy, bx, by, c["ink"], 2.6))
    p.append(block(c, bx, by + 32, 64, 64, "2 kg", "b", lab_dy=6))
    # 3 kg block hanging from movable pulley
    p.append(line(mx, my, mx, 322, c["axis"], 3))
    p.append(block(c, mx, 322 + 40, 80, 80, "3 kg", "a", lab_dy=6))
    # labels
    p.append(text(lx - 14, 150, "繩的一端固定", "small", "end", c["muted"]))
    p.append(text(lx - 14, 214, "兩股繩支撐動滑輪", "small", "end", c["muted"]))
    p.append(text(mx - r1 - 10, my + 56, "動滑輪", "small", "end", c["muted"]))
    p.append(text(fcx + r2 + 14, fcy - 8, "定滑輪", "small", "start", c["muted"]))
    # displacement arrows: 3 kg up q (50 px), 2 kg down 2q (100 px)
    ax_ = mx - 100
    p.append(arrow(ax_, 395, ax_, 345, c["accent"]))
    p.append(text(ax_ - 10, 372, "*q*（向上）", "small", "end", c["accent"]))
    ax2 = bx + 70
    p.append(arrow(ax2, by + 10, ax2, by + 110, c["accent"]))
    p.append(text(ax2 + 12, by + 62, "2*q*（向下）", "small", "start", c["accent"]))
    p.append(text(40, 500, "繩長不變：2*d*_3 + *d*_2 = 常數  ⇒  動滑輪上升 *q*，2 kg 下降 2*q*", "strong", "start", c["ink"]))
    p.append(text(40, 522, "*d*_3：動滑輪的深度；*d*_2：2 kg 物體自定滑輪下垂的長度", "small", "start", c["muted"]))
    return shell(c, w, h, "動滑輪系統示意圖",
                 "繩的一端固定在天花板，向下繞過掛有 3 公斤物體的動滑輪，再向上繞過定滑輪，自由端垂下掛 2 公斤物體。動滑輪下有兩股繩，所以動滑輪上升 q 時，2 公斤物體下降 2q。",
                 "\n".join("  " + s for s in p))


def fig_fbd(c):
    w, h = 860, 480
    p = []
    k = 4.0   # px per N (g = 10): 2T = 32.7 N, 3g = 30 N, T = 16.4 N, 2g = 20 N
    T = 180 / 11
    cx, cy = 230, 225
    p.append(text(cx, 50, "對 3 kg（動滑輪與物體，向上為正）", "strong", "middle", c["ink"]))
    p.append(block(c, cx, cy, 96, 70, "3 kg", "a"))
    p.append(arrow(cx - 18, cy - 35, cx - 18, cy - 35 - T * k, c["accent"], 3.2))
    p.append(arrow(cx + 18, cy - 35, cx + 18, cy - 35 - T * k, c["accent"], 3.2))
    p.append(text(cx - 28, cy - 35 - T * k + 4, "*T*", "strong", "end", c["accent"]))
    p.append(text(cx + 28, cy - 35 - T * k + 4, "*T*", "strong", "start", c["accent"]))
    p.append(text(cx, cy - 35 - T * k - 14, "共 2*T*", "small", "middle", c["accent"]))
    p.append(arrow(cx, cy + 35, cx, cy + 35 + 30 * k, c["ink"]))
    p.append(text(cx + 12, cy + 35 + 30 * k, "3*g*", "", "start"))
    p.append(arrow(cx + 100, cy + 20, cx + 100, cy - 40, c["muted"], 2))
    p.append(text(cx + 110, cy - 10, "正方向", "small", "start", c["muted"]))
    p.append(text(cx, 428, "2*T* − 3*g* = 3*a*", "strong", "middle", c["accent"]))
    bx = 640
    p.append(text(bx, 50, "對 2 kg（向下為正）", "strong", "middle", c["ink"]))
    p.append(block(c, bx, cy, 80, 70, "2 kg", "b"))
    p.append(arrow(bx, cy - 35, bx, cy - 35 - T * k, c["accent"], 3.2))
    p.append(text(bx + 12, cy - 35 - T * k + 4, "*T*", "strong", "start", c["accent"]))
    p.append(arrow(bx, cy + 35, bx, cy + 35 + 20 * k, c["ink"]))
    p.append(text(bx + 12, cy + 35 + 20 * k, "2*g*", "", "start"))
    p.append(arrow(bx + 100, cy - 40, bx + 100, cy + 20, c["muted"], 2))
    p.append(text(bx + 110, cy - 10, "正方向", "small", "start", c["muted"]))
    p.append(text(bx, 428, "2*g* − *T* = 2·(2*a*) = 4*a*", "strong", "middle", c["accent"]))
    p.append(text(bx, 452, "加速度是 2*a*，不是 *a*", "small", "middle", c["muted"]))
    p.append(text(cx, 452, "箭頭長度依本題數值按比例繪製", "small", "middle", c["muted"]))
    return shell(c, w, h, "動滑輪兩物體的自由體圖",
                 "3 公斤物體由動滑輪兩側各一股張力向上拉，共 2T，重力 3g 向下，向上為正；2 公斤物體受向上的張力 T 與向下的重力 2g，向下為正，加速度為 2a。",
                 "\n".join("  " + s for s in p))


if __name__ == "__main__":
    write(OUT, "setup", fig_setup, 900, 530)
    write(OUT, "fbd", fig_fbd, 860, 480)
