#!/usr/bin/env python3
"""Draw The Daily Globe for Friday 27 November 2026.

Fresh build for make.fun news-image-20261127. One 1024x1024 newspaper
page, drawn entirely with Pillow vector shapes and text: no photos, no
copied art, no copied text from any other entry. Every story was checked
against reporting dated 27 November 2026 (Reuters, AP and outlets
carrying their wires); the footer DATE CHECK names the borderline items.

Deterministic: fixed palette, fixed fonts, no randomness, no timestamps.
Run:  python3 draw27.py   -> writes entry.png next to this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN  # 976

# ---- palette: newsprint on cream paper ------------------------------------
PAPER = (247, 242, 231)
INK = (26, 24, 20)
MUTED = (96, 90, 78)
RED = (178, 34, 28)
RULE = (58, 52, 44)
SEA = (168, 198, 214)
LAND = (226, 214, 178)
LAND_DARK = (203, 188, 148)
SAND = (240, 232, 205)
GOLD = (176, 128, 28)
GREEN = (24, 128, 96)
BLUE = (36, 84, 158)

REGION = {
    "EUROPE": (36, 84, 158),
    "MIDDLE EAST": (178, 34, 28),
    "ASIA": (24, 128, 96),
    "GLOBAL": (122, 90, 160),
    "AMERICAS": (90, 60, 140),
    "AFRICA": (176, 110, 20),
}

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = lambda s: font("NotoSerif-Bold.ttf", s)
F_SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
F_SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s)
F_SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s)
F_SANS = lambda s: font("NotoSans-Regular.ttf", s)
F_SANS_B = lambda s: font("NotoSans-Bold.ttf", s)
F_SANS_I = lambda s: font("NotoSans-Italic.ttf", s)


def wrap(text, fnt, width):
    """Greedy word wrap; returns lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill=INK, leading=None):
    lh = leading if leading is not None else int(fnt.size * 1.32)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hline(d, x0, x1, y, fill=RULE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def disc(d, cx, cy, n, r=11, fill=RED, fg=(255, 255, 255)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
              outline=(255, 255, 255), width=1)
    f = F_SANS_B(13 if n < 10 else 10)
    t = str(n)
    d.text((cx - f.getlength(t) / 2, cy - f.size / 2 - 1), t, font=f, fill=fg)


def kicker_bar(d, x, y, w, region, label):
    d.rectangle([x, y, x + w, y + 20], fill=REGION[region])
    d.text((x + 8, y + 3), label, font=F_SANS_B(11), fill=(255, 255, 255))


# ---- the three main-story panels (all drawn, all original) ----------------

def panel_eu(d, x, y, w, h):
    """Brussels hemicycle: rows of seats, a split vote, NO DEAL stamp."""
    d.rectangle([x, y, x + w, y + h], fill=SAND, outline=RULE, width=1)
    d.text((x + 10, y + 7), "THE 2028-2034 BUDGET, € TRILLION",
           font=F_SANS_B(10), fill=MUTED)
    # Hemicycle arcs of seats: blue for, red against, grey undecided.
    cx, cy = x + w // 2, y + h - 8
    for ri, rad in enumerate((28, 42, 56)):
        for k in range(13):
            ang = 3.14159 * (0.08 + 0.84 * k / 12.0)
            px = cx + int(rad * 1.45 * -math.cos(ang))
            py = cy - int(rad * math.sin(ang))
            col = BLUE if k < 5 else (RED if k >= 8 else (150, 140, 120))
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col)
    # NO DEAL stamp, drawn straight (no rotation: deterministic text).
    d.rectangle([x + w - 118, y + 10, x + w - 12, y + 38], outline=RED, width=3)
    d.text((x + w - 108, y + 14), "NO DEAL", font=F_SANS_B(18), fill=RED)


