# schumann-surface · handoff 08 · Grok Build → Claude

Round 4 done. Owner this turn: `viewer/template.html` only.
Rebuild: `python scripts/build_viewer.py 1310 --main` and `python scripts/build_viewer.py 1306`.
Copied `index.html` and `SN_201306.html` into `site/public/viewer/`.

## Decisions

Cavity rest state is a **2D canvas atlas** (no orbit). Projection: azimuthal equidistant, Sierra Nevada at the centre, rim = 180° (antipode), north up, east right.

- **Rings.** |Pₙ¹(cos θ)| × pinned NS amplitudes, θ = radius from the station. Mode 1 red, 2 green, 3 blue. Dark ground; the pattern is the light. No competing base fill.
- **Gold slices.** Mode-1 `pol.az + π/2`, two opposite wedges, half-width from `coh` (October ~0.18 → ~55° half-angle). Strongest colour on the page. This is the measurement.
- **Chimneys.** `chimneys_month` projected by great-circle range and initial bearing from the station, labelled (Africa / Americas / SE Asia), disc size = UTC model at the pinned hour. Caption says they are a model, not a lightning map.
- **Terminator** from the same sun model; **Kp** is the outer rim colour.
- **No coastlines** (labels beat them; no extra polyline set).
- **Globe** remains a toggle in the Cavity panel. Same `pol`, same chimneys, same scrubber. WebGL is hidden while the atlas is up.

`series` / `xcorr` / `ac1` / `drawX`, calibration note, and credits were not edited. Modes 1–3 only. No new library.

## Contract

Nothing blocking. Optional later: `diurnal` frequency (still unused here). Chimney-centred standing waves would not be circles in this projection; the Director asked for station-centred rings, so that is what is drawn.

## Unfinished

No browser pass this session. Please click-check: gold slices fat at rest, Africa in a slice near 14 UTC, Americas near 20 UTC, June vs October chimney range, Globe toggle still paints the sphere without a console error.

## Correlation check

Oct 2013 correlation panel still prints **r(lag 0) = 0.036, N = 1486, N_eff = 69, 95% band = ±0.236**.

## At rest, Cavity, nothing touched

A dark disc with Sierra Nevada in the middle, concentric red/green/blue mode rings, two fat gold pie slices for the measured bearing, and three named chimney discs sitting at their true range and bearing; Kp is the coloured rim.
