<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/schumann-surface/readme.png" alt="Schumann Surface" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <a href="https://mcp-tool-shop-org.github.io/schumann-surface/"><img src="https://img.shields.io/badge/landing-page-0ea5e9" alt="Landing page"></a>
  <a href="https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada"><img src="https://img.shields.io/badge/dataset-Hugging%20Face-ffcc4d" alt="Dataset"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.ja.md">日本語</a> · <a href="README.zh.md">中文</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (BR)</a></p>

# schumann-surface

Schumann resonance as a 3D time–frequency surface with event lanes and an honest, lagged
cross-correlation panel. One month of a real ELF station rendered so a person can see the
daily lightning rhythm, the mode ribbons, and what a geomagnetic storm does and does not do.

Status: v1.0.0. October and June 2013 from the Sierra Nevada ELF station (University of Granada)
reproduced against the station's own published spectra and mode fits slot by slot; the remaining
ten months of the raw archive are flowing through the same pipeline. The viewer is a single
self-contained HTML file with four modes; live at the [landing page](https://mcp-tool-shop-org.github.io/schumann-surface/viewer/).

## What it shows

- **Surface**: time (one month, 30-min columns) × frequency (6–25 Hz, 0.125 Hz rows) × magnetic
  amplitude in dB re 1 pT/√Hz. NS and EW sensors as two stackable sheets.
- **Mode ribbons**: fitted centre frequency of modes 1–3 riding the surface.
- **Event lanes** in front of the surface: Kp geomagnetic index (3-hourly, GFZ), local night at the
  station (computed from the timestamp), earthquakes M6+ (USGS).
- **Correlation panel**: Pearson r versus lag (±24 h) between any surface series (mode amplitude,
  mode frequency, band power) and any event series, with a 95 % null band whose effective sample
  size is corrected for autocorrelation in both series (Bartlett). A curve inside the band is a
  null result and is displayed as one.

## Why the band is 6–25 Hz

The station's coil is an RLC sensor resonant near 33 Hz and calibrated by its authors for 6–25 Hz
only. Above 25 Hz the raw spectrum is dominated by the sensor resonance, not by the cavity, so
modes 4 and up are not resolvable from this instrument. A wider-band station is needed for them.

## Verification (October 2013, 4464 slots per sensor)

| Check against the station's published npz | NS | EW |
|---|---|---|
| Amplitude spectrum ratio ours/station, 6–25 Hz (median, p5, p95) | 1.0000 / 1.0000 / 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| Saturation fraction per slot, correlation | 1.000 | 1.000 |
| Mode 1 centre frequency, median difference | +0.004 Hz | +0.008 Hz |
| Mode 2 centre frequency, median difference | +0.000 Hz | +0.002 Hz |
| Mode 3 centre frequency, median difference | −0.000 Hz | +0.001 Hz |
| Mode peak amplitude ratio, median | 1.001 / 1.000 / 1.000 | 1.001 / 1.000 / 1.000 |

The residual frequency scatter is the two Levenberg–Marquardt implementations (lmfit at the station,
SciPy here) landing on different local minima for a few percent of slots; the viewer masks fits that
leave the documented per-mode windows.

The verifier is a gate: it exits non-zero unless ≥ 95 % of slots match within 30 s, the spectrum
ratio's 5th and 95th percentiles sit within 1 ± 0.005, every mode's median frequency difference is
under 0.02 Hz, and the saturation series correlate above 0.99.

## Lightning lane: model, not measurement

No openly downloadable measured global lightning series exists for 2013 (WWLLN is subscription, the
Blitzortung archive needs a participant login, NASA's LIS/OTD climatology sits behind Earthdata).
The viewer therefore carries a **chimney schedule** as a model lane: three Gaussians in UTC hour for
Southeast Asia, Africa and the Americas, after Whipple 1929, the Carnegie curve (Harrison 2013) and
the LIS/OTD diurnal climatology (Blakeslee et al. 2014). It is labelled as a model wherever shown.
The measured counterpart is also embedded: the per-UTC-hour mean of each mode's amplitude over the
month. See `docs/data-contract.md`.

## Data and licences

| Source | What | Licence | Use here |
|---|---|---|---|
| Salinas et al., Zenodo [10.5281/zenodo.6348930](https://zenodo.org/records/6348930) | raw 256 Hz time series, Mar–Dec 2013 and Jan–Feb 2017 | CC BY 4.0 | input; derived products are ours to publish with attribution |
| Salinas et al., Digibug [10481/71563](https://digibug.ugr.es/handle/10481/71563) | station-processed 10-min spectra + Lorentzian fits | CC BY-NC-ND 3.0 | verifier only, never redistributed |
| Salinas et al. 2022, *Computers & Geosciences* 165:105148; code [asalinas62/Sierra_Nevada_SR](https://github.com/asalinas62/Sierra_Nevada_SR) | calibration formula and processing chain | paper CC BY-NC-ND; code per its repo | method reproduced in `scripts/process_month.py` |
| GFZ Potsdam Kp index, Matzka et al. 2021 | 3-hourly Kp | CC BY 4.0 | event lane |
| USGS FDSN event service | earthquakes | public domain | event lane |

Nothing under `data/` is committed. The Zenodo archive is one 26.5 GB zip; the fetch script reads
its central directory over HTTP range requests and streams only the requested month.

## Pipeline

```bash
python scripts/fetch_zenodo_month.py 1310          # ~2.4 GB, one month, both sensors
python scripts/process_month.py 1310 0             # NS  -> data/derived/SN_1310_0.npz
python scripts/process_month.py 1310 1             # EW  -> data/derived/SN_1310_1.npz
python scripts/verify_against_granada.py 1310 0    # optional, needs the Digibug npz in data/granada/
python scripts/build_viewer.py 1310                # -> viewer/index.html (+ viewer/artifact.html)
python -m pytest -q tests                          # synthetic checks on the chain
```

Pinned method (mirrors the station chain so it can be verified): 10-s Hann windows, 50 % overlap,
zero-padded FFT to 8192 (31.25 mHz), saturated windows dropped, RLC calibration
`Scal(f) = 1e12/(2500·1.9e6) · sqrt((1-(f/f0)²)² + (2δf/f0)²) / f` with L = 298 kH,
C = 77.75 pF, R = 320 kΩ, anthropogenic-band straight-line filter, three Lorentzians plus a linear
term fitted in the amplitude domain over 6.35–23.75 Hz.

## Standards compliance

Scored 0–3 against the studio's six workflow standards.

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every numeric choice (window, overlap, FFT size, calibration constants, fit band, seeds) is a named constant at the top of `process_month.py` and written into the npz `method` field. Not yet byte-replayable across NumPy versions; no receipt of library versions. |
| ANDON_AUTHORITY | 2 | `verify_against_granada.py` is the halt point on disagreement with the station's published fits; the fetch script asserts every zip entry's inflated size before writing. |
| NAMED_COMPENSATORS | 2 | No irreversible external call in the pipeline. The only publish path is a git push of source; `data/` is ignored. Compensator for a bad `viewer/index.html`: rebuild from the npz. |
| DECOMPOSE_BY_SECRETS | 2 | Fetch, process, verify, build are four scripts with one job each; the viewer template knows nothing about the station and consumes a station-agnostic JSON block. |
| UNCERTAINTY_GATED_HUMANS | 1 | The correlation panel shows the null band, which is the uncertainty gate for the viewer. No human checkpoint in the pipeline itself. Remediation: make the verifier emit pass/fail against a stated tolerance (owner: next session). |
| EXTERNAL_VERIFIER | 3 | The verifier is the station's own independently produced output (different code, different authors, lmfit vs SciPy). Numbers in the table above. |

## Trust and data

The pipeline runs locally from a checkout. It reads and writes only under `data/` and `viewer/`.
Network access happens only when you ask a script to fetch: Zenodo (raw archive), Digibug (the
station's verifier files), GFZ (Kp), USGS (earthquakes). Uploading the dataset uses your own Hugging
Face login outside these scripts. No credentials are read or stored, no telemetry is sent, and the
viewer is a static page that loads Three.js and two fonts from public CDNs and nothing else.
Requirements: Python 3.11 or newer with NumPy, SciPy and PyArrow, on any OS; Node is only needed for
the optional landing page.

## Licence

MIT for the code. Derived data products carry the attribution required by their sources.

---

<p align="center">Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a></p>
