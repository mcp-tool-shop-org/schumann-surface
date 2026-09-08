# Viewer data contract

The `D` object that `scripts/build_viewer.py` embeds into `viewer/template.html` at `/*__DATA__*/`.
Station-agnostic: a second station only has to produce the same fields. `contract` bumps when a field
changes meaning; adding fields does not bump it.

## contract 4 (2026-09-08, later)

Adds `year`: one row per calendar day across every processed month, so a single month page can carry
the twelve-month picture. Contract 3 added `pol` (per-column polarisation) and `chimneys_month`.

| Field | Type | Meaning |
|---|---|---|
| `year.days[]` | `{date, n, NS?, EW?, kp_max, kp_mean}` | per day: `n` slots that day; per sensor `f[3]` mean centre Hz, `a[3]` mean peak pT/√Hz, `amed[3]` median peak, of unmasked fits; `kp_max`/`kp_mean` from the GFZ 3-hourly values; −1 or null = no data |
| `year.note` | str | what it is for and the known effect size to test against |
| `pol` | `{az[nt][3], ell[nt][3], coh[nt][3], note}` | per column, per mode: axial polarisation angle (radians from NS towards EW), ellipticity, NS/EW coherence; −9 = no data |
| `chimneys_month[]` | as `chimneys` plus `season` | seasonal centroids (position only; the UTC clock stays annual) |
| `contract` | int | 4 |

## contract 2 (2026-09-08)

| Field | Type | Meaning |
|---|---|---|
| `contract` | int | 2 |
| `station`, `lat`, `lon` | str, °, ° | station name and position (east positive) |
| `month` | "YYYY-MM" | the month rendered |
| `t0`, `dt`, `nt` | unix s, s, int | column grid: column i starts at `t0 + i*dt` |
| `f0`, `df`, `nf` | Hz, Hz, int | row grid: row j is `f0 + j*df`; for Sierra Nevada 6.0 / 0.125 / 152 |
| `sheets[]` | `{name, lo, hi, u8}` | one per sensor (NS, EW). `u8` is base64 of `nt*nf` bytes, row-major by column; 0 = no data; 1..255 map linearly to `lo..hi` dB re 1 pT/√Hz (amplitude, 20·log10) |
| `modes[name]` | `{f, a, g, sat}` | per sheet, per column: `f[nt][3]` centre frequency Hz, `a[nt][3]` peak amplitude pT/√Hz, `g[nt][3]` half-width Hz, `sat[nt]` saturated-window fraction. −1 = no fit or masked |
| `kp[]` | `[t, kp]` | 3-hourly GFZ Kp, interval start |
| `quakes[]` | `[t, mag, place]` | USGS M6+ |
| `storm_t` | unix s or null | an interval the page opens on |
| `chimneys[]` | `{name, peak_utc, sigma_h, weight, lat, lon}` | the three thunderstorm regions as a schedule. Model, not measurement |
| `chimney[nt]` | float | the schedule evaluated per column: sum of Gaussians in UTC hour. Model lane |
| `diurnal[name]` | `[24][3]` | measured: per-UTC-hour mean of each mode's peak amplitude over the month, per sheet |
| `calnote`, `credits[]` | str | keep verbatim in the page |

## Provenance of the model lane

There is no openly downloadable measured global lightning series for 2013: WWLLN is subscription,
the Blitzortung JSON archive answers 401 without a participant login, and NASA's LIS/OTD climatology
moved behind Earthdata login. The chimney schedule follows the structure known since Whipple 1929
(thunderstorm-day diurnal curves by continent) and the Carnegie curve (Harrison 2013, *Surveys in
Geophysics* 34:209), with UTC peaks and weights consistent with the LIS/OTD diurnal climatology
(Blakeslee, Mach, Bateman & Bailey 2014, *Atmospheric Research* 135–136:228). It is labelled a model
wherever it is shown. Replacing it with a measured series is a data decision, not a code change.
