#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up 19 November 2026.
Written from scratch for the make.fun news-image-20261119 bounty."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (26, 26, 26)
RED = (176, 30, 36)
BLUE = (31, 78, 121)
GOLD = (176, 132, 32)
GREY = (110, 108, 100)
CARD = (255, 253, 248)
RULE = (60, 58, 52)

F = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SERIF = "NotoSerif-Regular.ttf"
SANS_BLACK = "NotoSans-Black.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS = "NotoSans-Regular.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]


def fit_font(draw, s, name, size, max_w):
    f = font(name, size)
    while size > 10 and text_w(draw, s, f) > max_w:
        size -= 1
        f = font(name, size)
    return f


def wrap(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, s, f, x, y, max_w, leading, color, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=color)
        y += leading
    return y


def center(draw, s, f, cx, y, color):
    w = text_w(draw, s, f)
    draw.text((cx - w / 2, y), s, font=f, fill=color)
    return y + f.size


# ---- outer border ----
d.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=2)
d.rectangle([20, 20, W - 21, H - 21], outline=RULE, width=1)

MX = 44          # margin x
CW = W - 2 * MX  # content width

# ---- masthead ----
y = 34
f_title = fit_font(d, "THE WORLD IN ONE PICTURE", SERIF_BLACK, 62, CW)
center(d, "THE WORLD IN ONE PICTURE", f_title, W // 2, y, INK)
y += f_title.size + 12
d.line([(MX, y), (W - MX, y)], fill=RULE, width=3)
y += 10
f_date = font(SANS_BLACK, 30)
center(d, "THURSDAY, 19 NOVEMBER 2026", f_date, W // 2, y, RED)
y += 44
d.line([(MX, y), (W - MX, y)], fill=RULE, width=1)
d.line([(MX, y + 4), (W - MX, y + 4)], fill=RULE, width=1)
y += 14

# ---- lead story ----
lead_y = y
lead_h = 252
d.rectangle([MX, lead_y, W - MX, lead_y + lead_h], outline=RULE, width=1)
# illustration panel on the right
ill_x = W - MX - 330
d.rectangle([ill_x, lead_y, W - MX, lead_y + lead_h], fill=(233, 226, 210))
# skyline silhouettes
for bx, bw, bh in [(0, 46, 96), (52, 34, 130), (92, 58, 78), (156, 30, 118),
                   (192, 52, 88), (250, 40, 140), (296, 34, 100)]:
    d.rectangle([ill_x + bx, lead_y + lead_h - 66 - bh,
                 ill_x + bx + bw, lead_y + lead_h - 66], fill=(150, 142, 122))
# ground
d.rectangle([ill_x, lead_y + lead_h - 66, W - MX, lead_y + lead_h], fill=(196, 186, 162))
# round table
tx = ill_x + 165
d.ellipse([tx - 78, lead_y + lead_h - 58, tx + 78, lead_y + lead_h - 34],
          fill=(122, 74, 52))
d.rectangle([tx - 8, lead_y + lead_h - 44, tx + 8, lead_y + lead_h - 8],
            fill=(96, 58, 40))
# three chairs / figures (simple heads + shoulders)
for cx, col in [(tx - 62, (31, 78, 121)), (tx, (176, 30, 36)), (tx + 62, (31, 78, 121))]:
    d.ellipse([cx - 13, lead_y + lead_h - 118, cx + 13, lead_y + lead_h - 92], fill=col)
    d.pieslice([cx - 20, lead_y + lead_h - 96, cx + 20, lead_y + lead_h - 58],
               180, 360, fill=col)
# flags above the table: US, China, Russia (stylised stripes)
def flag(x0, y0, w, h, stripes):
    for i, c in enumerate(stripes):
        d.rectangle([x0, y0 + i * h // len(stripes), x0 + w,
                     y0 + (i + 1) * h // len(stripes)], fill=c)

flag(ill_x + 18, lead_y + 22, 84, 46,
     [(176, 30, 36), (248, 244, 236), (176, 30, 36), (248, 244, 236),
      (176, 30, 36), (248, 244, 236), (176, 30, 36)])
d.rectangle([ill_x + 18, lead_y + 22, ill_x + 18 + 34, lead_y + 22 + 24],
            fill=(31, 78, 121))
flag(ill_x + 123, lead_y + 22, 84, 46, [(222, 41, 16)] * 1)
# five-point star drawn as a polygon (no glyph dependency)
_scx, _scy, _r1, _r2 = ill_x + 140, lead_y + 34, 13, 5
_pts = []
for _i in range(10):
    _ang = -math.pi / 2 + _i * math.pi / 5
    _r = _r1 if _i % 2 == 0 else _r2
    _pts.append((_scx + _r * math.cos(_ang), _scy + _r * math.sin(_ang)))
d.polygon(_pts, fill=(255, 222, 89))
flag(ill_x + 228, lead_y + 22, 84, 46,
     [(248, 244, 236), (31, 78, 121), (176, 30, 36)])

# lead text (left side)
tx0 = MX + 18
tw = ill_x - tx0 - 16
ly = lead_y + 14
f_kick = font(SANS_BLACK, 17)
d.text((tx0, ly), "THE LEAD  ·  SHENZHEN, CHINA", font=f_kick, fill=RED)
ly += 28
f_head = fit_font(d, "TRUMP, XI AND PUTIN", SERIF_BLACK, 40, tw)
d.text((tx0, ly), "TRUMP, XI AND PUTIN", font=f_head, fill=INK)
ly += f_head.size + 2
f_head2 = fit_font(d, "MEET AT APEC", SERIF_BLACK, 40, tw)
d.text((tx0, ly), "MEET AT APEC", font=f_head2, fill=INK)
ly += f_head2.size + 10
f_sub = font(SANS_BOLD, 19)
ly = draw_wrapped(d, "First trilateral summit of the three leaders opens in Shenzhen.",
                  f_sub, tx0, ly, tw, 24, INK, max_lines=2)
ly += 6
f_body = font(SERIF, 17)
draw_wrapped(d, "Trade, security and Ukraine top the agenda as the world's three most powerful leaders sit down together.",
             f_body, tx0, ly, tw, 22, (70, 68, 60), max_lines=3)

# ---- cards grid: 3 cols x 2 rows ----
grid_y = lead_y + lead_h + 16
gw = (CW - 2 * 14) // 3
gh = 178
cards = [
    ("CULTURE · GAMES", RED, "GTA VI IS HERE",
     "After a 13-year wait, gamers step back into Vice City as the global rollout begins.", "game"),
    ("MIDDLE EAST", BLUE, "U.S. AND IRAN EXCHANGE FIRE AGAIN",
     "Tehran widens attacks to Gulf states; Kuwait and Bahrain hit.", "fire"),
    ("WASHINGTON", BLUE, "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
     "Democrats nominate Hakeem Jeffries to lead the House.", "capitol"),
    ("TECH · MARKETS", GOLD, "HUANG OUT AT NVIDIA",
     "Chipmaker halts H-chip sales to China; acting chief Colette Kress promises earlier pay rises.", "chip"),
    ("WEATHER", BLUE, "CYCLONE AKVAN NEARS INDIA",
     "Landfall expected between Machilipatnam and Puri on the east coast.", "storm"),
    ("SPACE", GOLD, "VOYAGER 1: ONE LIGHT-DAY OUT",
     "NASA to confirm today — the farthest human object ever, a light-day from Earth.", "sat"),
]


def icon(kind, x, y, s, col):
    if kind == "game":
        d.rounded_rectangle([x, y + s * 0.25, x + s, y + s * 0.75], radius=8, fill=col)
        d.ellipse([x + s * 0.18, y + s * 0.42, x + s * 0.34, y + s * 0.58], fill=PAPER)
        d.ellipse([x + s * 0.66, y + s * 0.42, x + s * 0.82, y + s * 0.58], fill=PAPER)
    elif kind == "fire":
        d.polygon([(x + s * 0.5, y), (x + s * 0.9, y + s * 0.55), (x + s * 0.72, y + s * 0.55),
                   (x + s * 0.85, y + s * 0.8), (x + s * 0.5, y + s), (x + s * 0.15, y + s * 0.8),
                   (x + s * 0.28, y + s * 0.55), (x + s * 0.1, y + s * 0.55)], fill=col)
    elif kind == "capitol":
        d.rectangle([x, y + s * 0.75, x + s, y + s * 0.9], fill=col)
        d.rectangle([x + s * 0.15, y + s * 0.6, x + s * 0.85, y + s * 0.75], fill=col)
        d.pieslice([x + s * 0.3, y + s * 0.15, x + s * 0.7, y + s * 0.65], 180, 360, fill=col)
        d.rectangle([x + s * 0.48, y, x + s * 0.52, y + s * 0.2], fill=col)
    elif kind == "chip":
        d.rectangle([x + s * 0.15, y + s * 0.15, x + s * 0.85, y + s * 0.85], fill=col)
        d.rectangle([x + s * 0.35, y + s * 0.35, x + s * 0.65, y + s * 0.65], fill=PAPER)
        for i in range(3):
            d.line([(x + s * (0.25 + i * 0.25), y), (x + s * (0.25 + i * 0.25), y + s * 0.15)], fill=col, width=3)
            d.line([(x + s * (0.25 + i * 0.25), y + s * 0.85), (x + s * (0.25 + i * 0.25), y + s)], fill=col, width=3)
            d.line([(x, y + s * (0.25 + i * 0.25)), (x + s * 0.15, y + s * (0.25 + i * 0.25))], fill=col, width=3)
            d.line([(x + s * 0.85, y + s * (0.25 + i * 0.25)), (x + s, y + s * (0.25 + i * 0.25))], fill=col, width=3)
    elif kind == "storm":
        cx, cy = x + s / 2, y + s / 2
        for r in range(4, int(s * 0.5), 4):
            a0 = r * 1.4
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 220, fill=col, width=3)
    elif kind == "sat":
        d.rectangle([x + s * 0.1, y + s * 0.4, x + s * 0.35, y + s * 0.6], fill=col)
        d.rectangle([x + s * 0.65, y + s * 0.4, x + s * 0.9, y + s * 0.6], fill=col)
        d.ellipse([x + s * 0.35, y + s * 0.3, x + s * 0.65, y + s * 0.7], fill=col)
        d.line([(x + s * 0.65, y + s * 0.3), (x + s * 0.95, y)], fill=col, width=3)


for i, (kick, col, head, sub, kind) in enumerate(cards):
    r, c = divmod(i, 3)
    x0 = MX + c * (gw + 14)
    y0 = grid_y + r * (gh + 14)
    d.rectangle([x0, y0, x0 + gw, y0 + gh], fill=CARD, outline=RULE, width=1)
    d.rectangle([x0, y0, x0 + gw, y0 + 4], fill=col)
    cx = x0 + 14
    cy = y0 + 14
    d.text((cx, cy), kick, font=font(SANS_BLACK, 14), fill=col)
    icon(kind, x0 + gw - 46, cy - 4, 32, col)
    hy = cy + 24
    f_ch = font(SANS_BLACK, 21)
    # shrink headline font until wrapped headline fits 3 lines
    size = 21
    while size > 14:
        f_ch = font(SANS_BLACK, size)
        if len(wrap(d, head, f_ch, gw - 28)) <= 3:
            break
        size -= 1
    hy = draw_wrapped(d, head, f_ch, cx, hy, gw - 28, size + 5, INK, max_lines=3)
    f_cs = font(SANS, 15)
    draw_wrapped(d, sub, f_cs, cx, hy + 6, gw - 28, 19, (70, 68, 60), max_lines=3)

# ---- ALSO TODAY strip ----
strip_y = grid_y + 2 * gh + 14 + 14
d.rectangle([MX, strip_y, W - MX, strip_y + 108], fill=(233, 226, 210), outline=RULE, width=1)
d.text((MX + 16, strip_y + 10), "ALSO TODAY", font=font(SANS_BLACK, 17), fill=RED)
also = [
    ("EUROPE", "EU proposes a €45bn loan to Ukraine."),
    ("ASIA", "North Korea fires missiles after a U.S.–South Korea drill."),
    ("FINLAND", "World's first nuclear waste store opens."),
]
col_w = (CW - 32) // 3
for i, (k, t) in enumerate(also):
    ax = MX + 16 + i * col_w
    d.text((ax, strip_y + 36), k, font=font(SANS_BLACK, 13), fill=BLUE)
    draw_wrapped(d, t, font(SANS, 15), ax, strip_y + 56, col_w - 16, 19, INK, max_lines=2)

# ---- footer ----
fy = strip_y + 108 + 12
d.line([(MX, fy), (W - MX, fy)], fill=RULE, width=1)
fy += 10
f_foot = font(SANS_BOLD, 15)
center(d, "THURSDAY 19 NOVEMBER 2026  ·  THE WORLD IN ONE PICTURE  ·  make.fun",
       f_foot, W // 2, fy, GREY)

img.save("entry.png", optimize=True)
print("saved", img.size)
