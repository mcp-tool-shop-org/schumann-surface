# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-09-08

### Added
- Range-request fetcher for single months of the 26.5 GB Zenodo raw archive (`fetch_zenodo_month.py`).
- Processing chain that mirrors the Sierra Nevada station's own (Welch, saturation, RLC calibration,
  anthropogenic filter, three-Lorentzian fit) and reproduces its published spectra at ratio 1.0000.
- Verifier against the station's published products with stated tolerances; exits non-zero outside them.
- NS × EW polarisation (azimuth, ellipticity, coherence) per slot and mode.
- Event lanes: GFZ Kp, local night, USGS M6+ earthquakes, and a clearly labelled chimney-schedule model.
- Self-contained 3D viewer with four modes (Surface, Day stack, Cavity globe, Trajectory), pinned
  spectrum, shared scrubber, and a lagged cross-correlation panel with a Bartlett-corrected null band.
- Parquet dataset export and the public dataset card + knowledge base
  (`mcp-tool-shop/schumann-sierra-nevada` on Hugging Face).
- Month pipeline driver (`pipeline_month.py`), synthetic tests for the chain, `verify.sh`.
- Knowledge-injection LoRA experiment under `experiments/schumann-sft/` with the fair-baseline contract.
