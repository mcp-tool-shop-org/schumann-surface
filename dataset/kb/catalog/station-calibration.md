# Station and calibration
_The Sierra Nevada ELF station: sensor model, calibrated band, why higher modes are unreachable_ · wave 1 · 2026-09-08 · [‹ catalog index](README.md)

4 findings · 3 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| Raw counts rise ~40x from 6 to 25 Hz and hump at 30–33 Hz | measured this build · 2026 | In raw counts the 8 Hz mode sits at ~3e3 counts²/Hz while 33 Hz reaches 2.4e5: the sensor resonance dominates above 25 Hz. | ✓ |
| Schumann resonance data processing programs and four-year measurements from Sierra Nevada ELF station | Salinas, Rodríguez-Camacho, Portí, Carrión, Fornieles-Callejón, Toledo-Redondo · 2022 | The magnetometers are calibrated for 6–25 Hz only; the calibration is amplitude-only because the tenth-order 50 Hz Butterworth makes the phase unreliable; Scal(f) = 1e12/(2500·1.9e6)·sqrt((1-(f/f0)^2)^2+(2δf/f0)^2)/f. | ✓ |
| Sierra_Nevada_SR: Reading_Fourier.py constants | Salinas & Rodríguez-Camacho (station code) · 2022 | The code uses C_total = 40 + 0.65·55 + 2 pF = 77.75 pF (the paper prints 40 pF), giving a coil resonance f0 = 33.06 Hz and δ = 2.58e-3; volts = counts·10/2^15; saturation /V/ > 9.99. | ✓ |
| Extremely low frequency band station for natural electromagnetic noise measurement | Fornieles-Callejón et al. · 2015 | Two induction-coil magnetometers (NS, EW) at 2500 m in Sierra Nevada, 19 µV/pT at 10 Hz, 28 dB SNR for 1 pT, 256 Hz sampling, lower band limit 6 Hz to avoid 1/f noise. | · |

## Detail

### Raw counts rise ~40x from 6 to 25 Hz and hump at 30–33 Hz · `load-bearing`
**In raw counts the 8 Hz mode sits at ~3e3 counts²/Hz while 33 Hz reaches 2.4e5: the sensor resonance dominates above 25 Hz.**
- **Implication:** Modes 4+ are not resolvable from this station; a wider-band instrument is required for them.
- **Identifier:** `schumann-surface build receipt`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Raw counts rise ~40x from 6 to 25 Hz and hump at 30–33 Hz](https://github.com/mcp-tool-shop-org/schumann-surface)

### Schumann resonance data processing programs and four-year measurements from Sierra Nevada ELF station · `load-bearing`
**The magnetometers are calibrated for 6–25 Hz only; the calibration is amplitude-only because the tenth-order 50 Hz Butterworth makes the phase unreliable; Scal(f) = 1e12/(2500·1.9e6)·sqrt((1-(f/f0)^2)^2+(2δf/f0)^2)/f.**
- **Implication:** The surface stops at 25 Hz and shows modes 1–3 only; anything above is instrument, not cavity.
- **Identifier:** `10.1016/j.cageo.2022.105148`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Schumann resonance data processing programs and four-year measurements from Sierra Nevada ELF station](https://www.sciencedirect.com/science/article/pii/S0098300422001030)

### Sierra_Nevada_SR: Reading_Fourier.py constants · `load-bearing`
**The code uses C_total = 40 + 0.65·55 + 2 pF = 77.75 pF (the paper prints 40 pF), giving a coil resonance f0 = 33.06 Hz and δ = 2.58e-3; volts = counts·10/2^15; saturation |V| > 9.99.**
- **Implication:** Only the code's constants reproduce the station spectra; the paper's 40 pF would put the resonance at 46 Hz and mis-tilt every spectrum.
- **Identifier:** `asalinas62/Sierra_Nevada_SR`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Sierra_Nevada_SR: Reading_Fourier.py constants](https://github.com/asalinas62/Sierra_Nevada_SR)

### Extremely low frequency band station for natural electromagnetic noise measurement · `directional`
**Two induction-coil magnetometers (NS, EW) at 2500 m in Sierra Nevada, 19 µV/pT at 10 Hz, 28 dB SNR for 1 pT, 256 Hz sampling, lower band limit 6 Hz to avoid 1/f noise.**
- **Implication:** A suburban receiver would not match this site; a coil is a separate hardware decision.
- **Identifier:** `10.1002/2014RS005567`
- **Verify:** default unverified (existence may be gated; claim not abstract-NLI-supported)
- **Sources:** [Extremely low frequency band station for natural electromagnetic noise measurement](https://agupubs.onlinelibrary.wiley.com/doi/10.1002/2014RS005567)

