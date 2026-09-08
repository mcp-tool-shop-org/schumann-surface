"""One month end to end: fetch raw (Zenodo range), process both sensors, polarisation, verify against
the station if its npz is available (range-extracted from Digibug), export Parquet.
Usage: python scripts/pipeline_month.py 1303 [1304 ...]
Skips steps whose outputs already exist. Logs to data/pipeline_<month>.log.
"""
import json, os, struct, subprocess, sys, urllib.request, zlib

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
PY = sys.executable
DIGI = "https://digibug.ugr.es/bitstream/handle/10481/71563/Npz.zip?sequence=1&isAllowed=y"


def run(args, log):
    log.write(f"$ {' '.join(args)}\n"); log.flush()
    r = subprocess.run([PY] + args, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    log.write(f"exit {r.returncode}\n"); log.flush()
    return r.returncode


def digibug_entries():
    p = os.path.join(DATA, "digibug-71563-entries.json")
    if os.path.exists(p):
        return json.load(open(p))
    def rng(a, b):
        req = urllib.request.Request(DIGI, headers={"Range": f"bytes={a}-{b}", "User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(req, timeout=600).read()
    SIZE = 3579685616
    tail = rng(SIZE - 65536, SIZE - 1)
    i = tail.rfind(b"PK\x06\x07")
    if i >= 0:
        z64off = struct.unpack("<Q", tail[i + 8:i + 16])[0]; z = rng(z64off, z64off + 55); nrec, cdsize, cdoff = struct.unpack("<QQQ", z[32:56])
    else:
        i = tail.rfind(b"PK\x05\x06"); nrec, cdsize, cdoff = struct.unpack("<HII", tail[i + 10:i + 20])
    cd = rng(cdoff, cdoff + cdsize - 1); p0, ents = 0, []
    while p0 < len(cd) and cd[p0:p0 + 4] == b"PK\x01\x02":
        meth, = struct.unpack("<H", cd[p0 + 10:p0 + 12]); csz, usz = struct.unpack("<II", cd[p0 + 20:p0 + 28])
        n, m, k = struct.unpack("<HHH", cd[p0 + 28:p0 + 34]); lho, = struct.unpack("<I", cd[p0 + 42:p0 + 46])
        name = cd[p0 + 46:p0 + 46 + n].decode(); ents.append((name, meth, csz, usz, lho)); p0 += 46 + n + m + k
    json.dump(ents, open(p, "w"))
    return ents


def fetch_granada(month, log):
    outdir = os.path.join(DATA, "granada"); os.makedirs(outdir, exist_ok=True)
    want = [f"Npz/SN_{month}_LO_6_1_0.npz", f"Npz/SN_{month}_LO_6_1_1.npz"]
    if all(os.path.exists(os.path.join(outdir, os.path.basename(w))) for w in want):
        return True
    try:
        ents = digibug_entries()
        def rng(a, b):
            req = urllib.request.Request(DIGI, headers={"Range": f"bytes={a}-{b}", "User-Agent": "Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=600).read()
        for name, meth, csz, usz, lho in ents:
            if name in want:
                hdr = rng(lho, lho + 29); n, x = struct.unpack("<HH", hdr[26:30]); st = lho + 30 + n + x
                raw = rng(st, st + csz - 1); d = zlib.decompressobj(-15).decompress(raw) if meth == 8 else raw
                assert len(d) == usz
                open(os.path.join(outdir, os.path.basename(name)), "wb").write(d); log.write(f"granada {name} {len(d)}\n")
        return True
    except Exception as e:
        log.write(f"granada fetch failed: {e!r}\n"); return False


def month(m):
    year = "20" + m[:2]; yyyymm = "20" + m
    with open(os.path.join(DATA, f"pipeline_{m}.log"), "a", encoding="utf8") as log:
        raw = os.path.join(DATA, "raw", year, m)
        if not (os.path.isdir(raw) and len(os.listdir(raw)) > 100):
            if run(["scripts/fetch_zenodo_month.py", m], log): return False
        for s in (0, 1):
            if not os.path.exists(os.path.join(DATA, "derived", f"SN_{m}_{s}.npz")):
                if run(["scripts/process_month.py", m, str(s)], log): return False
        if not os.path.exists(os.path.join(DATA, "derived", f"POL_{m}.npz")):
            if run(["scripts/polarisation_month.py", m], log): return False
        # lanes
        kp_path = os.path.join(DATA, "lanes", f"kp_{yyyymm}.txt")
        if not os.path.exists(kp_path):
            src = os.path.join(DATA, "lanes", "Kp_ap_since_1932.txt")
            if not os.path.exists(src):
                urllib.request.urlretrieve("https://kp.gfz-potsdam.de/app/files/Kp_ap_since_1932.txt", src)
            with open(src) as f, open(kp_path, "w") as o:
                for line in f:
                    if line.startswith(f"{year} {m[2:]} "): o.write(line)
        q_path = os.path.join(DATA, "lanes", f"usgs_{yyyymm}_m6.geojson")
        if not os.path.exists(q_path):
            y, mo = int(year), int(m[2:]); nxt = f"{y + (mo == 12)}-{(mo % 12) + 1:02d}-01"
            urllib.request.urlretrieve(f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={year}-{m[2:]}-01&endtime={nxt}&minmagnitude=6", q_path)
        if fetch_granada(m, log):
            for s in (0, 1):
                if run(["scripts/verify_against_granada.py", m, str(s)], log):
                    log.write(f"VERIFY FAILED {m} sensor {s}\n"); return False
        if run(["scripts/export_dataset.py", m], log): return False
        log.write(f"MONTH {m} DONE\n")
    return True


if __name__ == "__main__":
    ok = [m for m in sys.argv[1:] if month(m)]
    print("done:", ok)
