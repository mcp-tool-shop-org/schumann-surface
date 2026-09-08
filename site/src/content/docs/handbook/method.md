---
title: Method and verification
description: The pinned processing chain, the calibration constants, and the receipt against the station.
sidebar:
  order: 4
---

## The station

Sierra Nevada ELF station, University of Granada, 37.04 N 3.32 W, 2500 m. Two induction-coil
magnetometers, NS and EW. 256 Hz sampling (period 3906 µs, so an hour file of 921,600 samples lasts
3599.77 s and drifts 0.23 s per hour), 16-bit over ±10 V, 19 µV/pT at 10 Hz before the ×2500
amplifier, 28 dB signal-to-noise for 1 pT in the 6–25 Hz band.

## Calibration

The coil, cabling and amplifier form an RLC circuit. With the constants in the station's code,
L = 298 kH, C = 40 + 0.65·55 + 2 = 77.75 pF and R = 320 kΩ, the resonance sits at

```
f0 = 1 / (2π √(LC)) = 33.06 Hz,   δ = (R/2) √(C/L) = 2.58 × 10⁻³
```

The method paper prints only the 40 pF sensor capacitance, which would put f0 at 46 Hz; only the
code's constants reproduce the station's spectra. Amplitude-only calibration:

```
Scal(f) = 1e12 / (2500 · 1.9e6) · √((1 − (f/f0)²)² + (2 δ f/f0)²) / f      [pT/√Hz per V/√Hz]
```

1/2500 removes the amplifier gain, 1/1.9e6 is the sensitivity, 1/f is Faraday's law for an
induction coil, and the square root undoes the RLC response. Phase is not calibrated because a
tenth-order Butterworth against 50 Hz mains makes it unreliable.

## The chain, pinned

1. Volts = counts · 10 / 2¹⁵. Saturation is |V| > 9.99 V.
2. Each 10-minute slot is 119 windows of 2560 samples (10 s) at 50 % overlap, Hann with unit mean
   power, zero-padded to an 8192-point FFT (31.25 mHz bins). Windows containing a saturated sample
   are dropped; the dropped fraction is `sat`.
3. Amplitude spectral density `√(Σ|X|² · 2 / (n_kept · 256 · 2560))`, DC bin over √2, times Scal(f).
4. Anthropogenic bands 14.55–15.35 and 16.50–16.90 Hz are straight-lined when their relative
   deviation exceeds 2.5× that of reference bands 13.5–13.9 and 15.8–16.4 Hz.
5. Three Lorentzians plus a linear term, `Σ aₖ/(1+((f−fₖ)/sₖ)²) + m f + n`, fitted in the amplitude
   domain over 6.35–23.75 Hz with Levenberg–Marquardt, seeds 8.011 / 14.2 / 20.63 Hz, widths
   1.78 / 1.94 / 2.56 Hz. A fit is masked if it leaves 6.5–9.5, 12.5–16 or 18.5–22.5 Hz or its
   half-width leaves 0.3–5 Hz.
6. Polarisation from the NS × EW cross-spectrum averaged ±0.5 Hz about each fitted centre:
   `az = ½·atan2(2 Re Sxy, Sxx − Syy)`, ellipticity from the imaginary part, coherence
   `|Sxy|²/(Sxx Syy)`. The calibration cancels in these ratios.

## Verification against the station

The station publishes its own processed products (CC BY-NC-ND, used here only as a verifier).
Slot by slot:

| | Oct 2013 NS | Oct 2013 EW | Jun 2013 NS | Jun 2013 EW |
|---|---|---|---|---|
| spectrum ratio ours/station, p5 and p95 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| saturation correlation | 1.000 | 1.000 | 1.000 | 1.000 |
| mode-1 centre, median difference | +0.004 Hz | +0.008 Hz | +0.004 Hz | −0.02 Hz |

The verifier is a gate: it exits 2 unless at least 95 % of slots match within 30 s, the ratio's 5th
and 95th percentiles sit within 1 ± 0.005, each mode's median frequency difference is under
0.02 Hz, and the saturation series correlate above 0.99. The residual frequency scatter is two
Levenberg–Marquardt implementations choosing different local minima on a few percent of slots.

Independent of the station, the repository's tests check that a 10 mV tone is recovered at its
frequency, saturated windows are dropped, the Hann window has unit power, and three synthetic
Lorentzians are recovered to within 0.03 Hz.
