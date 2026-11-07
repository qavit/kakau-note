#!/usr/bin/env python3
"""Figures for 「雙斜面連結體：不同方向的力，為什麼還能相減？」 (system-method-double-incline).

    python3 assets/img/posts/system-method-double-incline/src/generate_figures.py
"""
import math
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OUT.parent / "_figlib"))
from figlib import *  # noqa: E402,F401,F403

SA, CA = 0.8, 0.6    # sin53, cos53
SB, CB = 0.6, 0.8    # sin37, cos37


def unit_up_left():   # left slope, pointing up toward the apex (screen coords, y down)
    return (CA, -SA)


def fig_setup(c):
    w, h = 1000, 460
    H = 270
    apex = (500, 90)
    lb = (apex[0] - H * CA / SA, apex[1] + H)      # left base
    rb = (apex[0] + H * CB / SB, apex[1] + H)      # right base
    p = []
    p.append(f'<polygon points="{lb[0]:.1f},{lb[1]:.1f} {apex[0]},{apex[1]} {rb[0]:.1f},{rb[1]:.1f}" fill="{c["other_wash"]}" stroke="{c["axis"]}" stroke-width="2.4" stroke-linejoin="round"/>')
    p.append(text(500, lb[1] + 30, "兩個斜面皆光滑", "small", "middle", c["muted"]))
    # angle arcs
    r = 46
    p.append(f'<path d="M {lb[0] + r:.1f} {lb[1]:.1f} A {r} {r} 0 0 0 {lb[0] + r * CA:.1f} {lb[1] - r * SA:.1f}" fill="none" stroke="{c["muted"]}" stroke-width="1.6"/>')
    p.append(text(lb[0] + r + 10, lb[1] - 8, "α = 53°", "small", "start", c["muted"]))
    p.append(f'<path d="M {rb[0] - r:.1f} {rb[1]:.1f} A {r} {r} 0 0 1 {rb[0] - r * CB:.1f} {rb[1] - r * SB:.1f}" fill="none" stroke="{c["muted"]}" stroke-width="1.6"/>')
    p.append(text(rb[0] - r - 10, rb[1] - 8, "β = 37°", "small", "end", c["muted"]))
    # unit vectors along slopes (screen coords)
    uL = (CA, -SA); nL = (-SA, -CA)       # up-slope, outward normal (left)
    uR = (CB, SB);  nR = (SB, -CB)        # down-slope, outward normal (right)
    bh = 56
    offL = bh / 2 + 2
    # block positions: distance s down-slope from apex
    sL, sR = 0.52 * H / SA, 0.45 * H / SB
    def on_slope(u_to_apex, s, n, off):
        return (apex[0] - u_to_apex[0] * s + n[0] * off, apex[1] - u_to_apex[1] * s + n[1] * off)
    # left: u_to_apex = uL (going up toward apex); point = apex - uL*s
    c1 = on_slope(uL, sL, nL, offL)
    c2 = on_slope((-uR[0], -uR[1]), sR, nR, offL)
    # rope: parallel to slope at height offL to the pulley, pulley at intersection of offset lines
    # solve apex + nL*d + uL*t = apex + nR*d + uR*(-t2)  -> intersection
    d = offL
    # P = apex + nL*d + uL*t ; need P on right offset line: (P-apex-nR*d) x uR = 0
    ax_, ay_ = nL[0] * d - nR[0] * d, nL[1] * d - nR[1] * d
    t = -(ax_ * uR[1] - ay_ * uR[0]) / (uL[0] * uR[1] - uL[1] * uR[0])
    P = (apex[0] + nL[0] * d + uL[0] * t, apex[1] + nL[1] * d + uL[1] * t)
    p.append(line(apex[0], apex[1], P[0], P[1], c["axis"], 3))
    p.append(line(c1[0] + uL[0] * 38, c1[1] + uL[1] * 38, P[0], P[1], c["ink"], 2.4))
    p.append(line(c2[0] + uR[0] * -38, c2[1] + uR[1] * -38, P[0], P[1], c["ink"], 2.4))
    p.append(pulley(c, P[0], P[1], 15))
    p.append(block(c, c1[0], c1[1], 76, bh, "m₁", "a", angle=-53, lab_dy=0).replace("m₁", rich("*m*_1")))
    p.append(block(c, c2[0], c2[1], 84, bh, "m₂", "b", angle=37, lab_dy=0).replace("m₂", rich("*m*_2")))
    # mass labels
    p.append(text(c1[0] - nL[0] * 46 + 6, c1[1] - nL[1] * 46 + 6, "5 kg", "small", "start", c["accent"]))
    p.append(text(c2[0] - nR[0] * 46 - 6, c2[1] - nR[1] * 46 + 6, "9 kg", "small", "end", c["muted"]))
    # q arrows beside blocks (below the slope, i.e. inside the wedge)
    inL = nL; inR = nR      # draw q arrows on the outer side, clear of the wedge
    q1 = (c1[0] + inL[0] * 58, c1[1] + inL[1] * 58)
    p.append(arrow(q1[0] - uL[0] * 36, q1[1] - uL[1] * 36, q1[0] + uL[0] * 36, q1[1] + uL[1] * 36, c["accent"]))
    p.append(text(q1[0] + inL[0] * 22 - 4, q1[1] + inL[1] * 22, "+*q*（沿斜面向上）", "small", "end", c["accent"]))
    q2 = (c2[0] + inR[0] * 58, c2[1] + inR[1] * 58)
    p.append(arrow(q2[0] - uR[0] * 36, q2[1] - uR[1] * 36, q2[0] + uR[0] * 36, q2[1] + uR[1] * 36, c["accent"]))
    p.append(text(q2[0] + inR[0] * 22 + 4, q2[1] + inR[1] * 22, "+*q*（沿斜面向下）", "small", "start", c["accent"]))
    p.append(text(40, 44, "兩個物體各在自己的斜面軌道上，共用同一個座標 *q*", "strong", "start", c["ink"]))
    p.append(text(40, 70, "*m*_2 沿斜面下滑 *q*，*m*_1 就沿斜面上滑 *q*：*a*_1 = *a*_2 = *a*", "small", "start", c["muted"]))
    return shell(c, w, h, "雙斜面連結體示意圖",
                 "頂端有定滑輪的背靠背斜面：左側傾角 53 度的斜面上有 5 公斤的 m1，右側傾角 37 度的斜面上有 9 公斤的 m2，輕繩平行斜面連接兩者。m2 沿斜面下滑 q，m1 沿斜面上滑 q。",
                 "\n".join("  " + s for s in p))


