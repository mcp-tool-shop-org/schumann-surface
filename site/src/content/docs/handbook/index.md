---
title: Schumann Surface Handbook
description: What the tool shows, where the data comes from, and how to reproduce every number.
sidebar:
  order: 0
---

**Schumann Surface** renders one month of a real extremely-low-frequency (ELF) station as a 3D
object you can turn, scrub and interrogate, with event lanes beside it and a correlation panel
that shows the null band instead of hiding it.

The data is the University of Granada's Sierra Nevada ELF station, whose raw 256 Hz recordings
are public under CC BY 4.0. The processing chain here mirrors the station's own and reproduces its
published spectra at a ratio of 1.0000, slot by slot. The derived products are published as a
dataset on Hugging Face with a knowledge base inside.

## Pages

- [Getting started](./getting-started/) — fetch one month, process it, verify it, open the viewer.
- [The viewer](./viewer/) — the four modes, the lanes, the scrubber, and the correlation panel.
- [Data contract and dataset](./reference/) — every field the viewer consumes and every table the dataset ships.
- [Method and verification](./method/) — the pinned chain, the calibration constants, and the receipt against the station.
- [Honesty rules](./honesty/) — measured versus model, one-station geometry, and how to read a null result.

## What the instrument can see

The station's coils are calibrated for 6 to 25 Hz and resonate near 33 Hz. That means modes 1, 2
and 3 of the Schumann resonance, near 7.8, 14 and 20 Hz, are all this instrument resolves. The
viewer never invents higher modes, and neither should you.
