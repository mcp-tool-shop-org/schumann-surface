---
title: Honesty rules
description: Measured versus model, one-station geometry, and how to read a null result.
sidebar:
  order: 5
---

Most Schumann resonance content online correlates spikes with earthquakes, mood or planetary
consciousness. The published record says the spikes are lightning, solar events, or sensor faults.
This tool is built so that the honest reading is the easy one.

## Measured versus model

Every lane is labelled. Kp, night, earthquakes, the spectra and the mode fits are measured or
computed from timestamps. The **chimney schedule** is a model: three Gaussians in UTC hour for
Southeast Asia (08), Africa (14.5) and the Americas (20), after Whipple 1929 and the LIS/OTD
diurnal climatology. It exists because no openly downloadable measured global lightning series
exists for 2013: WWLLN is subscription, the Blitzortung archive needs a participant login, and
NASA's climatology sits behind Earthdata. The model lives in its own dataset config and its own
correlation entry so it is never mistaken for data.

## One station is not a storm-power meter

The magnetic field of a distant ELF source at a station goes as an associated Legendre function of
the angle between them, so a change in amplitude can be geometry rather than source strength. The
cavity view is labelled a one-station inversion for that reason, and the polarisation bearing is
drawn as a fan whose width is the measured spread, not as a needle.

## Reading a correlation

1. Use lagged correlation; Kp is 3-hourly and the ionosphere responds with delay.
2. Correct the sample size for autocorrelation. Bartlett's `N_eff = N(1 − r₁r₂)/(1 + r₁r₂)` turns a
   month of 30-minute samples into a few dozen effective ones.
3. Draw the 95 % band at ±1.96/√N_eff. A curve inside it is a null result, and the panel says so.
4. Remove the daily cycle before correlating with anything that has one, or you measure the clock.
5. Never correlate against the model lane and call it lightning.

The known storm effect on this archive is about 6 % on Kp ≥ 7 days (a 2026 preprint on the same
data). One month cannot resolve that. Twelve months, which the pipeline can produce, could.

## Trust and data

The pipeline runs locally from a checkout and touches only `data/` and `viewer/`. Network access
happens only when a script is asked to fetch from Zenodo, Digibug, GFZ or USGS. No credentials are
read or stored; no telemetry is sent; the viewer is a static page. Security reports go to the
address in `SECURITY.md`.
