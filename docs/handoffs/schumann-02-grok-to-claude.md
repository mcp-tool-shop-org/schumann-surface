# schumann-surface · handoff 02 · Grok Build → Claude

Round 1 done. Owner this turn: `viewer/template.html` only. Rebuild: `python scripts/build_viewer.py 1310` → `viewer/SN_201310.html` (+ `artifact_201310.html`). `--main` also writes `index.html` / `artifact.html`. Head was `9c2eaa7`.

## Research notes (≤ 600 words)

Schumann resonances are TM standing waves of the Earth–ionosphere shell. A vertical lightning current at angular distance θ from the observer gives \(E_r \propto P_n(\cos\theta)\) and \(H_\varphi \propto P_n^1(\cos\theta)\). Mode n is the n-th Legendre pattern: n wavelengths around the globe. Magnetic field (what this station’s coils measure) is zero at the source and the antipode and peaks on the nodal circles of \(E_r\). A single station’s modal amplitude is source strength times that Legendre weight, so it is not a global storm-power meter.

- Nickolaenko & Hayakawa (2002), *Resonances in the Earth-Ionosphere Cavity*, https://doi.org/10.1007/978-94-017-0395-6 — \(E_r\) and \(H_\varphi\) are Legendre / associated-Legendre in source–observer angle; amplitude is non-monotonic with range.
- Sentman (1995), “Schumann Resonances,” *Handbook of Atmospheric Electrodynamics* I, https://doi.org/10.1201/9780203719503-11 — ELF pulses that circumnavigate form globally coherent quasi-standing waves.
- Williams (1992), “The Schumann Resonance: A Global Tropical Thermometer,” *Science* 256:1184–1187, https://doi.org/10.1126/science.256.5060.1184 — SR intensity tracks tropical temperature because flash rate (the drive) rises nonlinearly with convection.
- Bozóki et al. (2025), *JGR Atmospheres*, https://doi.org/10.1029/2025JD043989 — restates the zonal series: \(B_\Phi \propto \sum P_n^1(\cos\theta)\).

Nodal geometry used on the shell (n = 1, 2, 3 only): \(P_1^1 \propto \sin\theta\) (magnetic antinode at 90° from the storm); \(P_2^1 \propto 3\cos\theta\sin\theta\); \(P_3^1 \propto (5\cos^2\theta-1)\sin\theta\). \(E_r\) nodes of \(P_2\) sit near 54.7° / 125.3°; of \(P_3\) near 39.2° / 90° / 140.8°. Sierra Nevada (~37°N, 3°W) sits on the source-side lobe for a typical African chimney (θ ~ 20–40°), not on a node.

The diurnal clock is Whipple’s three-continent thunderstorm-area curve, recovered in SR intensity at 08 / 14 / 20 UTC.

- Whipple (1929), *QJRMS*, https://doi.org/10.1002/qj.49705522902 — world thunderstorm area peaks with Africa ~14–15 UTC and the Americas ~19–20 UTC; Asia fills morning UTC.
- Christian et al. (2003), *JGR*, https://doi.org/10.1029/2002JD002347 — OTD climatology concentrates lightning in three continental chimneys; Congo is the year-round core.
- Greenberg & Price (2007), *Radio Sci.*, https://doi.org/10.1029/2006RS003477 — SR/ELF amplitude maxima at 08, 14 and 20 UT (Asia, Africa, America).
- Peterson, Mach & Buechler (2021), *JGR*, https://doi.org/10.1029/2020JD033885 — monthly lightning centre migrates N–S; SON pulls Americas and Asia south, Africa stays near the equator.

October-specific UTC peak hours are not published. Annual 08 / 14 / 20 is the right clock. October centroids sit at or south of the equator (MC ~0–8°S 105°E, Congo ~0–5°S 25°E, Amazon ~10–15°S 63°W).

Volume: a 48 × 31 × 152 field is ~226k voxels. Three.js r128 has `DataTexture3D` (WebGL 2) and `ShaderMaterial`; `MarchingCubes` in examples is a metaball demo, not in `three.min.js`. 31 translucent slabs (`depthWrite: false`) stay interactive; 1488 slabs would not. A spherical shell is colour (or vertex displacement) on `SphereGeometry` — colour-only is the reduced-motion path.

- Three.js r128 `DataTexture3D`, https://github.com/mrdoob/three.js/blob/r128/docs/api/en/textures/DataTexture3D.html
- Three.js r128 `OrbitControls.js`, https://github.com/mrdoob/three.js/blob/r128/examples/js/controls/OrbitControls.js — `enableDamping` + `dampingFactor` 0.05 need an rAF update; not in `three.min.js`, so the orbit is custom with the same time constant.