def panel(c, cx, cy, u_pos, n_out, to_apex_sign, mg, m_label, kind, angle, Ns, Ts, comp_s, title, sin_t, cos_t, name):
    """One free-body panel drawn on the real slope orientation. Lengths: 1.3 px per N."""
    k = 1.8
    p = []
    bw, bh = 96, 56
    # slope line through block bottom centre
    bot = (cx - n_out[0] * bh / 2, cy - n_out[1] * bh / 2)
    ul = u_pos
    p.append(line(bot[0] - ul[0] * 230, bot[1] - ul[1] * 230, bot[0] + ul[0] * 230, bot[1] + ul[1] * 230, c["axis"], 2.4))
    p.append(block(c, cx, cy, bw, bh, "", kind, angle=angle))
    # weight (vertical)
    p.append(arrow(cx, cy, cx, cy + mg * k, c["ink"]))
    p.append(text(cx + 10, cy + mg * k + 4, f"*m*_{name[-1]} *g*", "", "start"))
    # normal
    p.append(arrow(cx, cy, cx + n_out[0] * Ns * k, cy + n_out[1] * Ns * k, c["ink"]))
    p.append(text(cx + n_out[0] * (Ns * k + 16) - 12, cy + n_out[1] * (Ns * k + 16) + 2, "*N*", "", "middle"))
    # tension toward the apex
    tdir = (u_pos[0] * to_apex_sign, u_pos[1] * to_apex_sign)
    p.append(arrow(cx, cy, cx + tdir[0] * Ts * k, cy + tdir[1] * Ts * k, c["accent"], 3.2))
    p.append(text(cx + tdir[0] * (Ts * k + 16), cy + tdir[1] * (Ts * k + 16) + 4, "*T*", "strong", "middle", c["accent"]))
    # weight components (dashed)
    w_along = (0 * u_pos[0] + 1 * u_pos[1])         # g . u_pos  (g = (0,1))
    ex = (u_pos[0] * w_along * mg * k, u_pos[1] * w_along * mg * k)
    p.append(line(cx, cy, cx + ex[0], cy + ex[1], c["muted"], 1.8, dash=True))
    p.append(line(cx + ex[0], cy + ex[1], cx, cy + mg * k, c["muted"], 1.4, dash=True))
    return p, ex


def fig_fbd(c):
    w, h = 1000, 500
    p = []
    # left panel: m1  (up-slope positive; slope rises to the right)
    uL = (CA, -SA); nL = (-SA, -CA)
    pp, ex = panel(c, 250, 200, uL, nL, +1, 50, "m1", "a", -53, 30, 45, 40, "", SA, CA, "m1")
    p += pp
    p.append(text(250, 52, "對 *m*_1（沿斜面向上為正）", "strong", "middle", c["ink"]))
    p.append(text(250 + ex[0] - 14, 200 + ex[1] + 20, "*m*_1 *g* sin α", "small", "end", c["muted"]))
    p.append(text(250, 440, "*T* − *m*_1 *g* sin α = *m*_1 *a*", "strong", "middle", c["accent"]))
    p.append(text(250, 466, "垂直斜面：*N* = *m*_1 *g* cos α（不含 *a*）", "small", "middle", c["muted"]))
    # right panel: m2 (down-slope positive; slope descends to the right)
    uR = (CB, SB); nR = (SB, -CB)
    pp, ex = panel(c, 750, 200, uR, nR, -1, 90, "m2", "b", 37, 72, 45, 54, "", SB, CB, "m2")
    p += pp
    p.append(text(750, 52, "對 *m*_2（沿斜面向下為正）", "strong", "middle", c["ink"]))
    p.append(text(750 + ex[0] + 12, 200 + ex[1] + 24, "*m*_2 *g* sin β", "small", "start", c["muted"]))
    p.append(text(750, 440, "*m*_2 *g* sin β − *T* = *m*_2 *a*", "strong", "middle", c["accent"]))
    p.append(text(750, 466, "垂直斜面：*N* = *m*_2 *g* cos β（不含 *a*）", "small", "middle", c["muted"]))
    p.append(text(500, 486, "箭頭長度依本題數值按比例繪製；虛線為重力沿斜面與垂直斜面的分解", "small", "middle", c["muted"]))
    return shell(c, w, h, "雙斜面兩物體的自由體圖",
                 "m1 與 m2 各自在斜面上受重力、正向力與沿斜面指向滑輪的張力。重力分解為沿斜面與垂直斜面的分量。沿斜面方向的方程式含有加速度，垂直斜面方向只決定正向力。",
                 "\n".join("  " + s for s in p))


if __name__ == "__main__":
    write(OUT, "setup", fig_setup, 1000, 460)
    write(OUT, "fbd", fig_fbd, 1000, 500)
