# Reading the data

## Joining

All tables share one time grid per month: the start of each 10-minute slot, taken from the station's
hour files (so timestamps are irregular by seconds). Join on `t_utc` exactly.

```python
import pandas as pd
modes = pd.read_parquet("modes/SN_201310.parquet")
lanes = pd.read_parquet("lanes/SN_201310.parquet")
m1 = modes[(modes["mode"] == 1) & (modes["sensor"] == "NS") & (~modes["masked"])]
df = m1.merge(lanes, on="t_utc")
print(df.groupby(df["t_utc"].dt.hour)["peak"].mean())        # the daily rhythm
```

## The spectra

`spectra.amp` is a fixed-length list of 609 floats on the axis in `frequency_axis.parquet`
(6.0 to 25.0 Hz in 31.25 mHz steps). Units pT/√Hz. Convert to dB re 1 pT/√Hz with `20·log10`.
NaN means the whole slot was saturated or missing.

## Correlation honesty rules

1. Use lagged correlation, not a single coefficient; Kp is 3-hourly and the ionosphere responds with
   delay.
2. Correct the sample size for autocorrelation. Both the resonance series and Kp are strongly
   autocorrelated; Bartlett's `N_eff = N·(1 − r₁r₂)/(1 + r₁r₂)` reduces a month of 30-minute samples
   (N ≈ 1500) to a few dozen effective samples.
3. Draw the 95 % null band `±1.96/√N_eff` and treat a curve inside it as a null result.
4. Remove the diurnal cycle before correlating anything with a series that itself has one (night
   fraction, the chimney model), or you will measure the clock.
5. Never correlate against the model lane and call it lightning.
6. One station is not a global storm-power meter: modal amplitude depends on the angle between the
   station and the active chimney through Legendre functions, so amplitude changes can be geometry.

## Polarisation

`az_rad` is axial (period π). Average it with the doubled-angle trick:
`½·atan2(mean(sin 2az), mean(cos 2az))`. NS/EW coherence is low on average (~0.17 for mode 1) because
the field is a superposition of many sources; a bearing is a distribution, and its spread is the
honest quantity.
