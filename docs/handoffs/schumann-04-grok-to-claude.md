# schumann-surface · handoff 04 · Grok Build → Claude

Round 2 done. Owner this turn: `viewer/template.html` only.
Rebuild: `python scripts/build_viewer.py 1310 --main` → `viewer/index.html`; `python scripts/build_viewer.py 1306` → `viewer/SN_201306.html`. Head was `8feb69d`.

## Decisions per item

1. **Cavity uses `pol`.** Dropped atan2-of-peak-amplitudes. Mode-1 `az` + π/2 is the source bearing; a second fan at +π is the 180° axial ambiguity. Fan half-width = 0.18 + 0.95·(1 − coh) rad (median October coh ≈ 0.18 → ~53° half-angle, a spread not a needle). Opacity also follows coh. Chimney weights = UTC Gaussian × (0.25 + 0.75 × fan match). Positions from `chimneys_month` (October SON south of the equator; June JJA north). Globe sprite and side-panel copy still say **one-station inversion**. Pin tooltip prints az / coh / fan half-angle.

2. **Month switch.** Header link row `Oct 2013 · Jun 2013` (`index.html` / `SN_201306.html`). Current month is marked, not a link. Day-stack `nD` is the calendar length of `D.month` (31 / 30), so June is not a 31-day block with an empty slab. Kp-strip caption uses `storm_t` when set; June has none, so no yellow tick.

3. **Look-for notes** (side panel, shown with the matching view — please click-check these in round 3):
   - **Cavity.** Two opposite yellow fans from Sierra Nevada. October fans should look fat. Scrub ~14 UTC: Africa (green) in a fan. ~20 UTC: Americas (blue). October chimney dots south of the equator; June north. Tooltip has az/coh.
   - **Trajectory.** Grey helix = diurnal loop (`diurnal` amplitudes). Coloured path is the data, Kp as colour. June vs October: loop amplitude and hour of the daily bulge should move. Yellow bead only when `storm_t` is set (Oct 2 03:00). Leaving the helix is a departure, not a fourth mode.

4. **Helix from `diurnal` (optional, done).** Amplitude of the grey loop is `D.diurnal.NS[hour][0]`. Frequency is still the hour-bin mean of fitted mode-1 *f*, because `diurnal` has no frequency.

`series` / `xcorr` / `ac1` / `drawX` were not edited. Calibration note and credits untouched. Modes 1–3 only.

## Data fields needed

Nothing blocking. Useful later, not this round:

- `diurnal` frequency (or `diurnal_f[24][3]`) so the helix does not mix two sources.
- `storm_t` for June if the 1 June Kp 7.0 interval should get a yellow bead (currently null).
- Optional: per-mode fans. Only mode 1 is drawn; 2 and 3 still colour the shell.

## Unfinished

- No browser pass here. Cavity fans and the June/October helix are the round-3 click-check.
- Fans are mode-1 only.
- Helix *f* is not in `diurnal`.
- June has no `storm_t`, so the trajectory storm marker is absent on that page.

## Correlation check

Oct 2013 correlation panel still prints **r(lag 0) = 0.036, N = 1486, N_eff = 69, 95% band = ±0.236**.
