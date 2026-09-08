"""Export the derived products of one month as Parquet tables for the public dataset.

Everything here descends from the CC BY 4.0 raw archive (Zenodo 6348930) through our own chain, so it
is ours to publish with attribution. Nothing from the CC BY-NC-ND station npz is read or written.

Output (data/dataset/):
  spectra/SN_<YYYYMM>_<NS|EW>.parquet   one row per 10-min slot: t_utc, sensor, sat, amp[609] (pT/sqrtHz, 6..25 Hz at 31.25 mHz)
  modes/SN_<YYYYMM>.parquet             one row per slot x sensor x mode: f_hz, peak, a, halfwidth_hz, chi2, masked
  polarisation/SN_<YYYYMM>.parquet      one row per slot x mode: az_rad, ellipticity, coherence, f_hz
  lanes/SN_<YYYYMM>.parquet             one row per slot: kp, night_fraction, quake_count_24h, quake_max_mag_24h
  model/chimney_<YYYYMM>.parquet        one row per slot: chimney_model  (MODEL lane, kept in its own file)
  frequency_axis.parquet                the 609 frequencies
Usage: python scripts/export_dataset.py 1310
"""
import json, os, sys, datetime as dt
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(__file__))
import process_month as pm  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "dataset")
F_LO, F_HI = 6.0, 25.0
WINDOWS = ((6.5, 9.5), (12.5, 16.0), (18.5, 22.5))


def sun_elev(t, lat, lon):
    d = t / 86400 - 10957.5
    g = np.radians(357.529 + 0.98560028 * d); q = 280.459 + 0.98564736 * d
    L = np.radians(q + 1.915 * np.sin(g) + 0.02 * np.sin(2 * g)); e = np.radians(23.439 - 0.00000036 * d)
    dec = np.arcsin(np.sin(e) * np.sin(L)); ra = np.arctan2(np.cos(e) * np.sin(L), np.cos(L))
    gmst = (18.697374558 + 24.06570982441908 * d) % 24
    ha = np.radians(gmst * 15 + lon) - ra; la = np.radians(lat)
    return np.degrees(np.arcsin(np.sin(la) * np.sin(dec) + np.cos(la) * np.cos(dec) * np.cos(ha)))


