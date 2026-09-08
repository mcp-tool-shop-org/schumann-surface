---
license: cc-by-4.0
pretty_name: Schumann Resonance — Sierra Nevada ELF station, calibrated 10-minute products
language:
  - en
tags:
  - schumann-resonance
  - elf
  - geophysics
  - ionosphere
  - space-weather
  - time-series
size_categories:
  - 100K<n<1M
configs:
  - config_name: modes
    data_files: "modes/*.parquet"
  - config_name: lanes
    data_files: "lanes/*.parquet"
  - config_name: polarisation
    data_files: "polarisation/*.parquet"
  - config_name: spectra
    data_files: "spectra/*.parquet"
  - config_name: model
    data_files: "model/*.parquet"
---

# Schumann Resonance — Sierra Nevada ELF station, calibrated 10-minute products

Calibrated magnetic amplitude spectra (6–25 Hz), Lorentzian mode fits for Schumann modes 1–3, NS/EW
polarisation, and aligned event lanes, derived from the raw 256 Hz recordings of the Sierra Nevada ELF
station (University of Granada, 37.04 N, 3.32 W, 2500 m). Every number here descends from the CC BY 4.0
raw archive through a processing chain that reproduces the station's own published products at a
spectrum ratio of 1.0000. The station's processed files are CC BY-NC-ND and are **not** included.

Months in this release: **2013-03, 2013-04, 2013-05, 2013-06, 2013-07, 2013-08, 2013-09, 2013-10, 2013-11, 2013-12, 2017-01, 2017-02** (both sensors), every one of them verified against the station's published products at a spectrum ratio of 1.0000.

## Read this first: what the instrument can and cannot see

The coils are calibrated for 6–25 Hz and resonate near 33 Hz, so **only modes 1, 2 and 3 exist in
this data**. Above 25 Hz the raw spectrum is the sensor, not the cavity. Amplitudes are in pT/√Hz after
the station's amplitude-only calibration; phase is not calibrated (a tenth-order 50 Hz Butterworth sits
in the chain), which is why polarisation is reported from ratios where the calibration cancels.

## Tables

| Config | Row | Columns |
|---|---|---|
| `spectra` | 10-min slot × sensor | `t_utc`, `sensor` (NS/EW), `sat` (fraction of 10-s windows dropped for saturation), `amp[609]` pT/√Hz on the 6–25 Hz axis in `frequency_axis.parquet` (31.25 mHz step) |
| `modes` | slot × sensor × mode | `f_hz` centre, `peak` amplitude at the centre (pT/√Hz), `a` Lorentzian amplitude, `halfwidth_hz`, `chi2`, `masked` (fit left the per-mode window: 6.5–9.5 / 12.5–16 / 18.5–22.5 Hz or width outside 0.3–5 Hz) |
| `polarisation` | slot × mode | `az_rad` axial polarisation angle of the horizontal field from the NS coil towards EW, in (−π/2, π/2]; source bearing ≈ az + π/2, two-fold ambiguous; `ellipticity` in [−1, 1]; `coherence` NS/EW magnitude-squared; `f_hz` used |
| `lanes` | slot | `kp` (GFZ, 3-hourly, interval containing the slot), `night_fraction` (sun below −6° at the station), `quake_count_24h`, `quake_max_mag_24h` (USGS M6+, trailing 24 h) |
| `model` | slot | `chimney_model` — a **model**, not a measurement: three Gaussians in UTC hour (Southeast Asia 08, Africa 14.5, Americas 20; σ 2.5 h; weights 0.8/1.0/0.9). Kept in its own config so it is never mistaken for data |

Slots start where the station's hour files start (the acquisition drifts 0.23 s per hour), so
timestamps are irregular by seconds; join tables on `t_utc` exactly, they share the grid.

## Method (pinned, reproduces the station)

10-s Hann windows (2560 samples, unit-power normalised), 50 % overlap, 119 windows per slot, FFT
zero-padded to 8192, windows with any saturated sample dropped. Amplitude
`sqrt(Σ|FFT|²·2/(n·fs·2560))` times the station calibration
`Scal(f) = 1e12/(2500·1.9e6)·sqrt((1−(f/f0)²)²+(2δf/f0)²)/f` with L = 298 kH, C = 77.75 pF,
R = 320 kΩ (f0 = 33.06 Hz, δ = 2.58e−3, the constants in the station's code rather than its paper).
Anthropogenic bands 14.55–15.35 and 16.50–16.90 Hz straight-lined when their deviation exceeds 2.5×
the reference bands. Three Lorentzians plus a linear term fitted in the amplitude domain over
6.35–23.75 Hz, Levenberg–Marquardt, seeds 8.011/14.2/20.63 Hz.

## Verification against the station's published fits

| | Oct 2013 NS | Oct 2013 EW | Jun 2013 NS | Jun 2013 EW |
|---|---|---|---|---|
| spectrum ratio ours/station, p5–p95 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| saturation correlation | 1.000 | 1.000 | 1.000 | 1.000 |
| mode-1 centre, median difference | +0.004 Hz | +0.008 Hz | +0.004 Hz | −0.02 Hz |

## Knowledge base

`kb/` carries the context the numbers need: the station and its calibration, the method step by step,
licences and provenance, the event lanes and what is model versus measurement, the verification receipt,
and the literature with identifiers. It is generated from the studio's `schumann-knowledge` base so the
two cannot drift.

## Licence and attribution

Data: CC BY 4.0. Please cite the source archive and the station's method paper alongside this dataset:

- Salinas, A., Rodríguez-Camacho, J., Portí, J., Carrión, M. C., Fornieles-Callejón, J., Toledo-Redondo, S. (2022). Four-year measurements from Sierra Nevada ELF station. Zenodo. https://doi.org/10.5281/zenodo.6348930
- Salinas, A. et al. (2022). Schumann resonance data processing programs and four-year measurements from Sierra Nevada ELF station. *Computers & Geosciences* 165, 105148. https://doi.org/10.1016/j.cageo.2022.105148
- Matzka, J. et al. (2021). The geomagnetic Kp index and derived indices of geomagnetic activity. *Space Weather*. https://doi.org/10.1029/2020SW002641 (Kp, CC BY 4.0)
- USGS Earthquake Hazards Program, FDSN event web service (public domain)

Derived products and code: mcp-tool-shop, MIT for the code. Not affiliated with the University of Granada.
