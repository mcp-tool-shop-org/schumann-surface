# schumann-surface · handoff 01 · Claude → Grok Build

Paste target: **Grok Build** (executor). Reply file: `docs/handoffs/schumann-02-grok-to-claude.md`.
Repo: `mcp-tool-shop-org/schumann-surface`, branch `main`, head `7beda8b`. Local clone `E:/AI/schumann-surface`.
Round: 1 of an alternating polish loop (Grok → Claude → Grok …). This round Grok owns
`viewer/template.html` only. Claude owns `scripts/`, `data/`, `tests/`, README. Don't cross the line;
ask for data fields instead (see "What to say back").

## Standards compliance (this handoff)

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Three.js pinned r128 on cdnjs; data contract below is versioned by field list; no other libraries without pinning. |
| ANDON_AUTHORITY | 2 | Any regression in the correlation panel's numbers (r, N_eff, band) on the shipped Oct 2013 data halts the round; the stats code is out of scope for edits. |
| NAMED_COMPENSATORS | 2 | No irreversible calls. Undo = `git revert` on `viewer/template.html`; `python scripts/build_viewer.py 1310` regenerates `index.html`/`artifact.html`. Owner: Claude. |
| DECOMPOSE_BY_SECRETS | 3 | Viewer (Grok) and data chain (Claude) are separate files with one JSON seam. |
| UNCERTAINTY_GATED_HUMANS | 2 | Director reviews the artifact at the end of each round; the handoff names the questions only the Director can answer. |
| EXTERNAL_VERIFIER | 2 | Claude verifies Grok's round against the brief and the data contract before republishing; Grok does the same on Claude's rounds. |

## Where we are

Step 1 proved the data path: October 2013 from the Sierra Nevada ELF station, reproduced against the
station's own published spectra and Lorentzian fits at ratio 1.0000 and mode frequencies within
hundredths of a hertz. The viewer today is a height-mapped spectrogram (time × frequency × dB) with
NS/EW sheets, mode ribbons, Kp / night / earthquake lanes, and a lagged cross-correlation panel with
a Bartlett-corrected null band. It renders and it is honest. It is also, as the Director noted on
review, a 3D view of a 2D graph rather than a 3D representation of the phenomenon.

Hard data limits you must respect (measured, see README): this station's usable band is 6–25 Hz,
so only modes 1–3 exist in the data. Higher modes need a different station. Do not fake them.

## Director's review, paraphrased (never quote the Director in any artifact)

1. The 3D should be the object being measured, not an extruded chart.
2. The "Spectrum at cursor" panel moves erratically under the mouse and is nauseating.
3. Every view we build stays selectable as a mode. Nothing is thrown away.

## What to research first (cite: author, year, title, URL, one-sentence finding)

- The physical picture of the modes: Schumann resonances as standing waves in the Earth–ionosphere
  shell, the mode fields as Legendre functions of source–observer angle, and why amplitude at a
  station depends on distance to the active thunderstorm region. Start with Nickolaenko & Hayakawa
  2002 (*Resonances in the Earth-Ionosphere Cavity*), Sentman 1995 (Handbook of Atmospheric
  Electrodynamics), Williams 1992 (*Science*, SR as a tropical thermometer).
- The diurnal source schedule: the three chimneys (Southeast Asia ~08 UTC, Africa ~14 UTC,
  Americas ~20 UTC) and their seasonal shift. Find the canonical source and its numbers.
- Three.js techniques for (a) a shell with an animated scalar field (vertex displacement or shader
  colour on a sphere), (b) a small volume: stacked translucent slabs vs marching-cubes iso-surfaces,
  and what stays interactive at ~1500 × 150 × 31 samples.
- Motion-sickness guidance for 3D UIs: what makes hover-driven redraws nauseating and the standard
  fixes (click-to-pin, damped camera, fixed axes, reduced-motion honouring).

Cap: 600 words of research notes in the reply, specific over broad.

## What to build (this round)

1. **Fix the cursor panel first.** Hover shows only a thin cursor line on the surface and the
   tooltip. The spectrum panel updates on click (pinned) and on keyboard left/right stepping.
   Fixed dB axis from the sheet's lo/hi, never rescaled per column. Honour `prefers-reduced-motion`.
   Damp the orbit camera (inertia with a short time constant, or none, but no snapping).
2. **View modes, selectable, all kept.** A mode switcher at the top of the side panel:
   - **Surface** — what exists now.
   - **Day stack** — fold time into hour-of-day × day-of-month × frequency. The 24-hour rhythm becomes
     a structure you can see across the block: the mode ridges are sheets through the volume and
     storm days are where the sheets deform. Render as stacked translucent slabs or an iso-surface at
     a chosen dB, with a threshold control.
   - **Cavity** — Earth as a globe with an exaggerated ionosphere shell. At the scrubbed time, draw the
     measured mode amplitudes as standing-wave patterns on the shell (mode n as the n-th Legendre
     pattern from the active chimney), the three chimneys pulsing on their UTC schedule, the day/night
     terminator, the station marker, and Kp as a tint on the polar shell. The data drives it: the
     mode amplitudes, frequencies and widths per column are already in the JSON (`modes.NS`,
     `modes.EW`); the NS/EW ratio gives you a crude arrival bearing.
   - **Trajectory** — cheap and honest: mode-1 frequency × mode-1 amplitude × time as a path in 3D,
     coloured by Kp. Shows the storm interval as a departure from the daily loop.
3. **One time scrubber** shared by every mode, with the month's Kp strip under it and the
   2013-10-02 03:00 UTC interval marked.
4. Keep the correlation panel and its statistics untouched. Keep the credits and the calibration
   note verbatim.

## Data contract (the `D` object embedded by `scripts/build_viewer.py`)

```
station, lat, lon, month            strings / numbers
t0 (unix s), dt (s per column), nt  1488 columns of 30 min for Oct 2013
f0 (Hz), df (Hz), nf                6.0, 0.125, 152
sheets[] {name NS|EW, lo, hi, u8}   u8 = base64 of nt*nf uint8; 0 = no data, 1..255 -> lo..hi dB re 1 pT/sqrtHz
modes[NS|EW] {f[nt][3], a[nt][3], g[nt][3], sat[nt]}   -1 = masked/no fit; a = peak amplitude pT/sqrtHz, g = half-width Hz
kp[] [t, kp]                        3-hourly, GFZ
quakes[] [t, mag, place]            USGS M6+
storm_t                             unix s of the flagged interval, or null
calnote, credits[]                  text, keep verbatim
```
Need more? Say exactly what, in the reply, and Claude adds it in the next round. Likely candidates:
per-column NS/EW phase or polarisation, chimney schedule as data, a per-day summary table.

## What not to touch

`scripts/*`, `tests/*`, `data/*`, README, the correlation statistics (`series`, `xcorr`, `ac1`,
`drawX`), the calibration note, the licence lines. No new libraries beyond Three.js r128 on cdnjs.
No screenshots-in-a-loop: build, look once, hand back.

## What to say back (in `schumann-02-grok-to-claude.md`)

- Research notes with citations (≤ 600 words).
- The design decisions you made for each mode and why, in ≤ 10 bullets.
- Any data fields you need from the chain, named precisely.
- What you did not finish and why.
- A one-line verification: does `python scripts/build_viewer.py 1310` still produce a page whose
  correlation panel prints the same r / N_eff / band as before your changes.
