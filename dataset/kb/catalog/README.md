# Catalog — schumann-knowledge (Schumann resonance data and physics)

Generated from `findings.db` · wave 1 · 2026-09-08. NEVER hand-edited — regenerated from the DB.

Sung-voice craft for **score-lock** SVS vs lyrics-to-song generators. Not a models table — weights live in [model-knowledge](../../model-knowledge/catalog/audio.md).

**26 findings · 14/26 verified** (verified live against the source during the 2026-09-08 build).

## Verified shortlist

| Lane | Finding | Claim | ✓ |
|---|---|---|---|
| Data sources and licences | [Blitzortung JSON lightning archive (10-minute files)](data-sources.md) | The archive path C{container}/{year}/{month}/{day}/{hour}/{10min}.json answers HTTP 401 without a participant login; 2013 coverage unknown. | ✓ |
| Data sources and licences | [FDSN event web service](data-sources.md) | GeoJSON query by time window and minimum magnitude returns M6+ events for any 2013 month without a key (16 in October, 8 in June). | ✓ |
| Data sources and licences | [Four-year measurements from Sierra Nevada ELF station (raw time-domain archive)](data-sources.md) | The only openly downloadable numeric Schumann resonance source: one 26.5 GB zip of 256 Hz int16 hour files, NS and EW coils, for 2013-03..12 and 2017-01..02, licensed CC BY 4.0. | ✓ |
| Data sources and licences | [Processed 10-minute spectra and Lorentzian fits (Digibug npz archive)](data-sources.md) | The station's own processed products (3.58 GB zip of monthly npz, 43 MB each) are CC BY-NC-ND 3.0. | ✓ |
| Data sources and licences | [The geomagnetic Kp index and derived indices of geomagnetic activity](data-sources.md) | GFZ publishes the full 3-hourly Kp record since 1932 as one CC BY 4.0 text file; October 2013's strongest interval is 2013-10-02 03:00 UTC at Kp 7.67, June 2013 peaks at Kp 7.0. | ✓ |
| Station and calibration | [Raw counts rise ~40x from 6 to 25 Hz and hump at 30–33 Hz](station-calibration.md) | In raw counts the 8 Hz mode sits at ~3e3 counts²/Hz while 33 Hz reaches 2.4e5: the sensor resonance dominates above 25 Hz. | ✓ |
| Station and calibration | [Schumann resonance data processing programs and four-year measurements from Sierra Nevada ELF station](station-calibration.md) | The magnetometers are calibrated for 6–25 Hz only; the calibration is amplitude-only because the tenth-order 50 Hz Butterworth makes the phase unreliable; Scal(f) = 1e12/(2500·1.9e6)·sqrt((1-(f/f0)^2)^2+(2δf/f0)^2)/f. | ✓ |
| Station and calibration | [Sierra_Nevada_SR: Reading_Fourier.py constants](station-calibration.md) | The code uses C_total = 40 + 0.65·55 + 2 pF = 77.75 pF (the paper prints 40 pF), giving a coil resonance f0 = 33.06 Hz and δ = 2.58e-3; volts = counts·10/2^15; saturation /V/ > 9.99. | ✓ |
| Processing chain | [Anthropogenic filter and Lorentzian fit](processing-chain.md) | Bands 14.55–15.35 and 16.50–16.90 Hz are replaced by a straight line when their relative deviation exceeds 2.5x that of reference bands; three Lorentzians plus a linear term are fitted in the amplitude domain over 6.35–23.75 Hz with lmfit LM, seeds 8.011/14.2/20.63 Hz and widths 1.78/1.94/2.56 Hz. | ✓ |
| Processing chain | [Reproduction against the station npz, Oct and Jun 2013](processing-chain.md) | Spectrum ratio ours/station 1.0000 at p5 and p95 over 6–25 Hz for 4464 (Oct) and 4320 (Jun) slots per sensor; saturation correlation 1.000; median mode-frequency differences ≤ 0.008 Hz. | ✓ |
| Processing chain | [Welch chain: 10-s Hann windows, 5-s overlap, zero-padded FFT to 8192, saturated windows dropped](processing-chain.md) | Each 10-min slot is 119 windows of 2560 samples with a unit-power Hann; amplitude = sqrt(sum/FFT/²·2/(n·fs·2560)); any window with a saturated sample is dropped and the fraction recorded. | ✓ |
| Event lanes: measured vs model | [Geomagnetic storm enhancement of Schumann resonance amplitude: a dose-response analysis using the Sierra Nevada ELF archive](event-lanes.md) | Preprint, single author: daily mean mode-1 amplitude rises from 0.345 (Kp<5) to 0.351 (Kp 5–6.7) to 0.366 (Kp≥7), +6.2 %, surviving season and lightning controls. | ✓ |
| Event lanes: measured vs model | [Lag correlation mode-1 amplitude vs Kp, Oct 2013](event-lanes.md) | r(lag 0) = 0.036, N = 1486, N_eff = 69 (Bartlett), 95 % band ±0.236: inside the null on one month at 30-min resolution. | ✓ |
| Event lanes: measured vs model | [Measured diurnal: NS mode-1 amplitude by UTC hour, Oct 2013](event-lanes.md) | Per-hour mean NS mode-1 peak runs 0.34 pT/√Hz at 01 UTC to 0.49 at 19–20 UTC, a clean Americas-chimney afternoon peak seen from Spain. | ✓ |

## Lanes

- [Data sources and licences](data-sources.md) — Where Schumann resonance exists as numbers, where only as pictures, and under which licence (6 findings)
- [Station and calibration](station-calibration.md) — The Sierra Nevada ELF station: sensor model, calibrated band, why higher modes are unreachable (4 findings)
- [Processing chain](processing-chain.md) — Welch, saturation, anthropogenic filter, Lorentzian fit, polarisation; verification against the station (4 findings)
- [Event lanes: measured vs model](event-lanes.md) — Kp, earthquakes, terminator, lightning; what is measured, what is modelled, what is unavailable (5 findings)
- [Cavity physics and correlation honesty](cavity-physics.md) — Modes as standing waves, chimney schedule, storm effects, null-band correlation rules, motion safety (7 findings)

## Legend

- **✓** verified live against the source (fetched, read, or executed) during the build. · = cited by a lane, not yet retrieval-checked.
- Decisive axis: **measured vs model** — every lane on the surface is labelled one or the other.
