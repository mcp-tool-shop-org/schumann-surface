# schumann-surface: how it works

Mapped at 2026-10-15 from commit a0cdb88 by Atlas 1.24.0.

## What this is

11 parts, mostly HTML (40 files), Python (15), shell (7), CSS (2), JavaScript (2), TypeScript (2) and Astro (1). Work enters through 2 doors; the busiest is ci, which reaches 2 parts. It deploys a site to GitHub Pages.

## What changed since 2026-10-14 (5a7c31b)

Nothing structural changed since 2026-10-14; 1 file changed content.

## What comes in

1. **ci.** On a pull request touching 5 paths; on a push touching 5 paths; or by hand. Runs tests/.
2. **Deploy site to GitHub Pages.** On a push to main touching 2 paths; or by hand. Runs site/astro.config.mjs and site/src/.

## What happens through ci

1. The workflow runs tests/ in tests.
2. That reaches scripts (1 file).

## Who reads the results

ci writes nothing this map can see.

## The other doors

**Deploy site to GitHub Pages** runs site/astro.config.mjs and site/src/, and deploys the site.

## What breaks what

- **scripts** is imported only from tests, by 1 part (tests), and sits on the path of 1 door.
- **viewer/** is written by scripts and read by the repository root and scripts; a hand edit reaches every reader.

## What tends to change together

No two source files changed together often enough to name.

Window: 180 days; a pair counts from 3 shared commits, since the window holds fewer than 30 qualifying commits.

## What no test touches

Every code part is imported by at least one test.

experiments/schumann-sft/test_router.py runs in no workflow.

verify.sh runs in no workflow.

## Written but never read

- **dataset/kb/catalog/** is written by experiments/schumann-sft/finish_and_train.sh and read by nothing else in this repository.
- **experiments/schumann-sft/runs/** is written by experiments/schumann-sft/runpod.mjs and read by nothing else in this repository.

## Helpers that look duplicated

No two parts export a helper that looks alike.

## Generated, never hand-edited

- **dataset/kb/catalog/** is written by experiments/schumann-sft/finish_and_train.sh.
- **experiments/schumann-sft/runs/** is written by experiments/schumann-sft/runpod.mjs.
- **viewer/** is written by scripts/build_viewer.py, except viewer/template.html, which it reads and people write.

## Hand-authored

People write .claude/, .github/, assets/, docs/, the repository root and site/. Nothing in this repository writes to them.

## Where to start

.github/workflows/ci.yml → scripts/process_month.py

Read those in order to follow one pull request end to end.

## What this map cannot see

- 17 reads use paths built at run time and are not named here.
- 12 writes go to places this repository does not track, so they are not listed as generated.
- 2 writes and 12 reads go to a path their caller passes, not to this repository.
- 2 writes and 7 reads go to the home directory (.ssh/), not to this repository.
- 3 commands are built at run time and not followed.
- Statistics confidence is low: fewer than 30 qualifying commits in the window, and fewer than 25 source files reach 10 revisions.

Regenerate with `npx --yes @dogfood-lab/atlas map`.
