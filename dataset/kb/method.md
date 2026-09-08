# The processing chain, step by step

Every number below is pinned in `scripts/process_month.py` and `scripts/polarisation_month.py` of the
source repository and is the reason the chain reproduces the station's products at ratio 1.0000.

1. **Read** an hour file: int16 little-endian, ×10/2¹⁵ → volts. Timestamp from the `_info.txt`.
2. **Slot** the hour into six 10-minute pieces of 153,600 samples.
3. **Window** each slot into 119 segments of 2560 samples (10 s) at 50 % overlap. Hann window
   `1 − cos²(πn/N)` normalised to unit mean power.
4. **Saturation**: any segment containing a sample with |V| > 9.99 is dropped; the dropped fraction is
   the `sat` column. If every segment is dropped the slot is empty (NaN).
5. **FFT** each segment zero-padded to 8192 points (31.25 mHz bins); accumulate |X|².
6. **Amplitude spectral density** `sqrt(Σ|X|² · 2 / (n_kept · 256 · 2560))`, DC bin divided by √2.
7. **Calibrate** by multiplying with Scal(f) (see station-and-calibration.md). Keep 6–25 Hz.
8. **Anthropogenic filter**: in bands 14.55–15.35 Hz and 16.50–16.90 Hz, if the relative deviation
   from a straight line exceeds 2.5× that of the reference bands 13.5–13.9 / 15.8–16.4 Hz, replace the
   band with the line.
9. **Lorentzian fit** over 6.35–23.75 Hz, amplitude domain:
   `Σₖ aₖ / (1 + ((f − fₖ)/sₖ)²) + m·f + n`, k = 1..3, seeds f = 8.011 / 14.2 / 20.63 Hz,
   s = 1.78 / 1.94 / 2.56 Hz, aₖ = the month-mean spectrum at the seed, Levenberg–Marquardt, unbounded.
   Output per mode: centre `f_hz`, `peak` = model value at the centre, `a`, `halfwidth_hz` = |s|, `chi2`.
   The station uses lmfit, we use SciPy's LM; a few percent of slots land on different local minima, so
   `masked` flags fits outside 6.5–9.5 / 12.5–16 / 18.5–22.5 Hz or widths outside 0.3–5 Hz.
10. **Polarisation** (separate pass over the NS/EW pair): same windows, cross-spectrum
    Sxy = ⟨X·conj(Y)⟩ with segments dropped if saturated in either coil; averaged over ±0.5 Hz about each
    mode's fitted centre;
    `az = ½·atan2(2 Re Sxy, Sxx − Syy)`, ellipticity from `tan(2χ) = 2 Im Sxy / √((Sxx−Syy)² + 4 Re² Sxy)`,
    coherence `|Sxy|² / (Sxx·Syy)`. The calibration cancels in these ratios. Azimuth is axial: the
    horizontal magnetic field of a distant ELF source is azimuthal about the source, so the source
    bearing is roughly az + 90°, with a 180° ambiguity.

Month files: `SN_<YYYYMM>_<sensor>` in the derived store; the dataset tables are one-to-one with them.
