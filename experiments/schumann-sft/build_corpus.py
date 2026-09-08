"""Build the knowledge-injection SFT corpus for the Schumann analyst adapter.

Sources: the dataset knowledge base (dataset/kb/*.md, read for the RAG control context), a
hand-authored fact table below (each fact = one thing a reader of the KB should come away knowing,
with several question phrasings and machine-checkable keys), and per-month statistics computed from
the exported Parquet tables in data/dataset/.

Splits, following the acoustic experiment contract:
  train  : every fact marked trainable, all phrasings except one
  test   : (a) the held-out phrasing of every trainable fact  -> kind "paraphrase"
           (b) facts marked heldout=True, never rendered for training -> kind "unseen"
           (c) data facts for months present, one held-out phrasing   -> kind "data"
The test file is never read by the trainer. Grading keys travel with each row.

Usage: python experiments/schumann-sft/build_corpus.py
Writes: experiments/schumann-sft/data/{sft-train.jsonl, sft-test.jsonl, kb-context.md, corpus-receipt.json}
"""
import glob, hashlib, json, os, random
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
OUT = os.path.join(HERE, "data")
random.seed(13)

SYSTEM = ("You are the analyst for the schumann-sierra-nevada dataset: calibrated Schumann resonance products "
          "derived from the Sierra Nevada ELF station's open raw archive. Answer precisely, give numbers and units "
          "when you know them, and say plainly when something is a model rather than a measurement.")

