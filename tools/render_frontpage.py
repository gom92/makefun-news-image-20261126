#!/usr/bin/env python3
"""Draw the 26 November 2026 front page and save it as entry.png.

Everything on the page is drawn from scratch with Pillow: the masthead,
the two photo panels (generated fresh for this entry), the briefs and the
numbers strip. No network is used. Run from the repository root:

    python3 tools/render_frontpage.py
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 20, 24)
NAVY = (16, 32, 56)
RED = (178, 34, 28)
GREY = (90, 92, 96)
LINE = (200, 192, 176)
PANEL = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_wrapped(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover_crop(img, tw, th):
    """Centre-crop an image to the target aspect, then resize."""
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def build():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((28, 14), "THE WORLD  •  ONE DAY IN PICTURES",
           font=font(SANS_B, 17), fill=(214, 196, 150))
    d.text((28, 38), "THURSDAY 26 NOVEMBER 2026",
           font=font(SERIF_B, 43), fill=(255, 255, 255))
    d.rectangle([0, 104, W, 110], fill=RED)

    # ---- Lead story: Cairo tanker fire ---------------------------------
    lead = Image.open(os.path.join(
        ROOT, "assets",
        "media-generation-cairo-tanker-fire-0-26b577b6-33b8-4839-9bf4-f4cf972201b8.png"))
    page.paste(cover_crop(lead, 592, 296), (28, 126))
    d.rectangle([28, 126, 620, 422], outline=INK, width=2)
    d.text((28, 432), "CAIRO", font=font(SANS_B, 16), fill=RED)
    d.text((28, 452), "Highway tanker fire",
           font=font(SERIF_B, 34), fill=INK)
    d.text((28, 490), "kills at least 30",
           font=font(SERIF_B, 34), fill=INK)
    deck = ("A fuel tanker crashes and bursts into flames on the highway "
            "ringing Cairo, killing at least 30 people and injuring 15 "
            "as firefighters battle the blaze into the evening.")
    draw_wrapped(d, 28, 536,
                 wrap(d, deck, font(SANS, 17), 592),
                 font(SANS, 17), (40, 42, 46), 22)

    # ---- Secondary story: Ukraine strikes Russian air base --------------
    jets = Image.open(os.path.join(
        ROOT, "assets",
        "media-generation-ukraine-airbase-strike-0-ae2b7184-7fe8-4f9d-9992-78cd3007b67a.png"))
    page.paste(cover_crop(jets, 352, 296), (644, 126))
    d.rectangle([644, 126, 996, 422], outline=INK, width=2)
    d.text((644, 432), "UKRAINE", font=font(SANS_B, 16), fill=RED)
    d.text((644, 452), "Air base hit,",
           font=font(SERIF_B, 30), fill=INK)
    d.text((644, 486), "five jets damaged",
           font=font(SERIF_B, 30), fill=INK)
    deck2 = ("Ukraine says it struck a major Russian air base and two "
             "oil refineries, damaging five planes in the overnight raid.")
    draw_wrapped(d, 644, 528,
                 wrap(d, deck2, font(SANS, 16), 352),
                 font(SANS, 16), (40, 42, 46), 21)

    # ---- The day in brief ----------------------------------------------
    d.rectangle([28, 636, 996, 638], fill=INK)
    d.text((28, 646), "THE DAY IN BRIEF",
           font=font(SERIF_B, 24), fill=INK)
    d.text((W - 28, 652), "THURSDAY 26 NOVEMBER 2026",
           font=font(SANS_B, 13), fill=GREY, anchor="ra")

    briefs = [
        ("TRADE", "US seeks 25% tariffs on 14 economies",
         "China, the EU and Japan in the firing line; rates of 20-40% floated."),
        ("KOREA", "Kim orders wider nuclear deployment",
         "North Korea's leader calls for more tactical nuclear weapons to be fielded."),
        ("USA", "Second judge blocks birthright order",
         "Trump's newest order curtailing birthright citizenship is halted again."),
        ("ISRAEL", "Judges urge dropping Netanyahu charges",
         "Israeli judges recommend removing the most serious charges against the PM."),
        ("SPACE", "SpaceX wins approval for orbital data centres",
         "The US government clears SpaceX to launch data centres in space."),
        ("PARADE", "Macy's parade postponed by storm",
         "The Thanksgiving parade is delayed for the first time as a nor'easter hits."),
    ]
    col_w = 472
    for i, (kicker, head, body) in enumerate(briefs):
        col = i % 2
        row = i // 2
        x = 28 + col * 496
        y = 690 + row * 74
        d.text((x, y), kicker, font=font(SANS_B, 13), fill=RED)
        d.text((x + 78, y - 1), head, font=font(SANS_B, 14), fill=INK)
        blines = wrap(d, body, font(SANS, 13), col_w)[:2]
        draw_wrapped(d, x, y + 21, blines, font(SANS, 13),
                     (52, 54, 58), 17)

    # ---- Numbers strip ---------------------------------------------------
    d.rectangle([28, 916, 996, 980], fill=NAVY)
    stats = [
        ("30", "killed in Cairo"),
        ("5", "planes damaged"),
        ("25%", "tariffs on 14 economies"),
        ("2,000", "migrants reach Canaries"),
    ]
    seg = 968 // 4
    for i, (num, label) in enumerate(stats):
        x = 28 + i * seg
        d.text((x + 18, 924), num, font=font(SERIF_B, 26), fill=(255, 255, 255))
        d.text((x + 18, 954), label, font=font(SANS, 13), fill=(214, 196, 150))
        if i:
            d.line([x, 926, x, 970], fill=(90, 110, 140), width=1)

    # ---- Footer ----------------------------------------------------------
    d.text((28, 992), "Sources: Reuters, AP, BBC, The Japan Times, Economic Times  •  All events of 26 November 2026",
           font=font(SANS, 12), fill=GREY)

    out = os.path.join(ROOT, "entry.png")
    page.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
