"""Embed a processed month into the viewer template -> viewer/index.html (self-contained).

Inputs : data/derived/SN_<YYMM>_0.npz (NS), _1.npz (EW)   from process_month.py
         data/lanes/kp_<YYYYMM>.txt   GFZ Kp lines (CC BY 4.0)
         data/lanes/usgs_<YYYYMM>_m6.geojson
Output : viewer/index.html
Downsample: time step TSTEP slots (3 = 30 min), frequency FBIN bins (4 = 0.125 Hz), 0..FMAX Hz.
Surface stored as uint8 over a dB window [P2, P99.5] per sheet, dB = 20 log10(amp / 1 pT/sqrtHz).
"""
import base64, json, os, sys, datetime as dt
import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
TSTEP, FMIN, FMAX, FBIN = 3, 6.0, 25.0, 4   # the station's calibrated band


def down_t(a, step):
    n = (len(a) // step) * step
    a = a[:n].reshape(-1, step, *a.shape[1:])
    with np.errstate(all="ignore"):
        return np.nanmean(a, axis=1)


def year_block():
    """Daily means over all processed months: mode fits (unmasked) per sensor, Kp max/mean, slot count."""
    import glob as _g
    kp = {}
    for kf in _g.glob(os.path.join(ROOT, "data", "lanes", "kp_*.txt")):
        for line in open(kf):
            c = line.split()
            if len(c) >= 9 and c[0].isdigit():
                kp.setdefault(f"{c[0]}-{c[1]}-{c[2]}", []).append(float(c[7]))
    days = {}
    for s, name in ((0, "NS"), (1, "EW")):
        for p in sorted(_g.glob(os.path.join(ROOT, "data", "derived", f"SN_*_{s}.npz"))):
            z = np.load(p); t = z["t"]; md = z["modes"].copy()
            for k, (lo_f, hi_f) in enumerate(((6.5, 9.5), (12.5, 16.0), (18.5, 22.5))):
                bad = ~((md[:, k, 0] >= lo_f) & (md[:, k, 0] <= hi_f) & (md[:, k, 3] > 0.3) & (md[:, k, 3] < 5.0)); md[bad, k, :] = np.nan
            dates = [dt.datetime.fromtimestamp(x, dt.timezone.utc).strftime("%Y-%m-%d") for x in t]
            for d in sorted(set(dates)):
                idx = np.array([i for i, x in enumerate(dates) if x == d])
                row = days.setdefault(d, {"date": d, "n": 0})
                with np.errstate(all="ignore"):
                    row[name] = {"f": np.round(np.nanmean(md[idx, :, 0], 0), 3).tolist(), "a": np.round(np.nanmean(md[idx, :, 1], 0), 4).tolist(),
                                 "amed": np.round(np.nanmedian(md[idx, :, 1], 0), 4).tolist()}
                row["n"] = max(row["n"], int(len(idx)))
    out = []
    for d in sorted(days):
        r = days[d]; k = kp.get(d, [])
        r["kp_max"] = max(k) if k else None; r["kp_mean"] = round(sum(k) / len(k), 2) if k else None
        for name in ("NS", "EW"):
            if name in r:
                r[name] = {kk: [(-1 if (v is None or v != v) else v) for v in vv] for kk, vv in r[name].items()}
        out.append(r)
    return {"days": out, "note": "Daily means of unmasked mode fits (f Hz, a peak pT/sqrtHz, amed median) per sensor across every processed month; kp_max/kp_mean from GFZ; -1 = no data. Built for a Year mode and a Kp dose-response panel; the known effect is about +6 % in mode-1 amplitude on Kp >= 7 days (Cann 2026), so show the null band."}


def main(month):
    sheets, modes = [], {}
    t = f = None
    nt = nfo = 0
    for s, name in ((0, "NS"), (1, "EW")):
        p = os.path.join(ROOT, "data", "derived", f"SN_{month}_{s}.npz")
        if not os.path.exists(p):
            continue
        z = np.load(p)
        t, f, amp, md, sat = z["t"], z["f"], z["amp"], z["modes"], z["sat"]
        fm = (f >= FMIN - 1e-9) & (f <= FMAX + 1e-9)
        A = amp[:, fm]
        nf = (A.shape[1] // FBIN) * FBIN
        A = A[:, :nf].reshape(A.shape[0], nf // FBIN, FBIN).mean(2)
        A = down_t(A, TSTEP)
        with np.errstate(all="ignore"):
            db = 20 * np.log10(A)
        lo, hi = np.nanpercentile(db, 2), np.nanpercentile(db, 99.5)
        u8 = np.where(np.isfinite(db), np.clip((db - lo) / (hi - lo), 0, 1) * 254 + 1, 0).astype(np.uint8)
        sheets.append({"name": name, "lo": float(lo), "hi": float(hi), "u8": base64.b64encode(u8.tobytes()).decode()})
        # Display gate: the station fits are unbounded LM; mask the rare wandering fits (documented windows)
        md = md.copy()
        for k, (lo_f, hi_f) in enumerate(((6.5, 9.5), (12.5, 16.0), (18.5, 22.5))):
            bad = ~((md[:, k, 0] >= lo_f) & (md[:, k, 0] <= hi_f) & (md[:, k, 3] > 0.3) & (md[:, k, 3] < 5.0))
            md[bad, k, :] = np.nan
        m = down_t(md, TSTEP)  # [nt, 3, 4] (f, peak, a, s)
        modes[name] = {"f": np.round(np.nan_to_num(m[:, :, 0], nan=-1), 3).tolist(),
                       "a": np.round(np.nan_to_num(m[:, :, 1], nan=-1), 4).tolist(),
                       "g": np.round(np.nan_to_num(m[:, :, 3], nan=-1), 3).tolist(),
                       "sat": np.round(down_t(sat, TSTEP), 3).tolist()}
        nt, nfo = u8.shape
    t0 = float(t[0]); dts = float(np.median(np.diff(t))) * TSTEP
    yyyymm = "20" + month
    kp = []
    for line in open(os.path.join(ROOT, "data", "lanes", f"kp_{yyyymm}.txt")):
        c = line.split()
        if len(c) < 9 or not c[0].isdigit():
            continue
        ts = dt.datetime(int(c[0]), int(c[1]), int(c[2]), int(float(c[3])), tzinfo=dt.timezone.utc).timestamp()
        kp.append([ts, float(c[7])])
    g = json.load(open(os.path.join(ROOT, "data", "lanes", f"usgs_{yyyymm}_m6.geojson")))
    quakes = [[q["properties"]["time"] / 1000, q["properties"]["mag"], q["properties"]["place"]] for q in g["features"]]
    # Chimney schedule: a MODEL lane, not measured lightning. Structure after Whipple 1929 (thunderstorm
    # diurnal curves by continent) and the Carnegie curve (Harrison 2013, Surv. Geophys.); UTC peaks and
    # relative weights consistent with the LIS/OTD diurnal climatology (Blakeslee et al. 2014, Atmos. Res.).
    # Measured 2013 global lightning (WWLLN, Blitzortung archive, LIS via Earthdata) needs an account.
    chimneys = [{"name": "Southeast Asia / Maritime Continent", "peak_utc": 8.0, "sigma_h": 2.5, "weight": 0.8, "lat": 5, "lon": 110},
                {"name": "Africa", "peak_utc": 14.5, "sigma_h": 2.5, "weight": 1.0, "lat": 5, "lon": 20},
                {"name": "Americas", "peak_utc": 20.0, "sigma_h": 2.5, "weight": 0.9, "lat": 0, "lon": -60}]
    def chimney_model(t):
        h = (t % 86400) / 3600.0
        v = 0.0
        for c in chimneys:
            d = min(abs(h - c["peak_utc"]), 24 - abs(h - c["peak_utc"]))
            v += c["weight"] * np.exp(-0.5 * (d / c["sigma_h"]) ** 2)
        return v
    chimney = [round(float(chimney_model(t0 + i * dts)), 4) for i in range(nt)]
    # Seasonal centroids (position only; the UTC clock stays annual). Approximate, read from the OTD/LIS
    # climatology maps (Christian et al. 2003, JGR) and the monthly lightning-centre migration in
    # Peterson, Mach & Buechler 2021 (JGR): SON pulls the Maritime Continent and the Americas south of
    # the equator while Africa stays near it; JJA sits north of the equator on all three.
    season_centroids = {"JJA": [(8, 105), (8, 15), (12, -75)], "SON": [(-4, 105), (-2, 25), (-12, -63)],
                        "DJF": [(-10, 120), (-10, 25), (-15, -60)], "MAM": [(2, 105), (0, 20), (-5, -65)]}
    season = {12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM", 6: "JJA", 7: "JJA", 8: "JJA", 9: "SON", 10: "SON", 11: "SON"}[int(yyyymm[4:])]
    chimneys_month = [dict(c, lat=la, lon=lo, season=season) for c, (la, lo) in zip(chimneys, season_centroids[season])]
    # Polarisation per column per mode from the NS x EW cross-spectrum (scripts/polarisation_month.py)
    pol = None
    pp = os.path.join(ROOT, "data", "derived", f"POL_{month}.npz")
    if os.path.exists(pp):
        z = np.load(pp)
        def circ_mean(a):  # mean of an axial (180-degree periodic) angle over the column
            with np.errstate(all="ignore"):
                return 0.5 * np.arctan2(np.nanmean(np.sin(2 * a), axis=1), np.nanmean(np.cos(2 * a), axis=1))
        n = (len(z["t"]) // TSTEP) * TSTEP
        az = z["az"][:n].reshape(-1, TSTEP, 3); ell = z["ell"][:n].reshape(-1, TSTEP, 3); coh = z["coh"][:n].reshape(-1, TSTEP, 3)
        pol = {"az": np.round(np.nan_to_num(np.stack([circ_mean(az[:, :, k]) for k in range(3)], 1), nan=-9), 4).tolist(),
               "ell": np.round(np.nan_to_num(np.nanmean(ell, 1), nan=-9), 3).tolist(),
               "coh": np.round(np.nan_to_num(np.nanmean(coh, 1), nan=-9), 3).tolist(),
               "note": "az: axial angle of the horizontal magnetic polarisation, radians from the NS coil towards EW, in (-pi/2, pi/2]; -9 = no data. Source bearing ~ az + pi/2, two-fold ambiguous. ell in [-1,1]; coh = NS/EW magnitude-squared coherence."}
    # Measured diurnal summary: per-UTC-hour mean of each mode's peak amplitude, both sheets.
    diurnal = {}
    for name in modes:
        a = np.array(modes[name]["a"], dtype=float); a[a < 0] = np.nan
        hours = ((t0 + np.arange(nt) * dts) % 86400) // 3600
        with np.errstate(all="ignore"):
            diurnal[name] = [[round(float(np.nanmean(a[hours == h, k])), 4) for k in range(3)] for h in range(24)]
    # Year block (contract 4): one row per calendar day across EVERY processed month in data/derived,
    # so a single page can show the twelve-month picture and the Kp dose-response one month cannot.
    year = year_block()
    data = {"station": "Sierra Nevada ELF station, Spain (37.04 N, 3.32 W, 2500 m)", "lat": 37.04, "lon": -3.32,
            "month": f"{yyyymm[:4]}-{yyyymm[4:]}", "t0": t0, "dt": dts, "nt": nt, "f0": FMIN, "df": float(f[1] - f[0]) * FBIN, "nf": nfo,
            "storm_t": dt.datetime(2013, 10, 2, 3, tzinfo=dt.timezone.utc).timestamp() if month == "1310" else None,
            "sheets": sheets, "modes": modes, "kp": kp, "quakes": quakes,
            "chimneys": chimneys, "chimneys_month": chimneys_month, "chimney": chimney, "diurnal": diurnal, "pol": pol, "year": year, "contract": 4,
            "calnote": "The surface covers 6 to 25 Hz, the band the station calibrates (modes 1 to 3). Below 6 Hz the sensor's 1/f noise dominates and the coil resonates near 33 Hz, so higher modes are not resolvable from this instrument.",
            "credits": ["Raw ELF data: Salinas et al., Zenodo 10.5281/zenodo.6348930, CC BY 4.0; processing chain after Salinas et al. 2022, Computers & Geosciences 165:105148",
                        "Kp index: GFZ Potsdam, Matzka et al. 2021, CC BY 4.0", "Earthquakes: USGS FDSN event service"]}
    tpl = open(os.path.join(ROOT, "viewer", "template.html"), encoding="utf8").read()
    out = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    main_page = "--main" in sys.argv
    op = os.path.join(ROOT, "viewer", "index.html" if main_page else f"SN_{yyyymm}.html")
    open(op, "w", encoding="utf8").write(out)
    # Artifact variant: same page without the document skeleton (the host supplies doctype/html/head/body)
    body = out
    for tag in ("<!doctype html>", "<html lang=\"en\">", "<head>", "</head>", "<body>", "</body>", "</html>"):
        body = body.replace(tag, "")
    body = body.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">', "")
    open(os.path.join(ROOT, "viewer", "artifact.html" if main_page else f"artifact_{yyyymm}.html"), "w", encoding="utf8").write(body.strip() + "\n")
    print(f"wrote {op} {os.path.getsize(op)/1e6:.1f} MB; nt={nt} nf={nfo} sheets={[s['name'] for s in sheets]} dt={dts:.0f}s")


if __name__ == "__main__":
    main(sys.argv[1])
