# The station and its calibration

**Sierra Nevada ELF station**, University of Granada. 37°02′ N, 3°19′ W, 2500 m, inside a national
park near the Refugio del Poqueira. Deployed July 2012, operating almost continuously since March
2013. Two induction-coil magnetometers, oriented north–south (sensor 0, "NS") and east–west (sensor 1,
"EW"). Sampling 256 Hz (period 3906 µs, so an hour file of 921,600 samples lasts 3599.77 s and the
acquisition drifts 0.23 s per hour; every file carries its own first-sample timestamp). Digitisation
16 bit over ±10 V; values beyond ±9.99 V are saturation. Sensitivity 19 µV/pT at 10 Hz before the
×2500 amplifier; 28 dB signal-to-noise for a 1 pT signal in 6–25 Hz.

## Why the band is 6–25 Hz

The coil plus its cabling and amplifier form an RLC circuit. The station's code models it with
L = 298 kH, R = 320 kΩ and a total capacitance C = 40 + 0.65·55 + 2 = 77.75 pF, which puts the
resonance at

    f0 = 1 / (2π √(LC)) = 33.06 Hz,   δ = (R/2) √(C/L) = 2.58 × 10⁻³.

The method paper prints only the 40 pF sensor capacitance, which would put f0 at 46 Hz; only the code's
constants reproduce the station's own spectra. In raw counts the 8 Hz mode sits near 3 × 10³
counts²/Hz while 30–33 Hz reaches 2.4 × 10⁵: above 25 Hz the record is the sensor ringing, not the
cavity. Below 6 Hz the coil's 1/f noise dominates. The authors therefore calibrate 6–25 Hz only, and
this dataset stops there. **Modes 1, 2 and 3 are all this instrument can resolve.**

## The calibration function

Amplitude-only (a tenth-order Butterworth against 50 Hz mains makes the phase unreliable):

    B(f) = Scal(f) · V(f)
    Scal(f) = 1e12 / (2500 · 1.9e6) · √((1 − (f/f0)²)² + (2 δ f/f0)²) / f      [pT/√Hz per V/√Hz]

1/2500 removes the amplifier gain, 1/1.9e6 is the magnetometer sensitivity, 1/f is Faraday's law for an
induction coil, and the square root undoes the RLC response. At 10 Hz, Scal ≈ 19 pT per volt, which
matches the quoted 19 µV/pT once the ×2500 gain is included.

## Sources

- Fornieles-Callejón et al. (2015), Extremely low frequency band station for natural electromagnetic
  noise measurement, *Radio Science*, doi:10.1002/2014RS005567.
- Salinas et al. (2022), Schumann resonance data processing programs and four-year measurements from
  Sierra Nevada ELF station, *Computers & Geosciences* 165:105148, doi:10.1016/j.cageo.2022.105148.
- Station code: github.com/asalinas62/Sierra_Nevada_SR (`Reading_Fourier.py` holds the constants).