Hover-driven spectrum redraw is vestibular conflict (still inner ear, moving field) and WCAG 2.3.3 animation-from-interaction. Pin on click; hover is a cursor; damp the camera; honour `prefers-reduced-motion`.

- W3C (2023), Understanding SC 2.3.3, https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html — hover/scroll motion must be disableable unless essential.
- Head (2015), “Designing Safer Web Animation For Motion Sensitivity,” https://alistapart.com/article/designing-safer-web-animation-for-motion-sensitivity/ — large relative motion triggers vestibular symptoms; colour/opacity changes do not.
- Laubheimer / NN/g (2020), https://www.nngroup.com/articles/animation-purpose-ux/ — motion hijacks peripheral attention; keep it for feedback, not continuous field updates.

## Design decisions (10)

1. **Cursor vs pin.** Hover moves only a white hairline on the NS/EW sheet and the tooltip. Spectrum, cavity, trajectory marker, stack highlight and scrubber update on click, arrow keys (shift = 1 day), or the shared slider.
2. **Fixed dB axis.** Slice uses the sheet’s `lo`/`hi` with labelled grid; NaNs are gaps, never a floor at 0 and never a per-column rescale.
3. **Camera.** Custom orbit (OrbitControls is not in r128 `three.min.js`). Inertia with damping 0.08 (~120 ms). `prefers-reduced-motion`: 1:1 drag, no coast, no view-switch lerp, no chimney scale easing. CSS kills transitions.
4. **Surface kept.** Existing height map, ribbons 1–3, Kp/night/quake lanes. Copy no longer names 26/33 Hz.
5. **Day stack = slabs, not marching cubes.** 31 `DataTexture` planes (hour × frequency), alpha from a dB threshold. Three mode-ridge meshes (fitted f of modes 1–3) as sheets through the block. MC is not in the pinned library.
6. **Cavity is a one-station inversion, labelled as such.** RGB shell = \(|P_n^1(\cos\theta)|\) × measured NS amplitude × chimney UTC weight, n = 1, 2, 3. NS/EW ratio crudely weights chimneys by predicted \(H_\varphi\) azimuth. Terminator from the same sun model as the night lane. Kp tints |lat| > 55°. Chimney size follows the scrubbed hour, not wall-clock.
7. **Chimney schedule.** Consumes `D.chimneys` when present (contract 2: 08 / 14.5 / 20 UTC, MC 5°N 110°E, Africa 5°N 20°E, Americas 0° 60°W). Fallback is the annual 08 / 14 / 20 table.
8. **Trajectory.** Mode-1 f × a × time, coloured by Kp. Grey helix = month-mean diurnal loop. Yellow sphere at `storm_t`.
9. **One scrubber.** Range input + Kp strip + yellow tick at 2013-10-02 03:00 UTC (`D.storm_t`). All four views read `pin`.
10. **No new library, no higher modes.** Three.js r128 cdnjs only. Shell and ribbons stop at mode 3.

## Data fields wanted from the chain

Already used from contract 2: `chimneys[{name,peak_utc,sigma_h,weight,lat,lon}]`. Not used: `chimney[]` (per-column model series), `diurnal` (I recompute a 48-bin mean for the helix).

Please add, named exactly:

- `chimneys_month[{name,peak_utc,sigma_h,weight,lat,lon}]` — October centroids (Africa ~0–5°S 25°E, Americas ~10–15°S 63°W, MC ~0–8°S 105°E). Annual peaks stay 08 / 14 / 20; the gap is position, not hour.
- `modes.NS.az[nt]` and `modes.EW.az[nt]` or a single `pol[nt]` (radians, source azimuth from NS/EW). The present atan2(EW, NS) on peak amplitudes is the crude bearing; phase would make the cavity less of a cartoon.
- Optional, not blocking: `chimney[]` as a selectable event series in the correlation panel (Claude’s side — I must not touch `series` / `xcorr`).

## Unfinished

- No in-browser visual pass this session (no browser tool). Stack UV vs hour/frequency after `rotation.x = π/2` may be flipped; click-to-pin on the volume is the tell.
- No `DataTexture3D` raymarch / GPU iso. Thresholded slabs only.
- Cavity is didactic, not a three-source least-squares inversion. Polarisation is amplitude-only.
- Chimneys do not walk with day-of-month (need `chimneys_month`).
- Trajectory helix uses 48 half-hour means, not `D.diurnal` (24 h). Harmless; can switch if you want one number.

## Correlation check

`python scripts/build_viewer.py 1310` still prints **r(lag 0) = 0.036, N = 1486, N_eff = 69, 95% band = ±0.236** (mode-1 amplitude NS vs Kp; stays inside the null band). `series` / `xcorr` / `ac1` / `drawX`, the calibration note, and the credits are untouched.
