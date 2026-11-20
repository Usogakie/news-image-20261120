#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster (1024x1024 PNG).

News researched from live sources on 20 Nov 2026 (One Turn day page,
Just Security Early Edition, Morning Briefing, Bangladesh Chronicle):
  - ICJ rules Myanmar committed genocide against the Rohingya (9-6),
    the court's first such finding against a state.
  - Trump, Xi and Putin hold their first three-way summit in Shenzhen
    and issue a joint peace declaration; ~70 minutes, no breakthrough
    on Ukraine, Iran or nuclear arms.
  - Russian overnight strikes hit Kyiv bridges, killing 8; Ukraine's
    allies meet in Berlin and say Europe is ready to talk with Russia.
  - Houthi missile damages the PIF Tower in Riyadh's financial district.
  - Markets slide: S&P 500 down ~2% for a fifth straight day,
    Nikkei -4.8%, SoftBank -16%.
  - Anthropic debuts on Nasdaq, closing ~$97, 17% above its $83 IPO price.
  - COP31 draft in Antalya drops any call to phase out fossil fuels.
  - Kenya discharges its last Ebola patient, 37 days after its first case.

Run:  python3 draw_news.py   -> writes entry.png next to this file.
Only Pillow is needed at build time; the graded entrypoint (main.ts)
just copies the finished entry.png, so the sandbox needs no libraries.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 33, 61)
RED = (193, 39, 45)
GOLD = (176, 141, 45)
TEAL = (15, 106, 104)
CARD = (255, 253, 247)
RULE = (20, 33, 61)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_scales(draw, cx, cy, s, color):
    """Simple scales-of-justice pictogram centred at (cx, cy), size s."""
    draw.line([(cx, cy - s), (cx, cy + s)], fill=color, width=max(4, s // 12))
    draw.line([(cx - s, cy - s // 3), (cx + s, cy - s // 3)], fill=color,
              width=max(4, s // 12))
    draw.ellipse([cx - s // 8, cy - s - s // 6, cx + s // 8, cy - s + s // 6],
                 fill=color)
    for side in (-1, 1):
        px = cx + side * s
        draw.line([(cx + side * s, cy - s // 3), (px, cy + s // 5)],
                  fill=color, width=max(3, s // 16))
        draw.line([(px - s // 3, cy + s // 5), (px + s // 3, cy + s // 5)],
                  fill=color, width=max(3, s // 16))
        draw.polygon([(px - s // 2, cy + s // 5), (px + s // 2, cy + s // 5),
                      (px, cy + s // 2)], fill=color)
    draw.rectangle([cx - s // 2, cy + s, cx + s // 2, cy + s + s // 6],
                   fill=color)


def draw_icon(draw, kind, cx, cy, r, color):
    """Small geometric pictogram for a story card, centred at (cx, cy)."""
    if kind == "summit":
        for dx, s in ((-r // 2, r), (r // 2, r)):
            draw.ellipse([cx + dx - s // 2, cy - s // 2,
                          cx + dx + s // 2, cy + s // 2],
                         outline=color, width=5)
        draw.line([(cx - r // 2, cy), (cx + r // 2, cy)], fill=color, width=5)
    elif kind == "blast":
        pts = []
        for i in range(12):
            ang = i * math.pi / 6
            rr = r if i % 2 == 0 else r // 2
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=color)
        draw.ellipse([cx - r // 4, cy - r // 4, cx + r // 4, cy + r // 4],
                     fill=PAPER)
    elif kind == "tower":
        draw.rectangle([cx - r // 3, cy - r, cx + r // 3, cy + r], fill=color)
        draw.polygon([(cx - r // 2, cy - r), (cx + r // 2, cy - r),
                      (cx, cy - r - r // 2)], fill=color)
        for yy in range(cy - r + 12, cy + r - 6, 16):
            draw.rectangle([cx - r // 5, yy, cx + r // 5, yy + 7], fill=PAPER)
    elif kind == "chart":
        draw.line([(cx - r, cy + r // 2), (cx - r // 3, cy),
                   (cx + r // 3, cy + r // 4), (cx + r, cy - r // 2)],
                  fill=color, width=6, joint="curve")
        draw.polygon([(cx + r, cy - r // 2), (cx + r - 14, cy - r // 2),
                      (cx + r, cy - r // 2 + 14)], fill=color)
        draw.line([(cx - r, cy + r), (cx + r, cy + r)], fill=color, width=4)
    elif kind == "chip":
        draw.rectangle([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                       outline=color, width=6)
        draw.rectangle([cx - r // 5, cy - r // 5, cx + r // 5, cy + r // 5],
                       fill=color)
        for dx in (-r // 2, 0, r // 2):
            draw.line([(cx + dx, cy - r), (cx + dx, cy - r // 2)],
                      fill=color, width=4)
            draw.line([(cx + dx, cy + r // 2), (cx + dx, cy + r)],
                      fill=color, width=4)
    elif kind == "leaf":
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                     outline=color, width=6)
        draw.line([(cx - r, cy + r // 2), (cx + r, cy - r // 2)],
                  fill=color, width=5)
        draw.line([(cx, cy), (cx, cy + r)], fill=color, width=5)


def card(draw, x, y, w, h, kicker, headline, body, icon, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD,
                           outline=(210, 200, 175), width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=accent)
    draw.text((x + 16, y + 16), kicker, font=font(SANS_B, 18), fill=accent)
    draw_icon(draw, icon, x + w - 26, y + 32, 14, accent)
    hl = wrap(draw, headline, font(SERIF_B, 27), w - 32)
    yy = text_block(draw, x + 16, y + 46, hl, font(SERIF_B, 27), INK, 31)
    bd = wrap(draw, body, font(SANS, 20), w - 32)
    text_block(draw, x + 16, yy + 8, bd[:3], font(SANS, 20), (60, 60, 60), 25)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 18], fill=RED)

    # ---- Masthead -------------------------------------------------------
    d.text((512, 30), "THE WORLD IN ONE DAY", font=font(SERIF_B, 58),
           fill=INK, anchor="ma")
    d.text((512, 104), "FRIDAY  \u2022  20 NOVEMBER 2026  \u2022  THE DAY'S NEWS, IN ONE PICTURE",
           font=font(SANS_B, 23), fill=RED, anchor="ma")
    d.line([(48, 146), (976, 146)], fill=RULE, width=3)

    # ---- Hero: the day's biggest story ----------------------------------
    hx, hy, hw, hh = 48, 162, 928, 250
    d.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=16, fill=INK)
    d.text((hx + 28, hy + 18), "THE HAGUE  \u2022  TOP STORY",
           font=font(SANS_B, 22), fill=(232, 196, 90))
    hl = wrap(d, "World court: Myanmar committed genocide",
              font(SERIF_B, 42), 590)
    yy = text_block(d, hx + 28, hy + 50, hl, font(SERIF_B, 42),
                    (255, 253, 247), 48)
    body = ("The International Court of Justice rules 9\u20136 that Myanmar "
            "committed genocide against the Rohingya \u2014 its first such "
            "finding against a state.")
    bl = wrap(d, body, font(SANS, 24), 590)
    text_block(d, hx + 28, yy + 8, bl, font(SANS, 24), (220, 220, 210), 30)
    draw_scales(d, hx + hw - 110, hy + 128, 62, (232, 196, 90))

    # ---- Story grid ------------------------------------------------------
    stories = [
        ("SHENZHEN \u2022 SUMMIT", "Trump, Xi & Putin meet",
         "Three-way summit issues a joint peace declaration; no Ukraine "
         "breakthrough.", "summit", TEAL),
        ("KYIV \u2022 WAR", "Bridges hit in overnight strikes",
         "Russian strikes kill 8 in Kyiv; allies meet in Berlin, ready "
         "to talk with Russia.", "blast", RED),
        ("RIYADH \u2022 CONFLICT", "Missile damages PIF Tower",
         "Houthi strike hits the Saudi capital's financial district.",
         "tower", RED),
        ("MARKETS \u2022 ECONOMY", "Stocks slide worldwide",
         "S&P 500 falls ~2% for a fifth straight day; Nikkei \u22124.8%; "
         "SoftBank \u221216%.", "chart", TEAL),
        ("NEW YORK \u2022 TECH", "Anthropic's big Nasdaq debut",
         "AI firm closes near $97, 17% above its $83 IPO price.",
         "chip", TEAL),
        ("ANTALYA \u2022 CLIMATE", "COP31 draft drops fossil fuels",
         "Negotiators remove any call to phase out fossil fuels from "
         "the draft deal.", "leaf", (90, 120, 40)),
    ]
    gx, gy, cw, ch, gap = 48, 428, 296, 224, 20
    for i, (kick, head, body, icon, accent) in enumerate(stories):
        x = gx + (i % 3) * (cw + gap)
        y = gy + (i // 3) * (ch + gap)
        card(d, x, y, cw, ch, kick, head, body, icon, accent)

    # ---- Footer ticker ---------------------------------------------------
    fy = 906
    d.line([(48, fy), (976, fy)], fill=RULE, width=3)
    d.text((48, fy + 12), "ALSO TODAY", font=font(SANS_B, 21), fill=RED)
    ticker = ("Kenya discharges its last Ebola patient  \u2022  Israeli troops "
              "cross Gaza's Yellow Line  \u2022  US Senate blocks Iran "
              "war-powers measure 51\u201348  \u2022  Cyclone Akvan hits Odisha")
    tl = wrap(d, ticker, font(SANS, 20), 928)
    text_block(d, 48, fy + 40, tl, font(SANS, 20), INK, 25)
    d.text((512, 1000), "Sources: ICJ \u2022 AP \u2022 Reuters \u2022 BBC \u2022 Just Security \u2022 One Turn",
           font=font(SANS, 15), fill=(110, 105, 90), anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
