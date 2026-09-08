# Processing chain
_Welch, saturation, anthropogenic filter, Lorentzian fit, polarisation; verification against the station_ · wave 1 · 2026-09-08 · [‹ catalog index](README.md)

4 findings · 3 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| Anthropogenic filter and Lorentzian fit | Salinas et al. · 2022 | Bands 14.55–15.35 and 16.50–16.90 Hz are replaced by a straight line when their relative deviation exceeds 2.5x that of reference bands; three Lorentzians plus a linear term are fitted in the amplitude domain over 6.35–23.75 Hz with lmfit LM, seeds 8.011/14.2/20.63 Hz and widths 1.78/1.94/2.56 Hz. | ✓ |
| Reproduction against the station npz, Oct and Jun 2013 | measured this build · 2026 | Spectrum ratio ours/station 1.0000 at p5 and p95 over 6–25 Hz for 4464 (Oct) and 4320 (Jun) slots per sensor; saturation correlation 1.000; median mode-frequency differences ≤ 0.008 Hz. | ✓ |
| Welch chain: 10-s Hann windows, 5-s overlap, zero-padded FFT to 8192, saturated windows dropped | Salinas et al. · 2022 | Each 10-min slot is 119 windows of 2560 samples with a unit-power Hann; amplitude = sqrt(sum/FFT/²·2/(n·fs·2560)); any window with a saturated sample is dropped and the fraction recorded. | ✓ |
| Use of the three-dimensional covariance matrix in analyzing the polarization properties of plane waves | Means · 1972 | Polarisation azimuth and ellipticity follow from the NS/EW cross-spectral matrix: az = ½·atan2(2 Re Sxy, Sxx−Syy), ellipticity from the imaginary part. | · |

## Detail

### Anthropogenic filter and Lorentzian fit · `load-bearing`
**Bands 14.55–15.35 and 16.50–16.90 Hz are replaced by a straight line when their relative deviation exceeds 2.5x that of reference bands; three Lorentzians plus a linear term are fitted in the amplitude domain over 6.35–23.75 Hz with lmfit LM, seeds 8.011/14.2/20.63 Hz and widths 1.78/1.94/2.56 Hz.**
- **Implication:** The fit is unbounded; a few percent of slots land on a different local minimum between lmfit and SciPy, so the viewer masks fits outside per-mode windows.
- **Identifier:** `10.1016/j.cageo.2022.105148`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Anthropogenic filter and Lorentzian fit](https://www.sciencedirect.com/science/article/pii/S0098300422001030)

### Reproduction against the station npz, Oct and Jun 2013 · `load-bearing`
**Spectrum ratio ours/station 1.0000 at p5 and p95 over 6–25 Hz for 4464 (Oct) and 4320 (Jun) slots per sensor; saturation correlation 1.000; median mode-frequency differences ≤ 0.008 Hz.**
- **Implication:** The chain is an external-verifier pass (different code, different authors); the verifier now exits non-zero outside stated tolerances.
- **Identifier:** `schumann-surface verify receipt`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Reproduction against the station npz, Oct and Jun 2013](https://github.com/mcp-tool-shop-org/schumann-surface)

### Welch chain: 10-s Hann windows, 5-s overlap, zero-padded FFT to 8192, saturated windows dropped · `load-bearing`
**Each 10-min slot is 119 windows of 2560 samples with a unit-power Hann; amplitude = sqrt(sum|FFT|²·2/(n·fs·2560)); any window with a saturated sample is dropped and the fraction recorded.**
- **Implication:** Pinning exactly these numbers is what makes the reproduction ratio 1.0000; any other window or normalisation drifts.
- **Identifier:** `10.1016/j.cageo.2022.105148`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Welch chain: 10-s Hann windows, 5-s overlap, zero-padded FFT to 8192, saturated windows dropped](https://www.sciencedirect.com/science/article/pii/S0098300422001030)

### Use of the three-dimensional covariance matrix in analyzing the polarization properties of plane waves · `directional`
**Polarisation azimuth and ellipticity follow from the NS/EW cross-spectral matrix: az = ½·atan2(2 Re Sxy, Sxx−Syy), ellipticity from the imaginary part.**
- **Implication:** Per-slot, per-mode azimuth is computable from the raw pair; measured Oct 2013 gives mode-1 azimuth IQR ~20° and NS/EW coherence ~0.17, so bearing is a distribution, not a point.
- **Identifier:** `10.1029/JA077i028p05551`
- **Verify:** default unverified (existence may be gated; claim not abstract-NLI-supported)
- **Sources:** [Use of the three-dimensional covariance matrix in analyzing the polarization properties of plane waves](https://doi.org/10.1029/JA077i028p05551)

