# schumann-surface · handoff 07 · Claude → Grok Build

Paste target: **Grok Build** (executor). Reply file: `docs/handoffs/schumann-08-grok-to-claude.md`.
Repo `mcp-tool-shop-org/schumann-surface`, branch `main`, head after `38ed474`. Round 4. Ownership
unchanged (Grok: `viewer/template.html`; Claude: everything else). Rebuild both months and copy them into
`site/public/viewer/`; Claude pushes and Pages deploys.

## Standards compliance (this handoff)

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Three.js r128 on cdnjs; contract 3 unchanged; the atlas is a 2D canvas or one textured plane, no new library. |
| ANDON_AUTHORITY | 2 | Oct 2013 correlation numbers (r 0.036, N_eff 69, band ±0.236) must survive; a console error on the live page halts the round. |
| NAMED_COMPENSATORS | 2 | `git revert` on the template; `build_viewer.py` regenerates; Pages redeploys on push. Owner: Claude. |
| DECOMPOSE_BY_SECRETS | 3 | One file each side; projection changes, data does not. |
| UNCERTAINTY_GATED_HUMANS | 2 | The Director judged the round-3 globe unreadable at rest from a screenshot and chose the atlas; that judgement is the gate for this round. |
| EXTERNAL_VERIFIER | 2 | Claude click-checks the live page after the push. |

## Decision (Director, round 3 review)

The globe is the right physics and the wrong reading surface: one camera, half the Earth hidden, fans on
the far side, chimney dots lost, and the base colour added for brightness swallowed the mode pattern.
At rest the view shows cartoon geography and none of the measurement.

**Round 4: the Cavity rest state becomes a station-centred azimuthal equidistant atlas. The globe stays
as a toggle ("Globe"), same data, same scrubber, only the projection changes.**

## The atlas

- Centre = Sierra Nevada. Radius = angular distance θ from the station (0 at centre, 180° at the rim).
  Angle = bearing from the station (north up, east right).
- Mode n pattern: |Pₙ¹(cos θ)| scaled by the pinned column's fitted amplitude, drawn as concentric
  rings, one colour per mode (keep red / green / blue). They are circles in this projection by
  construction. No base fill that competes with them; a dark ground and the pattern as the light.
- Polarisation: bearing = `pol.az + π/2`, drawn as two opposite pie slices from the centre to the rim.
  Slice half-width from coherence as now (October median ≈ 0.18 should look fat). This is the
  measurement; give it the strongest colour on the page.
- Chimneys at their true θ and bearing from `chimneys_month` (great-circle distance and initial
  bearing from the station), labelled by name, disc size following the UTC schedule at the pinned
  hour. Africa at ~14 UTC should land in a slice; the Americas at ~20 UTC in the other or the same.
- Terminator as a curve from the same sun model; Kp as the outer rim tint.
- Coastlines are optional and low-contrast; if drawing them costs more than a small inline polyline
  set, leave them out. Labels beat coastlines here.
- A 2D canvas is fine. If you draw it as a textured plane in the Three.js scene, no orbit on it.

## What not to touch

`scripts/*`, `tests/*`, `data/*`, `dataset/*`, `site/*` other than copying the built viewer pages,
README, the correlation statistics, the calibration note, credits. Modes 1–3 only.

## What to say back

Decisions, anything you needed that the contract lacks, unfinished items, the one-line correlation
check, and a sentence on what a person sees at rest in the new Cavity without touching anything.
