"""Build entry.png for news-image-20261123 (account 2, formula 3-6-24).

3 mega-heroes + 6 hero panels + 24 compact briefs = 33 verified stories
from Monday 23 November 2026, with a world map, a numbers strip, a
DATE CHECK bar and a footer. Flat-vector art drawn in code with PIL.
Deterministic: same input bytes give the same output bytes, no network.
Run: python3 build.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 16  # outer margin

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---- palette ---------------------------------------------------------
NAVY = (15, 42, 68)
NAVY2 = (23, 64, 102)
RED = (192, 57, 43)
PAPER = (255, 255, 255)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LINE = (200, 200, 200)
SEA = (197, 221, 239)
LAND = (207, 225, 189)
LAND_LINE = (104, 144, 104)
CREAM = (250, 246, 236)

REGION_COLOR = {
    "North America": (30, 111, 184),
    "Europe": (122, 79, 163),
    "Middle East": (192, 57, 43),
    "Africa": (217, 142, 0),
    "Asia-Pacific": (30, 138, 90),
    "Latin America": (224, 106, 0),
    "Global": (90, 90, 90),
}
REGION_SHORT = {
    "North America": "N. AMERICA",
    "Europe": "EUROPE",
    "Middle East": "M. EAST",
    "Africa": "AFRICA",
    "Asia-Pacific": "ASIA-PACIFIC",
    "Latin America": "LATIN AMERICA",
    "Global": "GLOBAL",
}

# ---- data: 33 stories (number, headline, region, status, source, lon, lat)
HEROES = [
    (1, "Nvidia brings back Jensen Huang as CEO \u2014 shares jump 31%",
     "North America", "CONFIRMED", "Reuters", -121.0, 37.4),
    (2, "COP31 climate talks collapse without a deal",
     "Global", "REPORTED", "Reuters / Al Jazeera", 30.7, 36.9),
    (3, "Ukraine sinks Russian corvette in Libya with sea drones",
     "Africa", "REPORTED", "Euronews / AFP", 20.1, 32.1),
]
PANELS = [
    (4, "Democrats win 258 House seats \u2014 largest majority since 1992",
     "North America", "CONFIRMED", "AP", -77.0, 38.9),
    (5, "CrowdStrike buys Zscaler in $44B all-stock deal",
     "North America", "CONFIRMED", "Reuters", -97.7, 30.3),
    (6, "US moves to recover $1B+ crypto from Binance hack",
     "North America", "CONFIRMED", "Reuters", -77.0, 38.9),
    (7, "Oregon and Virginia sue SpaceX over Grok deepfakes",
     "North America", "CONFIRMED", "AP", -123.0, 44.9),
    (8, "Palisades fire arsonist convicted by federal jury",
     "North America", "CONFIRMED", "AP", -118.2, 34.1),
    (9, "OpenAI chief scientist proposes shared AI safety limits",
     "North America", "REPORTED", "OpenAI", -122.4, 37.8),
]
BRIEFS = [
    (10, "EU proposes 22nd sanctions package on Russia", "Europe", 4.4, 50.8),
    (11, "Belgium strike grounds flights; 582 cancelled", "Europe", 4.4, 50.8),
    (12, "NATO pledges space defence after satellite reports", "Europe", 13.4, 52.5),
    (13, "Spain court clears Puigdemont to return from exile", "Europe", -3.7, 40.4),
    (14, "About 450 German schools receive bomb threats", "Europe", 7.9, 48.0),
    (15, "NHS opens AI breast screening trial EDITH", "Europe", 0.1, 52.2),
    (16, "US unveils sweeping Iran sanctions", "Middle East", 51.4, 35.7),
    (17, "Iran vows \u201cevery means\u201d against US naval blockade", "Middle East", 56.3, 26.6),
    (18, "Iran flogs singer Parastoo Ahmadi 74 times", "Middle East", 50.9, 34.6),
    (19, "Houthis claim attacks on Saudi oil refinery", "Middle East", 46.7, 24.7),
    (20, "Kenya and DR Congo restore ambassador ties", "Africa", 36.8, -1.3),
    (21, "African energy exporters gain extra $21.6B", "Africa", 7.5, 9.1),
    (22, "DR Congo halts cobalt exports from 30 Nov", "Africa", 15.3, -4.3),
    (23, "Sudan: drones top killer of civilians in 2026, UN says", "Africa", 32.5, 15.6),
    (24, "Asian chip stocks slide as Wall Street rout spreads", "Asia-Pacific", 127.0, 37.6),
    (25, "Thai court halves jail term of royal-insult lawmaker", "Asia-Pacific", 100.5, 13.8),
    (26, "Macquarie-led group buys EDOTCO towers for $1.2B", "Asia-Pacific", 101.7, 3.1),
    (27, "China sentences official to death for leaking secrets", "Asia-Pacific", 116.4, 39.9),
    (28, "Philippines ferry fire: 311 passengers rescued", "Asia-Pacific", 123.9, 10.3),
    (29, "Indonesia president to name VP candidates", "Asia-Pacific", 106.8, -6.2),
    (30, "Bangladesh: Hasina to be jailed if she returns", "Asia-Pacific", 90.4, 23.8),
    (31, "Panama: First Quantum accepts Cobre Panama terms", "Latin America", -79.5, 9.0),
    (32, "Bolsonaro rushed to ICU with bowel obstruction", "Latin America", -47.9, -15.8),
    (33, "49ers beat Vikings 35\u201310 in Mexico City", "Latin America", -99.1, 19.4),
]
NUMBERS = [
    ("258", "HOUSE SEATS, DEMOCRATS"),
    ("+31%", "NVIDIA SHARES"),
    ("$44B", "CROWDSTRIKE DEAL"),
    ("582", "FLIGHTS CANCELLED"),
    ("$21.6B", "AFRICAN ENERGY WINDFALL"),
    ("311", "FERRY PASSENGERS SAVED"),
]
REGION_COUNTS = [
    ("North America", 7), ("Europe", 6), ("Middle East", 4),
    ("Africa", 5), ("Asia-Pacific", 7), ("Latin America", 3), ("Global", 1),
]

# Detailed continent outlines as (lon, lat) polygons, drawn by hand from
# the real coastlines so each landmass reads at a glance: Alaska and the
# Hudson Bay notch, Florida and Baja, the Yucatan and Panama isthmus,
# Greenland, the Brazil bulge, Iberia, the Italy boot, Greece, Scandinavia,
# the UK and Ireland, the African horn and bulge, Madagascar, Arabia,
# India, the Malay peninsula, Indonesia, Japan, the Philippines,
# New Guinea, Australia, Tasmania and New Zealand.
CONTINENTS = [
    # North America (Bering Strait, down the Pacific coast, Panama,
    # up the Caribbean/Gulf/Atlantic coast, Hudson Bay notch, Arctic coast)
    [(-168, 66), (-161, 58), (-156, 58), (-150, 60), (-144, 60), (-140, 60),
     (-135, 57), (-130, 54), (-125, 49), (-124, 43), (-121, 36), (-117, 32),
     (-114, 29), (-110, 24), (-106, 21), (-100, 18), (-95, 16), (-90, 14),
     (-86, 12), (-83, 9), (-80, 8), (-78, 8), (-81, 10), (-84, 11),
     (-87, 14), (-88, 16), (-88, 19), (-91, 21), (-95, 24), (-97, 26),
     (-94, 29), (-90, 29), (-86, 30), (-83, 30), (-81, 26), (-80, 27),
     (-78, 30), (-76, 34), (-74, 38), (-73, 41), (-70, 42), (-68, 44),
     (-65, 44), (-60, 46), (-56, 47), (-55, 50), (-59, 53), (-63, 56),
     (-66, 58), (-70, 60), (-75, 62), (-78, 61), (-80, 57), (-83, 55),
     (-86, 55), (-89, 56), (-91, 59), (-94, 62), (-93, 66), (-90, 68),
     (-86, 68), (-82, 69), (-78, 69), (-74, 70), (-70, 70), (-65, 69),
     (-60, 68), (-58, 66), (-60, 64), (-65, 63), (-70, 65), (-75, 67),
     (-80, 68), (-85, 68), (-90, 68), (-95, 68), (-100, 68), (-105, 68),
     (-110, 68), (-115, 68), (-120, 69), (-125, 70), (-130, 69), (-135, 69),
     (-140, 70), (-145, 70), (-150, 71), (-155, 71), (-160, 70), (-165, 68),
     (-168, 66)],
    # Greenland
    [(-58, 64), (-52, 60), (-46, 60), (-41, 63), (-36, 66), (-30, 68),
     (-25, 70), (-20, 73), (-22, 77), (-28, 80), (-35, 80), (-45, 79),
     (-52, 77), (-56, 74), (-58, 70), (-58, 64)],
    # South America
    [(-80, 10), (-77, 5), (-80, -2), (-81, -5), (-78, -9), (-75, -14),
     (-72, -18), (-70, -23), (-70, -28), (-71, -33), (-73, -38), (-73, -44),
     (-74, -50), (-70, -54), (-66, -55), (-66, -49), (-63, -42), (-59, -36),
     (-55, -34), (-51, -30), (-48, -27), (-42, -23), (-39, -18), (-36, -11),
     (-35, -7), (-38, -4), (-42, -2), (-46, -1), (-50, 0), (-53, 4),
     (-57, 6), (-61, 9), (-66, 10), (-70, 12), (-75, 10), (-77, 8),
     (-80, 10)],
    # Europe (Iberia, Italy boot, Greece, Scandinavia, Black Sea coast)
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 49),
     (0, 51), (3, 53), (5, 53), (8, 55), (8, 57), (10, 59), (12, 57),
     (18, 56), (18, 54), (21, 55), (21, 57), (24, 58), (23, 60), (25, 60),
     (30, 62), (30, 65), (28, 67), (25, 69), (20, 70), (18, 69), (14, 67),
     (12, 65), (10, 63), (6, 61), (5, 58), (8, 58), (6, 55), (3, 52),
     (0, 50), (-2, 49), (-5, 48), (-2, 47), (-4, 44), (-2, 43), (0, 40),
     (3, 41), (7, 44), (10, 44), (12, 44), (14, 42), (16, 40), (16, 38),
     (18, 40), (19, 42), (21, 41), (23, 39), (23, 37), (26, 38), (26, 36),
     (28, 37), (30, 36), (27, 36), (23, 36), (21, 36), (18, 36), (15, 37),
     (12, 38), (10, 37), (8, 39), (5, 38), (2, 38), (0, 38), (-2, 37),
     (-6, 36), (-9, 37), (-10, 36)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 57), (0, 54), (1, 51),
     (-2, 50), (-5, 50)],
    # Ireland
    [(-10, 52), (-6, 52), (-6, 55), (-8, 55), (-10, 54), (-10, 52)],
    # Iceland
    [(-22, 64), (-18, 63), (-15, 64), (-16, 66), (-20, 66), (-22, 65),
     (-22, 64)],
    # Africa (west bulge, horn, southern taper)
    [(-6, 35), (-1, 35), (5, 37), (10, 37), (11, 34), (15, 32), (20, 32),
     (25, 32), (30, 31), (33, 30), (35, 28), (37, 24), (38, 20), (40, 15),
     (43, 11), (46, 11), (50, 12), (51, 11), (49, 7), (47, 3), (44, 0),
     (41, -3), (40, -8), (40, -13), (39, -18), (37, -23), (35, -27),
     (32, -29), (28, -33), (24, -34), (19, -35), (17, -32), (15, -27),
     (13, -20), (12, -14), (12, -8), (13, -4), (12, 0), (10, 3), (7, 4),
     (3, 5), (-2, 5), (-7, 4), (-11, 6), (-14, 8), (-17, 12), (-17, 15),
     (-16, 20), (-15, 24), (-14, 27), (-11, 30), (-8, 32), (-6, 35)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -20), (48, -23), (45, -25),
     (43, -23), (43, -19), (44, -16)],
    # Asia (Siberia, Pacific coast, Malay peninsula, India, Arabia, Levant)
    [(28, 41), (30, 43), (33, 44), (36, 45), (39, 46), (42, 45), (46, 44),
     (49, 45), (52, 46), (55, 47), (58, 48), (62, 48), (66, 50), (70, 52),
     (74, 54), (78, 57), (81, 60), (84, 63), (88, 66), (92, 68), (96, 70),
     (100, 72), (104, 73), (108, 74), (112, 73), (116, 73), (120, 73),
     (125, 72), (130, 72), (135, 72), (140, 72), (145, 71), (150, 70),
     (155, 69), (160, 67), (163, 65), (168, 66), (173, 66), (178, 65),
     (178, 62), (173, 60), (168, 60), (162, 58), (158, 54), (155, 50),
     (151, 47), (146, 44), (142, 42), (140, 38), (137, 35), (134, 34),
     (131, 33), (128, 31), (125, 30), (122, 29), (120, 26), (118, 24),
     (114, 22), (111, 21), (109, 19), (108, 15), (107, 11), (105, 9),
     (103, 8), (101, 7), (99, 9), (98, 12), (96, 15), (93, 18), (91, 21),
     (89, 22), (87, 21), (84, 19), (81, 16), (80, 12), (79, 9), (77, 8),
     (76, 10), (74, 13), (73, 17), (72, 20), (70, 22), (67, 23), (65, 25),
     (62, 25), (59, 25), (57, 26), (55, 27), (53, 27), (51, 28), (49, 29),
     (48, 30), (46, 30), (43, 30), (41, 31), (39, 33), (37, 35), (35, 36),
     (33, 36), (31, 36), (29, 37), (28, 39), (28, 41)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (139, 37),
     (140, 38), (141, 40), (141, 42), (143, 42), (142, 44), (140, 43),
     (139, 40), (137, 37), (135, 35), (133, 34), (131, 33), (130, 31)],
    # Philippines
    [(120, 18), (122, 18), (122, 15), (124, 13), (126, 11), (125, 9),
     (123, 8), (122, 10), (121, 13), (120, 16), (120, 18)],
    # Sumatra
    [(95, 5), (97, 4), (99, 2), (101, 0), (103, -2), (105, -4), (106, -6),
     (104, -5), (102, -3), (100, -1), (98, 1), (96, 3), (95, 5)],
    # Java
    [(105, -6), (108, -7), (111, -7), (114, -8), (114, -9), (111, -8),
     (108, -8), (105, -7), (105, -6)],
    # Borneo
    [(109, 1), (111, 2), (114, 4), (117, 5), (119, 2), (118, -1), (116, -3),
     (114, -4), (111, -3), (109, -1), (109, 1)],
    # Sulawesi
    [(119, 0), (121, 1), (123, 0), (122, -2), (120, -3), (119, -2),
     (119, 0)],
    # New Guinea
    [(131, -1), (134, -2), (137, -2), (140, -3), (143, -4), (146, -6),
     (148, -8), (150, -9), (147, -9), (144, -8), (141, -8), (138, -8),
     (135, -6), (132, -3), (131, -1)],
    # Sri Lanka
    [(80, 9), (81, 8), (81, 6), (80, 6), (80, 9)],
    # Taiwan
    [(120, 23), (121, 24), (122, 25), (121, 23), (120, 23)],
    # Cuba
    [(-85, 22), (-82, 23), (-79, 22), (-76, 21), (-74, 20), (-77, 21),
     (-80, 22), (-84, 23), (-85, 22)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (117, -35), (121, -34), (125, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (143, -38),
     (146, -39), (149, -37), (151, -35), (153, -31), (153, -27), (152, -24),
     (150, -22), (147, -19), (144, -16), (142, -14), (142, -11), (139, -12),
     (136, -13), (135, -15), (132, -12), (130, -13), (127, -14), (124, -15),
     (121, -17), (118, -20), (115, -21), (113, -22)],
    # Tasmania
    [(145, -41), (147, -41), (148, -42), (147, -43), (145, -43), (145, -41)],
    # New Zealand (North Island)
    [(173, -35), (175, -37), (177, -38), (178, -38), (177, -39), (175, -40),
     (174, -41), (173, -39), (173, -36), (173, -35)],
    # New Zealand (South Island)
    [(167, -45), (169, -44), (171, -43), (173, -42), (174, -41), (172, -41),
     (170, -43), (168, -44), (167, -46), (167, -45)],
]


# ---- text helpers ----------------------------------------------------
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, fnt, max_w, ell="\u2026"):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + ell, font=fnt) > max_w:
        text = text[:-1]
    return text + ell


def chip(draw, x, y, text, fnt, fg, bg):
    """Small rounded tag; returns width used."""
    w = int(draw.textlength(text, font=fnt)) + 12
    h = 18
    draw.rounded_rectangle([x, y, x + w, y + h], radius=9, fill=bg)
    draw.text((x + 6, y + 3), text, font=fnt, fill=fg)
    return w


def num_badge(draw, cx, cy, n, r, fill, fnt):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                 outline=(255, 255, 255), width=2)
    t = str(n)
    tw = draw.textlength(t, font=fnt)
    th = fnt.size
    draw.text((cx - tw / 2, cy - th / 2 - 1), t, font=fnt, fill=(255, 255, 255))


# ---- flat-vector hero art -------------------------------------------
def art_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 244, 234))
    # rising bars + chart line
    base = y + h - 16
    bw, gap = 34, 14
    heights = [18, 30, 26, 44, 58]
    bx = x + 18
    pts = []
    for i, hh in enumerate(heights):
        d.rectangle([bx, base - hh, bx + bw, base],
                    fill=(46, 160, 67) if i % 2 == 0 else (110, 200, 130))
        pts.append((bx + bw / 2, base - hh - 6))
        bx += bw + gap
    d.line(pts, fill=(20, 110, 50), width=4)
    d.text((x + 240, y + 8), "+31%", font=font(SANS_B, 28),
           fill=(20, 110, 50))


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(253, 236, 234))
    cx, cy, r = x + 105, y + h / 2 + 2, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(191, 224, 242),
              outline=NAVY2, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=NAVY2,
              width=2)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY2, width=2)
    d.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], 0, 360, fill=NAVY2,
          width=2)
    # red slash over the globe
    d.line([cx - r - 6, cy + r + 6, cx + r + 6, cy - r - 6], fill=RED, width=6)
    d.text((x + 168, y + 18), "NO", font=font(SANS_B, 40), fill=RED)
    d.text((x + 168, y + 60), "DEAL", font=font(SANS_B, 40), fill=RED)


def art_benghazi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # waves
    for k, wy in enumerate((y + h - 34, y + h - 22, y + h - 12)):
        pts = []
        for i in range(13):
            px = x + i * (w / 12)
            py = wy + (6 if i % 2 == 0 else -6)
            pts.append((px, py))
        d.line(pts, fill=(90, 160, 210) if k < 2 else (30, 111, 184), width=3)
    # ship hull + superstructure
    hx, hy = x + 60, y + h - 44
    d.polygon([(hx, hy), (hx + 170, hy), (hx + 150, hy + 18), (hx + 14, hy + 18)],
              fill=(40, 40, 40))
    d.rectangle([hx + 40, hy - 22, hx + 110, hy], fill=(70, 70, 70))
    d.rectangle([hx + 62, hy - 36, hx + 88, hy - 22], fill=(90, 90, 90))
    d.line([hx + 75, hy - 52, hx + 75, hy - 36], fill=(40, 40, 40), width=3)
    d.polygon([(hx + 75, hy - 52), (hx + 95, hy - 46), (hx + 75, hy - 40)],
              fill=RED)
    # drone above the ship
    dx, dy = x + w - 70, y + 26
    d.ellipse([dx - 8, dy - 6, dx + 8, dy + 6], fill=(30, 30, 30))
    for sx in (-16, 16):
        d.line([dx + sx - 10, dy - 8, dx + sx + 10, dy - 8], fill=(30, 30, 30),
               width=3)
        d.ellipse([dx + sx - 4, dy - 12, dx + sx + 4, dy - 4], fill=(90, 90, 90))
    d.line([dx, dy + 6, dx, dy + 16], fill=(30, 30, 30), width=2)
    d.text((x + w - 118, y + h - 30), "SEA DRONES", font=font(SANS_B, 15),
           fill=NAVY2)


HERO_ART = {1: art_nvidia, 2: art_cop31, 3: art_benghazi}


# ---- flat-vector panel icons ----------------------------------------
def icon_ballot(d, x, y, s):
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=(30, 111, 184))
    d.rectangle([x + 14, y + 26, x + s - 14, y + s - 12], fill=(255, 255, 255))
    d.rectangle([x + 22, y + 18, x + s - 22, y + 26], fill=(255, 255, 255))
    d.line([x + 20, y + 42, x + 28, y + 50, x + 44, y + 32], fill=RED, width=4)


def icon_shield(d, x, y, s):
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=(30, 111, 184))
    cx, cy = x + s / 2, y + s / 2 - 2
    d.polygon([(cx, cy - 20), (cx + 16, cy - 12), (cx + 16, cy + 6),
               (cx, cy + 20), (cx - 16, cy + 6), (cx - 16, cy - 12)],
              fill=(255, 255, 255))
    d.polygon([(cx + 3, cy - 10), (cx - 5, cy + 2), (cx + 1, cy + 2),
               (cx - 3, cy + 12), (cx + 6, cy - 2), (cx, cy - 2)],
              fill=(30, 111, 184))


def icon_coin(d, x, y, s):
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=(30, 111, 184))
    cx, cy = x + s / 2, y + s / 2
    d.ellipse([cx - 19, cy - 19, cx + 19, cy + 19], fill=(255, 200, 60),
              outline=(255, 255, 255), width=2)
    d.text((cx - 7, cy - 13), "$", font=font(SANS_B, 24), fill=(120, 80, 0))


def icon_gavel(d, x, y, s):
    # scales of justice (lawsuit)
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=(30, 111, 184))
    cx = x + s / 2
    d.line([cx, y + 10, cx, y + 50], fill=(255, 255, 255), width=3)
    d.line([x + 12, y + 16, x + s - 12, y + 16], fill=(255, 255, 255), width=3)
    for sx in (x + 12, x + s - 12):
        d.line([sx, y + 16, sx, y + 28], fill=(255, 255, 255), width=2)
        d.polygon([(sx - 8, y + 28), (sx + 8, y + 28), (sx, y + 40)],
                  fill=(255, 200, 60))
    d.rectangle([x + 20, y + 50, x + s - 20, y + 54], fill=(255, 255, 255))


def icon_flame(d, x, y, s):
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=(30, 111, 184))
    cx, cy = x + s / 2, y + s / 2 + 4
    d.polygon([(cx, cy - 24), (cx + 14, cy - 2), (cx + 10, cy + 16),
               (cx - 10, cy + 16), (cx - 14, cy - 2)], fill=(255, 120, 40))
    d.polygon([(cx, cy - 8), (cx + 7, cy + 4), (cx + 5, cy + 14),
               (cx - 5, cy + 14), (cx - 7, cy + 4)], fill=(255, 200, 60))


def icon_robot(d, x, y, s):
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=(30, 111, 184))
    d.line([x + 32, y + 12, x + 32, y + 20], fill=(255, 255, 255), width=3)
    d.ellipse([x + 28, y + 8, x + 36, y + 16], fill=(255, 200, 60))
    d.rounded_rectangle([x + 14, y + 20, x + 50, y + 46], radius=6,
                        fill=(255, 255, 255))
    d.ellipse([x + 21, y + 28, x + 27, y + 34], fill=NAVY)
    d.ellipse([x + 37, y + 28, x + 43, y + 34], fill=NAVY)
    d.line([x + 24, y + 40, x + 40, y + 40], fill=NAVY, width=2)


PANEL_ICON = {4: icon_ballot, 5: icon_shield, 6: icon_coin,
              7: icon_gavel, 8: icon_flame, 9: icon_robot}


# ---- sections --------------------------------------------------------
def draw_header(d):
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.text((MX, 8), "THE WORLD IN ONE DAY", font=font(SERIF_B, 38),
           fill=(255, 255, 255))
    d.text((MX, 52), "3 MEGA-HEROES  \u2022  6 PANELS  \u2022  24 BRIEFS",
           font=font(SANS_B, 13), fill=(174, 214, 241))
    d.text((W - MX, 10), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 20),
           fill=(255, 255, 255), anchor="ra")
    d.text((W - MX, 40), "33 STORIES  \u2022  7 REGIONS  \u2022  ONE PICTURE",
           font=font(SANS_B, 13), fill=(174, 214, 241), anchor="ra")


def draw_utc_strip(d):
    y0, y1 = 76, 106
    d.rectangle([0, y0, W, y1], fill=(255, 255, 255))
    d.line([0, y1, W, y1], fill=LINE, width=1)
    d.text((MX, y0 + 8), "THE DAY IN UTC", font=font(SANS_B, 13), fill=NAVY)
    x0, x1, by = 172, W - MX, y0 + 9
    seg_w = (x1 - x0) / 3
    cols = [(214, 234, 248), (174, 214, 241), (127, 179, 213)]
    labels = ["MORNING", "AFTERNOON", "EVENING"]
    for i in range(3):
        sx = x0 + i * seg_w
        d.rectangle([sx, by, sx + seg_w - 2, by + 13], fill=cols[i])
        tw = d.textlength(labels[i], font=font(SANS_B, 11))
        d.text((sx + (seg_w - 2 - tw) / 2, by + 1), labels[i],
               font=font(SANS_B, 11), fill=NAVY)
    # segment labels sit inside the bar; no per-event times are shown.


def draw_heroes(d):
    y, cw, chh = 106, 326, 216
    for i, (n, head, region, status, src, _lon, _lat) in enumerate(HEROES):
        x = MX + i * (cw + 7)
        d.rectangle([x, y, x + cw, y + chh], fill=(255, 255, 255),
                    outline=LINE, width=1)
        HERO_ART[n](d, x + 1, y + 1, cw - 2, 96)
        num_badge(d, x + 20, y + 20, n, 14, NAVY, font(SANS_B, 16))
        lines = wrap(d, head, font(SERIF_B, 18), cw - 24)[:3]
        ly = y + 106
        for ln in lines:
            d.text((x + 12, ly), ln, font=font(SERIF_B, 18), fill=INK)
            ly += 22
        cy = y + chh - 40
        w1 = chip(d, x + 12, cy, REGION_SHORT[region], font(SANS_B, 11),
                  (255, 255, 255), REGION_COLOR[region])
        chip(d, x + 12 + w1 + 6, cy, status, font(SANS_B, 11),
             (255, 255, 255), (30, 138, 90) if status == "CONFIRMED"
             else (217, 142, 0))
        d.text((x + 12, y + chh - 19), "Source: " + src,
               font=font(SANS, 11), fill=GREY)


def draw_panels(d):
    d.text((MX, 324), "SIX MORE THAT MOVED THE DAY", font=font(SANS_B, 15),
           fill=RED)
    d.line([MX + 268, 332, W - MX, 332], fill=RED, width=2)
    cw, chh = 326, 88
    for i, (n, head, region, status, src, _lon, _lat) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x = MX + col * (cw + 7)
        y = 340 + row * (chh + 2)
        d.rectangle([x, y, x + cw, y + chh], fill=(255, 255, 255),
                    outline=LINE, width=1)
        PANEL_ICON[n](d, x + 8, y + 12, 64)
        lines = wrap(d, head, font(SANS_B, 15), cw - 96)[:2]
        ly = y + 9
        for ln in lines:
            d.text((x + 80, ly), ln, font=font(SANS_B, 15), fill=INK)
            ly += 19
        cy = y + 50
        w1 = chip(d, x + 80, cy, REGION_SHORT[region], font(SANS_B, 10),
                  (255, 255, 255), REGION_COLOR[region])
        chip(d, x + 80 + w1 + 5, cy, status, font(SANS_B, 10),
             (255, 255, 255), (30, 138, 90) if status == "CONFIRMED"
             else (217, 142, 0))
        d.text((x + 80, y + 71), "Source: " + src, font=font(SANS, 10),
               fill=GREY)


# ---- briefs, map, numbers, footer ------------------------------------
def draw_briefs(d):
    d.text((MX, 522), "24 MORE IN BRIEF \u2014 THE REST OF THE DAY",
           font=font(SANS_B, 15), fill=RED)
    d.line([MX + 330, 530, W - MX, 530], fill=RED, width=2)
    cols = [(MX, 488), (520, 488)]
    for ci, (cx, cw) in enumerate(cols):
        for ri in range(12):
            n, head, _region, _lon, _lat = BRIEFS[ci * 12 + ri]
            y = 544 + ri * 18
            d.text((cx, y), str(n) + ".", font=font(SANS_B, 12), fill=NAVY)
            d.text((cx + 28, y), trunc(d, head, font(SANS, 12), cw - 28),
                   font=font(SANS, 12), fill=INK)


OFFSETS = {6: (13, -10), 11: (16, 10), 15: (-14, -10), 14: (18, -4),
           12: (-16, -10), 9: (-16, -12), 8: (14, 12), 18: (13, 9),
           26: (12, 10), 29: (-10, 14), 33: (-14, 10)}


def draw_map(d):
    d.text((MX, 762), "WHERE IT HAPPENED \u2014 33 STORIES PINNED",
           font=font(SANS_B, 15), fill=NAVY)
    d.line([MX + 340, 770, W - MX, 770], fill=NAVY, width=2)
    mx0, my0, mw, mh = MX, 782, 684, 140
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=SEA, outline=LINE,
                width=1)

    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw,
                my0 + (85 - lat) / 145 * mh)

    for lon in range(-180, 181, 30):
        x, _ = proj(lon, 85)
        d.line([x, my0, x, my0 + mh], fill=(178, 208, 226), width=1)
    for lat in (-60, -30, 0, 30, 60):
        _, y = proj(0, lat)
        d.line([mx0, y, mx0 + mw, y], fill=(178, 208, 226), width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE, width=2)
    # ocean labels (empty water, clear of every dot)
    ocean = (110, 135, 160)
    for olon, olat, name in ((-155, -28, "PACIFIC OCEAN"),
                             (-30, -35, "ATLANTIC OCEAN"),
                             (80, -40, "INDIAN OCEAN")):
        ox, oy = proj(olon, olat)
        d.text((ox, oy), name, font=font(SANS_B, 10), fill=ocean,
               anchor="mm")
    all_stories = ([(n, region, lon, lat)
                    for n, _h, region, _s, _src, lon, lat in HEROES + PANELS]
                   + [(n, region, lon, lat)
                      for n, _h, region, lon, lat in BRIEFS])
    for n, region, lon, lat in all_stories:
        tx, ty = proj(lon, lat)
        dx, dy = OFFSETS.get(n, (0, 0))
        cx, cy = tx + dx, ty + dy
        if (dx, dy) != (0, 0):
            d.line([tx, ty, cx, cy], fill=GREY, width=1)
        r = 8
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=REGION_COLOR[region], outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=font(SANS_B, 9))
        d.text((cx - tw / 2, cy - 5), t, font=font(SANS_B, 9),
               fill=(255, 255, 255))
    # legend: region counts in two columns
    lx = 712
    d.text((lx, 784), "STORIES BY REGION", font=font(SANS_B, 12), fill=NAVY)
    for i, (region, cnt) in enumerate(REGION_COUNTS):
        col = i // 4
        row = i % 4
        x = lx + col * 150
        y = 806 + row * 19
        d.rectangle([x, y + 1, x + 12, y + 13], fill=REGION_COLOR[region])
        d.text((x + 17, y), "%s \u2014 %d" % (region, cnt),
               font=font(SANS, 12), fill=INK)
    note = ("Dots numbered as in the lists above. #4/#6, #10/#11, "
            "#1/#8/#9, #16/#18, #33 offset slightly.")
    ly = 890
    for ln in wrap(d, note, font(SANS, 11), W - MX - lx):
        d.text((lx, ly), ln, font=font(SANS, 11), fill=GREY)
        ly += 14


def draw_numbers(d):
    y0, y1 = 928, 970
    d.rectangle([0, y0, W, y1], fill=CREAM)
    d.line([0, y0, W, y0], fill=LINE, width=1)
    d.text((MX + 4, y0 + 5), "THE DAY", font=font(SANS_B, 14), fill=RED)
    d.text((MX + 4, y0 + 22), "IN NUMBERS", font=font(SANS_B, 14), fill=RED)
    x0 = 172
    cw = (W - MX - x0) / 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = x0 + i * cw + cw / 2
        d.text((cx, y0 + 2), num, font=font(SANS_B, 22), fill=NAVY,
               anchor="ma")
        d.text((cx, y0 + 27), cap, font=font(SANS, 9), fill=GREY, anchor="ma")
        if i:
            d.line([x0 + i * cw, y0 + 6, x0 + i * cw, y1 - 6], fill=LINE,
                   width=1)


def draw_footer(d):
    d.line([0, 972, W, 972], fill=LINE, width=1)
    d.text((MX, 977), "DATE CHECK \u2014 Left out: \u201cEl Chapo Isidro\u201d "
           "(21 Nov); APEC ends (19 Nov); Anthropic IPO (19 Nov); "
           "N. Korea threat (24 Nov). Not yet verified: Nepal pledge.",
           font=font(SANS, 11), fill=INK)
    d.text((MX, 992), "Every story above happened or was first reported on "
           "Monday 23 November 2026. CONFIRMED = event on 23 Nov; "
           "REPORTED = first reported 23 Nov.",
           font=font(SANS, 11), fill=INK)
    d.text((MX, 1007), "Sources: Reuters, AP, AFP, Al Jazeera, BBC, "
           "Bloomberg, Bild, NHS, US Treasury, CREA, UN OHCHR, OkayAfrica. "
           "Flat-vector art drawn in code \u2014 no AI photos.",
           font=font(SANS, 10), fill=GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_utc_strip(d)
    draw_heroes(d)
    draw_panels(d)
    draw_briefs(d)
    draw_map(d)
    draw_numbers(d)
    draw_footer(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    return out


if __name__ == "__main__":
    print(build())
