# schumann-surface · handoff 06 · Grok Build → Claude

Round 3 done. Owner this turn: `viewer/template.html` only.
Rebuild: `python scripts/build_viewer.py 1310 --main` and `python scripts/build_viewer.py 1306`.
Copied into `site/public/viewer/` (`index.html`, `SN_201306.html`) so Pages `/viewer/` is the live path.

## Decisions

1. **Cavity size, brightness, fans.** The fans were drawn at Earth radius (90) while the shell sits at 118, so from the default camera they showed as two thin spines through a dark ball. They now live on the shell (`FAN_R = RI+5`) as translucent wedges with a centre spine and a closed bright edge. Opacity floor is 0.28 (was ~0.16 at October coh). The shell has a steel-blue base albedo so the Legendre pattern modulates a visible globe, not a black void; Earth, ambient light, and chimney markers (with halos, on the shell) are lifted to match. Default camera: dist 250 (was 380), more equatorial (`phi` 1.22), so the globe fills most of the canvas; wheel still zooms.

2. **Trajectory as a coil, not a streak.** Time is compressed 6× by default (`tX = SX / 6`), so one day is a short step against the f × a plane (~267 units for the month vs ~220–260 for amplitude/frequency). The diurnal mean is a light tube (`TubeGeometry`), not a grey polyline. The storm is a large yellow bead with a halo and a `storm` label. A **Time compression** slider (1–10×) is on the Trajectory panel if someone wants the raw month-long streak. Camera dist 520 aimed at the coil.

Elsewhere: look-for notes for those two views were updated to match the new rest state. `series` / `xcorr` / `ac1` / `drawX` untouched. Modes 1–3 only. No new libraries.

## Correlation check

Oct 2013 correlation panel still prints **r(lag 0) = 0.036, N = 1486, N_eff = 69, 95% band = ±0.236**.
