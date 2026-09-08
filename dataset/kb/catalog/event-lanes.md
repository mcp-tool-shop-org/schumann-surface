# Event lanes: measured vs model
_Kp, earthquakes, terminator, lightning; what is measured, what is modelled, what is unavailable_ · wave 1 · 2026-09-08 · [‹ catalog index](README.md)

5 findings · 3 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| Geomagnetic storm enhancement of Schumann resonance amplitude: a dose-response analysis using the Sierra Nevada ELF archive | Cann · 2026 | Preprint, single author: daily mean mode-1 amplitude rises from 0.345 (Kp<5) to 0.351 (Kp 5–6.7) to 0.366 (Kp≥7), +6.2 %, surviving season and lightning controls. | ✓ |
| Lag correlation mode-1 amplitude vs Kp, Oct 2013 | measured this build · 2026 | r(lag 0) = 0.036, N = 1486, N_eff = 69 (Bartlett), 95 % band ±0.236: inside the null on one month at 30-min resolution. | ✓ |
| Measured diurnal: NS mode-1 amplitude by UTC hour, Oct 2013 | measured this build · 2026 | Per-hour mean NS mode-1 peak runs 0.34 pT/√Hz at 01 UTC to 0.49 at 19–20 UTC, a clean Americas-chimney afternoon peak seen from Spain. | ✓ |
| On the association of the diurnal variation of electric potential gradient in fine weather with the distribution of thunderstorms over the globe | Whipple · 1929 | World thunderstorm area peaks in three continental chimneys, Africa ~14–15 UTC, the Americas ~19–20 UTC, Asia filling the morning UTC hours. | · |
| Seasonal variations in the lightning diurnal cycle and implications for the global electric circuit | Blakeslee, Mach, Bateman, Bailey · 2014 | LIS/OTD-derived global flash rate by UTC hour varies by season; the Carnegie-curve shape is recovered with continental peaks. | · |

## Detail

### Geomagnetic storm enhancement of Schumann resonance amplitude: a dose-response analysis using the Sierra Nevada ELF archive · `load-bearing`
**Preprint, single author: daily mean mode-1 amplitude rises from 0.345 (Kp<5) to 0.351 (Kp 5–6.7) to 0.366 (Kp≥7), +6.2 %, surviving season and lightning controls.**
- **Implication:** The Kp effect is real and small; it needs the lag-correlation panel to show, and will not jump out of a surface.
- **Identifier:** `10.22541/essoar.15002103`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Geomagnetic storm enhancement of Schumann resonance amplitude: a dose-response analysis using the Sierra Nevada ELF archive](https://essopenarchive.org/doi/10.22541/essoar.15002103)

### Lag correlation mode-1 amplitude vs Kp, Oct 2013 · `load-bearing`
**r(lag 0) = 0.036, N = 1486, N_eff = 69 (Bartlett), 95 % band ±0.236: inside the null on one month at 30-min resolution.**
- **Implication:** One month cannot resolve a 6 % effect; the honest display is the null band, and the dataset across 12 months is what could.
- **Identifier:** `schumann-surface build receipt`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Lag correlation mode-1 amplitude vs Kp, Oct 2013](https://github.com/mcp-tool-shop-org/schumann-surface)

### Measured diurnal: NS mode-1 amplitude by UTC hour, Oct 2013 · `load-bearing`
**Per-hour mean NS mode-1 peak runs 0.34 pT/√Hz at 01 UTC to 0.49 at 19–20 UTC, a clean Americas-chimney afternoon peak seen from Spain.**
- **Implication:** The daily rhythm is the first thing a viewer should learn; it is measured, and it is embedded as `diurnal` in the data contract.
- **Identifier:** `schumann-surface build receipt`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Measured diurnal: NS mode-1 amplitude by UTC hour, Oct 2013](https://github.com/mcp-tool-shop-org/schumann-surface)

### On the association of the diurnal variation of electric potential gradient in fine weather with the distribution of thunderstorms over the globe · `directional`
**World thunderstorm area peaks in three continental chimneys, Africa ~14–15 UTC, the Americas ~19–20 UTC, Asia filling the morning UTC hours.**
- **Implication:** The chimney schedule lane is a model built on this structure and is labelled as such wherever shown.
- **Identifier:** `10.1002/qj.49705522902`
- **Verify:** default unverified (existence may be gated; claim not abstract-NLI-supported)
- **Sources:** [On the association of the diurnal variation of electric potential gradient in fine weather with the distribution of thunderstorms over the globe](https://doi.org/10.1002/qj.49705522902)

### Seasonal variations in the lightning diurnal cycle and implications for the global electric circuit · `directional`
**LIS/OTD-derived global flash rate by UTC hour varies by season; the Carnegie-curve shape is recovered with continental peaks.**
- **Implication:** Weights and hours of the model lane are chosen consistent with this climatology; replacing the model with a measured series is a data decision, not code.
- **Identifier:** `10.1016/j.atmosres.2012.09.023`
- **Verify:** default unverified (existence may be gated; claim not abstract-NLI-supported)
- **Sources:** [Seasonal variations in the lightning diurnal cycle and implications for the global electric circuit](https://doi.org/10.1016/j.atmosres.2012.09.023)

