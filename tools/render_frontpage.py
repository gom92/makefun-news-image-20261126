#!/usr/bin/env python3
"""Render the 26 November 2026 front page (thin wrapper).

The real renderer lives in main.py at the repository root; this shim
exists so the page can still be rebuilt with:

    python3 tools/render_frontpage.py

It adds the repo root to sys.path, imports build_page from main, and
runs it.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from main import build_page  # noqa: E402


if __name__ == "__main__":
    path = build_page()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
