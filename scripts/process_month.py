"""Raw Sierra Nevada hour files -> calibrated 10-minute amplitude spectra + Lorentzian mode fits.

Mirrors the station's own chain (Salinas et al. 2022, Computers & Geosciences 165:105148,
code github.com/asalinas62/Sierra_Nevada_SR: Reading_Fourier.py, Antropo.py, Lorentz_Lmfit.py)
so that the output can be checked slot-by-slot against the published npz files.

Input : data/raw/<YYYY>/<YYMM>/smplGRTU1_sensor_<s>_<YYMMDDHH>  (+ _info.txt)
        int16 LE, 256 Hz, 921600 samples per hour file, sensor 0 = NS, 1 = EW.
        Volts = counts * 10 / 2**15. Saturation = |V| > 9.99.
Output: data/derived/SN_<YYMM>_<s>.npz
        t        unix seconds, start of each 10-min slot (slots follow the hour files, as the station does)
        f        frequency axis 0..FMAX Hz, step 256/8192 = 31.25 mHz
        amp      float32 [slots, freqs] amplitude spectral density, pT/sqrt(Hz), NaN where no data
        sat      fraction of saturated 10-s windows per slot
        modes    float32 [slots, 3, 4] per mode: (f_k, peak, a_k, s_k); NaN on failure/no data
        chi2     fit chi-square per slot

Pinned method:
  Welch: 10-s Hann windows (2560 samples, unit-power normalised), 50 % overlap, 119 windows per slot,
  zero-padded FFT to 8192, windows containing any saturated sample dropped.
  amp = sqrt(sum|FFT|^2 * 2 / (nwin * fs * 2560)) * Scal(f)
  Scal(f) = 1e12/(2500 * 1.9e6) * sqrt((1-(f/f0)^2)^2 + (2 d f/f0)^2) / f
    with L = 298 kH, C = 40 + 0.65*55 + 2 pF, R = 320 kOhm, f0 = 1/(2 pi sqrt(LC)), d = R/2 sqrt(C/L).
  The station calibrates 6..25 Hz only. We apply the same formula over 0..FMAX and label it.
  Anthropogenic filter: bands 14.55-15.35 and 16.50-16.90 Hz replaced by a straight line when their
  relative deviation exceeds 2.5x that of reference bands 13.5-13.9 / 15.8-16.4 Hz.
  Lorentzian (amplitude domain, 6.35..23.75 Hz):
    sum_k a_k / (1 + ((f - f_k)/s_k)^2) + m f + n, seeds f = 8.011/14.2/20.63, s = 1.78/1.94/2.56,
    a_k = month-mean spectrum at the seed, Levenberg-Marquardt, unbounded (as the station does).
"""
import glob, os, re, sys, datetime as dt
import numpy as np
from scipy.optimize import least_squares

FS, NWIN, NFFT, FMAX = 256, 2560, 8192, 26.0
FACDAT = 10.0 / 2 ** 15
SATLIM = 9.99
DF = FS / NFFT
ROOT = os.path.join(os.path.dirname(__file__), "..", "data")

L, C, R = 298e3, 40e-12 + 0.65 * 55e-12 + 2e-12, 320e3
F0 = 1 / (2 * np.pi * np.sqrt(C * L)); DELTA = R / 2 * np.sqrt(C / L)


def scal(f):
    f = np.where(f > 0, f, np.nan)
    return 1e12 / (2500.0 * 1.9e6) * np.sqrt((1 - (f / F0) ** 2) ** 2 + (2 * DELTA * f / F0) ** 2) / f


def hann(m):
    w = 1.0 - np.cos(np.arange(m) * np.pi / m) ** 2
    return w / np.sqrt(np.sum(w ** 2) / m)


HANN = hann(NWIN)
NFREQ = int(round(FMAX / DF)) + 1
FREQ = np.arange(NFREQ) * DF
SCAL = scal(FREQ)


def parse_info(path):
    txt = open(path, encoding="latin1").read()
    ts = re.search(r"1st sample timestamp: (\S+) (\S+) UTC", txt)
    d = dt.datetime.strptime(ts.group(1) + " " + ts.group(2), "%d-%m-%Y %H:%M:%S.%f").replace(tzinfo=dt.timezone.utc)
    return d.timestamp()


