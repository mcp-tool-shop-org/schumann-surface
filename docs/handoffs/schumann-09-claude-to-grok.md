# schumann-surface · handoff 09 · Claude → Grok Build

Paste target: **Grok Build** (executor). Reply file: `docs/handoffs/schumann-10-grok-to-claude.md`.
Repo `mcp-tool-shop-org/schumann-surface`, branch `main`. Round 5. Ownership unchanged (Grok:
`viewer/template.html`; Claude: everything else). Rebuild all twelve months and copy them into
`site/public/viewer/` (`python scripts/build_viewer.py <YYMM>` for each, `1310 --main`); Claude pushes.

## Standards compliance (this handoff)

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Three.js r128 on cdnjs; contract 4 documented in `docs/data-contract.md`; no new library. |
| ANDON_AUTHORITY | 2 | Oct 2013 correlation numbers (r 0.036, N_eff 69, band ±0.236) must survive; a console error on any of the twelve live pages halts the round. |
| NAMED_COMPENSATORS | 2 | `git revert` on the template; `build_viewer.py` regenerates; Pages redeploys on push. Owner: Claude. |
| DECOMPOSE_BY_SECRETS | 3 | One file each side; the new data lives in one added field. |
| UNCERTAINTY_GATED_HUMANS | 2 | The dose-response panel must show class sizes and a null band; a thin class is shown thin, never smoothed. Director reviews the live page. |
| EXTERNAL_VERIFIER | 2 | Claude click-checks the live Year mode and recomputes the class means in Python against the panel's numbers. |

## Where we are

Twelve months are processed and verified (24/24 against the station). The viewer has two months
live; the other ten pages are built and will be on Pages with this round. Every page now carries a
`year` block (contract 4): one row per calendar day across all twelve months, with the daily mean and
median peak amplitude and mean centre frequency of modes 1–3 per sensor from unmasked fits, the day's
maximum and mean Kp, and the slot count. 361 days; two of them at Kp ≥ 7.

This is the picture one month could never show. The known result to test against (Cann 2026,
preprint, on this same archive): daily mean mode-1 amplitude rises about 6 % on Kp ≥ 7 days, after
season and lightning controls. One month's lag panel sits inside the null band; the year is where the
claim lives or dies.

## What to build (round 5)

1. **Month selector for all twelve pages.** The header row becomes a selector (Mar 2013 … Feb 2017).
   Every page is self-contained; the selector just links.
2. **Year mode** (fifth mode, all others kept). Time axis = the 361 days. Two panels:
   - **Daily ribbon**: mode-1 daily mean amplitude (NS and EW as two lines) with a 7-day median under
     it, Kp max as a bar strip beneath, storm days (Kp ≥ 7) marked. Month boundaries and the 2013 → 2017
     gap drawn honestly as a gap, not a join.
   - **Kp dose-response panel**: daily mode-1 amplitude grouped by the day's Kp max into the preprint's
     classes, Kp < 5, 5–6.7, ≥ 7. Show each class's mean and a bootstrap 95 % interval (1000 resamples,
     in-page), the class size n, and the ratio of each class to the quiet class. Draw the quiet-class
     interval as the null band. A season control is required: subtract each month's median before
     grouping (label it "month-demeaned"), and show the raw grouping beside it so a reader sees what the
     control did. If the ≥ 7 class has two days, say two days, in the panel.
3. **Seasonal frequency panel** (small): monthly mean centre frequency of modes 1–3, NS, with the
   station's known range (mode 1 drifts roughly 7.6–7.9 Hz through the year).
4. Nothing else changes. No new library. Modes 1–3 only. Correlation statistics untouched.

## What to say back

The numbers the dose-response panel prints for Oct 2013 NS (class means, n, ratios, interval) so
Claude can recompute them; decisions; unfinished items; the one-line correlation check; and one
sentence on what a person sees in Year mode at rest.
