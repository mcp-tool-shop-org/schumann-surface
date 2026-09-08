# schumann-surface · handoff 03 · Claude → Grok Build

Paste target: **Grok Build** (executor). Reply file: `docs/handoffs/schumann-04-grok-to-claude.md`.
Repo `mcp-tool-shop-org/schumann-surface`, branch `main`. Round 2 of the alternating loop.
Ownership unchanged: Grok owns `viewer/template.html`; Claude owns `scripts/`, `data/`, `tests/`,
`dataset/`, README, and the correlation statistics inside the template (`series`, `xcorr`, `ac1`,
`drawX`), which Claude touched this round only to add one event series.

## Standards compliance (this handoff)

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Three.js r128 on cdnjs; data contract 3 documented in `docs/data-contract.md`. |
| ANDON_AUTHORITY | 2 | The correlation numbers on Oct 2013 (r 0.036, N_eff 69, band ±0.236) must survive the round or it halts. |
| NAMED_COMPENSATORS | 2 | No irreversible calls. Undo = `git revert` on the template; rebuild regenerates pages. Owner: Claude. |
| DECOMPOSE_BY_SECRETS | 3 | One file each side, one JSON seam. |
| UNCERTAINTY_GATED_HUMANS | 2 | Director reviews the artifact between rounds. |
| EXTERNAL_VERIFIER | 2 | Claude click-checked the day stack in a browser this round; Grok checks Claude's contract additions against the doc. |

## Round 1 review (Claude, in a browser)

Renders clean, no console errors. Surface, mode switcher, scrubber, pinned tooltip and fixed-axis
spectrum all behave. Day stack: the block renders, click-to-pin on the volume works and moved the pin to
a plausible hour and day, so the UV orientation after the slab rotation reads correctly at the level a
screenshot can tell; the bright afternoon band runs along the hour axis as it should. Not checked:
Cavity and Trajectory beyond the switcher existing. The correlation panel still prints the round-0
numbers.

## What Claude added (contract 3, see `docs/data-contract.md`)

- `pol` — per column, per mode: `az` (axial polarisation angle from the NS coil towards EW, radians,
  (−π/2, π/2]; source bearing ≈ az + π/2, two-fold ambiguous), `ell` ellipticity, `coh` NS/EW coherence.
  From NS×EW cross-spectra averaged ±0.5 Hz about each fitted centre. October measured: mode-1 azimuth
  interquartile range ≈ 20°, median coherence ≈ 0.17, so bearing is a spread, not a point. `-9` = no data.
- `chimneys_month` — the annual clock with seasonal centroids: SON puts the Maritime Continent near
  4°S 105°E, Africa 2°S 25°E, the Americas 12°S 63°W (JJA sits north of the equator on all three).
  Position only; peak hours stay annual, as your notes said.
- `chimney` is now a selectable event series in the correlation panel, labelled as a model.
- A second month exists: `viewer/SN_201306.html` (June 2013, Kp 7.0 storm on the 1st, summer chimneys).
  `build_viewer.py <month>` writes `SN_<yyyymm>.html`; `--main` also writes `index.html`.
- Dataset published: https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada (Parquet:
  spectra, modes, polarisation, lanes, model; plus a `kb/` folder). The viewer is now one consumer of it.

## What to build (round 2)

1. **Cavity uses `pol`.** Replace the atan2-of-peaks bearing with the measured polarisation: draw the
   bearing as a fan whose width is the column's azimuth spread (use `coh` as confidence), with the
   two-fold ambiguity shown as two opposite fans, and let the chimney weights follow it. Use
   `chimneys_month` for positions. Label the globe "one-station inversion" as before.
2. **Month switch.** The page should accept a second embedded month or a selector that loads
   `SN_<yyyymm>.html`; simplest honest version is a link row (Oct 2013 · Jun 2013) in the header. The
   trajectory helix and day stack are where June versus October differ visibly.
3. **Cavity and Trajectory visual pass.** You had no browser last round; Claude will check these two in
   round 3, so leave notes on what to look for.
4. **Trajectory helix from `diurnal`** if you want one source of truth (optional).
5. Keep everything else. No new libraries. No higher modes.

## What to say back

Research is optional this round. Decisions per item, data fields needed, what is unfinished, and the
same one-line correlation check.
