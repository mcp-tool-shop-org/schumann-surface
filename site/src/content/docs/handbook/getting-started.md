---
title: Getting started
description: Fetch one month of raw data, process it, verify it against the station, build the viewer.
sidebar:
  order: 1
---

## Requirements

Python 3.11 or newer with NumPy, SciPy and PyArrow. Any OS. About 3 GB of disk per month of raw
data. Node is only needed if you want to build the landing page.

```bash
git clone https://github.com/mcp-tool-shop-org/schumann-surface
cd schumann-surface
pip install numpy scipy pyarrow pytest
python -m pytest -q tests          # synthetic checks on the chain, no data needed
```

## One month, end to end

Months are named `YYMM`. October 2013 is `1310`; the raw archive holds March to December 2013
and January to February 2017.

```bash
python scripts/pipeline_month.py 1310
```

This runs, in order, and skips anything already done:

1. **Fetch.** The Zenodo record is a single 26.5 GB zip. The fetcher reads its central directory
   over HTTP range requests and streams only the month's contiguous span, about 2.4 GB, then
   inflates each hour file locally. Roughly twenty minutes on a 2 MB/s link.
2. **Process** both sensors: `data/derived/SN_1310_0.npz` (NS) and `SN_1310_1.npz` (EW).
3. **Polarisation** from the NS × EW cross-spectra: `data/derived/POL_1310.npz`.
4. **Lanes.** Kp from GFZ, M6+ earthquakes from USGS, both into `data/lanes/`.
5. **Verify** against the station's own published products if they can be fetched. The verifier
   exits non-zero outside stated tolerances and the pipeline stops there.
6. **Export** Parquet tables into `data/dataset/`.

Each step is also a script you can run alone; see the [reference](../reference/).

## Build and open the viewer

```bash
python scripts/build_viewer.py 1310 --main     # -> viewer/index.html
python scripts/build_viewer.py 1306            # -> viewer/SN_201306.html
```

Open `viewer/index.html` in a browser. It is a single file with the month embedded; it loads
Three.js and two fonts from public CDNs and nothing else.

## Verify the checkout

```bash
bash verify.sh
```

Runs the tests, checks the version against the changelog, checks the viewer template still has
its data hook, builds the October page if the derived month is present, and builds the site if
`site/` exists.
