#!/usr/bin/env python3
"""Render the 26 November 2026 front page and copy it to the output dir.

This is the entrypoint for make.fun news-image-20261126. It draws the
whole front page from scratch with Pillow — masthead, two photo panels,
the briefs grid, the numbers strip and the footer — then saves the
result as entry.png next to this file and copies it to
$MAKEFUN_OUTPUT_DIR (default "out").

No network, no randomness: the same inputs always produce the same
bytes. The two photographs are the entry's own generated panels in
assets/; everything else is drawn.

Usage:
    MAKEFUN_OUTPUT_DIR=/output python3 main.py
"""

import hashlib
import os
import shutil

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# Page geometry and palette.
PAGE_W, PAGE_H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 20, 24)
NAVY = (16, 32, 56)
RED = (178, 34, 28)
GREY = (90, 92, 96)
GOLD = (214, 196, 150)
BODY = (40, 42, 46)
BODY2 = (52, 54, 58)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, max_width):
    """Greedy wrap: pack words into lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw stacked lines, returning the y below the last one."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover(img, target_w, target_h):
    """Centre-crop to the target aspect, then resize to it."""
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale + 0.5)
    new_h = int(src_h * scale + 0.5)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def draw_masthead(d):
    d.rectangle([0, 0, PAGE_W, 104], fill=NAVY)
    d.text((28, 14), "THE WORLD  •  ONE DAY IN PICTURES",
           font=load_font(SANS_BOLD, 17), fill=GOLD)
    d.text((28, 38), "THURSDAY 26 NOVEMBER 2026",
           font=load_font(SERIF_BOLD, 43), fill=(255, 255, 255))
    d.rectangle([0, 104, PAGE_W, 110], fill=RED)


def draw_lead_story(d, page):
    photo = Image.open(os.path.join(
        ASSETS,
        "media-generation-cairo-tanker-fire-0-26b577b6-33b8-4839-9bf4-f4cf972201b8.png"))
    page.paste(cover(photo, 592, 296), (28, 126))
    d.rectangle([28, 126, 620, 422], outline=INK, width=2)
    d.text((28, 432), "CAIRO", font=load_font(SANS_BOLD, 16), fill=RED)
    d.text((28, 452), "Highway tanker fire",
           font=load_font(SERIF_BOLD, 34), fill=INK)
    d.text((28, 490), "kills at least 30",
           font=load_font(SERIF_BOLD, 34), fill=INK)
    deck = ("A fuel tanker crashes and bursts into flames on the highway "
            "ringing Cairo, killing at least 30 people and injuring 15 "
            "as firefighters battle the blaze into the evening.")
    draw_lines(d, 28, 536,
               fit_lines(d, deck, load_font(SANS, 17), 592),
               load_font(SANS, 17), BODY, 22)


def draw_secondary_story(d, page):
    photo = Image.open(os.path.join(
        ASSETS,
        "media-generation-ukraine-airbase-strike-0-ae2b7184-7fe8-4f9d-9992-78cd3007b67a.png"))
    page.paste(cover(photo, 352, 296), (644, 126))
    d.rectangle([644, 126, 996, 422], outline=INK, width=2)
    d.text((644, 432), "UKRAINE", font=load_font(SANS_BOLD, 16), fill=RED)
    d.text((644, 452), "Air base hit,",
           font=load_font(SERIF_BOLD, 30), fill=INK)
    d.text((644, 486), "five jets damaged",
           font=load_font(SERIF_BOLD, 30), fill=INK)
    deck = ("Ukraine says it struck a major Russian air base and two "
            "oil refineries, damaging five planes in the overnight raid.")
    draw_lines(d, 644, 528,
               fit_lines(d, deck, load_font(SANS, 16), 352),
               load_font(SANS, 16), BODY, 21)


BRIEFS = [
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


def draw_briefs(d):
    d.rectangle([28, 636, 996, 638], fill=INK)
    d.text((28, 646), "THE DAY IN BRIEF",
           font=load_font(SERIF_BOLD, 24), fill=INK)
    d.text((PAGE_W - 28, 652), "THURSDAY 26 NOVEMBER 2026",
           font=load_font(SANS_BOLD, 13), fill=GREY, anchor="ra")
    for i, (kicker, head, body) in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        x = 28 + col * 496
        y = 690 + row * 74
        d.text((x, y), kicker, font=load_font(SANS_BOLD, 13), fill=RED)
        d.text((x + 78, y - 1), head, font=load_font(SANS_BOLD, 14), fill=INK)
        lines = fit_lines(d, body, load_font(SANS, 13), 472)[:2]
        draw_lines(d, x, y + 21, lines, load_font(SANS, 13), BODY2, 17)


STATS = [
    ("30", "killed in Cairo"),
    ("5", "planes damaged"),
    ("25%", "tariffs on 14 economies"),
    ("2,000", "migrants reach Canaries"),
]


def draw_numbers_strip(d):
    d.rectangle([28, 916, 996, 980], fill=NAVY)
    seg = 968 // 4
    for i, (num, label) in enumerate(STATS):
        x = 28 + i * seg
        d.text((x + 18, 924), num, font=load_font(SERIF_BOLD, 26),
               fill=(255, 255, 255))
        d.text((x + 18, 954), label, font=load_font(SANS, 13), fill=GOLD)
        if i:
            d.line([x, 926, x, 970], fill=(90, 110, 140), width=1)


def draw_footer(d):
    d.text((28, 992),
           "Sources: Reuters, AP, BBC, The Japan Times, Economic Times  •  All events of 26 November 2026",
           font=load_font(SANS, 12), fill=GREY)


def build_page():
    """Draw the full front page and save it as entry.png."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)
    draw_masthead(d)
    draw_lead_story(d, page)
    draw_secondary_story(d, page)
    draw_briefs(d)
    draw_numbers_strip(d)
    draw_footer(d)
    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True)
    return out


def sha256_file(path):
    """SHA-256 of a file, read in chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_path = build_page()
    size = os.path.getsize(out_path)
    digest = sha256_file(out_path)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(out_path, os.path.join(out_dir, "entry.png"))
    print(f"wrote {out_path} ({size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
