#!/usr/bin/env python3
"""Figures for 「整體法的真正公式：從三物體連結體到廣義座標」 (system-method-general-formula).

Mobile-first: ~460-unit-wide canvases, free-body panels stacked vertically.

    python3 assets/img/posts/system-method-general-formula/src/generate_figures.py
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OUT.parent / "_figlib"))
from figlib import *  # noqa: E402,F401,F403

W = 460
SETUP_H = 530
FBD_H = 945


def fig_setup(c):
    p = []
    cy = 40
    ink, axis = c["ink"], c["axis"]
    p.append(hatch(c, 130, 280, cy))
    r = 20
    # movable pulley (A) and fixed pulley 1 (ceiling)
    mx, my = 180, 230
    lx, fx = mx - r, mx + r                      # 160, 200
    p1x, p1y = fx + r, 82                         # fixed pulley 1 centre (220, 82)
    b1x = p1x + r                                 # rope 1 meets B at x = 240
    # B has two hooks: rope 1 (left) and rope 2 (right)
    b2x = 310
    btop = 300
    bcx, bcy, bw, bh = (b1x + b2x) / 2, btop + 30, 84, 60
    # table + pulley 2 + C
    p2x, p2y = 330, 148
    tabley = 150
    # rope 1
    p.append(line(lx, cy, lx, my, ink, 2.6))
    p.append(f'<circle cx="{lx}" cy="{cy}" r="5" fill="{ink}"/>')
    p.append(f'<path d="M {lx} {my} A {r} {r} 0 0 0 {fx} {my}" fill="none" stroke="{ink}" stroke-width="2.6"/>')
    p.append(line(fx, my, fx, p1y, ink, 2.6))
    p.append(f'<path d="M {fx} {p1y} A {r} {r} 0 0 1 {b1x} {p1y}" fill="none" stroke="{ink}" stroke-width="2.6"/>')
    p.append(line(b1x, p1y, b1x, btop, ink, 2.6))
    # pulley 1 axle to ceiling
    p.append(line(p1x, cy, p1x, p1y, axis, 3))
    p.append(pulley(c, p1x, p1y, r))
    p.append(pulley(c, mx, my, r))
    # A hangs from movable pulley
    p.append(line(mx, my, mx, 290, axis, 3))
    p.append(block(c, mx, 322, 76, 64, "A 3 kg", "a"))
    # B
    p.append(block(c, bcx, bcy, bw, bh, "B 2 kg", "b"))
    # table
    p.append(line(348, tabley, 440, tabley, axis, 2.4))
    p.append(line(348, tabley, 348, tabley + 18, axis, 2.4))
    p.append(line(p2x, p2y, 348, tabley, axis, 3))
    # rope 2: C -> pulley 2 top -> around left -> down to B
    cx_, cw, ch_ = 392, 66, 44
    cyc = tabley - ch_ / 2
    p.append(line(cx_ - cw / 2, p2y - r, p2x, p2y - r, ink, 2.6))
    p.append(f'<path d="M {p2x} {p2y - r} A {r} {r} 0 0 0 {p2x - r} {p2y}" fill="none" stroke="{ink}" stroke-width="2.6"/>')
    p.append(line(b2x, p2y, b2x, btop, ink, 2.6))
    p.append(pulley(c, p2x, p2y, r))
    p.append(block(c, cx_, tabley - ch_ / 2 + 0, cw, ch_, "C 1 kg", "b"))
    # labels
    p.append(text(lx - 12, 130, "繩端固定", "small", "end", c["muted"]))
    p.append(text(lx - 12, 252, "動滑輪", "small", "end", c["muted"]))
    p.append(text(p1x + 32, 76, "定滑輪", "small", "start", c["muted"]))
    p.append(text(318, 184, "定滑輪", "small", "start", c["muted"]))
    p.append(text(440, 206, "光滑桌面", "small", "end", c["muted"]))
    p.append(text(251, 285, "繩 1", "small", "start", c["muted"]))
    p.append(text(322, 285, "繩 2", "small", "start", c["muted"]))
    # displacement arrows
    p.append(arrow(60, 360, 60, 310, c["accent"]))
    p.append(text(60, 384, "A：*q*", "small", "middle", c["accent"]))
    p.append(text(60, 404, "向上", "small", "middle", c["accent"]))
    p.append(arrow(372, 330, 372, 430, c["accent"]))
    p.append(text(372, 454, "B：2*q*", "small", "middle", c["accent"]))
    p.append(text(372, 474, "向下", "small", "middle", c["accent"]))
    p.append(arrow(430, 96, 330, 96, c["accent"]))
    p.append(text(380, 76, "C：2*q*（朝滑輪）", "small", "middle", c["accent"]))
    p.append(text(W / 2, 508, "繩 1：2*d*_A + *d*_B = 常數", "small", "middle", c["muted"]))
    return shell(c, W, SETUP_H, "三物體連結體示意圖",
                 "繩 1 一端固定在天花板，向下繞過掛有 3 公斤物體 A 的動滑輪，再繞過天花板上的定滑輪，垂下接 2 公斤物體 B 的左側吊鉤。繩 2 接在 B 的右側吊鉤，向上繞過桌邊的定滑輪後水平接到光滑桌面上的 1 公斤物體 C。A 上升 q 時，B 下降 2q，C 朝滑輪前進 2q。",
                 "\n".join("  " + s for s in p))


def fig_fbd(c):
    p = []
    cx = 230
    ink, acc, mut = c["ink"], c["accent"], c["muted"]
    # --- panel A
    p.append(text(cx, 30, "對 A 3 kg（向上為正）", "strong", "middle", ink))
    cy = 170
    p.append(block(c, cx, cy, 96, 70, "A", "a"))
    for dx in (-20, 20):
        p.append(arrow(cx + dx, cy - 35, cx + dx, cy - 35 - 60, acc, 3.2))
    p.append(text(cx - 30, cy - 35 - 60 + 10, "*T*_1", "strong", "end", acc))
    p.append(text(cx + 30, cy - 35 - 60 + 10, "*T*_1", "strong", "start", acc))
    p.append(text(cx, cy - 35 - 60 - 12, "共 2*T*_1", "small", "middle", acc))
    p.append(arrow(cx, cy + 35, cx, cy + 35 + 56, ink))
    p.append(text(cx + 12, cy + 35 + 56, "3*g*", "", "start"))
    p.append(arrow(400, cy + 30, 400, cy - 30, mut, 2))
    p.append(text(400, cy - 42, "正方向", "small", "middle", mut))
    p.append(text(cx, 300, "2*T*_1 − 3*g* = 3*a*", "strong", "middle", acc))
    # --- panel B
    oy = 325
    cy = oy + 140
    p.append(text(cx, oy + 30, "對 B 2 kg（向下為正）", "strong", "middle", ink))
    p.append(block(c, cx, cy, 90, 70, "B", "b"))
    p.append(arrow(cx - 22, cy - 35, cx - 22, cy - 35 - 60, acc, 3.2))
    p.append(arrow(cx + 22, cy - 35, cx + 22, cy - 35 - 36, acc, 3.2))
    p.append(text(cx - 32, cy - 35 - 60 + 10, "*T*_1", "strong", "end", acc))
    p.append(text(cx + 32, cy - 35 - 36 + 10, "*T*_2", "strong", "start", acc))
    p.append(arrow(cx, cy + 35, cx, cy + 35 + 56, ink))
    p.append(text(cx + 12, cy + 35 + 56, "2*g*", "", "start"))
    p.append(arrow(400, cy - 30, 400, cy + 30, mut, 2))
    p.append(text(400, cy - 42, "正方向", "small", "middle", mut))
    p.append(text(cx, oy + 268, "2*g* − *T*_1 − *T*_2 = 2·(2*a*) = 4*a*", "strong", "middle", acc))
    p.append(text(cx, oy + 294, "B 的加速度是 2*a*，不是 *a*", "small", "middle", mut))
    # --- panel C
    oy2 = oy + 320
    cy = oy2 + 120
    p.append(text(cx, oy2 + 30, "對 C 1 kg（朝滑輪，向左為正）", "strong", "middle", ink))
    p.append(block(c, cx, cy, 80, 50, "C", "b"))
    p.append(arrow(cx - 40, cy, cx - 40 - 64, cy, acc, 3.2))
    p.append(text(cx - 40 - 32, cy - 12, "*T*_2", "strong", "middle", acc))
    p.append(arrow(cx, cy - 25, cx, cy - 25 - 34, mut, 2.4))
    p.append(text(cx + 10, cy - 25 - 34 + 10, "*N*", "small", "start", mut))
    p.append(arrow(cx, cy + 25, cx, cy + 25 + 34, mut, 2.4))
    p.append(text(cx + 10, cy + 25 + 34, "*m*_C*g*", "small", "start", mut))
    p.append(arrow(420, cy + 40, 360, cy + 40, mut, 2))
    p.append(text(390, cy + 62, "正方向", "small", "middle", mut))
    p.append(text(cx, oy2 + 225, "*T*_2 = 1·(2*a*) = 2*a*", "strong", "middle", acc))
    p.append(text(cx, oy2 + 251, "*N* 與重力互相抵消，不影響水平運動", "small", "middle", mut))
    p.append(text(cx, oy2 + 277, "箭頭長度僅為示意，不代表大小", "small", "middle", mut))
    return shell(c, W, FBD_H, "三物體 A、B、C 的自由體圖",
                 "A 受動滑輪兩側共 2T1 向上與重力 3g 向下，向上為正；B 受左側繩 T1 與右側繩 T2 向上與重力 2g 向下，向下為正，加速度為 2a；C 在光滑桌面上受繩 T2 朝滑輪，向左為正，加速度為 2a，重力與支持力抵消。",
                 "\n".join("  " + s for s in p))


if __name__ == "__main__":
    write(OUT, "setup", fig_setup, W, SETUP_H)
    write(OUT, "fbd", fig_fbd, W, FBD_H)
