# Data sources and licences
_Where Schumann resonance exists as numbers, where only as pictures, and under which licence_ · wave 1 · 2026-09-08 · [‹ catalog index](README.md)

6 findings · 5 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| Blitzortung JSON lightning archive (10-minute files) | Blitzortung.org / limaps.org · 2026 | The archive path C{container}/{year}/{month}/{day}/{hour}/{10min}.json answers HTTP 401 without a participant login; 2013 coverage unknown. | ✓ |
| FDSN event web service | USGS · 2026 | GeoJSON query by time window and minimum magnitude returns M6+ events for any 2013 month without a key (16 in October, 8 in June). | ✓ |
| Four-year measurements from Sierra Nevada ELF station (raw time-domain archive) | Salinas, Rodríguez-Camacho, Portí, Carrión, Fornieles-Callejón, Toledo-Redondo · 2022 | The only openly downloadable numeric Schumann resonance source: one 26.5 GB zip of 256 Hz int16 hour files, NS and EW coils, for 2013-03..12 and 2017-01..02, licensed CC BY 4.0. | ✓ |
| Processed 10-minute spectra and Lorentzian fits (Digibug npz archive) | Salinas et al. · 2022 | The station's own processed products (3.58 GB zip of monthly npz, 43 MB each) are CC BY-NC-ND 3.0. | ✓ |
| The geomagnetic Kp index and derived indices of geomagnetic activity | Matzka, Stolle, Yamazaki, Bronkalla, Morschhauser · 2021 | GFZ publishes the full 3-hourly Kp record since 1932 as one CC BY 4.0 text file; October 2013's strongest interval is 2013-10-02 03:00 UTC at Kp 7.67, June 2013 peaks at Kp 7.0. | ✓ |
| GCI magnetometer network spectrograms | HeartMath Institute, Global Coherence Initiative · 2026 | Six sites publish daily spectrogram images only; no numeric API; the Alberta station had been dark ~80 days at the time of checking. | · |

## Detail

### Blitzortung JSON lightning archive (10-minute files) · `load-bearing`
**The archive path C{container}/{year}/{month}/{day}/{hour}/{10min}.json answers HTTP 401 without a participant login; 2013 coverage unknown.**
- **Implication:** No measured global lightning series for 2013 without an account; the viewer carries a labelled model lane instead.
- **Identifier:** `limaps.org/JSON`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Blitzortung JSON lightning archive (10-minute files)](https://www.limaps.org/json-data-archive.html)

### FDSN event web service · `load-bearing`
**GeoJSON query by time window and minimum magnitude returns M6+ events for any 2013 month without a key (16 in October, 8 in June).**
- **Implication:** The earthquake lane exists so its correlation can be shown flat; it is the honesty feature, not a claim.
- **Identifier:** `earthquake.usgs.gov/fdsnws`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [FDSN event web service](https://earthquake.usgs.gov/fdsnws/event/1/)

### Four-year measurements from Sierra Nevada ELF station (raw time-domain archive) · `load-bearing`
**The only openly downloadable numeric Schumann resonance source: one 26.5 GB zip of 256 Hz int16 hour files, NS and EW coils, for 2013-03..12 and 2017-01..02, licensed CC BY 4.0.**
- **Implication:** Derived products built from this archive are publishable with attribution; the range-request extractor makes one month (~2.4 GB) fetchable in ~20 min without the whole zip.
- **Identifier:** `10.5281/zenodo.6348930`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Four-year measurements from Sierra Nevada ELF station (raw time-domain archive)](https://zenodo.org/records/6348930)

### Processed 10-minute spectra and Lorentzian fits (Digibug npz archive) · `load-bearing`
**The station's own processed products (3.58 GB zip of monthly npz, 43 MB each) are CC BY-NC-ND 3.0.**
- **Implication:** Use only as a verifier; never redistribute, never derive a shipped dataset from it.
- **Identifier:** `10481/71563`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [Processed 10-minute spectra and Lorentzian fits (Digibug npz archive)](https://digibug.ugr.es/handle/10481/71563)

### The geomagnetic Kp index and derived indices of geomagnetic activity · `load-bearing`
**GFZ publishes the full 3-hourly Kp record since 1932 as one CC BY 4.0 text file; October 2013's strongest interval is 2013-10-02 03:00 UTC at Kp 7.67, June 2013 peaks at Kp 7.0.**
- **Implication:** Kp is the one geomagnetic lane that needs no account and reaches back to any month in the raw archive.
- **Identifier:** `Kp_ap_since_1932`
- **Verify:** wave-01 verification.md: verified live against the source this session
- **Sources:** [The geomagnetic Kp index and derived indices of geomagnetic activity](https://kp.gfz-potsdam.de/app/files/Kp_ap_since_1932.txt)

### GCI magnetometer network spectrograms · `directional`
**Six sites publish daily spectrogram images only; no numeric API; the Alberta station had been dark ~80 days at the time of checking.**
- **Implication:** A live feed from this network means digitising PNGs with a known colour map, not reading numbers.
- **Identifier:** `nocc.heartmath.org`
- **Verify:** default unverified (existence may be gated; claim not abstract-NLI-supported)
- **Sources:** [GCI magnetometer network spectrograms](https://www.heartmath.org/gci/)

