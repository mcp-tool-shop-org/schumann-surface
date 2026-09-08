---
title: Data contract and dataset
description: The scripts, the JSON block the viewer consumes, and the Parquet tables the dataset ships.
sidebar:
  order: 3
---

## Scripts

| Script | Job | Output |
|---|---|---|
| `fetch_zenodo_month.py YYMM` | Range-extract one month from the 26.5 GB Zenodo zip | `data/raw/YYYY/YYMM/` |
| `process_month.py YYMM S` | Welch, calibration, filter, Lorentzian fit for sensor S (0 = NS, 1 = EW) | `data/derived/SN_YYMM_S.npz` |
| `polarisation_month.py YYMM` | NS × EW cross-spectra → azimuth, ellipticity, coherence per slot and mode | `data/derived/POL_YYMM.npz` |
| `verify_against_granada.py YYMM S` | Slot-by-slot check against the station's published npz; exits 2 outside tolerance | receipt on stdout |
| `export_dataset.py YYMM` | Parquet tables for the public dataset | `data/dataset/` |
| `build_viewer.py YYMM [--main]` | Embed a month into the viewer template | `viewer/SN_YYYYMM.html`, and `index.html` with `--main` |
| `pipeline_month.py YYMM ...` | All of the above in order, skipping what exists | logs in `data/pipeline_YYMM.log` |

Every script's module docstring is its help text and names its inputs, outputs and pinned numbers.

## The viewer's data contract (version 3)

`build_viewer.py` embeds one JSON object into `viewer/template.html`. A second station only has to
produce the same fields.

| Field | Meaning |
|---|---|
| `station`, `lat`, `lon`, `month` | station name and position (east positive), month rendered |
| `t0`, `dt`, `nt` | column grid: column i starts at `t0 + i·dt` (unix seconds) |
| `f0`, `df`, `nf` | row grid: row j is `f0 + j·df` Hz (6.0, 0.125, 152 for Sierra Nevada) |
| `sheets[]` | per sensor: `lo`, `hi` dB window and `u8`, base64 of nt×nf bytes; 0 = no data, 1..255 map to lo..hi |
| `modes[NS|EW]` | per column: `f[3]` centre Hz, `a[3]` peak pT/√Hz, `g[3]` half-width Hz, `sat`; −1 = masked |
| `pol` | per column, per mode: `az` axial polarisation angle (radians from NS towards EW), `ell`, `coh`; −9 = no data |
| `kp[]`, `quakes[]` | `[t, kp]` 3-hourly; `[t, mag, place]` |
| `chimneys[]`, `chimneys_month[]` | the thunderstorm schedule (model): name, peak UTC, sigma, weight, lat, lon; the month variant carries seasonal centroids |
| `chimney[]` | the schedule evaluated per column (model lane) |
| `diurnal[NS|EW]` | measured per-UTC-hour mean of each mode's peak amplitude |
| `storm_t` | the interval the page opens on |
| `calnote`, `credits[]` | kept verbatim on the page |

The full document with provenance of the model lane is `docs/data-contract.md` in the repository.

## The dataset

[mcp-tool-shop/schumann-sierra-nevada](https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada),
CC BY 4.0. Five configs, one grid per month, joined on `t_utc`:

| Config | Row | Columns |
|---|---|---|
| `spectra` | slot × sensor | `t_utc`, `sensor`, `sat`, `amp[609]` pT/√Hz on the 6–25 Hz axis in `frequency_axis.parquet` |
| `modes` | slot × sensor × mode | `f_hz`, `peak`, `a`, `halfwidth_hz`, `chi2`, `masked` |
| `polarisation` | slot × mode | `az_rad`, `ellipticity`, `coherence`, `f_hz` |
| `lanes` | slot | `kp`, `night_fraction`, `quake_count_24h`, `quake_max_mag_24h` |
| `model` | slot | `chimney_model` — a model, kept in its own config so it is never mistaken for data |

```python
import pandas as pd
modes = pd.read_parquet("modes/SN_201310.parquet")
lanes = pd.read_parquet("lanes/SN_201310.parquet")
m1 = modes[(modes["mode"] == 1) & (modes.sensor == "NS") & ~modes.masked]
df = m1.merge(lanes, on="t_utc")
df.groupby(df.t_utc.dt.hour)["peak"].mean()   # the daily rhythm
```

The dataset's `kb/` folder carries the station and calibration notes, the method, the lanes, the
reading rules and the verification receipt, generated from the studio's knowledge base so the two
cannot drift.