# (key types) num: number within tol; str: substring (case-insensitive); any: at least one of the substrings
FACTS = [
  dict(id="station-location", q=["Where is the station that produced this dataset?", "Which station recorded the data, and where is it?", "Tell me the location and altitude of the ELF station.", "What are the coordinates of the Sierra Nevada ELF station?"],
       a="The Sierra Nevada ELF station of the University of Granada, Spain, at 37.04 N, 3.32 W, about 2500 m above sea level in the Sierra Nevada National Park near the Refugio del Poqueira.",
       keys=[("str", "Granada"), ("num", 37.04, 0.05), ("num", 2500, 50)]),
  dict(id="band-limits", q=["What frequency band does the dataset cover and why?", "Why does the data stop at 25 Hz?", "What is the calibrated band of the instrument?", "Between which frequencies is the station calibrated?"],
       a="6 to 25 Hz. The station's authors calibrate only that band: below 6 Hz the coil's 1/f noise dominates and above 25 Hz the sensor's own resonance near 33 Hz dominates the record, so the data covers modes 1 to 3 only.",
       keys=[("num", 6, 0.1), ("num", 25, 0.1), ("any", ["33", "resonance"])]),
  dict(id="modes-resolvable", q=["How many Schumann modes can this station resolve?", "Does the dataset contain modes 4 and 5?", "Which modes are in the modes table?", "Can I get the fourth Schumann mode from this data?"],
       a="Only modes 1, 2 and 3, near 7.8, 14 and 20 Hz. Modes 4 and higher fall above the 25 Hz calibrated band where the coil resonance (about 33 Hz) dominates, so they are not resolvable from this instrument.",
       keys=[("any", ["three", "1, 2 and 3", "1-3", "1 to 3"]), ("any", ["not", "cannot", "only"])]),
  dict(id="coil-resonance", q=["At what frequency does the station's coil resonate?", "What is f0 of the sensor's RLC model?", "Where is the magnetometer's self-resonance?", "What resonance frequency does the calibration model use?"],
       a="About 33.06 Hz, from the RLC model with L = 298 kH, C = 77.75 pF and R = 320 kOhm (damping factor about 2.6e-3).",
       keys=[("num", 33.06, 0.2)]),
  dict(id="calibration-constants", q=["What are the RLC constants in the calibration?", "Give me the inductance, capacitance and resistance used to calibrate the coils.", "Which component values define the sensor model?", "What L, C and R does the calibration function use?"],
       a="L = 298 kH, total capacitance C = 77.75 pF (40 + 0.65*55 + 2 pF), R = 320 kOhm. These are the values in the station's code; the paper prints only the 40 pF sensor capacitance.",
       keys=[("num", 298, 1), ("num", 77.75, 0.1), ("num", 320, 1)]),
  dict(id="paper-vs-code", q=["Where do the paper and the station code disagree?", "Why does using the paper's capacitance give the wrong resonance?", "Is the calibration in the paper the same as in the code?", "What discrepancy exists between the published method and the repository?"],
       a="The paper prints a 40 pF capacitance, which would put the coil resonance near 46 Hz; the code uses 77.75 pF, giving 33.06 Hz. Only the code's constants reproduce the station's own spectra.",
       keys=[("num", 40, 0.5), ("num", 77.75, 0.1), ("any", ["46", "33"])]),
  dict(id="scal-formula", q=["What is the calibration function Scal(f)?", "How are volts converted to picotesla per root hertz?", "Write out the amplitude calibration formula.", "What does the RLC calibration multiply the spectrum by?"],
       a="Scal(f) = 1e12/(2500 * 1.9e6) * sqrt((1 - (f/f0)^2)^2 + (2*delta*f/f0)^2) / f, in pT/sqrt(Hz) per V/sqrt(Hz). 1/2500 removes the amplifier gain, 1/1.9e6 is the sensitivity, 1/f is Faraday's law for an induction coil, and the square root undoes the RLC response.",
       keys=[("str", "2500"), ("str", "1.9e6"), ("any", ["1/f", "/ f", "Faraday"])]),
  dict(id="amplitude-only", q=["Is the calibration phase-accurate?", "Why is only the amplitude calibrated?", "Can I recover phase from the calibrated spectra?", "What limits the calibration to amplitude?"],
       a="No. A tenth-order Butterworth filter against 50 Hz mains makes the phase unreliable, so the station calibrates amplitude only. Polarisation is computed from NS/EW ratios where the calibration cancels.",
       keys=[("any", ["Butterworth", "50 Hz"]), ("any", ["amplitude", "not"])]),
  dict(id="sampling", q=["What is the sampling rate of the raw data?", "How many samples are in an hour file and how long does it last?", "Describe the raw file format.", "How are the raw recordings stored?"],
       a="256 Hz, int16 little-endian, 921,600 samples per hour file. The sampling period is 3906 microseconds, so an hour file lasts 3599.77 s and the acquisition drifts 0.23 s per hour; each file carries its own first-sample timestamp.",
       keys=[("num", 256, 0.5), ("num", 921600, 1)]),
  dict(id="volts", q=["How are counts converted to volts?", "What is the ADC scale of the raw data?", "What voltage does one count represent?", "What are the saturation limits?"],
       a="Volts = counts * 10 / 2^15 (16-bit over +-10 V). A sample with |V| > 9.99 V counts as saturated, and any 10-second window containing one is dropped.",
       keys=[("any", ["10 / 2^15", "10/2^15", "2**15", "32768"]), ("num", 9.99, 0.02)]),
  dict(id="welch", q=["What are the Welch parameters of the processing chain?", "How is each 10-minute spectrum computed?", "Describe the windowing and FFT size.", "What window length and overlap does the chain use?"],
       a="Each 10-minute slot is split into 119 windows of 2560 samples (10 s) at 50 percent overlap, Hann-windowed with unit mean power, zero-padded to an 8192-point FFT (31.25 mHz bins); windows containing a saturated sample are dropped and the power is averaged over the rest.",
       keys=[("num", 2560, 1), ("num", 8192, 1), ("any", ["50", "half", "1280"])]),
  dict(id="frequency-step", q=["What is the frequency resolution of the spectra table?", "How many frequency bins are in a spectrum row?", "What is the spacing of frequency_axis.parquet?", "How fine is the frequency axis?"],
       a="31.25 mHz (256 Hz / 8192). The spectra rows carry 609 values from 6.0 to 25.0 Hz.",
       keys=[("num", 31.25, 0.1), ("num", 609, 1)]),
  dict(id="antropo", q=["What does the anthropogenic filter do?", "Which bands are treated as human-made noise?", "How is anthropogenic noise removed?", "What is the straight-line filter in the chain?"],
       a="Two bands, 14.55-15.35 Hz and 16.50-16.90 Hz, are replaced by a straight line when their relative deviation exceeds 2.5 times that of reference bands 13.5-13.9 and 15.8-16.4 Hz.",
       keys=[("num", 14.55, 0.05), ("num", 16.5, 0.05), ("num", 2.5, 0.1)]),
  dict(id="lorentz-fit", q=["How are the mode parameters fitted?", "What model is fitted to each spectrum?", "Describe the Lorentzian fit.", "What are the seeds of the mode fit?"],
       a="Three Lorentzians plus a linear term, a_k/(1+((f-f_k)/s_k)^2) + m f + n, fitted in the amplitude domain over 6.35-23.75 Hz with Levenberg-Marquardt, seeds 8.011, 14.2 and 20.63 Hz with widths 1.78, 1.94 and 2.56 Hz.",
       keys=[("num", 6.35, 0.05), ("num", 23.75, 0.05), ("num", 8.011, 0.05)]),
  dict(id="masked", q=["What does the masked column in the modes table mean?", "When is a mode fit masked?", "Why are some mode fits flagged?", "What are the per-mode windows used for masking?"],
       a="A fit is masked when its centre leaves the per-mode window (6.5-9.5, 12.5-16 or 18.5-22.5 Hz) or its half-width falls outside 0.3-5 Hz. The fit is unbounded, so a few percent of slots land on a wrong local minimum.",
       keys=[("num", 6.5, 0.1), ("num", 9.5, 0.1), ("any", ["0.3", "5 Hz", "width"])]),
  dict(id="verification", q=["How well does the chain reproduce the station's published products?", "What is the verification result against the station's files?", "Was the processing validated?", "How close are the spectra to the station's own?"],
       a="Slot by slot against the station's published npz: amplitude spectrum ratio 1.0000 at the 5th and 95th percentile over 6-25 Hz, saturation correlation 1.000, and median mode-frequency differences within about 0.01 Hz, for both sensors in October and June 2013.",
       keys=[("any", ["1.0000", "1.000"]), ("any", ["0.01", "hundredth", "0.004", "0.008"])]),
  dict(id="verifier-tolerance", q=["What tolerances does the verifier gate enforce?", "When does the verify script fail?", "What makes verify_against_granada exit non-zero?", "State the verification pass criteria."],
       a="At least 95 percent of slots matched within 30 s, spectrum ratio 5th and 95th percentiles within 1 +- 0.005, each mode's median frequency difference under 0.02 Hz, and saturation correlation above 0.99; otherwise it exits 2.",
       keys=[("num", 95, 1), ("num", 0.02, 0.005), ("num", 0.99, 0.005)]),
  dict(id="licence-raw", q=["What licence covers the raw archive?", "Can the derived data be redistributed?", "Under what terms is the Zenodo archive published?", "Is the dataset free to reuse?"],
       a="The raw archive on Zenodo (10.5281/zenodo.6348930, Salinas et al.) is CC BY 4.0, so products derived from it, including this dataset, can be published with attribution. The dataset itself is CC BY 4.0.",
       keys=[("any", ["CC BY 4.0", "CC-BY-4.0", "CC BY"]), ("any", ["attribution", "attrib"])]),
  dict(id="licence-processed", q=["Why are the station's own processed files not in the dataset?", "What licence do the Digibug npz files carry?", "Can the station's Lorentzian fits be redistributed?", "Are the University of Granada processed products included?"],
       a="No. The station's processed npz files on Digibug (10481/71563) are CC BY-NC-ND 3.0; they were used only as a verifier and are never redistributed.",
       keys=[("any", ["NC-ND", "NoDerivs", "NonCommercial"]), ("any", ["verif", "not"])]),
  dict(id="months-available", q=["Which months exist in the raw archive?", "What is the time coverage of the source data?", "How many months of raw data are there?", "What period does the Zenodo archive span?"],
       a="Twelve months: March to December 2013 and January to February 2017. The archive is one 26.5 GB zip; the fetcher reads its central directory over HTTP range requests and streams one month at a time.",
       keys=[("any", ["twelve", "12"]), ("str", "2013"), ("str", "2017")]),
  dict(id="lanes-kp", q=["Where does the Kp lane come from?", "What is the kp column in the lanes table?", "What geomagnetic index is aligned with the slots?", "How is Kp attached to each slot?"],
       a="The 3-hourly planetary Kp index from GFZ Potsdam (Matzka et al. 2021, CC BY 4.0); each slot carries the value of the 3-hour interval containing it.",
       keys=[("str", "GFZ"), ("any", ["3-hour", "three-hour", "3 hour", "3-hourly"])]),
  dict(id="lanes-quakes", q=["What do quake_count_24h and quake_max_mag_24h mean?", "How are earthquakes included in the lanes?", "Which earthquakes appear in the dataset?", "Why is there an earthquake column at all?"],
       a="USGS M6 and greater events in the trailing 24 hours before each slot: the count and the largest magnitude. It exists so the correlation can be shown flat; no physical mechanism is expected.",
       keys=[("str", "USGS"), ("any", ["24", "trailing"]), ("any", ["6", "M6"])]),
  dict(id="night", q=["How is night_fraction computed?", "What does the night lane mean?", "What defines night at the station?", "Is night_fraction a measurement?"],
       a="The fraction of each 10-minute slot during which the sun is below -6 degrees elevation at the station, computed from the timestamp with a low-precision ephemeris. It is computed, not measured.",
       keys=[("num", -6, 0.5), ("any", ["comput", "ephemeris"])]),
  dict(id="chimney-model", q=["What is chimney_model?", "Is the chimney lane a measurement?", "Describe the lightning lane in the dataset.", "How is the thunderstorm schedule represented?"],
       a="A model, not a measurement: three Gaussians in UTC hour for the thunderstorm chimneys, Southeast Asia at 08, Africa at 14.5 and the Americas at 20 UTC, sigma 2.5 hours, weights 0.8, 1.0 and 0.9. It sits in its own config so it is never mistaken for data.",
       keys=[("any", ["model", "not a measurement"]), ("num", 14.5, 0.5), ("num", 20, 0.5)]),
  dict(id="no-lightning", q=["Why is there no measured lightning series?", "Could you add WWLLN or Blitzortung data?", "Where would measured lightning come from?", "Why was a model used instead of lightning data?"],
       a="No openly downloadable measured global lightning series exists for 2013: WWLLN is subscription, the Blitzortung archive answers 401 without a participant login, and NASA's LIS/OTD climatology sits behind Earthdata login. Adding one is a data decision and a join on t_utc.",
       keys=[("any", ["WWLLN", "Blitzortung", "Earthdata"]), ("any", ["login", "subscription", "account"])]),
  dict(id="diurnal-measured", q=["When during the day is mode 1 strongest in October 2013?", "What does the measured daily rhythm look like?", "At what UTC hour does the NS mode-1 amplitude peak?", "Which chimney dominates the October afternoon at this station?"],
       a="The per-UTC-hour mean of the NS mode-1 peak rises from about 0.34 pT/sqrt(Hz) at 01 UTC to about 0.49 at 19-20 UTC: the Americas chimney afternoon, seen from Spain.",
       keys=[("any", ["19", "20"]), ("any", ["Americas", "America"])]),
  dict(id="kp-effect", q=["What effect does a geomagnetic storm have on mode-1 amplitude?", "Does Kp change the Schumann resonance?", "What did the Cann preprint find?", "How big is the storm effect on this archive?"],
       a="Small and real: a 2026 preprint on this archive (Cann, ESS Open Archive) reports daily mean mode-1 amplitude rising about 6 percent on Kp 7 and above days after season and lightning controls. One month at 30-minute resolution cannot resolve it; the correlation stays inside the null band.",
       keys=[("num", 6, 1), ("any", ["Cann", "preprint"])]),
  dict(id="null-band", q=["How should I test a correlation honestly with this data?", "What is the Bartlett correction and why use it?", "Why is the correlation panel's null band so wide?", "What effective sample size does a month give?"],
       a="Use lagged correlation, correct the sample size for autocorrelation with Bartlett's N_eff = N(1-r1 r2)/(1+r1 r2), draw the 95 percent band at +-1.96/sqrt(N_eff), and treat a curve inside it as a null result. A month of 30-minute samples (N about 1500) shrinks to a few dozen effective samples.",
       keys=[("str", "Bartlett"), ("any", ["1.96", "95"]), ("any", ["N_eff", "effective"])]),
  dict(id="oct-storm", q=["What was the strongest geomagnetic interval in October 2013?", "When did the Kp 7.7 storm happen?", "Which interval does the viewer open on?", "Give the peak Kp of October 2013."],
       a="2013-10-02 03:00 UTC, Kp 7.67 (Kp 8-). It is the interval the viewer opens on.",
       keys=[("str", "2013-10-02"), ("num", 7.67, 0.1)]),
  dict(id="jun-storm", q=["What was the peak Kp in June 2013?", "When was the June 2013 storm?", "Which day in June 2013 had the strongest geomagnetic activity?", "Give June 2013's strongest Kp interval."],
       a="Kp 7.0 on 2013-06-01.",
       keys=[("str", "2013-06-01"), ("num", 7.0, 0.1)]),
  dict(id="polarisation-az", q=["What is az_rad in the polarisation table?", "How is the polarisation azimuth defined?", "What is the reference direction for az_rad?", "How do I turn az_rad into a source bearing?"],
       a="The axial polarisation angle of the horizontal magnetic field, in radians from the NS coil axis towards EW, in (-pi/2, pi/2]. The source bearing is roughly az + pi/2 with a 180-degree ambiguity, because the magnetic field of a distant ELF source is azimuthal about the source.",
       keys=[("any", ["NS", "north"]), ("any", ["pi/2", "90"]), ("any", ["ambigu", "180"])]),
  dict(id="polarisation-method", q=["How is the polarisation computed?", "What formula gives the azimuth from the cross-spectrum?", "How wide is the averaging band for polarisation?", "Where does ellipticity come from?"],
       a="From the NS x EW cross-spectral matrix averaged +-0.5 Hz about each mode's fitted centre: az = 0.5 atan2(2 Re Sxy, Sxx - Syy), ellipticity from tan(2 chi) = 2 Im Sxy / sqrt((Sxx-Syy)^2 + 4 Re^2 Sxy), coherence |Sxy|^2/(Sxx Syy). The calibration cancels in these ratios.",
       keys=[("any", ["atan2", "arctan"]), ("num", 0.5, 0.05)]),
  dict(id="polarisation-spread", q=["How consistent is the polarisation azimuth in October 2013?", "What NS/EW coherence does mode 1 show?", "Is the bearing a point or a spread?", "How much does mode-1 azimuth scatter?"],
       a="A spread: mode-1 azimuth has an interquartile range of about 20 degrees and NS/EW coherence of only about 0.17, because the field is a superposition of many sources. The spread is the honest quantity.",
       keys=[("num", 20, 5), ("num", 0.17, 0.05)]),
  dict(id="tables", q=["What tables are in the dataset?", "List the dataset configs.", "How is the dataset organised?", "What files does the Hugging Face dataset contain?"],
       a="Five configs: spectra (slot x sensor, 609-value amplitude rows), modes (slot x sensor x mode fits), polarisation (slot x mode), lanes (Kp, night fraction, earthquakes), and model (the chimney schedule, kept separate). Plus frequency_axis.parquet and a kb/ folder.",
       keys=[("str", "spectra"), ("str", "modes"), ("str", "lanes"), ("str", "polarisation")]),
  dict(id="join", q=["How do I join the tables?", "Are the timestamps regular?", "What key links spectra, modes and lanes?", "Why are the slot times not on exact 10-minute marks?"],
       a="Join on t_utc exactly; all tables share one grid per month. Slots start where the station's hour files start, and the acquisition drifts 0.23 s per hour, so timestamps are irregular by seconds.",
       keys=[("str", "t_utc"), ("any", ["0.23", "drift", "irregular"])]),
  dict(id="units", q=["What are the units of the spectra?", "How do I convert amp to decibels?", "What does 0.4 in the spectra table mean?", "Are the amplitudes in tesla?"],
       a="pT/sqrt(Hz), amplitude spectral density. Decibels re 1 pT/sqrt(Hz) are 20 log10(amp). A typical mode-1 peak is 0.3 to 0.5 pT/sqrt(Hz).",
       keys=[("any", ["pT/sqrt(Hz)", "pT/√Hz", "picotesla"]), ("str", "20")]),
  dict(id="one-station", q=["Is the station amplitude a measure of global lightning power?", "Why can one station mislead about storm activity?", "How does geometry affect the mode amplitudes?", "Why is the cavity view called a one-station inversion?"],
       a="No. Modal amplitude at a station depends on the angle to the active chimney through Legendre functions (H proportional to P_n^1(cos theta)), so amplitude changes can be geometry rather than source strength. One station is not a global storm-power meter.",
       keys=[("any", ["Legendre", "P_n", "angle"]), ("any", ["not", "No"])]),
  dict(id="sensitivity", q=["What is the magnetometer's sensitivity?", "What signal-to-noise does the station quote?", "How sensitive are the coils at 10 Hz?", "What did the 2015 station paper specify?"],
       a="19 microvolts per picotesla at 10 Hz before the x2500 amplifier, and 28 dB signal-to-noise for a 1 pT signal in the 6-25 Hz band (Fornieles-Callejon et al. 2015, Radio Science).",
       keys=[("num", 19, 0.5), ("num", 28, 0.5)]),
  dict(id="saturation-column", q=["What is the sat column?", "How often are windows saturated?", "What does a sat value of 0.017 mean?", "How is saturation reported?"],
       a="The fraction of the slot's 119 ten-second windows that were dropped for containing a saturated sample. October 2013 averaged about 0.011 on NS and 0.013 on EW; 0.017 means two windows of 119.",
       keys=[("num", 119, 1), ("any", ["fraction", "dropped"])]),
  dict(id="chimneys-season", q=["Do the chimney positions move with season?", "Where are the chimney centroids in October?", "What are the seasonal chimney positions used?", "Does the chimney clock change by month?"],
       a="Position moves, the clock does not: in September-November the Maritime Continent sits near 4 S 105 E, Africa near 2 S 25 E and the Americas near 12 S 63 W, while the peak hours stay at the annual 08, 14.5 and 20 UTC.",
       keys=[("any", ["105", "25 E", "63"]), ("any", ["annual", "stay", "does not"])]),
  # held-out facts: never rendered for training
  dict(id="ho-fetch-size", heldout=True, q=["How large is one month of raw data?", "How much does the fetcher download per month?"],
       a="About 2.4 GB compressed per month (2.7 GB extracted), streamed by HTTP range requests from the 26.5 GB Zenodo zip.",
       keys=[("num", 2.4, 0.3), ("num", 26.5, 0.5)]),
  dict(id="ho-hann", heldout=True, q=["How is the Hann window normalised in the chain?", "What normalisation does the window use?"],
       a="1 - cos^2(pi n / N), scaled to unit mean power so the amplitude density is unbiased.",
       keys=[("any", ["unit", "power"])]),
  dict(id="ho-dc", heldout=True, q=["What happens to the DC bin in the amplitude spectrum?", "Is the zero-frequency bin treated specially?"],
       a="The DC bin is divided by sqrt(2) after the one-sided scaling, as in the station's code.",
       keys=[("any", ["sqrt(2)", "root 2", "√2"])]),
  dict(id="ho-slot-count", heldout=True, q=["How many 10-minute slots does October 2013 have per sensor?", "How many rows per sensor are in the October 2013 spectra table?"],
       a="4464 slots per sensor (744 hour files times 6).",
       keys=[("num", 4464, 1)]),
  dict(id="ho-jun-slots", heldout=True, q=["How many slots does June 2013 have?", "How many rows per sensor for June 2013?"],
       a="4320 slots per sensor (720 hours times 6).",
       keys=[("num", 4320, 1)]),
  dict(id="ho-quake-count", heldout=True, q=["How many M6+ earthquakes occurred in October 2013?", "How many earthquakes are in the October 2013 lane?"],
       a="16 events of magnitude 6 or greater (USGS).",
       keys=[("num", 16, 0)]),
  dict(id="ho-reference-bands", heldout=True, q=["Which reference bands does the anthropogenic filter compare against?", "What are the comparison bands for the anthropogenic check?"],
       a="13.5-13.9 Hz and 15.8-16.4 Hz.",
       keys=[("num", 13.5, 0.05), ("num", 15.8, 0.05)]),
  dict(id="ho-viewer-open", heldout=True, q=["Which moment does the viewer show when it first opens?", "What is pinned when the page loads?"],
       a="The month's strongest geomagnetic interval, 2013-10-02 03:00 UTC at Kp 7.67.",
       keys=[("str", "2013-10-02")]),
  dict(id="ho-station-paper", heldout=True, q=["Which paper describes the station hardware?", "Where is the instrument itself documented?"],
       a="Fornieles-Callejon et al. 2015, Radio Science, doi 10.1002/2014RS005567.",
       keys=[("any", ["Fornieles", "2014RS005567"])]),
  dict(id="ho-dataset-licence", heldout=True, q=["What licence does the Hugging Face dataset carry?", "Under what terms is schumann-sierra-nevada published?"],
       a="CC BY 4.0, with attribution to Salinas et al. (Zenodo 10.5281/zenodo.6348930) and the 2022 method paper.",
       keys=[("any", ["CC BY 4.0", "CC-BY-4.0"])]),
]