def slot_spectrum(v):
    """v: 153600 volts -> (amp[NFREQ] in pT/sqrtHz or None, saturation fraction)."""
    nw = NWIN; pw = NWIN // 2
    ninter = int(round((len(v) - nw) / pw + 1))
    acc = np.zeros(NFREQ); nsat = 0
    buf = np.zeros(NFFT)
    for k in range(ninter):
        seg = v[k * pw:k * pw + nw]
        if np.any(np.abs(seg) > SATLIM):
            nsat += 1; continue
        buf[:nw] = seg * HANN
        acc += np.abs(np.fft.rfft(buf)[:NFREQ]) ** 2
    if nsat == ninter:
        return None, 1.0
    amp = np.sqrt(acc * 2.0 / ((ninter - nsat) * FS * nw))
    amp[0] /= np.sqrt(2.0)
    return (amp * SCAL).astype(np.float32), nsat / ninter


def pofre(f):
    return int(round(f / DF))


ANTRO = [((14.55, 15.35), (13.5, 13.9)), ((16.50, 16.90), (15.8, 16.4))]


def antropo(amp):
    def recta(val, frec):
        a = (val[-1] - val[0]) / (frec[-1] - frec[0]); mod = a * (frec - frec[0]) + val[0]
        d = (val - mod) / mod
        return mod, d.max() + d.min()
    out = amp.copy()
    for (a0, a1), (r0, r1) in ANTRO:
        ra, rb = pofre(r0), pofre(r1) + 1; aa, ab = pofre(a0), pofre(a1) + 1
        _, dref = recta(out[ra:rb], FREQ[ra:rb])
        mod, dev = recta(out[aa:ab], FREQ[aa:ab])
        if dev > 2.5 * abs(dref):
            out[aa:ab] = mod
    return out


FIT = (FREQ >= 6.35 - 1e-9) & (FREQ <= 23.75 + 1e-9)
SEED_F, SEED_S = (8.011, 14.2, 20.63), (1.78, 1.94, 2.56)


def model(p, x):
    return sum(p[k] / (1 + ((x - p[3 + k]) / p[6 + k]) ** 2) for k in range(3)) + p[9] * x + p[10]


def fit_modes(amp, seed_a):
    x, y = FREQ[FIT], amp[FIT]
    if not np.all(np.isfinite(y)):
        return np.full((3, 4), np.nan, np.float32), np.nan
    p0 = np.array([*seed_a, *SEED_F, *SEED_S, 0.0, 0.0])
    try:
        r = least_squares(lambda p: model(p, x) - y, p0, method="lm", max_nfev=2000)
    except Exception:
        return np.full((3, 4), np.nan, np.float32), np.nan
    p = r.x
    out = np.array([[p[3 + k], model(p, np.array([p[3 + k]]))[0], p[k], abs(p[6 + k])] for k in range(3)], np.float32)
    return out, float(np.sum(r.fun ** 2))


def main(month, sensor):
    year = "20" + month[:2]
    d = os.path.join(ROOT, "raw", year, month)
    infos = sorted(glob.glob(os.path.join(d, f"smplGRTU1_sensor_{sensor}_*_info.txt")))
    if not infos:
        sys.exit(f"no files in {d}")
    t, amps, sats = [], [], []
    for n, info in enumerate(infos):
        ts = parse_info(info)
        v = np.fromfile(info.replace("_info.txt", ""), dtype="<i2").astype(np.float64) * FACDAT
        for k in range(6):
            a, s = slot_spectrum(v[k * 153600:(k + 1) * 153600])
            t.append(ts + k * 153600 * 3906e-6); amps.append(a); sats.append(s)
        if n % 120 == 0:
            print(f"{month} s{sensor} hour {n}/{len(infos)}", flush=True)
    A = np.full((len(amps), NFREQ), np.nan, np.float32)
    for i, a in enumerate(amps):
        if a is not None:
            A[i] = antropo(a)
    mean = np.nanmean(A, axis=0)
    seed_a = [mean[pofre(f)] for f in SEED_F]
    modes, chi2 = [], []
    for i in range(len(A)):
        m, c = fit_modes(A[i], seed_a); modes.append(m); chi2.append(c)
    os.makedirs(os.path.join(ROOT, "derived"), exist_ok=True)
    out = os.path.join(ROOT, "derived", f"SN_{month}_{sensor}.npz")
    np.savez_compressed(out, t=np.array(t), f=FREQ, amp=A, sat=np.array(sats, np.float32), modes=np.array(modes), chi2=np.array(chi2),
                        method="Salinas2022 chain; Welch hann2560/8192 50%; Scal RLC; antropo; lorentz3 amp 6.35-23.75",
                        source="Zenodo 10.5281/zenodo.6348930 CC BY 4.0, Salinas et al.")
    ok = np.isfinite(np.array(modes)[:, :, 0]).all(1).sum()
    print(f"wrote {out}: {len(A)} slots, {ok} fitted, mean saturation {np.mean(sats):.4f}, f0_sensor={F0:.2f} Hz")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