def main(month):
    yyyymm = "20" + month
    for sub in ("spectra", "modes", "polarisation", "lanes", "model"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    fsel = (pm.FREQ >= F_LO - 1e-9) & (pm.FREQ <= F_HI + 1e-9)
    faxis = pm.FREQ[fsel]
    pq.write_table(pa.table({"f_hz": faxis.astype(np.float32)}), os.path.join(OUT, "frequency_axis.parquet"))
    modes_rows = {k: [] for k in ("t_utc", "sensor", "mode", "f_hz", "peak", "a", "halfwidth_hz", "chi2", "masked")}
    t_ref = None
    for s, name in ((0, "NS"), (1, "EW")):
        z = np.load(os.path.join(ROOT, "data", "derived", f"SN_{month}_{s}.npz"))
        t = z["t"]; t_ref = t if t_ref is None else t_ref
        amp = z["amp"][:, fsel].astype(np.float32)
        tbl = pa.table({"t_utc": pa.array((t * 1e6).astype("int64"), pa.timestamp("us", tz="UTC")), "sensor": [name] * len(t),
                        "sat": z["sat"].astype(np.float32), "amp": pa.array(list(amp), pa.list_(pa.float32(), amp.shape[1]))})
        pq.write_table(tbl, os.path.join(OUT, "spectra", f"SN_{yyyymm}_{name}.parquet"), compression="zstd")
        md = z["modes"]; chi = z["chi2"]
        for i in range(len(t)):
            for k in range(3):
                f, peak, a, g = md[i, k]
                masked = not (WINDOWS[k][0] <= f <= WINDOWS[k][1] and 0.3 < g < 5.0)
                modes_rows["t_utc"].append(int(t[i] * 1e6)); modes_rows["sensor"].append(name); modes_rows["mode"].append(k + 1)
                modes_rows["f_hz"].append(f); modes_rows["peak"].append(peak); modes_rows["a"].append(a); modes_rows["halfwidth_hz"].append(g)
                modes_rows["chi2"].append(chi[i]); modes_rows["masked"].append(bool(masked) or not np.isfinite(f))
    mt = pa.table({**{k: v for k, v in modes_rows.items() if k != "t_utc"}, "t_utc": pa.array(modes_rows["t_utc"], pa.timestamp("us", tz="UTC"))})
    pq.write_table(mt, os.path.join(OUT, "modes", f"SN_{yyyymm}.parquet"), compression="zstd")
    pp = os.path.join(ROOT, "data", "derived", f"POL_{month}.npz")
    if os.path.exists(pp):
        p = np.load(pp); rows = {k: [] for k in ("t_utc", "mode", "az_rad", "ellipticity", "coherence", "f_hz")}
        for i in range(len(p["t"])):
            for k in range(3):
                rows["t_utc"].append(int(p["t"][i] * 1e6)); rows["mode"].append(k + 1); rows["az_rad"].append(float(p["az"][i, k]))
                rows["ellipticity"].append(float(p["ell"][i, k])); rows["coherence"].append(float(p["coh"][i, k])); rows["f_hz"].append(float(p["fk"][i, k]))
        pt = pa.table({**{k: v for k, v in rows.items() if k != "t_utc"}, "t_utc": pa.array(rows["t_utc"], pa.timestamp("us", tz="UTC"))})
        pq.write_table(pt, os.path.join(OUT, "polarisation", f"SN_{yyyymm}.parquet"), compression="zstd")
    # lanes
    kp = []
    for line in open(os.path.join(ROOT, "data", "lanes", f"kp_{yyyymm}.txt")):
        c = line.split()
        if len(c) >= 9 and c[0].isdigit():
            kp.append((dt.datetime(int(c[0]), int(c[1]), int(c[2]), int(float(c[3])), tzinfo=dt.timezone.utc).timestamp(), float(c[7])))
    kp = np.array(kp)
    g = json.load(open(os.path.join(ROOT, "data", "lanes", f"usgs_{yyyymm}_m6.geojson")))
    qt = np.array([q["properties"]["time"] / 1000 for q in g["features"]]); qm = np.array([q["properties"]["mag"] for q in g["features"]])
    t = t_ref
    kp_col = np.array([kp[(kp[:, 0] <= tt) & (tt < kp[:, 0] + 10800), 1][0] if np.any((kp[:, 0] <= tt) & (tt < kp[:, 0] + 10800)) else np.nan for tt in t], np.float32)
    night = np.array([np.mean([sun_elev(tt + s * 100, 37.04, -3.32) < -6 for s in range(6)]) for tt in t], np.float32)
    qc = np.array([np.sum((qt >= tt - 86400) & (qt < tt)) for tt in t], np.int16)
    qmax = np.array([qm[(qt >= tt - 86400) & (qt < tt)].max() if np.any((qt >= tt - 86400) & (qt < tt)) else np.nan for tt in t], np.float32)
    lt = pa.table({"t_utc": pa.array((t * 1e6).astype("int64"), pa.timestamp("us", tz="UTC")), "kp": kp_col, "night_fraction": night,
                   "quake_count_24h": qc, "quake_max_mag_24h": qmax})
    pq.write_table(lt, os.path.join(OUT, "lanes", f"SN_{yyyymm}.parquet"))
    peaks = ((8.0, 0.8), (14.5, 1.0), (20.0, 0.9))
    def chim(tt):
        h = (tt % 86400) / 3600.0
        return sum(w * np.exp(-0.5 * (min(abs(h - p), 24 - abs(h - p)) / 2.5) ** 2) for p, w in peaks)
    ct = pa.table({"t_utc": pa.array((t * 1e6).astype("int64"), pa.timestamp("us", tz="UTC")), "chimney_model": np.array([chim(tt) for tt in t], np.float32)})
    pq.write_table(ct, os.path.join(OUT, "model", f"chimney_{yyyymm}.parquet"))
    sizes = {sub: sum(os.path.getsize(os.path.join(OUT, sub, f)) for f in os.listdir(os.path.join(OUT, sub))) for sub in ("spectra", "modes", "polarisation", "lanes", "model")}
    print(f"exported {yyyymm}: slots {len(t)}; folder sizes MB", {k: round(v / 1e6, 1) for k, v in sizes.items()})


if __name__ == "__main__":
    main(sys.argv[1])