def month_facts():
    """Data facts computed from the exported Parquet tables for every month present."""
    import pyarrow.parquet as pq
    facts = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "dataset", "modes", "SN_*.parquet"))):
        ym = os.path.basename(p)[3:9]; label = f"{ym[:4]}-{ym[4:]}"
        t = pq.read_table(p).to_pandas()
        ns = t[(t.sensor == "NS") & (~t.masked)]
        means = {k: float(ns[ns["mode"] == k]["f_hz"].mean()) for k in (1, 2, 3)}
        facts.append(dict(id=f"data-{ym}-meanf", q=[f"What were the mean mode centre frequencies (NS) in {label}?", f"Give the average mode 1, 2 and 3 frequencies for {label}.", f"In {label}, where did the three modes sit on average (NS sensor)?"],
                          a=f"NS, unmasked fits, {label}: mode 1 {means[1]:.2f} Hz, mode 2 {means[2]:.2f} Hz, mode 3 {means[3]:.2f} Hz.",
                          keys=[("num", round(means[1], 2), 0.05), ("num", round(means[2], 2), 0.05), ("num", round(means[3], 2), 0.05)]))
        m1 = ns[ns["mode"] == 1].copy(); m1["h"] = m1["t_utc"].dt.hour
        byh = m1.groupby("h")["peak"].mean(); hpk = int(byh.idxmax()); hlo = int(byh.idxmin())
        facts.append(dict(id=f"data-{ym}-diurnal", q=[f"At what UTC hour was NS mode-1 amplitude highest in {label}?", f"When in the day did mode 1 peak in {label}?", f"Give the strongest and weakest UTC hours for mode 1 in {label}."],
                          a=f"In {label} the NS mode-1 peak amplitude was highest around {hpk:02d} UTC ({byh.max():.3f} pT/sqrt(Hz)) and lowest around {hlo:02d} UTC ({byh.min():.3f}).",
                          keys=[("num", hpk, 1), ("num", hlo, 1)]))
        lp = os.path.join(ROOT, "data", "dataset", "lanes", f"SN_{ym}.parquet")
        if os.path.exists(lp):
            l = pq.read_table(lp).to_pandas(); kmax = float(l["kp"].max()); tmax = l.loc[l["kp"].idxmax(), "t_utc"]
            facts.append(dict(id=f"data-{ym}-kp", q=[f"What was the maximum Kp in {label} and when?", f"Give {label}'s strongest geomagnetic interval.", f"How high did Kp get in {label}?"],
                              a=f"Kp reached {kmax:.2f} in {label}, in the 3-hour interval starting {tmax.strftime('%Y-%m-%d %H:%M')} UTC.",
                              keys=[("num", round(kmax, 2), 0.05), ("str", tmax.strftime('%Y-%m-%d'))]))
    return facts


