"""Slot-by-slot check of our derived month against the station's published npz (CC BY-NC-ND, used
here only as a verifier, never redistributed).

Granada arrays (SN_<YYMM>_LO_6_1_<s>.npz, positional): arr_0 sat, arr_1 fre (6..25), arr_2 freajus,
arr_3 rs [slots,609] amplitude spectra, arr_4 rs_LO fit curves, arr_5 PARLO [slots,14]
(peak1..3, a1..3, f1..3, s1..3, m, n), arr_6 chi2, arr_7 errors, arr_8 [peak,f]x3, arr_9 timestamps.
Usage: python scripts/verify_against_granada.py 1310 0
"""
import os, sys, datetime as dt
import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..", "data")


def main(month, s):
    g = np.load(os.path.join(ROOT, "granada", f"SN_{month}_LO_6_1_{s}.npz"))
    m = np.load(os.path.join(ROOT, "derived", f"SN_{month}_{s}.npz"))
    gt = np.array([dt.datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc).timestamp() for x in g["arr_9"]])
    mt = m["t"]
    idx = np.clip(np.searchsorted(mt, gt), 0, len(mt) - 1)
    best = np.array([min(range(max(0, i - 1), min(len(mt), i + 2)), key=lambda j: abs(mt[j] - t)) for i, t in zip(idx, gt)])
    ok = np.abs(mt[best] - gt) < 30
    print(f"granada slots {len(gt)}, ours {len(mt)}, matched within 30 s: {ok.sum()}")
    gi, mi = np.where(ok)[0], best[ok]
    fg = g["arr_1"]; f = m["f"]; j0 = int(round(fg[0] / (f[1] - f[0])))
    G = g["arr_3"][gi]; M = m["amp"][mi][:, j0:j0 + len(fg)]
    both = np.isfinite(M).all(1) & np.isfinite(G).all(1) & (G > 0).all(1)
    ratio = M[both] / G[both]
    print(f"spectrum ratio ours/granada over 6-25 Hz, slots with data {both.sum()}: median {np.nanmedian(ratio):.4f}, "
          f"p5 {np.nanpercentile(ratio,5):.4f}, p95 {np.nanpercentile(ratio,95):.4f}")
    print("  per-band median ratio:", {f"{lo}-{hi}": round(float(np.nanmedian(ratio[:, (fg >= lo) & (fg < hi)])), 4) for lo, hi in ((6, 10), (10, 14), (14, 18), (18, 22), (22, 25))})
    P = g["arr_5"][gi]; ours = m["modes"][mi]
    for k, name in enumerate(("mode1", "mode2", "mode3")):
        df_ = ours[:, k, 0] - P[:, 6 + k]; dpk = ours[:, k, 1] / P[:, k]; ds = ours[:, k, 3] / np.abs(P[:, 9 + k])
        fin = np.isfinite(df_)
        print(f"{name}: f ours-granada median {np.nanmedian(df_):+.4f} Hz, p5/p95 {np.nanpercentile(df_[fin],5):+.3f}/{np.nanpercentile(df_[fin],95):+.3f}, "
              f"|d|<0.05 Hz in {np.mean(np.abs(df_[fin])<0.05)*100:.1f}% | peak ratio median {np.nanmedian(dpk):.4f} | width ratio median {np.nanmedian(ds):.4f}")
    print(f"granada mean f: {P[:,6:9].mean(0).round(3)}  ours: {np.nanmean(ours[:,:,0],0).round(3)}")
    sat = m["sat"][mi]; print(f"saturation ours mean {sat.mean():.4f} granada {g['arr_0'][gi].mean():.4f}, corr {np.corrcoef(sat, g['arr_0'][gi])[0,1]:.3f}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
