# schumann-surface

Schumann resonance as a 3D time–frequency surface with event lanes and an honest, lagged
cross-correlation panel. One month of a real ELF station rendered so a person can see the
daily lightning rhythm, the mode ribbons, and what a geomagnetic storm does and does not do.

Status: step 1 proven on October 2013 from the Sierra Nevada ELF station (University of
Granada). The processing chain reproduces the station's own published spectra and mode fits
slot by slot. The viewer is a single self-contained HTML file.

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

## Licence

MIT for the code. Derived data products carry the attribution required by their sources.
