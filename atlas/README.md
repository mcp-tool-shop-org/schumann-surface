# schumann-surface: how it works

Mapped at 2026-09-25 from commit 91dd356.

## What this is

11 parts, mostly Python (15 files), JavaScript (2) and TypeScript (2). Work enters through 2 doors; ci and Deploy site to GitHub Pages each reach 1 part, and ci is followed because a pull request goes through it.

## What changed since the last map

This is the first map.

## What comes in

1. **ci.** On a pull request touching 5 paths; on a push touching 5 paths; or by hand. Runs tests/.
2. **Deploy site to GitHub Pages.** On a push to main touching 2 paths; or by hand. Runs site/astro.config.mjs and site/src/.

## What happens through ci

1. The workflow runs tests/ in tests.

## Who reads the results

ci writes nothing this map can see.

## The other doors

**Deploy site to GitHub Pages** runs site/astro.config.mjs and site/src/, and deploys the site.

## What breaks what

- **viewer/** is written by scripts and read by the repository root, scripts and site; a hand edit reaches every reader.

## What tends to change together

No two source files changed together often enough to name.

Window: 180 days; a pair counts from 3 shared commits, since the window holds fewer than 30 qualifying commits.

## What no test touches

- **scripts** is imported by no test.

experiments/schumann-sft/test_router.py runs in no workflow.

## Written but never read

- **dataset/kb/catalog/** is written by experiments/schumann-sft/finish_and_train.sh and read by nothing else in this repository.
- **experiments/schumann-sft/runs/** is written by experiments/schumann-sft/runpod.mjs and read by nothing else in this repository.

## Helpers that look duplicated

No two parts export a helper that looks alike.

## Generated, never hand-edited

- **dataset/kb/catalog/** is written by experiments/schumann-sft/finish_and_train.sh.
- **experiments/schumann-sft/runs/** is written by experiments/schumann-sft/runpod.mjs.
- **viewer/** is written by scripts/build_viewer.py.

## Hand-authored

People write .claude/, .github/, assets/, docs/, the repository root and site/. Nothing in this repository writes to them.

## Where to start

ci runs no code this map can follow, so there is no path of files to read in order.

## What this map cannot see

- 1 import could not be resolved: `tests/test_chain.py` imports `process_month`, which is no module on its import path and no declared dependency.
- 21 reads use paths built at run time and are not named here.
- 12 writes go to places this repository does not track, so they are not listed as generated.
- 2 writes and 7 reads go to a path their caller passes, not to this repository.
- 2 writes and 7 reads go to the home directory (.ssh/), not to this repository.
- 1 command is built at run time and not followed.
- Statistics confidence is low: fewer than 30 qualifying commits in the window, and fewer than 20 source files reach 10 revisions.

Regenerate with `npx --yes @dogfood-lab/atlas map`.
