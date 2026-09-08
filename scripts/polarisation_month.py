"""NS x EW cross-spectra -> per-slot, per-mode magnetic polarisation (azimuth, ellipticity, coherence).

Reads both sensors' raw hour files for a month and the derived mode fits, and writes
data/derived/POL_<YYMM>.npz with, per 10-min slot and mode k = 1..3:
    az[slots,3]    polarisation azimuth of the horizontal magnetic field, radians, measured from the
                   NS coil axis towards EW, in (-pi/2, pi/2]; the ELF source lies roughly perpendicular
                   to the magnetic polarisation axis (H_phi is azimuthal about the source), so
                   source_bearing ~ az + pi/2 (two-fold ambiguous)
    ell[slots,3]   ellipticity in [-1, 1] (0 = linear, +-1 = circular; sign = rotation sense)
    coh[slots,3]   magnitude-squared coherence NS/EW at the mode
    fk[slots,3]    the mode centre frequency used (mean of the two sensors' fits)
Method: same 10-s Hann / 8192-point windows as process_month, saturated windows dropped in either
sensor, cross-spectrum Sxy = <X conj(Y)> accumulated over the slot, then averaged over +-0.5 Hz
around fk. Azimuth = 0.5 atan2(2 Re Sxy, Sxx - Syy); ellipticity from the Stokes-like quantities
(Fowler, Kotick & Elliott 1967; Means 1972). Calibration cancels in ratios (same Scal on both coils).
"""
import glob, os, re, sys, datetime as dt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import process_month as pm  # noqa: E402

ROOT = pm.ROOT
HALF = 0.5  # Hz averaging half-width around each mode


def hour_pairs(month):
    year = "20" + month[:2]
    d = os.path.join(ROOT, "raw", year, month)
    a = {os.path.basename(p)[-15:-9]: p for p in glob.glob(os.path.join(d, "smplGRTU1_sensor_0_*_info.txt"))}
    b = {os.path.basename(p)[-15:-9]: p for p in glob.glob(os.path.join(d, "smplGRTU1_sensor_1_*_info.txt"))}
    keys = sorted(set(a) & set(b))
    return [(a[k], b[k]) for k in keys]


def slot_cross(vx, vy):
    nw, pw = pm.NWIN, pm.NWIN // 2
    ninter = int(round((len(vx) - nw) / pw + 1))
    sxx = np.zeros(pm.NFREQ); syy = np.zeros(pm.NFREQ); sxy = np.zeros(pm.NFREQ, complex); n = 0
    bx = np.zeros(pm.NFFT); by = np.zeros(pm.NFFT)
    for k in range(ninter):
        a = vx[k * pw:k * pw + nw]; b = vy[k * pw:k * pw + nw]
        if np.any(np.abs(a) > pm.SATLIM) or np.any(np.abs(b) > pm.SATLIM):
            continue
        bx[:nw] = a * pm.HANN; by[:nw] = b * pm.HANN
        X = np.fft.rfft(bx)[:pm.NFREQ]; Y = np.fft.rfft(by)[:pm.NFREQ]
        sxx += np.abs(X) ** 2; syy += np.abs(Y) ** 2; sxy += X * np.conj(Y); n += 1
    if n == 0:
        return None
    return sxx / n, syy / n, sxy / n


def polarisation(sxx, syy, sxy, fk):
    out = np.full((3, 3), np.nan)
    for k, f in enumerate(fk):
        if not np.isfinite(f):
            continue
        m = (pm.FREQ >= f - HALF) & (pm.FREQ <= f + HALF)
        a, b, c = sxx[m].mean(), syy[m].mean(), sxy[m].mean()
        az = 0.5 * np.arctan2(2 * c.real, a - b)
        # ellipticity via the polarisation ellipse axes (Means 1972): tan(2*chi) = 2 Im(Sxy) / sqrt((Sxx-Syy)^2 + 4 Re(Sxy)^2)
        denom = np.sqrt((a - b) ** 2 + 4 * c.real ** 2)
        ell = np.tan(0.5 * np.arctan2(2 * c.imag, denom)) if denom > 0 else 0.0
        coh = abs(c) ** 2 / (a * b) if a > 0 and b > 0 else np.nan
        out[k] = (az, ell, coh)
    return out


def main(month):
    pairs = hour_pairs(month)
    if not pairs:
        sys.exit("no paired hour files")
    d0 = np.load(os.path.join(ROOT, "derived", f"SN_{month}_0.npz")); d1 = np.load(os.path.join(ROOT, "derived", f"SN_{month}_1.npz"))
    t0 = d0["t"]; f0 = d0["modes"][:, :, 0]; f1 = d1["modes"][:, :, 0]
    with np.errstate(all="ignore"):
        fk_all = np.nanmean(np.stack([f0, f1]), axis=0)
    t, az, ell, coh, fk_used = [], [], [], [], []
    for n, (ia, ib) in enumerate(pairs):
        ts = pm.parse_info(ia)
        vx = np.fromfile(ia.replace("_info.txt", ""), dtype="<i2").astype(np.float64) * pm.FACDAT
        vy = np.fromfile(ib.replace("_info.txt", ""), dtype="<i2").astype(np.float64) * pm.FACDAT
        for k in range(6):
            tt = ts + k * 153600 * 3906e-6
            j = int(np.argmin(np.abs(t0 - tt)))
            fk = fk_all[j] if abs(t0[j] - tt) < 30 else np.full(3, np.nan)
            cs = slot_cross(vx[k * 153600:(k + 1) * 153600], vy[k * 153600:(k + 1) * 153600])
            p = polarisation(*cs, fk) if cs else np.full((3, 3), np.nan)
            t.append(tt); az.append(p[:, 0]); ell.append(p[:, 1]); coh.append(p[:, 2]); fk_used.append(fk)
        if n % 120 == 0:
            print(f"{month} pol hour {n}/{len(pairs)}", flush=True)
    out = os.path.join(ROOT, "derived", f"POL_{month}.npz")
    np.savez_compressed(out, t=np.array(t), az=np.array(az, np.float32), ell=np.array(ell, np.float32), coh=np.array(coh, np.float32), fk=np.array(fk_used, np.float32),
                        method="cross-spectrum hann2560/8192 50%, +-0.5 Hz about fitted fk; az=0.5 atan2(2ReSxy,Sxx-Syy)")
    A = np.array(az); C = np.array(coh)
    print(f"wrote {out}: {len(t)} slots; median coherence per mode {np.nanmedian(C,0).round(3)}; azimuth IQR deg per mode {(np.degrees(np.nanpercentile(A,75,0)-np.nanpercentile(A,25,0))).round(1)}")


if __name__ == "__main__":
    main(sys.argv[1])
