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
    data = {"station": "Sierra Nevada ELF station, Spain (37.04 N, 3.32 W, 2500 m)", "lat": 37.04, "lon": -3.32,
            "month": f"{yyyymm[:4]}-{yyyymm[4:]}", "t0": t0, "dt": dts, "nt": nt, "f0": FMIN, "df": float(f[1] - f[0]) * FBIN, "nf": nfo,
            "storm_t": dt.datetime(2013, 10, 2, 3, tzinfo=dt.timezone.utc).timestamp() if month == "1310" else None,
            "sheets": sheets, "modes": modes, "kp": kp, "quakes": quakes,
            "calnote": "The surface covers 6 to 25 Hz, the band the station calibrates (modes 1 to 3). Below 6 Hz the sensor's 1/f noise dominates and the coil resonates near 33 Hz, so higher modes are not resolvable from this instrument.",
            "credits": ["Raw ELF data: Salinas et al., Zenodo 10.5281/zenodo.6348930, CC BY 4.0; processing chain after Salinas et al. 2022, Computers & Geosciences 165:105148",
                        "Kp index: GFZ Potsdam, Matzka et al. 2021, CC BY 4.0", "Earthquakes: USGS FDSN event service"]}
    tpl = open(os.path.join(ROOT, "viewer", "template.html"), encoding="utf8").read()
    out = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    op = os.path.join(ROOT, "viewer", "index.html")
    open(op, "w", encoding="utf8").write(out)
    # Artifact variant: same page without the document skeleton (the host supplies doctype/html/head/body)
    body = out
    for tag in ("<!doctype html>", "<html lang=\"en\">", "<head>", "</head>", "<body>", "</body>", "</html>"):
        body = body.replace(tag, "")
    body = body.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">', "")
    open(os.path.join(ROOT, "viewer", "artifact.html"), "w", encoding="utf8").write(body.strip() + "\n")
    print(f"wrote {op} {os.path.getsize(op)/1e6:.1f} MB; nt={nt} nf={nfo} sheets={[s['name'] for s in sheets]} dt={dts:.0f}s")


if __name__ == "__main__":
    main(sys.argv[1])