def rows_for(fact, phrasings, split, kind):
    return [{"id": f"{fact['id']}:{i}", "split": split, "kind": kind, "checks": fact["keys"],
             "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": q}, {"role": "assistant", "content": fact["a"]}]}
            for i, q in phrasings]


def main():
    os.makedirs(OUT, exist_ok=True)
    train, test = [], []
    for f in FACTS + month_facts():
        qs = list(enumerate(f["q"]))
        if f.get("heldout"):
            test += rows_for(f, qs, "test", "unseen"); continue
        random.shuffle(qs); ho, tr = qs[0], qs[1:]
        kind = "data" if f["id"].startswith("data-") else "paraphrase"
        test += rows_for(f, [ho], "test", kind); train += rows_for(f, tr, "train", kind)
    random.shuffle(train)
    with open(os.path.join(OUT, "sft-train.jsonl"), "w", encoding="utf-8") as fh:
        for r in train: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, "sft-test.jsonl"), "w", encoding="utf-8") as fh:
        for r in test: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    kb = []
    for p in sorted(glob.glob(os.path.join(ROOT, "dataset", "kb", "*.md"))):
        if os.path.basename(p) == "README.md": continue
        kb.append(open(p, encoding="utf-8").read())
    ctx = "\n\n---\n\n".join(kb)
    open(os.path.join(OUT, "kb-context.md"), "w", encoding="utf-8").write(ctx)
    receipt = {"train": len(train), "test": len(test), "test_kinds": {k: sum(1 for r in test if r["kind"] == k) for k in ("paraphrase", "unseen", "data")},
               "facts": len(FACTS), "context_chars": len(ctx), "train_sha256": hashlib.sha256(open(os.path.join(OUT, "sft-train.jsonl"), "rb").read()).hexdigest()}
    json.dump(receipt, open(os.path.join(OUT, "corpus-receipt.json"), "w"), indent=2)
    print(receipt)


if __name__ == "__main__":
    main()
