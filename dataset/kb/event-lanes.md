# Event lanes: what is measured and what is a model

| Lane | Table / column | Kind | Source | Notes |
|---|---|---|---|---|
| Geomagnetic activity | `lanes.kp` | measured | GFZ Potsdam Kp, 3-hourly, CC BY 4.0 (Matzka et al. 2021) | The value of the 3-hour interval containing the slot. October 2013's strongest interval is 2013-10-02 03:00 UTC, Kp 7.67; June 2013 peaks at 7.0 on 2013-06-01. |
| Local night | `lanes.night_fraction` | computed | Solar elevation at the station from the timestamp (NOAA-style low-precision ephemeris) | Fraction of the slot with the sun below −6°. |
| Earthquakes | `lanes.quake_count_24h`, `quake_max_mag_24h` | measured | USGS FDSN event service, M ≥ 6 | Trailing 24 h. Included so that its correlation can be shown flat; there is no physical mechanism expected. |
| Thunderstorm chimneys | `model.chimney_model` | **model** | Whipple 1929 structure; UTC peaks and weights consistent with the LIS/OTD diurnal climatology (Blakeslee et al. 2014) | Three Gaussians in UTC hour: Southeast Asia 08, Africa 14.5, Americas 20; σ = 2.5 h; weights 0.8 / 1.0 / 0.9. Not a measurement. |

## Why there is no measured lightning lane

No openly downloadable measured global lightning series exists for 2013. WWLLN is subscription;
the Blitzortung JSON archive answers HTTP 401 without a participant login; NASA's LIS/OTD
climatologies now sit behind an Earthdata login. Adding a measured series is a data decision and a
join on `t_utc`, not a code change.

## What the measured record itself says about the daily rhythm

The per-UTC-hour mean of the NS mode-1 peak amplitude in October 2013 rises from about 0.34 pT/√Hz at
01 UTC to 0.49 pT/√Hz at 19–20 UTC: the Americas chimney afternoon, seen from Spain. That curve is
computable from `modes` in one line and is the first thing the data should teach.

## What Kp does, honestly

A 2026 preprint on this same archive (Cann, ESS Open Archive, doi:10.22541/essoar.15002103) reports
mode-1 amplitude rising about 6 % on Kp ≥ 7 days after season and lightning controls. One month at
30-minute resolution cannot resolve that: mode-1 amplitude versus Kp in October 2013 gives
r(lag 0) = 0.036 with a Bartlett-corrected 95 % null band of ±0.24. The full twelve months are what
could. Show the null band; a curve inside it is a result.
