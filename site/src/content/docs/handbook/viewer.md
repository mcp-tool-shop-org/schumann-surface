---
title: The viewer
description: Four modes, the lanes, the scrubber, and the correlation panel.
sidebar:
  order: 2
---

Everything on the page reads one pinned moment. Click the surface, press the arrow keys
(shift steps a day), or drag the scrubber; hovering only moves a hairline and the tooltip, so the
page never redraws under your mouse.

## Modes

**Surface.** Time runs left to right across the month in 30-minute columns, frequency runs front
to back from 6 to 25 Hz in 0.125 Hz rows, and height and colour are amplitude in dB re 1 pT/√Hz.
The NS and EW coils are two sheets you can stack. Three ribbons ride the surface at the fitted
centre frequency of modes 1, 2 and 3.

**Day stack.** The month folded into hour-of-day × day-of-month × frequency, drawn as translucent
slabs with a dB threshold. The daily lightning rhythm becomes a shape through the block, and the
mode ridges become sheets that deform on storm days.

**Cavity.** An Earth with an exaggerated ionosphere shell. The measured mode amplitudes at the
pinned moment paint standing-wave patterns on the shell, the three thunderstorm chimneys pulse on
their UTC schedule at their seasonal positions, the terminator moves with the clock, and the
station's measured polarisation draws the source bearing as two opposite fans whose width follows
the NS/EW coherence. It is labelled a one-station inversion because that is what it is.

**Trajectory.** Mode-1 frequency × amplitude × time as a path, coloured by Kp, against a grey helix
of the month's mean daily loop. The storm interval is where the path leaves the loop.

## Lanes

In front of the surface, along the time axis:

- **Kp** (GFZ, 3-hourly): blue under 4, amber 4 to 5, red at 5 and above.
- **Night** at the station, computed from the timestamp.
- **Earthquakes** M6+ (USGS) as spheres sized by magnitude.

## Spectrum at pin

A fixed-axis slice of the pinned column with the three fitted centres marked. The axis never
rescales per column; gaps are gaps.

## Correlation, with the null shown

Pick a surface series (a mode's amplitude or frequency, a band power) and an event series (Kp,
night fraction, earthquakes, or the chimney model, which is labelled as a model). The panel draws
Pearson r against lag from −24 to +24 hours and shades the 95 % null band using an effective
sample size corrected for autocorrelation in both series (Bartlett). A curve that stays inside the
band is a null result, and the panel says so.

For October 2013, mode-1 amplitude against Kp reads r = 0.036 at lag 0 with N_eff = 69 and a band
of ±0.236. That is the honest answer for one month; the storm effect on this archive is about 6 %,
which twelve months could resolve and one cannot.

## Months

The header switches between the months that have been built. Each month is its own self-contained
page.
