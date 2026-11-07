#!/usr/bin/env python3
"""Figures for 「整體法是什麼？從最基本的滑車問題…」 (system-method-basic-pulley).

    python3 assets/img/posts/system-method-basic-pulley/src/generate_figures.py
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OUT.parent / "_figlib"))
from figlib import *  # noqa: E402,F401,F403


def fig_setup(c):
    w, h = 860, 420
    p = []
    ty = 250                      # table top
    p.append(f'<rect x="70" y="{ty}" width="500" height="22" fill="{c["other_wash"]}" stroke="{c["axis"]}" stroke-width="2"/>')
    p.append(text(150, ty + 17, "光滑桌面", "small", "middle", c["muted"]))
    px, py, r = 570, ty - 28 + 22, 22          # pulley centre; rope height = py - r
    rope_y = py - r
    p.append(line(px - 6, ty + 11, px, py, c["axis"], 3))
    p.append(pulley(c, px, py, r))
    ax_c = 300
    p.append(block(c, ax_c, ty - 32, 100, 64, "A  5 kg", "a"))
    p.append(line(ax_c + 50, rope_y, px, rope_y, c["ink"], 2.4))
    p.append(f'<path d="M {px} {rope_y} A {r} {r} 0 0 1 {px + r} {py}" fill="none" stroke="{c["ink"]}" stroke-width="2.4"/>')
    bx = px + r
    p.append(line(bx, py, bx, 320, c["ink"], 2.4))
    p.append(block(c, bx, 320 + 40, 84, 80, "B  10 kg", "b"))
    p.append(text(bx + 70, 305, "輕繩", "small", "start", c["muted"]))
    # displacement arrows (same q)
    p.append(arrow(ax_c - 40, ty - 86, ax_c + 60, ty - 86, c["accent"]))
    p.append(text(ax_c + 10, ty - 98, "*x*_A = *q*（朝滑輪為正）", "small", "middle", c["accent"]))
    p.append(arrow(bx + 78, 330, bx + 78, 410 - 8, c["accent"]))
    p.append(text(bx + 92, 372, "*y*_B = *q*", "small", "start", c["accent"]))
    p.append(text(bx + 92, 392, "（向下為正）", "small", "start", c["accent"]))
    p.append(text(60, 60, "繩長不變 ⇒ A 前進多少，B 就下降多少", "strong", "start", c["ink"]))
    p.append(text(60, 88, "兩者共用同一個座標 *q*，加速度大小相同：*a*_A = *a*_B = *a*", "small", "start", c["muted"]))
    return shell(c, w, h, "滑車問題示意圖",
                 "光滑水平桌面上的物體 A（5 公斤）以輕繩跨過桌邊定滑輪，連接垂掛的物體 B（10 公斤）。A 朝滑輪前進的位移與 B 下降的位移相同，都記為 q。",
                 "\n".join("  " + s for s in p))


def fig_fbd(c):
    w, h = 860, 430
    p = []
    L = 1.1   # px per N (g = 10): weight A 50 N, weight B 100 N, N = 50, T = 100/3
    # panel A
    cx, cy = 230, 215
    p.append(text(cx, 52, "對 A（水平方向，朝滑輪為正）", "strong", "middle", c["ink"]))
    p.append(block(c, cx, cy, 110, 66, "A", "a"))
    p.append(arrow(cx, cy - 33, cx, cy - 33 - 50 * L, c["ink"]))
    p.append(text(cx + 10, cy - 33 - 50 * L + 6, "*N*", "", "start"))
    p.append(arrow(cx, cy + 33, cx, cy + 33 + 50 * L, c["ink"]))
    p.append(text(cx + 10, cy + 33 + 50 * L - 2, "*m*_A *g*", "", "start"))
    p.append(arrow(cx + 55, cy, cx + 55 + 100 / 3 * L * 1.6, cy, c["accent"], 3.2))
    p.append(text(cx + 55 + 100 / 3 * L * 1.6 + 8, cy + 6, "*T*", "strong", "start", c["accent"]))
    p.append(arrow(cx - 150, cy - 95, cx - 90, cy - 95, c["muted"], 2))
    p.append(text(cx - 150, cy - 105, "正方向", "small", "start", c["muted"]))
    p.append(text(cx, 385, "*T* = *m*_A *a*", "strong", "middle", c["accent"]))
    p.append(text(cx, 408, "鉛直方向 *N* 與 *m*_A *g* 平衡，不提供加速度資訊", "small", "middle", c["muted"]))
    # panel B
    bx, by = 630, 215
    p.append(text(bx, 52, "對 B（鉛直方向，向下為正）", "strong", "middle", c["ink"]))
    p.append(block(c, bx, by, 90, 80, "B", "b"))
    p.append(arrow(bx, by - 40, bx, by - 40 - 100 / 3 * L * 1.6, c["accent"], 3.2))
    p.append(text(bx + 10, by - 40 - 100 / 3 * L * 1.6 + 8, "*T*", "strong", "start", c["accent"]))
    p.append(arrow(bx, by + 40, bx, by + 40 + 100 * L * 0.9, c["ink"]))
    p.append(text(bx + 10, by + 40 + 100 * L * 0.9 - 2, "*m*_B *g*", "", "start"))
    p.append(arrow(bx + 120, by - 40, bx + 120, by + 20, c["muted"], 2))
    p.append(text(bx + 130, by - 14, "正方向", "small", "start", c["muted"]))
    p.append(text(bx, 385, "*m*_B *g* − *T* = *m*_B *a*", "strong", "middle", c["accent"]))
    p.append(text(bx, 408, "箭頭長度依本題數值大致按比例繪製", "small", "middle", c["muted"]))
    return shell(c, w, h, "A、B 的自由體圖",
                 "A 受重力、正向力與水平向右的張力；B 受向下的重力與向上的張力。A 以朝滑輪為正，B 以向下為正，分別寫出 T = m_A a 與 m_B g − T = m_B a。",
                 "\n".join("  " + s for s in p))


if __name__ == "__main__":
    write(OUT, "setup", fig_setup, 860, 420)
    write(OUT, "fbd", fig_fbd, 860, 430)
