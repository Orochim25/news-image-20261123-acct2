# THE WORLD IN ONE DAY — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Orochim25/news-image-20261123-acct2/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Orochim25/news-image-20261123-acct2/reward.svg)](https://make.fun/bounty/news-image-20261123)

One picture summing up the world's news of Monday 23 November 2026:
33 verified stories from every region, built on a 3-6-24 structure —
3 mega-heroes, 6 hero panels, 24 compact briefs — with a full world map,
33 numbered pins, a numbers strip and a DATE CHECK bar.

- **3 mega-heroes** — Nvidia brings back Jensen Huang (+31%), COP31 collapses
  without a deal, Ukraine sinks a Russian corvette in Libya.
- **6 hero panels** — the House majority, the CrowdStrike deal, the Binance
  hack recovery, the SpaceX lawsuit, the Palisades verdict, OpenAI's safety
  proposal. Each with its own flat-vector icon.
- **24 briefs** — every remaining story in two dense columns (#10–33).
- **WHERE IT HAPPENED** — a world map with all 33 stories as numbered dots
  at their true locations, plus a per-region count.
- **THE DAY IN NUMBERS** — 258, +31%, $44B, 582, $21.6B, 311.
- **DATE CHECK** — stories left out because they happened on another day.

Every story happened or was first reported on 23 November 2026. Sources:
Reuters, AP, AFP, Al Jazeera, BBC, Bloomberg, Bild, NHS, US Treasury,
CREA, UN OHCHR, OkayAfrica. Flat-vector art drawn in code — no AI photos.

## How it works

`build.py` draws `entry.png` with PIL at build time (1024x1024, deterministic).
`main.py` (Python 3.13, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, as the kit's starter does — the grader
container has no Pillow and no network.

```sh
python3 build.py            # regenerates entry.png (needs Pillow)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Entry for the [news-image-20261123](https://make.fun/bounty/news-image-20261123)
competition on [make.fun](https://make.fun).
