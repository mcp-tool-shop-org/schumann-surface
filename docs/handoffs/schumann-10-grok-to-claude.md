# schumann-surface · handoff 10 · Grok Build → Claude

Round 5 done. Owner this turn: `viewer/template.html` only.
Rebuilt all twelve months (`1310 --main` plus the other eleven) and copied `index.html` + `SN_2013{03–12}.html` + `SN_20170{1,2}.html` into `site/public/viewer/`.

## Dose-response numbers (Year panel, Oct 2013 page, NS, 361 days)

These are the **year** block, not October-only. Same numbers on every month page. Sensor NS, mode-1 daily mean peak, unmasked. Classes: Kp max `< 5`, `5 ≤ kp < 7` (labelled 5–6.7), `≥ 7`. Bootstrap 1000, seed 13, mulberry32 as in the template. Quiet class = `< 5`.

**Raw**

| class | n | mean | 95 % CI | ratio to quiet |
|---|---|---|---|---|
| Kp < 5 | 337 | 0.375766 | [0.369955, 0.381585] | 1.000 |
| 5–6.7 | 22 | 0.391455 | [0.368950, 0.415477] | 1.042 |
| ≥ 7 | **2** | 0.418450 | [0.381300, 0.455600] | 1.114 |

≥ 7 days: **2013-06-01**, **2013-10-02**. The interval for n = 2 is the two observations.

**Month-demeaned** (each day's amplitude minus that month's median)

| class | n | residual mean | 95 % CI | Δ vs quiet residual |
|---|---|---|---|---|
| Kp < 5 | 337 | 0.002101 | [−0.001723, 0.006125] | 0 |
| 5–6.7 | 22 | 0.003291 | [−0.009891, 0.016155] | +0.001190 |
| ≥ 7 | 2 | 0.004750 | [−0.013500, 0.023000] | +0.002649 |

After the month median is gone, ≥ 7 sits inside the quiet band. n = 2 is two days, not a distribution. The panel prints that.

## Decisions

- Header is twelve self-contained links (Oct → `index.html`).
- Year is a 2D canvas (no orbit), fifth mode. Ribbon = NS + EW daily means + 7-day median within each contiguous block; Kp-max strip; storm days marked; 2014–2016 drawn as a labelled gap.
- Dose-response is the full 361 days. Raw and month-demeaned sit side by side; quiet-class CI is the null band. Ratios on the raw grouping; residuals + Δ on the demeaned one (a ratio of residuals is not a dose).
- Seasonal panel: monthly mean NS centre frequency, modes 1–3, with a 7.6–7.9 Hz band on mode 1.
- Month scrubber hides in Year (the year canvas is the time axis). Other four modes unchanged. `series` / `xcorr` / `ac1` / `drawX` untouched.

## Unfinished

No browser pass. Please click-check: gap is a hole, two storm dates are named, ≥ 7 whisker after demeaning overlaps the quiet band, month selector hits all twelve Pages paths, no console error.

## Correlation check

Oct 2013 correlation panel still prints **r(lag 0) = 0.036, N = 1486, N_eff = 69, 95% band = ±0.236**.

## At rest, Year, nothing touched

A 361-day ribbon of mode-1 amplitude (NS/EW plus a 7-day median), a Kp strip with two named storm days, a labelled hole where 2014–2016 are missing, and a dose-response whose ≥ 7 class is two days that sit inside the quiet band once each month's median is removed.
