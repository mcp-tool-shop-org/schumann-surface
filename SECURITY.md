# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |

## Reporting a Vulnerability

Email: **64996768+mcp-tool-shop@users.noreply.github.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Version affected
- Potential impact

### Response timeline

| Action | Target |
|--------|--------|
| Acknowledge report | 48 hours |
| Assess severity | 7 days |
| Release fix | 30 days |

## Scope

This is a data pipeline plus a static HTML viewer. It runs locally.

- **Data touched:** files under `data/` in the repository checkout (raw ELF recordings fetched from
  Zenodo, derived NPZ and Parquet products, small lane files from GFZ and USGS). Nothing outside the
  checkout is read or written.
- **Network egress:** only when a script is asked to fetch: `fetch_zenodo_month.py` (zenodo.org),
  `pipeline_month.py` (zenodo.org, digibug.ugr.es, kp.gfz-potsdam.de, earthquake.usgs.gov). Uploading
  to Hugging Face is a step you run yourself with your own login. No script contacts any other host.
- **The viewer** (`viewer/index.html`) is a single static page. It loads Three.js and two fonts from
  public CDNs and nothing else; it makes no requests for data and stores nothing.
- **No secrets handling.** No script reads, stores or transmits credentials.
- **No telemetry** is collected or sent by any part of this repository.
