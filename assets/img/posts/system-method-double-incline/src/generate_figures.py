#!/usr/bin/env python3
"""Figures for 「雙斜面連結體：不同方向的力，為什麼還能相減？」 (system-method-double-incline).

Mobile-first: ~460-unit-wide canvases, free-body panels stacked vertically.

    python3 assets/img/posts/system-method-double-incline/src/generate_figures.py
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OUT.parent / "_figlib"))
from figlib import *  # noqa: E402,F401,F403

W = 460
SA, CA = 0.8, 0.6    # sin53, cos53
SB, CB = 0.6, 0.8    # sin37, cos37


def fig_setup(c):
    h = 350
    H = 150
    apex = (190, 95)
    lb = (apex[0] - H * CA / SA, apex[1] + H)
    rb = (apex[0] + H * CB / SB, apex[1] + H)
    p = []
    p.append(f'<polygon points="{lb[0]:.1f},{lb[1]:.1f} {apex[0]},{apex[1]} {rb[0]:.1f},{rb[1]:.1f}" fill="{c["other_wash"]}" stroke="{c["axis"]}" stroke-width="2.4" stroke-linejoin="round"/>')
    r = 34
    p.append(f'<path d="M {lb[0] + r:.1f} {lb[1]:.1f} A {r} {r} 0 0 0 {lb[0] + r * CA:.1f} {lb[1] - r * SA:.1f}" fill="none" stroke="{c["muted"]}" stroke-width="1.6"/>')
    p.append(text(lb[0] + r + 6, lb[1] - 8, "α", "", "start", c["muted"]))
    p.append(f'<path d="M {rb[0] - r:.1f} {rb[1]:.1f} A {r} {r} 0 0 1 {rb[0] - r * CB:.1f} {rb[1] - r * SB:.1f}" fill="none" stroke="{c["muted"]}" stroke-width="1.6"/>')
    p.append(text(rb[0] - r - 6, rb[1] - 8, "β", "", "end", c["muted"]))
    uL = (CA, -SA); nL = (-SA, -CA)
    uR = (CB, SB);  nR = (SB, -CB)
    bh = 40
    off = bh / 2 + 2
    sL, sR = 0.5 * H / SA, 0.45 * H / SB
    c1 = (apex[0] - uL[0] * sL + nL[0] * off, apex[1] - uL[1] * sL + nL[1] * off)
    c2 = (apex[0] + uR[0] * sR + nR[0] * off, apex[1] + uR[1] * sR + nR[1] * off)
    ax_, ay_ = nL[0] * off - nR[0] * off, nL[1] * off - nR[1] * off
    t = -(ax_ * uR[1] - ay_ * uR[0]) / (uL[0] * uR[1] - uL[1] * uR[0])
    P = (apex[0] + nL[0] * off + uL[0] * t, apex[1] + nL[1] * off + uL[1] * t)
    p.append(line(apex[0], apex[1], P[0], P[1], c["axis"], 3))
    p.append(line(c1[0] + uL[0] * 28, c1[1] + uL[1] * 28, P[0], P[1], c["ink"], 2.4))
    p.append(line(c2[0] - uR[0] * 28, c2[1] - uR[1] * 28, P[0], P[1], c["ink"], 2.4))
    p.append(pulley(c, P[0], P[1], 12))
    p.append(block(c, c1[0], c1[1], 56, bh, "", "a", angle=-53))
    p.append(block(c, c2[0], c2[1], 62, bh, "", "b", angle=37))
    p.append(text(c1[0] + nL[0] * 34, c1[1] + nL[1] * 34 + 6, "*m*_1", "strong", "end", c["accent"]))
    p.append(text(c2[0] + nR[0] * 34, c2[1] + nR[1] * 34 + 6, "*m*_2", "strong", "start", c["muted"]))
    # q arrows on the outer side
    q1 = (c1[0] + nL[0] * 62, c1[1] + nL[1] * 62)
    p.append(arrow(q1[0] - uL[0] * 30, q1[1] - uL[1] * 30, q1[0] + uL[0] * 30, q1[1] + uL[1] * 30, c["accent"]))
    p.append(text(q1[0] + nL[0] * 8 - 4, q1[1] + nL[1] * 8, "+*q*", "strong", "end", c["accent"]))
    q2 = (c2[0] + nR[0] * 62, c2[1] + nR[1] * 62)
    p.append(arrow(q2[0] - uR[0] * 30, q2[1] - uR[1] * 30, q2[0] + uR[0] * 30, q2[1] + uR[1] * 30, c["accent"]))
    p.append(text(q2[0] + nR[0] * 8 + 4, q2[1] + nR[1] * 8, "+*q*", "strong", "start", c["accent"]))
    # legend
    y0 = lb[1] + 36
    p.append(text(W / 2, y0, "*m*_1：5 kg，α = 53°；*m*_2：9 kg，β = 37°", "small", "middle", c["muted"]))
    p.append(text(W / 2, y0 + 24, "+*q*：*m*_1 沿斜面向上，*m*_2 沿斜面向下", "small", "middle", c["accent"]))
    return shell(c, W, h, "雙斜面連結體示意圖",
                 "頂端有定滑輪的背靠背斜面：左側傾角 53 度的斜面上有 5 公斤的 m1，右側傾角 37 度的斜面上有 9 公斤的 m2，輕繩平行斜面連接兩者。m2 沿斜面下滑 q，m1 沿斜面上滑 q。",
                 "\n".join("  " + s for s in p))


def panel(c, cx, cy, u_pos, n_out, to_apex_sign, mg, Ns, Ts, kind, angle, sub, k):
    p = []
    bw, bh = 76, 46
    bot = (cx - n_out[0] * bh / 2, cy - n_out[1] * bh / 2)
    p.append(line(bot[0] - u_pos[0] * 125, bot[1] - u_pos[1] * 125, bot[0] + u_pos[0] * 125, bot[1] + u_pos[1] * 125, c["axis"], 2.4))
    p.append(block(c, cx, cy, bw, bh, "", kind, angle=angle))
    p.append(arrow(cx, cy, cx, cy + mg * k, c["ink"]))
    p.append(text(cx + 10, cy + mg * k + 2, f"*m*_{sub} *g*", "", "start"))
    p.append(arrow(cx, cy, cx + n_out[0] * Ns * k, cy + n_out[1] * Ns * k, c["ink"]))
    p.append(text(cx + n_out[0] * (Ns * k + 18) - 10 * (1 if n_out[0] < 0 else 0), cy + n_out[1] * (Ns * k + 18) + 4, "*N*", "", "middle"))
    td = (u_pos[0] * to_apex_sign, u_pos[1] * to_apex_sign)
    p.append(arrow(cx, cy, cx + td[0] * Ts * k, cy + td[1] * Ts * k, c["accent"], 3.2))
    p.append(text(cx + td[0] * (Ts * k + 18), cy + td[1] * (Ts * k + 18) + 6, "*T*", "strong", "middle", c["accent"]))
    w_along = u_pos[1]
    ex = (u_pos[0] * w_along * mg * k, u_pos[1] * w_along * mg * k)
    p.append(line(cx, cy, cx + ex[0], cy + ex[1], c["muted"], 1.8, dash=True))
    p.append(line(cx + ex[0], cy + ex[1], cx, cy + mg * k, c["muted"], 1.4, dash=True))
    return p, ex


def fig_fbd(c):
    h = 740
    p = []
    k = 1.35
    # m1
    cx, cy = 230, 150
    p.append(text(230, 30, "對 *m*_1（沿斜面向上為正）", "strong", "middle", c["ink"]))
    pp, ex = panel(c, cx, cy, (CA, -SA), (-SA, -CA), +1, 50, 30, 45, "a", -53, "1", k)
    p += pp
    p.append(text(cx + ex[0] - 8, cy + ex[1] + 22, "*m*_1 *g* sin α", "small", "end", c["muted"]))
    p.append(text(230, 290, "*T* − *m*_1 *g* sin α = *m*_1 *a*", "strong", "middle", c["accent"]))
    p.append(text(230, 316, "垂直斜面：*N* = *m*_1 *g* cos α，不含 *a*", "small", "middle", c["muted"]))
    # m2
    oy = 360
    cx, cy = 230, oy + 150
    p.append(text(230, oy + 30, "對 *m*_2（沿斜面向下為正）", "strong", "middle", c["ink"]))
    pp, ex = panel(c, cx, cy, (CB, SB), (SB, -CB), -1, 90, 72, 45, "b", 37, "2", k)
    p += pp
    p.append(text(cx + ex[0] + 8, cy + ex[1] + 24, "*m*_2 *g* sin β", "small", "start", c["muted"]))
    p.append(text(230, oy + 300, "*m*_2 *g* sin β − *T* = *m*_2 *a*", "strong", "middle", c["accent"]))
    p.append(text(230, oy + 326, "垂直斜面：*N* = *m*_2 *g* cos β，不含 *a*", "small", "middle", c["muted"]))
    p.append(text(230, oy + 358, "箭頭長度依本題數值按比例繪製；虛線為重力的分解", "small", "middle", c["muted"]))
    return shell(c, W, h, "雙斜面兩物體的自由體圖",
                 "m1 與 m2 各自在斜面上受重力、正向力與沿斜面指向滑輪的張力。重力分解為沿斜面與垂直斜面的分量。沿斜面方向的方程式含有加速度，垂直斜面方向只決定正向力。",
                 "\n".join("  " + s for s in p))


if __name__ == "__main__":
    write(OUT, "setup", fig_setup, W, 350)
    write(OUT, "fbd", fig_fbd, W, 740)
