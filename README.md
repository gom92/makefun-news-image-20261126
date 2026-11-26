# Thursday 26 November 2026 — in one image

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/gom92/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/gom92/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

A front-page image summing up the world news of **Thursday 26 November 2026**,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261126).

## The day

- **Lead — Cairo:** A fuel tanker crashes and bursts into flames on the
  highway ringing Cairo, killing at least 30 people and injuring 15.
- **Secondary — Ukraine:** Ukraine says it struck a major Russian air base
  and two oil refineries, damaging five planes in the overnight raid.
- **Briefs:** the US seeks 25% tariffs on 14 economies; Kim Jong Un orders
  wider deployment of tactical nuclear weapons; a second judge blocks
  Trump's birthright-citizenship order; Israeli judges recommend dropping
  the most serious charges against Netanyahu; SpaceX wins approval to launch
  data centres in space; the Macy's Thanksgiving parade is postponed for
  the first time as a nor'easter hits.
- **Numbers:** 30 killed in Cairo · 5 planes damaged · 25% tariffs on 14
  economies · 2,000 migrants reach the Canary Islands.

Sources: Reuters, AP, BBC, The Japan Times, Economic Times. Events are those that
happened or were first reported on 26 November 2026.

## How it is made

`tools/render_frontpage.py` draws the 1024×1024 front page with Pillow:
masthead, the two photo panels (generated fresh for this entry and kept
under `assets/`), the briefs and the numbers strip. `main.py` copies the
finished `entry.png` to the output directory.

```sh
python3 tools/render_frontpage.py   # rebuild entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program uses only the Python standard library, needs no network, and
writes byte-identical output on every run.

## Verification

- `entry.png` is 1024×1024 PNG, under 1 MiB.
- `main.py` was run twice offline; both runs produced the same SHA-256.
- The rendered page was viewed and checked: the date, both stories, all
  six briefs and the numbers strip are legible, with nothing clipped or
  overlapping.

## Referral

Use referral code `radjee14` when you sign up on make.fun.

## License

MIT — see [LICENSE](LICENSE).