def panel_kyiv(d, x, y, w, h):
    """Kyiv at night: dark sky, missile trails, a hit tower block, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 44), outline=RULE, width=1)
    # Stars.
    for sx, sy in [(0.08, 0.12), (0.22, 0.06), (0.38, 0.14), (0.55, 0.07),
                   (0.72, 0.12), (0.88, 0.06), (0.95, 0.18), (0.47, 0.20)]:
        px, py = x + int(w * sx), y + int(h * sy)
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(220, 220, 200))
    # Missile trails arcing down.
    for (x0, y0, x1, y1) in [(0.12, 0.05, 0.30, 0.62), (0.55, 0.02, 0.68, 0.55),
                             (0.85, 0.08, 0.92, 0.48)]:
        d.line([(x + int(w * x0), y + int(h * y0)),
                (x + int(w * x1), y + int(h * y1))], fill=(255, 190, 90), width=2)
        d.ellipse([x + int(w * x1) - 3, y + int(h * y1) - 3,
                   x + int(w * x1) + 3, y + int(h * y1) + 3], fill=(255, 120, 40))
    # Skyline: dark blocks, one burning.
    base = y + h
    for bx, bw, bh in [(0.02, 0.16, 0.34), (0.20, 0.13, 0.46), (0.35, 0.17, 0.30),
                       (0.54, 0.14, 0.52), (0.70, 0.15, 0.36), (0.87, 0.11, 0.42)]:
        d.rectangle([x + int(w * bx), base - int(h * bh),
                     x + int(w * (bx + bw)), base], fill=(12, 14, 26))
    # Burning block: orange windows + smoke.
    bx = x + int(w * 0.54)
    for wy in range(3):
        d.rectangle([bx + 6, base - int(h * 0.52) + wy * 12,
                     bx + 16, base - int(h * 0.52) + wy * 12 + 7], fill=(255, 140, 30))
    d.text((x + 10, y + 8), "113 DRONES · BALLISTIC MISSILES",
           font=F_SANS_B(10), fill=(255, 210, 140))
    for i, (sx, sy, sr) in enumerate([(0.58, 0.44, 8), (0.62, 0.36, 10), (0.66, 0.28, 12)]):
        d.ellipse([x + int(w * sx) - sr, y + int(h * sy) - sr // 2,
                   x + int(w * sx) + sr, y + int(h * sy) + sr // 2],
                  fill=(120, 120, 130))
    d.rectangle([x + 6, y + h - 26, x + 214, y + h - 4], fill=(24, 28, 44))
    d.text((x + 10, y + h - 22), "A mall hit in Kyiv; a tower block",
           font=F_SANS_B(10), fill=(235, 235, 220))
    d.text((x + 10, y + h - 11), "burns in Kharkiv",
           font=F_SANS(10), fill=(200, 200, 190))


def panel_gulf(d, x, y, w, h):
    """Gulf waters: tanker, Brent bars rising, warning flag."""
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=RULE, width=1)
    # Sand strip (Arabia) at bottom.
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 22),
               (x + int(w * 0.55), y + h - 34), (x, y + h - 26)], fill=LAND_DARK)
    d.text((x + 10, y + 8), "BRENT $/BARREL, THIS WEEK",
           font=F_SANS_B(10), fill=(20, 60, 90))
    # Rising bars: Mon-Thu approx 92.8 -> 96.1.
    vals = [92.8, 93.6, 95.9, 96.1]
    bx0, bw, gap = x + 12, 16, 8
    for i, v in enumerate(vals):
        bh = int((v - 90.0) * 5)
        d.rectangle([bx0 + i * (bw + gap), y + 62 - bh,
                     bx0 + i * (bw + gap) + bw, y + 62], fill=RED if i == 3 else BLUE)
    d.text((bx0, y + 66), "$96.14  ·  +3.9% wk",
           font=F_SANS_B(11), fill=INK)
    # Tanker hull on the waterline.
    ty = y + h - 52
    d.rectangle([x + 150, ty, x + 262, ty + 12], fill=(40, 40, 40))
    d.rectangle([x + 228, ty - 9, x + 238, ty], fill=(40, 40, 40))
    d.line([(x + 150, ty + 12), (x + 262, ty + 12)], fill=RED, width=2)
    d.text((x + 150, ty + 16), "GULF TANKER TRAFFIC", font=F_SANS_B(9), fill=INK)
    d.text((x + 150, ty + 27), "still moving", font=F_SANS(9), fill=MUTED)
    # Warning pennant.
    d.polygon([(x + w - 34, y + 10), (x + w - 10, y + 18), (x + w - 34, y + 26)],
              fill=(255, 200, 40), outline=RED)


# ---- schematic world map ---------------------------------------------------

def world_map(d, x, y, w, h, pins):
    """Schematic continents (equirectangular outlines) with numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 238), outline=RULE, width=1)
    d.text((x + 10, y + 6), "WHERE IT HAPPENED", font=F_SANS_B(11), fill=INK)
    d.text((x + 10, y + 20), "Pins carry the story numbers.",
           font=F_SANS_I(10), fill=MUTED)
    ox, oy = x + 14, y + 34
    mw, mh = w - 28, h - 44

    def P(lon, lat):
        return (ox + (lon + 170) / 360.0 * mw, oy + (90 - lat) / 180.0 * mh)

    continents = [
        [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-82, 62), (-76, 45),
         (-70, 42), (-80, 32), (-84, 30), (-97, 26), (-105, 20), (-95, 16),
         (-83, 9), (-79, 9), (-92, 15), (-105, 23), (-117, 33), (-125, 49),
         (-150, 60), (-168, 66)],
        [(-79, 9), (-62, 10), (-52, 5), (-35, -8), (-40, -22), (-48, -28),
         (-58, -35), (-65, -41), (-70, -30), (-70, -18), (-77, -12),
         (-81, -5), (-79, 9)],
        [(-10, 35), (-6, 36), (3, 37), (10, 37), (12, 44), (19, 46), (23, 40),
         (28, 36), (36, 36), (43, 39), (48, 41), (41, 46), (30, 46), (24, 45),
         (19, 42), (13, 45), (8, 44), (3, 43), (-2, 44), (-2, 48), (-5, 50),
         (-10, 53), (-10, 35)],
        [(-18, 35), (-17, 32), (-10, 31), (-6, 30), (10, 34), (11, 34),
         (20, 32), (30, 31), (32, 31), (35, 28), (39, 21), (43, 12), (51, 12),
         (55, 17), (58, 20), (52, 25), (48, 29), (44, 29), (40, 31), (35, 36),
         (30, 36), (27, 37), (23, 36), (19, 36), (15, 38), (12, 38), (8, 37),
         (3, 37), (-6, 35), (-10, 37), (-18, 35)],
        [(-18, 15), (-17, 15), (-16, 12), (-13, 8), (-8, 5), (-8, 4), (9, 4),
         (14, -2), (12, -5), (13, -12), (12, -18), (16, -29), (20, -35),
         (28, -33), (32, -29), (35, -24), (40, -16), (40, -10), (42, -1),
         (48, 2), (51, 11), (44, 11), (39, 15), (35, 18), (30, 18), (22, 21),
         (15, 24), (10, 30), (0, 32), (-6, 34), (-10, 31), (-17, 21),
         (-18, 15)],
        [(68, 75), (100, 77), (140, 72), (170, 66), (178, 65), (162, 60),
         (158, 53), (142, 50), (140, 40), (130, 33), (122, 30), (120, 23),
         (110, 20), (105, 9), (100, 8), (97, 16), (92, 21), (89, 22), (80, 13),
         (77, 8), (73, 16), (66, 25), (61, 25), (57, 27), (52, 29), (48, 30),
         (44, 39), (40, 41), (35, 44), (30, 46), (28, 45), (24, 41), (20, 40),
         (15, 38), (10, 37), (5, 36), (0, 36), (-5, 36), (-9, 43), (-9, 49),
         (-5, 50), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55),
         (24, 58), (28, 59), (30, 62), (32, 65), (40, 68), (50, 69), (68, 75)],
        [(114, -22), (122, -14), (130, -12), (137, -12), (142, -11),
         (146, -19), (150, -23), (153, -27), (150, -37), (140, -38),
         (130, -32), (124, -33), (115, -35), (114, -22)],
    ]
    for poly in continents:
        d.polygon([P(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(120, 105, 75))
    for n, lon, lat in pins:
        px, py = P(lon, lat)
        disc(d, int(px), int(py), n, r=9)


# ---- story data: every item checked against 27 Nov 2026 reporting ---------

NUMBERS = [
    ("BRENT CRUDE", "$96.14", "+3.9% on the week"),
    ("SHANGHAI COMP.", "+3.0%", "STAR 50 +12%"),
    ("EU BUDGET", "€1.58tn", "no deal in Brussels"),
    ("UKRAINE LOAN", "$49bn", "stalled at the summit"),
    ("RUSSIAN DRONES", "113", "in one overnight wave"),
    ("UKRAINE TOLL", "10 killed", "58 hurt, 3 of them children"),
]

MAINS = [
    {
        "n": 1, "region": "EUROPE", "kicker": "EUROPE · BRUSSELS",
        "headline": "EU leaders leave Brussels with no budget deal",
        "body": ("After 12+ hours, the summit fails on the 2028-2034 "
                 "budget and a new $49bn loan for Ukraine. Macron sets a "
                 "year-end deadline; leaders meet again 17-18 Dec."),
        "source": "AP · REUTERS, 27 NOV",
        "panel": panel_eu,
    },
    {
        "n": 2, "region": "MIDDLE EAST", "kicker": "WAR · UKRAINE",
        "headline": "Overnight strikes kill 10 across Ukraine",
        "body": ("Ballistic missiles hit a Kyiv shopping centre, wounding "
                 "7; a drone sets a Kharkiv tower block ablaze, killing a "
                 "couple on the 15th floor. 113 drones in the wave; 87 downed."),
        "source": "UKRAINIAN OFFICIALS · WIRE REPORTS, 27 NOV",
        "panel": panel_kyiv,
    },
    {
        "n": 3, "region": "GLOBAL", "kicker": "ENERGY · THE GULF",
        "headline": "Gulf warnings push oil to its first weekly gain in four",
        "body": ("Iran warns a foreign military presence in the Gulf would "
                 "heighten tensions as Seoul widens its naval patrols. "
                 "Brent $96.14, up 3.9% on the week, down 18% on the month."),
        "source": "REUTERS, 27 NOV",
        "panel": panel_gulf,
    },
]

CARDS = [
    (4, "EUROPE", "Drone breaches Latvian airspace",
     "Unidentified drone crosses early Friday as Russia downs 40+ drones."),
    (5, "MIDDLE EAST", "Turkey ratifies Mecca defence pact",
     "Erdogan signs the pact with Pakistan and Saudi Arabia into law."),
    (6, "ASIA", "India-US trade deal 'near done'",
     "Goyal: deal close; US would cap tariffs at 17% with a deal, not 25%."),
    (7, "ASIA", "China stocks jump on support vow",
     "Shanghai +3%, STAR 50 +12% after Beijing vows market support."),
    (8, "EUROPE", "Hernández de Cos to lead the ECB",
     "EU leaders pick Spain's Pablo Hernández de Cos to succeed Lagarde."),
    (9, "ASIA", "Seoul sends six North Koreans home",
     "Six rescued from a drifting boat go home by sea; a seventh stays."),
    (10, "EUROPE", "IAEA seeks pause to fix Zaporizhzhia link",
     "Watchdog seeks a local ceasefire after the plant's 28th power loss."),
    (11, "ASIA", "Duterte's ICC trial opens on Monday",
     "Ex-leader, 81, faces 85 murder counts from his drug war; plea first."),
    (12, "ASIA", "Cambodia, Thailand agree site visit",
     "Both sides allow a visit to disputed islands in UN-backed proceedings."),
    (13, "GLOBAL", "US pressed Venezuela, Iraq on OPEC",
     "Washington urged both to consider leaving OPEC and blocked dues."),
]

BRIEFS = [
    (14, "China tests Taiwan landing tactics in Fujian drills, linking civilian ships into a floating bridge."),
    (15, "Iraq's PM orders the oil ministry to take over Kurdish-area oilfields; Kurdish leaders reject it."),
    (16, "Musk promises every US child two SpaceX shares — a gift put at about $18bn in all."),
    (17, "Nvidia: S&P puts its rating on watch; it halts chip-server shipments to four SE Asian states."),
    (18, "Dollar heads for a third monthly gain at 103.8; a December Fed rate rise is seen as near-certain."),
    (19, "Asia steadies: South Korea +4%, Nikkei +0.7% on the week; Nasdaq futures +1%, S&P +0.8%."),
    (20, "Wall Street shut for Thanksgiving; cash Treasuries reopen, 10-year yield 4.89%."),
]

PINS = [
    (1, 4.4, 50.8), (2, 30.5, 52.0), (3, 56.0, 26.0), (4, 24.1, 56.9),
    (5, 32.9, 39.9), (6, 77.2, 28.6), (7, 116.4, 39.9),
    (9, 127.0, 37.5), (10, 36.0, 46.0), (11, 121.0, 14.6), (12, 103.8, 13.8),
    (13, -66.9, 10.5), (14, 119.6, 25.0), (20, -77.0, 38.9),
]


# ---- page assembly ----------------------------------------------------------

def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=RULE, width=2)

    # Kicker bar.
    d.rectangle([MARGIN, 16, MARGIN + CW, 36], fill=RED)
    d.text((MARGIN + 10, 20), "WORLD NEWS IN ONE PAGE",
           font=F_SANS_B(11), fill=(255, 255, 255))
    right = "No. 27  ·  2026"
    d.text((MARGIN + CW - 10 - F_SANS_B(11).getlength(right), 20), right,
           font=F_SANS_B(11), fill=(255, 255, 255))

    # Masthead: name, then the date as the hero.
    title = "The Daily Globe"
    tf = F_MAST(54)
    d.text(((W - tf.getlength(title)) / 2, 42), title, font=tf, fill=INK)
    date = "FRIDAY 27 NOVEMBER 2026"
    df = F_SERIF_B(28)
    d.text(((W - df.getlength(date)) / 2, 96), date, font=df, fill=RED)
    sub = "The world on Friday — 20 stories, one page"
    sf = F_SERIF_I(13)
    d.text(((W - sf.getlength(sub)) / 2, 128), sub, font=sf, fill=MUTED)

    # Key-numbers band.
    by = 152
    d.rectangle([MARGIN, by, MARGIN + CW, by + 56], outline=RULE, width=1)
    cell = CW / 6.0
    for i, (lab, val, note) in enumerate(NUMBERS):
        x = MARGIN + int(i * cell)
        if i:
            d.line([(x, by + 6), (x, by + 50)], fill=RULE, width=1)
        d.text((x + 10, by + 5), lab, font=F_SANS_B(9), fill=MUTED)
        vf = F_SERIF_B(20)
        d.text((x + 10, by + 18), val, font=vf, fill=RED if i in (0, 5) else INK)
        d.text((x + 10, by + 42), note, font=F_SANS(9), fill=MUTED)

    # Three main stories.
    colw = 312
    gap = (CW - 3 * colw) // 2
    my = 220
    for i, m in enumerate(MAINS):
        x = MARGIN + i * (colw + gap)
        disc(d, x + 12, my + 10, m["n"], r=11)
        d.text((x + 30, my + 2), m["kicker"], font=F_SANS_B(11), fill=RED)
        kicker_bar(d, x, my + 20, colw, m["region"], m["kicker"])
        m["panel"](d, x, my + 44, colw, 96)
        hy = my + 148
        hy = text_block(d, x, hy, wrap(m["headline"], F_SERIF_B(19), colw),
                        F_SERIF_B(19), leading=22)
        hy = text_block(d, x, hy + 4, wrap(m["body"], F_SANS(12), colw),
                        F_SANS(12), leading=14)

    # Ten small cards, two rows of five.
    cw2, ch2, cg = 187, 82, 10
    cy = 480
    for idx, (n, region, head, body) in enumerate(CARDS):
        row, col = divmod(idx, 5)
        x = MARGIN + col * (cw2 + cg)
        y = cy + row * (ch2 + 10)
        d.rectangle([x, y, x + cw2, y + ch2], outline=RULE, width=1)
        disc(d, x + 11, y + 11, n, r=9)
        d.text((x + 24, y + 4), region, font=F_SANS_B(8), fill=REGION[region])
        ty = text_block(d, x + 8, y + 22,
                        wrap(head, F_SANS_B(11), cw2 - 16), F_SANS_B(11),
                        leading=13)
        text_block(d, x + 8, ty + 1,
                   wrap(body, F_SANS(9), cw2 - 16)[:2], F_SANS(9), leading=11)

    # Map (left) and briefs (right).
    my2 = 664
    world_map(d, MARGIN, my2, 596, 276, PINS)
    bx = MARGIN + 608
    bw = CW - 608
    d.rectangle([bx, my2, bx + bw, my2 + 276], outline=RULE, width=1)
    d.text((bx + 10, my2 + 8), "THE DAY IN BRIEF", font=F_SANS_B(12), fill=INK)
    hline(d, bx + 10, bx + bw - 10, my2 + 28, fill=RULE, width=1)
    yy = my2 + 36
    for n, txt in BRIEFS:
        disc(d, bx + 16, yy + 8, n, r=9)
        yy = text_block(d, bx + 30, yy,
                        wrap(txt, F_SANS(10), bw - 42), F_SANS(10), leading=13)
        yy += 6

    # Footer: date discipline.
    fy = 950
    hline(d, MARGIN, MARGIN + CW, fy, fill=RULE, width=2)
    foot = ("DATE CHECK — This page covers only what happened, or was first reported, "
            "on Friday 27 November 2026 in some time zone. The EU summit ended late "
            "Thu 26 Nov in Brussels and the ECB choice was announced Thu 26 Nov; both "
            "led Fri 27 Nov front pages, and the Kyiv overnight toll was updated Fri 27 Nov. "
            "Left out as other days' news: the Everest helicopter collision (Tue 3 Nov), "
            "the Cairo tanker fire (25 Nov) and the Macy's parade postponement (26 Nov).")
    text_block(d, MARGIN, fy + 6, wrap(foot, F_SANS(10), CW), F_SANS(10),
               fill=MUTED, leading=13)
    credit = "Drawn in code for make.fun news-image-20261127 · Sources: Reuters, AP, wire reports dated 27 Nov 2026 · All art original"
    cf = F_SANS_I(9)
    d.text((MARGIN, H - 22), credit, font=cf, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    draw()
