"""Synthetic checks on the processing chain. Run: python -m pytest -q  (or python tests/test_chain.py)"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import process_month as pm  # noqa: E402


def test_calibration_constants():
    # Station model: coil resonance ~33 Hz, damping ~2.6e-3 (Salinas et al. 2022, Reading_Fourier.py)
    assert abs(pm.F0 - 33.06) < 0.05
    assert abs(pm.DELTA - 0.00258) < 5e-5
    # Station paper quotes 19 uV/pT at 10 Hz before the x2500 amplifier: 1/(19e-6*2500) ~ 21 pT per volt.
    s10 = pm.scal(np.array([10.0]))[0]
    assert 15 < s10 < 25, s10


def test_hann_unit_power():
    w = pm.hann(2560)
    assert abs(np.mean(w ** 2) - 1.0) < 1e-9


def test_spectrum_recovers_tone_amplitude():
    fs, n = 256, 153600
    tt = np.arange(n) / fs
    f_tone = 8.0
    v = 0.01 * np.sin(2 * np.pi * f_tone * tt)  # 10 mV tone, well below saturation
    amp, sat = pm.slot_spectrum(v)
    assert sat == 0.0
    j = pm.pofre(f_tone)
    assert np.argmax(amp[pm.pofre(6):pm.pofre(25)]) + pm.pofre(6) == j


def test_saturation_drops_windows():
    v = np.zeros(153600); v[:5000] = 10.0
    amp, sat = pm.slot_spectrum(v)
    assert 0 < sat < 0.1


def test_lorentzian_fit_recovers_modes():
    f = pm.FREQ
    truth = [(0.4, 7.8, 1.7), (0.35, 14.1, 1.9), (0.3, 20.5, 2.5)]
    y = sum(a / (1 + ((f - fk) / s) ** 2) for a, fk, s in truth) + 0.05 + 0.002 * f
    rng = np.random.default_rng(0)
    y = (y + rng.normal(0, 0.005, len(f))).astype(np.float32)
    m, chi2 = pm.fit_modes(y, [0.4, 0.35, 0.3])
    for k, (a, fk, s) in enumerate(truth):
        assert abs(m[k, 0] - fk) < 0.03, (k, m[k])
        assert abs(m[k, 3] - s) < 0.15, (k, m[k])


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
