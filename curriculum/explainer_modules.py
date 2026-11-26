"""Storyboards for every module except m02 (hand-built in explainer_scenes.py).

Each module is a SPEC: one entry per script scene, saying which drawing goes with which spoken line.
Reusable station layouts (title, quote-with-story-beats, bullet cards, closing note) place them on a
grid; the camera visits each station in reading order, and the finished board doubles as the module's
printable map (see build_explainer.py --board).
"""
import math

from explainer_scenes import (COPPER, CREAM, INK, MAROON, SAGE, SKY, SW, TEAL, C, P, T, arrow, beaker, blocks, brain, bubble,
                              calendar, check, checklist, coin, compass, cross, gear, grid, hourglass, kettle, magnifier,
                              molecule, monitor, network, notebook, plug, rrect, rulecard, scale, scroll, toolbox, venn3, wrench)


# ───────────────────────── more drawings (each fits a ~200px box centred on cx, cy at s=1) ─────────────────────────
def _pts(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def target(cx, cy, s=1, miss=False):
    out = C(cx, cy, 95 * s, fill="#fff") + C(cx, cy, 64 * s, MAROON, fill=MAROON, op=.25) + C(cx, cy, 32 * s, fill=MAROON, op=.9)
    tx, ty = (cx + 120 * s, cy - 105 * s) if miss else (cx, cy)
    out += P(f"M{tx+110*s} {ty-100*s} L{tx+6*s} {ty-6*s}", w=SW + 2) + P(f"M{tx+110*s} {ty-100*s} l{-8*s} {-30*s} M{tx+110*s} {ty-100*s} l{30*s} {8*s}", COPPER, w=SW + 2)
    return out


def cycle(cx, cy, s=1):
    r, out = 80 * s, ""
    for i, c in enumerate([MAROON, TEAL, COPPER]):
        a0, a1 = math.radians(i * 120 + 15), math.radians(i * 120 + 105)
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        out += P(f"M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}", c, w=SW + 4)
        ha = a1 + math.pi / 2
        out += P(f"M{x1 + 24*s*math.cos(ha - 2.5):.1f} {y1 + 24*s*math.sin(ha - 2.5):.1f} L{x1:.1f} {y1:.1f} L{x1 + 24*s*math.cos(ha + 2.5):.1f} {y1 + 24*s*math.sin(ha + 2.5):.1f}", c, w=SW + 4)
    return out


def globe(cx, cy, s=1):
    r = 90 * s
    return (C(cx, cy, r, fill=SKY) + P(f"M{cx-r} {cy} H{cx+r} M{cx} {cy-r} Q{cx-70*s} {cy} {cx} {cy+r} Q{cx+70*s} {cy} {cx} {cy-r}", w=4)
            + P(f"M{cx-80*s} {cy-40*s} Q{cx} {cy-25*s} {cx+80*s} {cy-40*s} M{cx-80*s} {cy+40*s} Q{cx} {cy+25*s} {cx+80*s} {cy+40*s}", w=3)
            + P(f"M{cx-60*s} {cy-30*s} q{20*s} {-25*s} {45*s} {-10*s} q{10*s} {30*s} {-20*s} {40*s}Z", SAGE, fill=SAGE, op=.8, w=3))


def flowchart(cx, cy, s=1):
    out = P(rrect(cx - 60 * s, cy - 100 * s, 120 * s, 50 * s, 8), fill=SKY)
    out += P(_pts([(cx, cy - 30 * s), (cx + 55 * s, cy + 5 * s), (cx, cy + 40 * s), (cx - 55 * s, cy + 5 * s)]) + "Z", fill=COPPER, op=.8)
    out += P(rrect(cx - 130 * s, cy + 60 * s, 100 * s, 45 * s, 8), fill="#fff") + P(rrect(cx + 30 * s, cy + 60 * s, 100 * s, 45 * s, 8), fill="#fff")
    return out + P(f"M{cx} {cy-50*s} V{cy-30*s} M{cx-55*s} {cy+5*s} H{cx-80*s} V{cy+60*s} M{cx+55*s} {cy+5*s} H{cx+80*s} V{cy+60*s}", w=4)


def piano(cx, cy, s=1):
    out = P(rrect(cx - 110 * s, cy - 40 * s, 220 * s, 110 * s, 6), fill="#fff")
    for i in range(1, 8):
        out += P(f"M{cx-110*s+i*27.5*s} {cy-40*s} V{cy+70*s}", w=3)
    for i in [1, 2, 4, 5, 6]:
        out += P(rrect(cx - 110 * s + i * 27.5 * s - 8 * s, cy - 40 * s, 16 * s, 62 * s, 2), fill=INK)
    out += P(rrect(cx - 90 * s, cy - 120 * s, 180 * s, 70 * s, 4), fill=CREAM)   # the punched paper roll
    for i, (dx, dy) in enumerate([(-60, -100), (-30, -80), (0, -100), (30, -70), (60, -90), (-45, -65), (15, -85)]):
        out += P(rrect(cx + dx * s, cy + dy * s, 16 * s, 8 * s, 2), fill=MAROON, w=2)
    return out


def retry(cx, cy, s=1):
    r = 80 * s
    x1, y1 = cx + r * math.cos(math.radians(-60)), cy + r * math.sin(math.radians(-60))
    return (P(f"M{cx + r*math.cos(math.radians(-40)):.1f} {cy + r*math.sin(math.radians(-40)):.1f} A{r} {r} 0 1 1 {x1:.1f} {y1:.1f}", MAROON, w=SW + 4)
            + P(f"M{x1 - 30*s:.1f} {y1 - 8*s:.1f} L{x1:.1f} {y1:.1f} L{x1 + 4*s:.1f} {y1 + 30*s:.1f}", MAROON, w=SW + 4)
            + T(cx, cy + 20 * s, "×3", int(56 * s), INK))


def curtain(cx, cy, s=1):
    out = P(f"M{cx-120*s} {cy-100*s} H{cx+120*s}", w=SW + 4)
    out += P(f"M{cx-120*s} {cy-100*s} Q{cx-60*s} {cy-20*s} {cx-110*s} {cy+100*s} H{cx-60*s} Q{cx-50*s} {cy} {cx-10*s} {cy-100*s}Z", fill=MAROON, op=.85)
    out += P(f"M{cx+120*s} {cy-100*s} Q{cx+60*s} {cy-20*s} {cx+110*s} {cy+100*s} H{cx+60*s} Q{cx+50*s} {cy} {cx+10*s} {cy-100*s}Z", fill=MAROON, op=.85)
    return out + P(f"M{cx-140*s} {cy+100*s} H{cx+140*s}", w=SW + 3) + T(cx, cy + 50 * s, "★", int(60 * s), COPPER)


def crack(cx, cy, s=1):
    return (P(rrect(cx - 110 * s, cy - 80 * s, 220 * s, 150 * s, 12), fill=SKY)
            + P(_pts([(cx - 20 * s, cy - 80 * s), (cx, cy - 30 * s), (cx - 30 * s, cy + 5 * s), (cx + 10 * s, cy + 40 * s), (cx - 5 * s, cy + 70 * s)]), MAROON, w=SW + 1)
            + P(f"M{cx} {cy+70*s} V{cy+105*s} M{cx-50*s} {cy+108*s} H{cx+50*s}", w=SW + 2))


def question(cx, cy, s=1, color=MAROON):
    return (P(f"M{cx-45*s} {cy-50*s} Q{cx-45*s} {cy-105*s} {cx} {cy-105*s} Q{cx+50*s} {cy-105*s} {cx+50*s} {cy-55*s} Q{cx+50*s} {cy-20*s} {cx} {cy} V{cy+35*s}", color, w=SW + 8)
            + C(cx, cy + 85 * s, 13 * s, color, fill=color))


def database(cx, cy, s=1):
    out = ""
    for i, c in enumerate([TEAL, SKY, TEAL]):
        y = cy - 70 * s + i * 50 * s
        out += P(f"M{cx-90*s} {y} V{y+50*s} A{90*s} {25*s} 0 0 0 {cx+90*s} {y+50*s} V{y}", fill=c, op=.8)
    return out + P(f"M{cx-90*s} {cy-70*s} A{90*s} {25*s} 0 1 0 {cx+90*s} {cy-70*s} A{90*s} {25*s} 0 1 0 {cx-90*s} {cy-70*s}", fill="#fff")


def stop(cx, cy, s=1):
    pts = [(cx + 95 * s * math.cos(math.pi / 8 + i * math.pi / 4), cy + 95 * s * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    return P(_pts(pts) + "Z", fill=MAROON, op=.9) + T(cx, cy + 18 * s, "STOP", int(50 * s), "#fff")


def calculator(cx, cy, s=1):
    out = P(rrect(cx - 75 * s, cy - 100 * s, 150 * s, 200 * s, 14), fill=SKY) + P(rrect(cx - 55 * s, cy - 80 * s, 110 * s, 45 * s, 6), fill="#fff")
    for r in range(3):
        for c in range(3):
            out += P(rrect(cx - 55 * s + c * 40 * s, cy - 20 * s + r * 38 * s, 30 * s, 28 * s, 5), fill=COPPER if c == 2 else "#fff", w=3)
    return out + T(cx + 40 * s, cy - 45 * s, "42", int(30 * s), INK, "end")


def shield(cx, cy, s=1):
    return (P(f"M{cx} {cy-105*s} L{cx+85*s} {cy-75*s} Q{cx+85*s} {cy+50*s} {cx} {cy+105*s} Q{cx-85*s} {cy+50*s} {cx-85*s} {cy-75*s}Z", fill=TEAL, op=.8)
            + P(f"M{cx-35*s} {cy} L{cx-8*s} {cy+28*s} L{cx+40*s} {cy-30*s}", "#fff", w=SW + 5))


def doc(cx, cy, s=1, lines=5, color="#fff"):
    out = P(f"M{cx-75*s} {cy-100*s} H{cx+40*s} L{cx+75*s} {cy-65*s} V{cy+100*s} H{cx-75*s}Z", fill=color) + P(f"M{cx+40*s} {cy-100*s} V{cy-65*s} H{cx+75*s}", w=4)
    for i in range(lines):
        out += P(f"M{cx-50*s} {cy-45*s+i*32*s} H{cx+(50 - (30 if i == lines - 1 else 0))*s}", w=4)
    return out


def docs(cx, cy, s=1):
    return doc(cx - 40 * s, cy - 20 * s, .8 * s) + doc(cx, cy, .8 * s) + doc(cx + 40 * s, cy + 20 * s, .8 * s, color=CREAM)


def contract(cx, cy, s=1):
    return doc(cx, cy, s, 3) + P(f"M{cx-50*s} {cy+60*s} q{15*s} {-25*s} {30*s} 0 t{30*s} 0 t{30*s} -5", MAROON, w=4) + T(cx + 40 * s, cy - 70 * s, "v2", int(30 * s), TEAL)


def pin(cx, cy, s=1):
    return (P(f"M{cx-45*s} {cy-30*s} H{cx+45*s} L{cx+25*s} {cy-75*s} V{cy-100*s} H{cx-25*s} V{cy-75*s}Z", fill=MAROON, op=.85)
            + P(f"M{cx} {cy-30*s} V{cy+100*s}", w=SW + 1) + T(cx + 70 * s, cy + 40 * s, "v1.2", int(34 * s), TEAL, "start"))


def dice(cx, cy, s=1):
    out = P(rrect(cx - 95 * s, cy - 50 * s, 100 * s, 100 * s, 16), fill="#fff") + P(rrect(cx + 5 * s, cy - 80 * s, 100 * s, 100 * s, 16), fill=COPPER, op=.85)
    for dx, dy in [(-70, -25), (-45, 0), (-20, 25)]:
        out += C(cx + dx * s, cy + dy * s, 8 * s, fill=INK)
    for dx, dy in [(30, -55), (80, -55), (30, -5), (80, -5)]:
        out += C(cx + dx * s, cy + dy * s, 8 * s, fill=INK)
    return out


def trace(cx, cy, s=1):
    out = P(f"M{cx-110*s} {cy-90*s} V{cy+90*s}", w=3)
    for i, (x0, w, c) in enumerate([(0, 200, TEAL), (15, 80, COPPER), (100, 90, SAGE), (105, 40, MAROON), (150, 30, COPPER)]):
        out += P(rrect(cx - 100 * s + x0 * s, cy - 80 * s + i * 34 * s, w * s, 24 * s, 5), fill=c, op=.85, w=3)
    return out


def coffee(cx, cy, s=1):
    return (P(f"M{cx-70*s} {cy-40*s} H{cx+60*s} L{cx+50*s} {cy+80*s} Q{cx+48*s} {cy+95*s} {cx+30*s} {cy+95*s} H{cx-50*s} Q{cx-68*s} {cy+95*s} {cx-70*s} {cy+80*s}Z", fill=COPPER, op=.85)
            + P(f"M{cx+58*s} {cy-10*s} Q{cx+110*s} {cy-5*s} {cx+95*s} {cy+30*s} Q{cx+85*s} {cy+50*s} {cx+52*s} {cy+50*s}", w=SW + 1)
            + P(f"M{cx-30*s} {cy-60*s} q{-15*s} {-25*s} 0 {-45*s} M{cx+10*s} {cy-60*s} q{-15*s} {-25*s} 0 {-45*s}", w=4))


def knife(cx, cy, s=1):
    out = P(rrect(cx - 110 * s, cy - 25 * s, 220 * s, 60 * s, 28), fill=MAROON, op=.9) + T(cx, cy + 14 * s, "+", int(42 * s), "#fff")
    out += P(f"M{cx-80*s} {cy-25*s} L{cx-140*s} {cy-110*s} L{cx-100*s} {cy-30*s}", fill=SKY)        # blade
    out += P(f"M{cx+60*s} {cy-25*s} L{cx+90*s} {cy-120*s} L{cx+75*s} {cy-25*s}", fill=SKY)          # screwdriver
    return out + P(f"M{cx-10*s} {cy-25*s} L{cx+10*s} {cy-100*s} M{cx+10*s} {cy-100*s} l{-12*s} 8", w=4) + P(f"M{cx+80*s} {cy+35*s} L{cx+130*s} {cy+90*s}", w=SW + 1)


def function(cx, cy, s=1):
    return (P(rrect(cx - 70 * s, cy - 60 * s, 140 * s, 120 * s, 14), fill=SKY) + T(cx, cy + 18 * s, "f( )", int(54 * s), INK)
            + arrow(cx - 150 * s, cy, cx - 78 * s, cy, TEAL, 5) + arrow(cx + 78 * s, cy, cx + 150 * s, cy, MAROON, 5)
            + T(cx - 150 * s, cy - 25 * s, "X", int(36 * s), TEAL) + T(cx + 150 * s, cy - 25 * s, "Y", int(36 * s), MAROON))


def idcard(cx, cy, s=1):
    return (P(rrect(cx - 110 * s, cy - 70 * s, 220 * s, 140 * s, 14), fill="#fff") + P(rrect(cx - 110 * s, cy - 70 * s, 220 * s, 35 * s, 10), fill=TEAL, op=.85)
            + C(cx - 55 * s, cy + 10 * s, 26 * s, fill=SKY) + P(f"M{cx-90*s} {cy+60*s} Q{cx-55*s} {cy+20*s} {cx-20*s} {cy+60*s}", w=4)
            + P(f"M{cx+5*s} {cy} H{cx+85*s} M{cx+5*s} {cy+30*s} H{cx+65*s}", w=4))


def pipeline(cx, cy, s=1):
    out = ""
    for i, c in enumerate([TEAL, COPPER, MAROON]):
        x = cx - 120 * s + i * 120 * s
        out += P(rrect(x - 40 * s, cy - 40 * s, 80 * s, 80 * s, 12), fill=c, op=.85)
        if i:
            out += arrow(x - 78 * s, cy, x - 46 * s, cy, INK, 4)
    return out


def map_(cx, cy, s=1):
    pts = [(cx - 110 * s, cy - 80 * s), (cx - 40 * s, cy - 100 * s), (cx + 40 * s, cy - 80 * s), (cx + 110 * s, cy - 100 * s),
           (cx + 110 * s, cy + 80 * s), (cx + 40 * s, cy + 100 * s), (cx - 40 * s, cy + 80 * s), (cx - 110 * s, cy + 100 * s)]
    return (P(_pts(pts) + "Z", fill=CREAM) + P(f"M{cx-40*s} {cy-100*s} V{cy+80*s} M{cx+40*s} {cy-80*s} V{cy+100*s}", w=3)
            + f'<path d="M{cx-85*s} {cy+60*s} Q{cx-40*s} {cy-30*s} {cx} {cy+10*s} T{cx+75*s} {cy-55*s}" stroke="{MAROON}" stroke-width="5" fill="none" stroke-dasharray="10 10"/>'
            + P(f"M{cx+60*s} {cy-70*s} l{30*s} {30*s} M{cx+90*s} {cy-70*s} l{-30*s} {30*s}", MAROON, w=SW + 1))


def shapes(cx, cy, s=1):
    return (C(cx - 60 * s, cy - 40 * s, 40 * s, fill=TEAL, op=.8) + P(rrect(cx + 10 * s, cy - 90 * s, 80 * s, 80 * s, 6), fill=COPPER, op=.8)
            + P(_pts([(cx - 40 * s, cy + 20 * s), (cx + 10 * s, cy + 100 * s), (cx - 90 * s, cy + 100 * s)]) + "Z", fill=MAROON, op=.8)
            + P(f"M{cx+40*s} {cy+30*s} l{25*s} {45*s} l{25*s} {-45*s} l{-25*s} {-20*s}Z", fill=SAGE, op=.8))


def fanout(cx, cy, s=1):
    out = C(cx - 90 * s, cy, 34 * s, fill=MAROON, op=.85)
    for i, c in enumerate([TEAL, COPPER, SAGE]):
        y = cy - 85 * s + i * 85 * s
        out += arrow(cx - 52 * s, cy, cx + 50 * s, y, INK, 4, 0) + C(cx + 85 * s, y, 28 * s, fill=c, op=.85)
    return out


def megaphone(cx, cy, s=1):
    return (P(f"M{cx-80*s} {cy-25*s} L{cx+50*s} {cy-85*s} V{cy+85*s} L{cx-80*s} {cy+25*s}Z", fill=COPPER, op=.85)
            + P(rrect(cx - 105 * s, cy - 28 * s, 30 * s, 56 * s, 6), fill=INK) + P(f"M{cx-60*s} {cy+25*s} L{cx-45*s} {cy+85*s}", w=SW + 2)
            + P(f"M{cx+75*s} {cy-40*s} q{20*s} {40*s} 0 {80*s} M{cx+100*s} {cy-65*s} q{35*s} {65*s} 0 {130*s}", w=4))


def book(cx, cy, s=1):
    return (P(f"M{cx} {cy-60*s} Q{cx-60*s} {cy-95*s} {cx-115*s} {cy-70*s} V{cy+80*s} Q{cx-60*s} {cy+55*s} {cx} {cy+90*s}Z", fill="#fff")
            + P(f"M{cx} {cy-60*s} Q{cx+60*s} {cy-95*s} {cx+115*s} {cy-70*s} V{cy+80*s} Q{cx+60*s} {cy+55*s} {cx} {cy+90*s}Z", fill="#fff")
            + P(f"M{cx-90*s} {cy-30*s} Q{cx-50*s} {cy-45*s} {cx-20*s} {cy-25*s} M{cx-90*s} {cy+10*s} Q{cx-50*s} {cy-5*s} {cx-20*s} {cy+15*s} M{cx+20*s} {cy-25*s} Q{cx+50*s} {cy-45*s} {cx+90*s} {cy-30*s}", w=3)
            + P(f"M{cx} {cy-60*s} V{cy+90*s}", MAROON, w=SW))


def blackbox(cx, cy, s=1):
    return (P(rrect(cx - 70 * s, cy - 70 * s, 140 * s, 140 * s, 10), fill=INK, op=.9) + T(cx, cy + 18 * s, "?", int(60 * s), "#fff")
            + arrow(cx - 160 * s, cy - 30 * s, cx - 78 * s, cy - 30 * s, TEAL, 5) + arrow(cx + 78 * s, cy + 30 * s, cx + 160 * s, cy + 30 * s, MAROON, 5))


def chart(cx, cy, s=1, down=False):
    out = P(f"M{cx-100*s} {cy-90*s} V{cy+80*s} H{cx+110*s}", w=SW + 1)
    pts = [(-80, 50), (-40, 20), (0, 30), (40, -20), (80, -60)] if not down else [(-80, -60), (-40, -50), (0, -10), (40, 30), (80, 60)]
    return out + P(_pts([(cx + x * s, cy + y * s) for x, y in pts]), MAROON if down else SAGE, w=SW + 2) + "".join(C(cx + x * s, cy + y * s, 8 * s, fill=INK) for x, y in pts)


def nosign(cx, cy, s=1):
    return wrench(cx, cy, .9 * s, ang=-40) + C(cx, cy, 95 * s, MAROON, w=SW + 4) + P(f"M{cx-67*s} {cy+67*s} L{cx+67*s} {cy-67*s}", MAROON, w=SW + 4)


def key(cx, cy, s=1):
    return (C(cx - 60 * s, cy, 45 * s, fill=COPPER, op=.9) + C(cx - 60 * s, cy, 15 * s, fill="#fff")
            + P(f"M{cx-15*s} {cy} H{cx+110*s} M{cx+70*s} {cy} V{cy+35*s} M{cx+100*s} {cy} V{cy+28*s}", w=SW + 4))


def film(cx, cy, s=1):
    out = P(rrect(cx - 120 * s, cy - 65 * s, 240 * s, 130 * s, 6), fill=INK, op=.85)
    for i in range(3):
        out += P(rrect(cx - 105 * s + i * 72 * s, cy - 40 * s, 66 * s, 80 * s, 4), fill=[SKY, CREAM, SKY][i], w=2)
    for i in range(8):
        out += P(rrect(cx - 112 * s + i * 30 * s, cy - 60 * s, 12 * s, 10 * s, 2), fill="#fff", w=1) + P(rrect(cx - 112 * s + i * 30 * s, cy + 50 * s, 12 * s, 10 * s, 2), fill="#fff", w=1)
    return out


def kv(cx, cy, s=1):
    out = ""
    for i in range(3):
        y = cy - 75 * s + i * 52 * s
        out += P(rrect(cx - 110 * s, y, 95 * s, 44 * s, 6), fill=COPPER, op=.75, w=3) + P(rrect(cx - 5 * s, y, 115 * s, 44 * s, 6), fill="#fff", w=3)
    return out + T(cx - 62 * s, cy - 42 * s, "key", int(26 * s)) + T(cx + 52 * s, cy - 42 * s, "value", int(26 * s))


def clock(cx, cy, s=1):
    return C(cx, cy, 90 * s, fill="#fff") + P(f"M{cx} {cy-60*s} V{cy} L{cx+45*s} {cy+25*s}", MAROON, w=SW + 2) + "".join(
        P(f"M{cx + 75*s*math.cos(a):.1f} {cy + 75*s*math.sin(a):.1f} L{cx + 88*s*math.cos(a):.1f} {cy + 88*s*math.sin(a):.1f}", w=4) for a in [i * math.pi / 6 for i in range(12)])


def trash(cx, cy, s=1):
    return (P(f"M{cx-65*s} {cy-55*s} L{cx-50*s} {cy+100*s} H{cx+50*s} L{cx+65*s} {cy-55*s}", fill=SKY) + P(f"M{cx-85*s} {cy-60*s} H{cx+85*s} M{cx-25*s} {cy-60*s} V{cy-85*s} H{cx+25*s} V{cy-60*s}", w=SW + 1)
            + P(f"M{cx-25*s} {cy-25*s} V{cy+70*s} M{cx} {cy-25*s} V{cy+70*s} M{cx+25*s} {cy-25*s} V{cy+70*s}", w=4))


def music(cx, cy, s=1):
    return (P(f"M{cx-40*s} {cy+60*s} V{cy-80*s} L{cx+70*s} {cy-100*s} V{cy+40*s}", w=SW + 3)
            + f'<ellipse cx="{cx-62*s}" cy="{cy+62*s}" rx="{28*s}" ry="{21*s}" stroke="{INK}" stroke-width="{SW}" fill="{MAROON}"/>'
            + f'<ellipse cx="{cx+48*s}" cy="{cy+42*s}" rx="{28*s}" ry="{21*s}" stroke="{INK}" stroke-width="{SW}" fill="{MAROON}"/>'
            + P(f"M{cx-40*s} {cy-50*s} L{cx+70*s} {cy-70*s}", w=SW + 3))


def chain(cx, cy, s=1):
    out = ""
    for i in range(5):
        x = cx - 110 * s + i * 52 * s
        out += f'<ellipse cx="{x:.1f}" cy="{cy + (i % 2) * 6 * s:.1f}" rx="{34*s}" ry="{20*s}" stroke="{[INK, COPPER][i % 2]}" stroke-width="{SW+1}" fill="none"/>'
    return out + T(cx, cy + 90 * s, "…step 20", int(34 * s), MAROON)


def mirror(cx, cy, s=1):
    return (f'<ellipse cx="{cx}" cy="{cy-15*s}" rx="{70*s}" ry="{90*s}" stroke="{INK}" stroke-width="{SW+2}" fill="{SKY}"/>'
            + P(f"M{cx-30*s} {cy-60*s} l{40*s} {-25*s} M{cx-35*s} {cy-30*s} l{55*s} {-35*s}", "#fff", w=5) + P(f"M{cx} {cy+75*s} V{cy+105*s} M{cx-45*s} {cy+105*s} H{cx+45*s}", w=SW + 2))


def tree(cx, cy, s=1):
    out, nodes = "", [(cx, cy - 85 * s), (cx - 80 * s, cy), (cx + 80 * s, cy), (cx - 115 * s, cy + 85 * s), (cx - 45 * s, cy + 85 * s), (cx + 45 * s, cy + 85 * s), (cx + 115 * s, cy + 85 * s)]
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]:
        out += P(f"M{nodes[a][0]:.0f} {nodes[a][1]:.0f} L{nodes[b][0]:.0f} {nodes[b][1]:.0f}", w=4)
    cols = [MAROON, TEAL, TEAL, SKY, SAGE, SKY, SKY]
    return out + "".join(C(f"{x:.0f}", f"{y:.0f}", 22 * s, fill=c) for (x, y), c in zip(nodes, cols))


def envelope(cx, cy, s=1):
    return P(rrect(cx - 110 * s, cy - 70 * s, 220 * s, 140 * s, 10), fill="#fff") + P(f"M{cx-108*s} {cy-66*s} L{cx} {cy+10*s} L{cx+108*s} {cy-66*s}", w=SW) + T(cx, cy + 55 * s, "{ }", int(36 * s), TEAL)


def hierarchy(cx, cy, s=1):
    out = P(rrect(cx - 50 * s, cy - 105 * s, 100 * s, 60 * s, 10), fill=MAROON, op=.85)
    for i, c in enumerate([TEAL, COPPER, SAGE]):
        x = cx - 100 * s + i * 100 * s
        out += P(f"M{cx} {cy-45*s} L{x} {cy+40*s}", w=4) + P(rrect(x - 40 * s, cy + 40 * s, 80 * s, 55 * s, 10), fill=c, op=.85)
    return out


def swap(cx, cy, s=1):
    return (C(cx - 90 * s, cy, 38 * s, fill=TEAL, op=.85) + C(cx + 90 * s, cy, 38 * s, fill=COPPER, op=.85)
            + arrow(cx - 45 * s, cy - 25 * s, cx + 45 * s, cy - 25 * s, INK, 5, -14) + arrow(cx + 45 * s, cy + 25 * s, cx - 45 * s, cy + 25 * s, INK, 5, -14)
            + T(cx, cy - 60 * s, "hello · v?", int(28 * s), INK))


def server(cx, cy, s=1):
    out = ""
    for i in range(3):
        y = cy - 95 * s + i * 65 * s
        out += P(rrect(cx - 100 * s, y, 200 * s, 55 * s, 8), fill=SKY) + C(cx + 70 * s, y + 27 * s, 9 * s, fill=SAGE) + P(f"M{cx-75*s} {y+27*s} H{cx+20*s}", w=4)
    return out


def tangle(cx, cy, s=1):
    return (P(f"M{cx-110*s} {cy-40*s} C{cx-20*s} {cy-120*s} {cx+30*s} {cy+90*s} {cx+110*s} {cy-20*s}", TEAL, w=SW + 1)
            + P(f"M{cx-110*s} {cy+30*s} C{cx-40*s} {cy+110*s} {cx+60*s} {cy-120*s} {cx+110*s} {cy+50*s}", COPPER, w=SW + 1)
            + P(f"M{cx-100*s} {cy-80*s} C{cx+80*s} {cy-60*s} {cx-90*s} {cy+90*s} {cx+90*s} {cy+90*s}", MAROON, w=SW + 1))


def log(cx, cy, s=1):
    out = P(rrect(cx - 100 * s, cy - 95 * s, 200 * s, 190 * s, 10), fill="#fff")
    for i in range(5):
        y = cy - 65 * s + i * 34 * s
        out += C(cx - 75 * s, y, 7 * s, fill=[SAGE, SAGE, COPPER, SAGE, MAROON][i]) + P(f"M{cx-55*s} {y} H{cx+(75 - (i % 3) * 25)*s}", w=4)
    return out


def lock(cx, cy, s=1):
    return (P(f"M{cx-50*s} {cy-20*s} V{cy-60*s} A{50*s} {50*s} 0 0 1 {cx+50*s} {cy-60*s} V{cy-20*s}", w=SW + 5)
            + P(rrect(cx - 80 * s, cy - 25 * s, 160 * s, 125 * s, 14), fill=COPPER, op=.9) + C(cx, cy + 25 * s, 14 * s, fill=INK) + P(f"M{cx} {cy+30*s} V{cy+65*s}", w=SW + 2))


def funnel(cx, cy, s=1):
    out = P(f"M{cx-110*s} {cy-70*s} H{cx+110*s} L{cx+25*s} {cy+20*s} V{cy+90*s} L{cx-25*s} {cy+70*s} V{cy+20*s}Z", fill=SKY)
    return out + "".join(C(cx + dx * s, cy - 100 * s, 10 * s, fill=c) for dx, c in [(-70, MAROON), (-25, TEAL), (20, COPPER), (65, SAGE)]) + C(cx, cy + 115 * s, 10 * s, fill=TEAL)


def states(cx, cy, s=1):
    out, pts = "", [(cx - 100 * s, cy + 40 * s), (cx, cy - 60 * s), (cx + 100 * s, cy + 40 * s)]
    out += arrow(pts[0][0] + 20 * s, pts[0][1] - 35 * s, pts[1][0] - 38 * s, pts[1][1] + 10 * s, INK, 4, -15)
    out += arrow(pts[1][0] + 38 * s, pts[1][1] + 10 * s, pts[2][0] - 20 * s, pts[2][1] - 35 * s, INK, 4, -15)
    return out + "".join(C(f"{x:.0f}", f"{y:.0f}", 38 * s, fill=c, op=.85) for (x, y), c in zip(pts, [TEAL, COPPER, SAGE])) + T(cx, cy + 115 * s, "1 → 2 → 3", int(30 * s))


def bell(cx, cy, s=1):
    return (P(f"M{cx-80*s} {cy+50*s} Q{cx-55*s} {cy+30*s} {cx-55*s} {cy-20*s} Q{cx-55*s} {cy-90*s} {cx} {cy-90*s} Q{cx+55*s} {cy-90*s} {cx+55*s} {cy-20*s} Q{cx+55*s} {cy+30*s} {cx+80*s} {cy+50*s}Z", fill=COPPER, op=.9)
            + C(cx, cy + 70 * s, 18 * s, fill=INK) + P(f"M{cx} {cy-90*s} V{cy-110*s}", w=SW + 1)
            + P(f"M{cx-105*s} {cy-60*s} q{-15*s} {30*s} 0 {60*s} M{cx+105*s} {cy-60*s} q{15*s} {30*s} 0 {60*s}", w=4))


def person(cx, cy, s=1, fill=SKY):
    return C(cx, cy - 55 * s, 40 * s, fill="#fff") + P(f"M{cx-80*s} {cy+100*s} Q{cx-80*s} {cy} {cx} {cy} Q{cx+80*s} {cy} {cx+80*s} {cy+100*s}Z", fill=fill)


def mismatch(cx, cy, s=1):
    return (P(f"M{cx-120*s} {cy-50*s} H{cx-20*s} V{cy-20*s} h{-20*s} v{40*s} h{20*s} V{cy+50*s} H{cx-120*s}Z", fill=TEAL, op=.85)
            + P(f"M{cx+120*s} {cy-50*s} H{cx+20*s} V{cy-5*s} l{-25*s} {15*s} l{25*s} {15*s} V{cy+50*s} H{cx+120*s}Z", fill=COPPER, op=.85)
            + T(cx, cy - 80 * s, "≠", int(60 * s), MAROON))


def trophy(cx, cy, s=1):
    return (P(f"M{cx-60*s} {cy-90*s} H{cx+60*s} V{cy-30*s} Q{cx+60*s} {cy+30*s} {cx} {cy+35*s} Q{cx-60*s} {cy+30*s} {cx-60*s} {cy-30*s}Z", fill=COPPER, op=.9)
            + P(f"M{cx-60*s} {cy-70*s} q{-50*s} 0 {-40*s} {40*s} q{10*s} {25*s} {45*s} {20*s} M{cx+60*s} {cy-70*s} q{50*s} 0 {40*s} {40*s} q{-10*s} {25*s} {-45*s} {20*s}", w=SW)
            + P(f"M{cx} {cy+35*s} V{cy+75*s} M{cx-45*s} {cy+90*s} H{cx+45*s}", w=SW + 4) + T(cx, cy - 25 * s, "1", int(48 * s), INK))


def fence(cx, cy, s=1):
    out = P(f"M{cx-120*s} {cy-20*s} H{cx+120*s} M{cx-120*s} {cy+40*s} H{cx+120*s}", w=SW + 1)
    for i in range(5):
        x = cx - 100 * s + i * 50 * s
        out += P(f"M{x-15*s} {cy+85*s} V{cy-60*s} L{x} {cy-85*s} L{x+15*s} {cy-60*s} V{cy+85*s}Z", fill=CREAM)
    return out


def slider(cx, cy, s=1):
    out = ""
    for i, (v, c) in enumerate([(-40, TEAL), (30, MAROON), (-10, COPPER)]):
        x = cx - 80 * s + i * 80 * s
        out += P(f"M{x} {cy-95*s} V{cy+95*s}", w=SW + 2) + P(rrect(x - 30 * s, cy + v * s - 15 * s, 60 * s, 30 * s, 6), fill=c, op=.95)
    return out


def pause(cx, cy, s=1):
    return C(cx, cy, 90 * s, fill=SKY) + P(rrect(cx - 40 * s, cy - 45 * s, 25 * s, 90 * s, 6), fill=INK) + P(rrect(cx + 15 * s, cy - 45 * s, 25 * s, 90 * s, 6), fill=INK)


def eye(cx, cy, s=1):
    return (P(f"M{cx-120*s} {cy} Q{cx} {cy-110*s} {cx+120*s} {cy} Q{cx} {cy+110*s} {cx-120*s} {cy}Z", fill="#fff")
            + C(cx, cy, 40 * s, fill=TEAL, op=.9) + C(cx, cy, 16 * s, fill=INK) + C(cx + 12 * s, cy - 12 * s, 6 * s, "#fff", fill="#fff", w=1))


def undo(cx, cy, s=1):
    return (P(f"M{cx-60*s} {cy-20*s} H{cx+30*s} A{60*s} {60*s} 0 0 1 {cx+30*s} {cy+100*s} H{cx-40*s}", TEAL, w=SW + 4)
            + P(f"M{cx-25*s} {cy-55*s} L{cx-65*s} {cy-20*s} L{cx-25*s} {cy+15*s}", TEAL, w=SW + 4))


def buttons(cx, cy, s=1):
    out = ""
    for i, (c, glyph) in enumerate([(SAGE, "✓"), (COPPER, "✎"), (MAROON, "✕")]):
        x = cx - 90 * s + i * 90 * s
        out += P(rrect(x - 38 * s, cy - 38 * s, 76 * s, 76 * s, 16), fill=c, op=.9) + T(x, cy + 17 * s, glyph, int(48 * s), "#fff")
    return out


def road(cx, cy, s=1):
    return (P(f"M{cx-40*s} {cy+100*s} C{cx-120*s} {cy+30*s} {cx+90*s} {cy+10*s} {cx+10*s} {cy-100*s} L{cx+30*s} {cy-100*s} C{cx+120*s} {cy+10*s} {cx-80*s} {cy+30*s} {cx+60*s} {cy+100*s}Z", fill="#c7a98a", op=.7)
            + f'<path d="M{cx+10*s} {cy+95*s} C{cx-80*s} {cy+30*s} {cx+100*s} {cy+10*s} {cx+20*s} {cy-95*s}" stroke="#fff" stroke-width="5" fill="none" stroke-dasharray="14 12"/>')


def flag(cx, cy, s=1):
    return P(f"M{cx-60*s} {cy+100*s} V{cy-100*s}", w=SW + 3) + P(f"M{cx-60*s} {cy-100*s} Q{cx} {cy-125*s} {cx+80*s} {cy-90*s} V{cy-10*s} Q{cx} {cy-45*s} {cx-60*s} {cy-20*s}Z", fill=SAGE, op=.9) + P(f"M{cx-100*s} {cy+100*s} H{cx-20*s}", w=SW + 3)


def queue(cx, cy, s=1):
    out = P(f"M{cx-120*s} {cy+50*s} H{cx+120*s}", w=SW)
    for i, c in enumerate([SKY, COPPER, TEAL, SAGE]):
        out += P(rrect(cx - 115 * s + i * 58 * s, cy - 10 * s, 50 * s, 55 * s, 6), fill=c, op=.85, w=4)
    return out + arrow(cx + 60 * s, cy - 60 * s, cx + 130 * s, cy - 60 * s, MAROON, 5) + P(f"M{cx-115*s} {cy-60*s} H{cx+40*s}", w=3)


def heartbeat(cx, cy, s=1):
    return P(_pts([(cx - 120 * s, cy), (cx - 50 * s, cy), (cx - 30 * s, cy - 60 * s), (cx, cy + 70 * s), (cx + 25 * s, cy - 90 * s), (cx + 50 * s, cy), (cx + 120 * s, cy)]), MAROON, w=SW + 2) + C(cx + 120 * s, cy, 10 * s, fill=MAROON)


def gavel(cx, cy, s=1):
    return (f'<g transform="rotate(-35 {cx} {cy})">' + P(rrect(cx - 80 * s, cy - 75 * s, 160 * s, 60 * s, 10), fill=MAROON, op=.85) + P(rrect(cx - 12 * s, cy - 15 * s, 24 * s, 120 * s, 8), fill=COPPER, op=.9) + "</g>"
            + P(rrect(cx - 30 * s, cy + 75 * s, 150 * s, 30 * s, 6), fill=CREAM))


def bellcurve(cx, cy, s=1):
    return (P(f"M{cx-120*s} {cy+70*s} H{cx+120*s}", w=SW) + P(f"M{cx-120*s} {cy+68*s} C{cx-50*s} {cy+68*s} {cx-40*s} {cy-90*s} {cx} {cy-90*s} C{cx+40*s} {cy-90*s} {cx+50*s} {cy+68*s} {cx+120*s} {cy+68*s}", fill=SKY, op=.8)
            + P(f"M{cx} {cy-90*s} V{cy+70*s}", TEAL, w=3) + T(cx + 30 * s, cy + 50 * s, "σ", int(42 * s), MAROON, "start"))


def spike(cx, cy, s=1):
    pts = [(-110, 20), (-80, 10), (-50, 25), (-20, 15), (0, -90), (20, 15), (50, 20), (80, 10), (110, 18)]
    return (f'<path d="M{cx-120*s} {cy-45*s} H{cx+120*s}" stroke="{MAROON}" stroke-width="4" stroke-dasharray="10 10" fill="none"/>'
            + P(_pts([(cx + x * s, cy + y * s) for x, y in pts]), TEAL, w=SW + 1) + C(cx, cy - 90 * s, 12 * s, fill=MAROON) + T(cx + 90 * s, cy - 55 * s, "3σ", int(32 * s), MAROON))


def drift(cx, cy, s=1):
    pts = [(-110, 50), (-80, 45), (-55, 52), (-30, 35), (-5, 30), (20, 18), (45, 5), (70, -10), (95, -28), (115, -40)]
    return (f'<path d="M{cx-120*s} {cy-80*s} H{cx+120*s}" stroke="{MAROON}" stroke-width="4" stroke-dasharray="10 10" fill="none"/>'
            + P(f"M{cx-120*s} {cy+85*s} H{cx+120*s}", w=SW) + P(_pts([(cx + x * s, cy + y * s) for x, y in pts]), COPPER, w=SW + 1)
            + T(cx - 110 * s, cy - 30 * s, "slow drift", int(30 * s), COPPER, "start"))


def gate(cx, cy, s=1):
    return (P(f"M{cx-100*s} {cy+100*s} V{cy-80*s} M{cx+100*s} {cy+100*s} V{cy-80*s}", w=SW + 4) + P(f"M{cx-100*s} {cy-60*s} H{cx+100*s}", w=SW + 2)
            + P(rrect(cx - 60 * s, cy - 25 * s, 120 * s, 60 * s, 10), fill=SAGE, op=.9) + T(cx, cy + 15 * s, "pass?", int(30 * s), "#fff"))


def twin(cx, cy, s=1):
    return monitor(cx - 65 * s, cy, .55 * s) + monitor(cx + 65 * s, cy, .55 * s) + T(cx + 65 * s, cy - 70 * s, "shadow", int(28 * s), TEAL)


def regex(cx, cy, s=1):
    return (P(rrect(cx - 115 * s, cy - 60 * s, 230 * s, 120 * s, 14), fill="#fff") + T(cx, cy + 16 * s, "/ign.re/i", int(40 * s), MAROON)
            + P(f"M{cx-90*s} {cy+30*s} H{cx+90*s}", COPPER, w=4))


def vectors(cx, cy, s=1):
    out = P(f"M{cx-110*s} {cy+90*s} H{cx+110*s} M{cx-110*s} {cy+90*s} V{cy-100*s}", w=4)
    for dx, dy in [(-40, -50), (-20, -30), (-55, -20), (-30, -70), (-5, -55)]:
        out += C(cx + dx * s, cy + dy * s, 11 * s, fill=MAROON, op=.85, w=2)
    out += f'<circle cx="{cx-30*s}" cy="{cy-45*s}" r="{62*s}" stroke="{MAROON}" stroke-width="3" fill="none" stroke-dasharray="8 8"/>'
    return out + C(cx + 70 * s, cy + 40 * s, 13 * s, fill=TEAL, w=2) + C(cx + 5 * s, cy - 10 * s, 13 * s, fill=COPPER, w=2)


def redact(cx, cy, s=1):
    out = P(f"M{cx-75*s} {cy-100*s} H{cx+40*s} L{cx+75*s} {cy-65*s} V{cy+100*s} H{cx-75*s}Z", fill="#fff")
    for i, (w, black) in enumerate([(100, False), (70, True), (100, False), (55, True), (85, False)]):
        y = cy - 55 * s + i * 34 * s
        out += P(rrect(cx - 50 * s, y - 9 * s, w * s, 18 * s, 3), fill=INK, w=2) if black else P(f"M{cx-50*s} {y} H{cx+(w-50)*s}", w=4)
    return out


ICONS = {
    # existing library, normalised to a ~200px box centred on (cx, cy)
    "bubble": lambda x, y, s: bubble(x - 110 * s, y - 75 * s, 220 * s, 130 * s), "kettle": lambda x, y, s: kettle(x, y + 10 * s, .8 * s),
    "magnifier": lambda x, y, s: magnifier(x - 25 * s, y - 25 * s, 1.1 * s), "checklist": lambda x, y, s: checklist(x - 75 * s, y - 95 * s, s),
    "wrench": lambda x, y, s: wrench(x, y, 1.1 * s, ang=40), "coin": lambda x, y, s: coin(x, y, 1.6 * s), "check": lambda x, y, s: check(x, y, 1.6 * s),
    "scroll": lambda x, y, s: scroll(x, y, .9 * s), "toolbox": lambda x, y, s: toolbox(x, y + 15 * s, .8 * s), "gear": lambda x, y, s: gear(x, y, 85 * s),
    "brain": lambda x, y, s: brain(x, y, 1.05 * s), "notebook": lambda x, y, s: notebook(x, y, s), "monitor": lambda x, y, s: monitor(x, y - 10 * s, s),
    "network": lambda x, y, s: network(x, y, .9 * s), "hourglass": lambda x, y, s: hourglass(x, y, s), "blocks": lambda x, y, s: blocks(x + 10 * s, y + 10 * s, .8 * s),
    "rulecard": lambda x, y, s: rulecard(x, y, s), "venn": lambda x, y, s: venn3(x, y - 10 * s, .75 * s), "plug": lambda x, y, s: plug(x - 20 * s, y - 10 * s, 1.1 * s),
    "compass": lambda x, y, s: compass(x, y, .9 * s), "molecule": lambda x, y, s: molecule(x, y, 1.2 * s), "calendar": lambda x, y, s: calendar(x, y + 10 * s, s),
    "scale": lambda x, y, s: scale(x, y, .85 * s), "beaker": lambda x, y, s: beaker(x, y, .9 * s), "cross": lambda x, y, s: cross(x, y, 1.2 * s),
    # new
    "target": target, "miss": lambda x, y, s: target(x - 30 * s, y + 20 * s, .8 * s, miss=True), "cycle": cycle, "globe": globe, "flowchart": flowchart,
    "piano": piano, "retry": retry, "curtain": curtain, "crack": crack, "question": question, "database": database, "stop": stop,
    "calculator": calculator, "shield": shield, "doc": doc, "docs": docs, "contract": contract, "pin": pin, "dice": dice, "trace": trace,
    "coffee": coffee, "knife": knife, "function": function, "idcard": idcard, "pipeline": pipeline, "map": map_, "shapes": shapes,
    "fanout": fanout, "megaphone": megaphone, "book": book, "blackbox": blackbox, "chart": chart, "chartdown": lambda x, y, s: chart(x, y, s, True),
    "nosign": nosign, "key": key, "film": film, "kv": kv, "clock": clock, "trash": trash, "music": music, "chain": chain, "mirror": mirror,
    "tree": tree, "envelope": envelope, "hierarchy": hierarchy, "swap": swap, "server": server, "tangle": tangle, "log": log, "lock": lock,
    "funnel": funnel, "states": states, "bell": bell, "person": person, "mismatch": mismatch, "trophy": trophy, "fence": fence,
    "slider": slider, "pause": pause, "eye": eye, "undo": undo, "buttons": buttons, "road": road, "flag": flag, "queue": queue,
    "regex": regex, "vectors": vectors, "redact": redact,
    "heartbeat": heartbeat, "gavel": gavel, "bellcurve": bellcurve, "spike": spike, "drift": drift, "gate": gate, "twin": twin,
}


def icon(name, cx, cy, s=1.0):
    return ICONS[name](cx, cy, s)


# ───────────────────────── text helpers ─────────────────────────
def wrap(s, n):
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + ([cur] if cur else [])


def split_bullet(b):
    for sep in (" — ", ": "):
        if sep in b:
            h, r = b.split(sep, 1)
            return h, r[0].upper() + r[1:] if r[:1].islower() and sep == ": " else r
    return b, ""


def text_block(b, x, y_mid, head, rest, li, off, hs, rs, hc, anchor, avail=1e9, rewrap=None):
    """Write a heading (coloured) and its explanation, vertically centred on y_mid."""
    gap = lambda sz: sz * 1.22  # noqa: E731
    k = 1.0
    while True:   # shrink (and rewrap wider) until the block fits its card
        if rewrap and k < 1:
            head, rest = rewrap(k)
        rows = [(t, round(hs * k), hc) for t in head] + [(t, round(rs * k), INK) for t in rest]
        total = sum(gap(sz) for _, sz, _ in rows)
        if total <= avail or k < .6:
            break
        k -= .08
    y = y_mid - total / 2
    for i, (t, sz, c) in enumerate(rows):
        y += gap(sz)
        b.write(x, round(y - sz * .28), t, li, off + 0.35 * i, sz, c, anchor)


# ───────────────────────── station layouts ─────────────────────────
def title_station(b, lec, x, y, deco):
    name, sub = lec["name"], f"{lec['track']} · {lec['module']}"
    ch = lec["chapters"].replace("Chapters ", "ch. ").replace("Chapter ", "ch. ")
    b.look(0, x, y, 1600, t=0)
    size = min(170, int(2900 / len(name)))
    b.add(P(f"M{x-480} {y+45} Q{x} {y+15} {x+480} {y+45}", MAROON, w=10), "draw", 0, 0.1, 0.9)
    b.write(x, y - 30, name, 0, -0.4, size, MAROON, dur=1.4)
    b.write(x, y + 140, sub, 0, 1.2, min(60, int(2700 / len(sub))), INK)
    b.write(x, y + 290, f"concepts after Caldwell, The Agentic AI Bible · {ch}", 1, 0.0, 42, TEAL)
    b.add(icon(deco[0], x - 640, y - 300, .75), "draw", 1, 0.8, 0.9)
    b.add(icon(deco[1], x + 640, y - 300, .75), "draw", 1, 2.4, 0.9)


def quote_station(b, sc, first, x, y, beats, quote_at):
    b.look(first, x, y, 1700)
    b.write(x, y - 390, sc.get("kicker", ""), first, 0.0, 58, COPPER)
    n = len(beats)
    xs = [x] if n == 1 else [x - 660 + i * 1320 / (n - 1) for i in range(n)]
    for i, (bx, (li, name, cap)) in enumerate(zip(xs, beats)):
        b.add(icon(name, bx, y - 160, .85 if n < 5 else .75), "draw", li, 0.2, 0.9)
        for j, t in enumerate(wrap(cap, 20 if n < 5 else 15)):
            b.write(bx, y + 40 + j * 50, t, li, 0.8 + j * .4, 42 if n < 5 else 38)
        if i:
            b.add(arrow(xs[i - 1] + 130, y - 160, bx - 130, y - 160, INK, 4, -18), "draw", li, 0.0, 0.5)
    li, off = quote_at
    lines = wrap(sc["quote"], 42)
    b.look(li, x, y + 70, 1700, off=off - 0.4)
    y0 = y + 250 - (len(lines) - 1) * 18
    b.write(x - 21 * len(lines[0]) / 1.4 - 70, y0 + 20, "“", li, off, 120, COPPER)
    for j, t in enumerate(lines):
        b.write(x, y0 + j * 76, t, li, off + 0.2 + j * 1.0, 58, MAROON, dur=max(0.8, 0.035 * len(t)))
    b.add(P(f"M{x-300} {y0 + len(lines) * 76 - 30} Q{x} {y0 + len(lines) * 76 - 50} {x+300} {y0 + len(lines) * 76 - 30}", COPPER, w=6), "draw", li, off + 0.4 + len(lines), 0.6)


def bullet_station(b, sc, first, x, y, cards):
    b.look(first, x, y, 1700)
    b.write(x, y - 420, sc.get("kicker", ""), first, 0.0, 46, TEAL)
    b.write(x, y - 330, sc.get("heading", ""), first, 0.3, 80, MAROON)
    bl, n = sc["bullets"], len(cards)
    accents = [MAROON, TEAL, COPPER, SAGE, MAROON]
    last_nudge = None
    for k, (name, li, off) in enumerate(cards):
        head, rest = split_bullet(bl[k])
        if n == 4:
            cx, cy, cw, ch = x + (-380 if k % 2 == 0 else 380), y - 70 + (k // 2) * 330, 720, 300
            b.add(P(rrect(cx - cw / 2, cy - ch / 2, cw, ch, 22), accents[k], fill="#fff", op=.55, w=4) + icon(name, cx - 235, cy, .72), "draw", li, off, 0.9)
            text_block(b, cx - 115, cy, wrap(head, 16), wrap(rest, 20), li, off + 0.6, 56, 44, accents[k], "start", 270,
                       lambda q, h=head, r=rest: (wrap(h, int(16 / q)), wrap(r, int(20 / q))))
        elif n == 5:
            cx, cy, cw, ch = x - 660 + k * 330, y + 110, 310, 560
            b.add(P(rrect(cx - cw / 2, cy - ch / 2, cw, ch, 22), accents[k], fill="#fff", op=.55, w=4) + icon(name, cx, cy - 150, .7), "draw", li, off, 0.9)
            text_block(b, cx, cy + 105, wrap(head, 11), wrap(rest, 14), li, off + 0.6, 48, 38, accents[k], "middle", 300,
                       lambda q, h=head, r=rest: (wrap(h, int(11 / q)), wrap(r, int(14 / q))))
        else:
            cx, cy, cw, ch = x + (k - (n - 1) / 2) * 520, y + 110, 480, 560
            b.add(P(rrect(cx - cw / 2, cy - ch / 2, cw, ch, 22), accents[k], fill="#fff", op=.55, w=4) + icon(name, cx, cy - 140, .9), "draw", li, off, 0.9)
            text_block(b, cx, cy + 115, wrap(head, 14), wrap(rest, 18), li, off + 0.6, 60, 46, accents[k], "middle", 290,
                       lambda q, h=head, r=rest: (wrap(h, int(14 / q)), wrap(r, int(18 / q))))
        # a gentle push toward each new card, unless one just happened
        t = b.at(li, off)
        if k and (last_nudge is None or t - last_nudge > 2.2):
            b.look(li, x + (cx - x) * .12, y + (cy - y) * .12, 1640, off=off - 0.2)
            last_nudge = t
    b.look(cards[-1][1], x, y, 1700, off=cards[-1][2] + 2.5)


def close_station(b, x, y, li, name, caption):
    b.look(li, x, y, 1500)
    b.add(icon(name, x, y - 90, 1.5), "draw", li, 0.2, 1.0)
    for j, t in enumerate(wrap(caption, 26)):
        b.write(x, y + 200 + j * 84, t, li, 1.0 + j * .5, 70, TEAL)


# m03 has a mid-lecture "map" scene: draw the anatomy as one diagram
def anatomy_station(b, x, y, first):
    b.look(first, x, y, 1700)
    b.write(x, y - 400, "The whole anatomy", first, 0.0, 84, MAROON)
    b.add(icon("brain", x - 520, y - 60, 1.1), "draw", first, 0.6, 1.0); b.write(x - 520, y + 120, "model", first, 1.2, 54, MAROON)
    b.add(arrow(x - 380, y - 90, x - 120, y - 90, MAROON, 7, -30), "draw", first + 1, 0.3, 0.6)
    b.write(x - 250, y - 175, "tool call", first + 1, 0.6, 44, MAROON)
    b.add(icon("shield", x, y - 70, .8), "draw", first + 2, 0.0, 0.8); b.write(x, y + 90, "validated input", first + 2, 0.6, 44, TEAL)
    b.add(arrow(x + 110, y - 90, x + 360, y - 90, TEAL, 7, -30), "draw", first + 2, 1.0, 0.6)
    b.add(icon("toolbox", x + 520, y - 60, 1.1), "draw", first + 2, 1.4, 1.0); b.write(x + 520, y + 120, "tools run it", first + 2, 2.0, 50, TEAL)
    b.add(arrow(x + 480, y + 220, x - 480, y + 220, COPPER, 7, -110), "draw", first + 2, 2.8, 1.2)
    b.write(x, y + 410, "observe every result", first + 2, 3.6, 62, COPPER)
    b.write(x - 520, y + 175, "never runs privileged ops", first + 1, 2.5, 38, INK)


# ───────────────────────── generic storyboard ─────────────────────────
def absolute(sp, f):
    """Specs marked rel=True count lines from the start of their scene; convert them to lecture-wide numbers."""
    if not sp.get("rel"):
        return sp
    sp = dict(sp)
    if "cards" in sp:
        sp["cards"] = [(c[0], c[1] + f) + tuple(c[2:]) for c in sp["cards"]]
    if "beats" in sp:
        sp["beats"] = [(b[0] + f,) + tuple(b[1:]) for b in sp["beats"]]
    if "quote_at" in sp:
        sp["quote_at"] = (sp["quote_at"][0] + f, sp["quote_at"][1])
    if "close" in sp:
        sp["close"] = (sp["close"][0] + f,) + tuple(sp["close"][1:])
    return sp



def make_board(spec):
    def board(b):
        lec = b.lec
        scenes, first, li = lec["scenes"], [], 0
        for sc in scenes:
            first.append(li); li += len(sc["lines"])
        plan = []  # (kind, scene index)
        assert len(spec) == len(scenes), f"{lec['id']}: {len(spec)} specs for {len(scenes)} scenes"
        specs = [absolute(sp, first[si]) for si, sp in enumerate(spec)]
        for si, (sc, sp) in enumerate(zip(scenes, specs)):
            if sc["type"] == "image" and "custom" not in sp:
                plan.append(("overview", si))
                if sp.get("close"):
                    plan.append(("close", si))
            else:
                plan.append(("station", si))
        cells = grid(sum(1 for k, _ in plan if k != "overview"))
        b.cells = cells
        ci = 0
        for kind, si in plan:
            sc, sp = scenes[si], specs[si]
            if kind == "overview":
                b.overview(first[si])
                continue
            x, y = cells[ci]; ci += 1
            if kind == "close":
                li, name, cap = sp["close"]
                close_station(b, x, y, li, name, cap)
            elif sc["type"] == "title":
                title_station(b, lec, x, y, sp["deco"])
            elif sc["type"] == "quote":
                quote_station(b, sc, first[si], x, y, sp["beats"], sp["quote_at"])
            elif sc["type"] == "bullets":
                bullet_station(b, sc, first[si], x, y, [(c[0], c[1], c[2] if len(c) > 2 else 0.3) for c in sp["cards"]])
            elif sp.get("custom") == "anatomy":
                anatomy_station(b, x, y, first[si])
        b.finale()
    return board


# ───────────────────────── per-module specs (line numbers are lecture-wide) ─────────────────────────
SPECS = {
    "m01": [
        {"deco": ["target", "cycle"]},
        {"beats": [(2, "coin", "an “autonomous” refund agent"), (3, "gear", "a routine model update"), (4, "database", "a stale catalog"),
                   (5, "check", "refunds for items never sold"), (6, "calendar", "months of postmortem")], "quote_at": (5, 2.0)},
        {"cards": [("target", 8), ("toolbox", 9), ("globe", 9, 3.0), ("cycle", 10)]},
        {"cards": [("bubble", 12), ("piano", 13), ("flowchart", 14), ("blocks", 15)]},
        {"cards": [("cycle", 17, 0.0), ("miss", 17, 1.2), ("retry", 17, 2.4)]},
        {"beats": [(19, "curtain", "a dazzling demo"), (20, "crack", "collapses in production"), (22, "question", "the right tool?")], "quote_at": (19, 1.5)},
        {"close": (24, "blocks", "next: the smallest real agent")},
    ],
    "m03": [
        {"deco": ["brain", "toolbox"]},
        {"beats": [(2, "coin", "the refund agent again"), (3, "scroll", "an invented policy"), (4, "question", "a missing organ"),
                   (5, "stop", "“I don't know”")], "quote_at": (3, 1.5)},
        {"cards": [("brain", 7), ("toolbox", 8), ("notebook", 9), ("cycle", 10), ("stop", 11)]},
        {"custom": "anatomy"},
        {"cards": [("calculator", 17), ("question", 17, 4.5), ("shield", 18), ("doc", 19)]},
        {"cards": [("pin", 22, 0.2), ("dice", 22, 1.6), ("trace", 22, 3.0), ("stop", 24, 0.5)]},
        {"cards": [("question", 26), ("flag", 27), ("coffee", 28)]},
    ],
    "m04": [
        {"deco": ["plug", "knife"]},
        {"cards": [("monitor", 3), ("megaphone", 4), ("doc", 5), ("knife", 6)]},
        {"cards": [("map", 8), ("shapes", 9), ("fanout", 10), ("globe", 11)]},
        {"cards": [("function", 14), ("bubble", 15), ("gear", 16), ("flowchart", 17, 2.5)]},
        {"cards": [("checklist", 19), ("flowchart", 20), ("idcard", 21, 1.0), ("pipeline", 22)]},
        {"beats": [(24, "docs", "ten real inputs"), (25, "function", "a fixed shape? a function call"), (26, "scale", "run both side by side"),
                   (27, "lock", "critical rules in code")], "quote_at": (24, 2.0)},
        {"close": (29, "brain", "next: the model and its tools")},
    ],
    "m05": [
        {"deco": ["brain", "wrench"]},
        {"cards": [("book", 3), ("bubble", 4), ("wrench", 5), ("shield", 6)]},
        {"beats": [(8, "dice", "trained by someone else"), (9, "blackbox", "messages in, calls out"), (10, "target", "what can you cause?")], "quote_at": (7, 0.3)},
        {"cards": [("docs", 11), ("shapes", 12), ("chart", 13), ("coin", 13, 3.0)]},
        {"cards": [("contract", 15), ("nosign", 16), ("retry", 17), ("key", 17, 3.5)]},
        {"close": (19, "fanout", "lab: a tool router")},
    ],
    "m06": [
        {"deco": ["notebook", "brain"]},
        {"beats": [(2, "chart", "great on day one"), (3, "bubble", "re-explain, every session"), (4, "chartdown", "usage down 60%"),
                   (5, "notebook", "a memory layer")], "quote_at": (4, 1.5)},
        {"cards": [("brain", 7), ("film", 8), ("book", 9), ("checklist", 10)]},
        {"cards": [("kv", 12), ("magnifier", 13), ("network", 14), ("blocks", 14, 4.0)]},
        {"cards": [("docs", 16), ("clock", 16, 4.5), ("idcard", 17), ("trash", 17, 3.5)]},
        {"close": (20, "music", "midterm: Encore, a music agent")},
    ],
    "m07": [
        {"deco": ["map", "checklist"]},
        {"beats": [(2, "map", "research → roadmap"), (3, "chartdown", "more items, more failures"), (4, "chain", "twenty steps deep"),
                   (5, "checklist", "a planning step")], "quote_at": (4, 1.5)},
        {"cards": [("cycle", 7), ("map", 8), ("mirror", 9), ("tree", 10)]},
        {"cards": [("checklist", 12), ("compass", 12, 3.5), ("mirror", 13), ("database", 15)]},
        {"close": (17, "wrench", "midterm workshop: bring Encore")},
    ],
    "m08": [
        {"deco": ["plug", "envelope"]},
        {"beats": [(2, "plug", "“the USB-C of AI”?"), (4, "envelope", "a JSON-RPC envelope"), (5, "doc", "what HTTP is to documents")], "quote_at": (3, 0.5)},
        {"cards": [("hierarchy", 6), ("swap", 7), ("toolbox", 8), ("server", 9)]},
        {"cards": [("tangle", 10), ("envelope", 11), ("network", 11, 3.0), ("crack", 12, 3.0)]},
        {"cards": [("log", 13), ("lock", 15), ("key", 15, 3.0), ("funnel", 16)]},
        {"close": (18, "server", "extra credit: your own MCP server")},
    ],
    "m09": [
        {"deco": ["fanout", "shield"]},
        {"beats": [(2, "chart", "six good months"), (3, "retry", "the same call, again"), (4, "question", "nothing changed?"),
                   (5, "cycle", "one flat loop"), (6, "states", "routing + state")], "quote_at": (4, 0.8)},
        {"cards": [("fanout", 8), ("shield", 9), ("states", 10), ("notebook", 11), ("bell", 13)]},
        {"cards": [("cycle", 15), ("chartdown", 16), ("shield", 17), ("bell", 18)]},
        {"close": (20, "hierarchy", "next: forming the band")},
    ],
    "m10": [
        {"deco": ["network", "hierarchy"]},
        {"beats": [(2, "pipeline", "extract → research → draft"), (3, "docs", "hundreds of pages"), (4, "mismatch", "mismatched schemas")], "quote_at": (4, 1.5)},
        {"cards": [("hierarchy", 6), ("pipeline", 7), ("fanout", 8), ("tree", 9)]},
        {"cards": [("lock", 11), ("contract", 12), ("trophy", 13), ("fence", 13, 4.0)]},
        {"beats": [(14, "contract", "version every contract"), (15, "mismatch", "the #1 pipeline failure"), (16, "database", "state & recovery, not role-play")], "quote_at": (15, 0.5)},
        {"close": (18, "hierarchy", "next: Encore Ensemble")},
    ],
    "m11": [
        {"deco": ["slider", "person"]},
        {"beats": [(2, "magnifier", "a fraud-detection agent"), (3, "check", "the clear 85%"), (4, "question", "the hard 15%"),
                   (6, "buttons", "escalate below a threshold")], "quote_at": (5, 0.3)},
        {"cards": [("pause", 8), ("eye", 9), ("scale", 10)]},
        {"cards": [("undo", 12), ("target", 12, 3.0), ("clock", 12, 6.0), ("stop", 14), ("slider", 15)]},
        {"cards": [("doc", 17), ("buttons", 17, 2.5), ("slider", 18), ("database", 19)]},
        {"cards": [("log", 21), ("queue", 22), ("bell", 23), ("flag", 24)]},
        {"close": (28, "road", "next: the long tour")},
    ],
    "m12": [
        {"deco": ["clock", "flag"]},
        {"beats": [(2, "doc", "a weekly regulatory briefing"), (3, "clock", "“forty minutes”"), (4, "retry", "throttling, retry storms"),
                   (5, "coin", "a $340 bill"), (6, "function", "built like a function call")], "quote_at": (5, 1.5)},
        {"cards": [("flag", 8), ("queue", 9), ("coin", 10), ("heartbeat", 11)]},
        {"cards": [("flag", 12), ("docs", 12, 2.5), ("trace", 13), ("gear", 13, 4.0)]},
        {"beats": [(15, "pipeline", "named stages"), (16, "database", "persist, then move on"), (17, "key", "idempotent tools"),
                   (18, "bell", "budget alarms in the loop")], "quote_at": (15, 0.5)},
        {"close": (20, "eye", "next: the sound check")},
    ],
    "m13": [
        {"deco": ["eye", "chart"]},
        {"beats": [(2, "check", "every test passed"), (3, "megaphone", "3× the complaints"), (4, "book", "a cold legal FAQ"),
                   (5, "magnifier", "three days to diagnose")], "quote_at": (3, 2.5)},
        {"cards": [("trace", 8, 0.3), ("log", 8, 3.0), ("gavel", 8, 5.5), ("drift", 8, 8.0)]},
        {"cards": [("bellcurve", 9), ("spike", 10), ("drift", 11), ("flag", 12)]},
        {"cards": [("coin", 13), ("trace", 14), ("gate", 15), ("twin", 15, 3.5)]},
        {"close": (17, "shield", "last track: keeping the show safe")},
    ],
    "m14": [
        {"deco": ["shield", "lock"]},
        {"beats": [(3, "compass", "the creator's intent and values"), (4, "tangle", "instructions from everywhere"), (6, "drift", "a quiet drift"),
                   (7, "shield", "guardrails at every boundary")], "quote_at": (5, 1.0)},
        {"cards": [("regex", 9), ("vectors", 10), ("brain", 11), ("funnel", 12)]},
        {"cards": [("contract", 14), ("redact", 14, 3.5), ("swap", 15), ("fence", 17)]},
        {"cards": [("bubble", 19), ("film", 21), ("drift", 22), ("lock", 23)]},
        {"beats": [(24, "shield", "holds even if misread"), (25, "lock", "allowlists · scopes · validators"), (26, "log", "log decisions, test grooming"),
                   (27, "flag", "capstone: bring evidence")], "quote_at": (24, 0.8)},
        {"close": (29, "music", "that's the whole show · thank you")},
    ],

    # ── lab and project tracks (line numbers relative to each scene) ──
    "lab1": [
        {"deco": ["monitor", "bubble"]},
        {"rel": True, "beats": [(1, "bubble", "a bare-bones chatbot"), (2, "globe", "add web search"), (3, "question", "is it an agent?")], "quote_at": (0, 1.5)},
        {"rel": True, "cards": [("monitor", 0), ("docs", 1), ("key", 2), ("lock", 3)]},
        {"rel": True, "cards": [("bubble", 0), ("swap", 1), ("question", 2), ("log", 3)]},
        {"rel": True, "cards": [("target", 0), ("globe", 1), ("compass", 2), ("scroll", 3)]},
        {"rel": True, "close": (1, "brain", "next: the model takes the controls")},
    ],
    "lab2": [
        {"deco": ["cycle", "toolbox"]},
        {"rel": True, "beats": [(0, "compass", "the model decides"), (1, "book", "agents, percepts, environments"), (2, "blocks", "the five-level ladder")], "quote_at": (2, 1.0)},
        {"rel": True, "cards": [("target", 1), ("toolbox", 2), ("docs", 3), ("cycle", 4)]},
        {"rel": True, "cards": [("stop", 0), ("log", 1), ("shield", 2), ("retry", 3)]},
        {"rel": True, "close": (1, "road", "next: harden it for the road")},
    ],
    "lab3": [
        {"deco": ["shield", "server"]},
        {"rel": True, "beats": [(0, "chain", "longer, harder tasks"), (1, "server", "online and offline"), (2, "coin", "cheap and expensive tiers")], "quote_at": (0, 2.5)},
        {"rel": True, "cards": [("docs", 0), ("scroll", 1), ("contract", 2), ("megaphone", 3)]},
        {"rel": True, "cards": [("log", 0), ("doc", 1), ("pin", 2), ("chart", 3)]},
        {"rel": True, "close": (1, "fanout", "next: tool routing")},
    ],
    "lab4": [
        {"deco": ["fanout", "toolbox"]},
        {"rel": True, "beats": [(0, "toolbox", "every tool, every call"), (1, "fanout", "route first"), (2, "gear", "a meta tool")], "quote_at": (0, 2.5)},
        {"rel": True, "cards": [("calendar", 0), ("cross", 0, 3.0), ("lock", 2), ("checklist", 3)]},
        {"rel": True, "cards": [("checklist", 0), ("bubble", 1), ("shield", 2), ("undo", 3)]},
        {"rel": True, "close": (1, "music", "next: Encore, and MCP")},
    ],
    "lab5": [
        {"deco": ["plug", "server"]},
        {"rel": True, "beats": [(0, "swap", "list, then call"), (1, "plug", "a Gradio server, a web client")], "quote_at": (1, 2.0)},
        {"rel": True, "cards": [("bubble", 0), ("calculator", 1), ("trophy", 2), ("globe", 3)]},
        {"rel": True, "cards": [("function", 1, 0.3), ("doc", 1, 2.5), ("kv", 1, 4.5), ("slider", 2)]},
        {"rel": True, "close": (1, "hierarchy", "use it in Encore Ensemble")},
    ],
    "encore": [
        {"deco": ["music", "notebook"]},
        {"rel": True, "beats": [(0, "music", "answers, finds, builds"), (1, "film", "recalls last week"), (2, "lock", "writes wait for approval"),
                                (3, "cycle", "the model picks each step")], "quote_at": (0, 2.5)},
        {"rel": True, "cards": [("cycle", 0), ("toolbox", 1), ("contract", 2), ("lock", 3)]},
        {"rel": True, "cards": [("brain", 1), ("film", 1, 3.0), ("book", 2), ("checklist", 2, 4.0)]},
        {"rel": True, "cards": [("magnifier", 0), ("docs", 1), ("chart", 1, 3.5), ("curtain", 2)]},
        {"rel": True, "close": (1, "hierarchy", "next: Encore Ensemble")},
    ],
    "ensemble": [
        {"deco": ["hierarchy", "music"]},
        {"rel": True, "beats": [(0, "music", "your midterm, extended"), (1, "crack", "failures in your traces"), (2, "scale", "before and after")], "quote_at": (2, 1.0)},
        {"rel": True, "cards": [("map", 1), ("plug", 2), ("shield", 3), ("hierarchy", 4)]},
        {"rel": True, "cards": [("log", 0), ("stop", 1), ("contract", 2), ("person", 3)]},
        {"rel": True, "close": (1, "trophy", "enjoy the show")},
    ],
}

BOARDS = {k: make_board(v) for k, v in SPECS.items()}
