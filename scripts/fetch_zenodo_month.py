"""Range-extract one month of raw Sierra Nevada ELF data from Zenodo 6348930.

The record is a single 26.5 GB zip. Zenodo honours HTTP Range, so we read the
zip64 central directory once (cached to data/zenodo-6348930-entries.json), then
stream only the contiguous byte span of the requested month and inflate each
entry locally. One month is ~2.4 GB compressed, ~2.7 GB raw.

Usage: python scripts/fetch_zenodo_month.py 1310      # Oct 2013
Output: data/raw/<YYYY>/<YYMM>/smplGRTU1_sensor_<s>_<YYMMDDHH>[ _info.txt]

Data format (from the *_info.txt files): int16 little-endian, sampling period
3906 us (256 Hz), 921600 samples per file = 1 hour, two sensors (0 = NS, 1 = EW).
Licence of the source: CC BY 4.0 (Salinas et al., University of Granada).
"""
import json, os, struct, subprocess, sys, zlib, time

URL = "https://zenodo.org/api/records/6348930/files/2013_2017.zip/content"
SIZE = 26496304719
ROOT = os.path.join(os.path.dirname(__file__), "..", "data")
ENTRIES = os.path.join(ROOT, "zenodo-6348930-entries.json")


def curl_range(a, b, out=None):
    cmd = ["curl", "-sSL", "-r", f"{a}-{b}", URL]
    if out:
        cmd += ["-o", out]
        return subprocess.run(cmd, check=True)
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def read_central_directory():
    tail = curl_range(SIZE - 65536, SIZE - 1)
    i = tail.rfind(b"PK\x06\x07")
    z64off = struct.unpack("<Q", tail[i + 8:i + 16])[0]
    z = curl_range(z64off, z64off + 55)
    assert z[:4] == b"PK\x06\x06"
    nrec, cdsize, cdoff = struct.unpack("<QQQ", z[32:56])
    cd = curl_range(cdoff, cdoff + cdsize - 1)
    p, ents = 0, []
    while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        meth, = struct.unpack("<H", cd[p + 10:p + 12])
        csz, usz = struct.unpack("<II", cd[p + 20:p + 28])
        n, m, k = struct.unpack("<HHH", cd[p + 28:p + 34])
        lho, = struct.unpack("<I", cd[p + 42:p + 46])
        name = cd[p + 46:p + 46 + n].decode("utf8", "replace")
        extra = cd[p + 46 + n:p + 46 + n + m]
        q = 0
        while q + 4 <= len(extra):
            hid, hl = struct.unpack("<HH", extra[q:q + 4]); d = extra[q + 4:q + 4 + hl]; r = 0
            if hid == 1:
                if usz == 0xFFFFFFFF: usz, = struct.unpack("<Q", d[r:r + 8]); r += 8
                if csz == 0xFFFFFFFF: csz, = struct.unpack("<Q", d[r:r + 8]); r += 8
                if lho == 0xFFFFFFFF: lho, = struct.unpack("<Q", d[r:r + 8]); r += 8
            q += 4 + hl
        ents.append((name, meth, csz, usz, lho))
        p += 46 + n + m + k
    assert len(ents) == nrec, (len(ents), nrec)
    return ents


def main(month):
    if os.path.exists(ENTRIES):
        ents = json.load(open(ENTRIES))
    else:
        ents = read_central_directory()
        json.dump(ents, open(ENTRIES, "w"))
    year = "20" + month[:2]
    m = sorted((e for e in ents if e[0].startswith(f"{year}/{month}/") and not e[0].endswith("/")), key=lambda e: e[4])
    if not m:
        sys.exit(f"no entries for {year}/{month}")
    lo, hi = m[0][4], m[-1][4] + 30 + 1024 + m[-1][2]
    outdir = os.path.join(ROOT, "raw", year, month)
    os.makedirs(outdir, exist_ok=True)
    span = os.path.join(ROOT, f"span_{month}.part")
    if not os.path.exists(span) or os.path.getsize(span) < hi - lo:
        print(f"streaming {len(m)} entries, {(hi-lo)/1e9:.2f} GB compressed -> {span}", flush=True)
        t = time.time(); curl_range(lo, hi - 1, span)
        print(f"done in {time.time()-t:.0f}s", flush=True)
    with open(span, "rb") as f:
        for name, meth, csz, usz, lho in m:
            f.seek(lho - lo)
            hdr = f.read(30)
            assert hdr[:4] == b"PK\x03\x04", name
            n, x = struct.unpack("<HH", hdr[26:30])
            f.seek(n + x, 1)
            raw = f.read(csz)
            data = zlib.decompressobj(-15).decompress(raw) if meth == 8 else raw
            assert len(data) == usz, (name, len(data), usz)
            with open(os.path.join(outdir, os.path.basename(name)), "wb") as o:
                o.write(data)
    os.remove(span)
    print(f"extracted {len(m)} files to {outdir}")


if __name__ == "__main__":
    main(sys.argv[1])
