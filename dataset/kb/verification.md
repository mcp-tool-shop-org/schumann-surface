# Verification receipt

The chain was checked slot by slot against the station's own published products (Digibug
10481/71563, CC BY-NC-ND, used only as a verifier and not redistributed). The verifier script exits
non-zero unless: ≥ 95 % of slots match within 30 s; the 5th and 95th percentiles of the spectrum ratio
sit within 1 ± 0.005; each mode's median frequency difference is under 0.02 Hz; the saturation series
correlate above 0.99.

| Month, sensor | slots matched | spectrum ratio p5 / median / p95 | sat corr | mode 1 / 2 / 3 median Δf (Hz) | peak ratio median |
|---|---|---|---|---|---|
| 2013-10 NS | 4464 / 4464 | 1.0000 / 1.0000 / 1.0000 | 1.000 | +0.004 / +0.000 / −0.000 | 1.001 / 1.000 / 1.000 |
| 2013-10 EW | 4464 / 4464 | 1.0000 / 1.0000 / 1.0000 | 1.000 | +0.008 / +0.002 / +0.001 | 1.001 / 1.000 / 1.000 |
| 2013-06 NS | 4320 / 4320 | 1.0000 / 1.0000 / 1.0000 | 1.000 | +0.004 / ≤0.01 / −0.001 | 1.000 / 1.000 / 1.000 |
| 2013-06 EW | 4320 / 4320 | 1.0000 / 1.0000 / 1.0000 | 1.000 | −0.02 / ≤0.03 / +0.000 | 1.000 / 1.000 / 1.000 |

The spectra agree to the last printed digit because the chain uses the station's exact window,
normalisation, calibration constants and filter. The small frequency scatter is two Levenberg–Marquardt
implementations (lmfit at the station, SciPy here) choosing different local minima on a few percent of
slots; `masked` marks those that leave the per-mode windows.

Independent of the station's outputs, synthetic tests in the repository check that a 10 mV tone is
recovered at its frequency, that saturated windows are dropped, that the Hann window has unit power,
and that three synthetic Lorentzians are recovered to within 0.03 Hz.
