#!/usr/bin/env python3
"""Entry for make.fun news-image-20261126.

Copies the front-page image built for Thursday 26 November 2026 to
the output directory. No network, no randomness: every run writes the
same bytes.

Usage:  MAKEFUN_OUTPUT_DIR=/output python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
