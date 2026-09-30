import csv, hashlib, os, subprocess, sys, json
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from compose import make, clean_lab
from vpage import page

REPO = "/home/claude/boundlesscaddesign-dev.github.io"
BASE = "https://boundlesscaddesign-dev.github.io"
ISO = {"Germany": "DE", "United Kingdom": "GB", "Canada": "CA", "Spain": "ES", "UAE": "AE", "Netherlands": "NL",
       "Sweden": "SE", "Belgium": "BE", "France": "FR", "Poland": "PL", "Austria": "AT", "Guatemala": "GT", "unknown": ""}
def lang_for(country):
    if country in ("Germany", "Austria", "Switzerland", "Liechtenstein"): return "de"
    if country in ("Spain", "Guatemala", "Mexico", "Chile", "Colombia", "Argentina", "Peru"): return "es"
    return "en"

def leads():
    rows = []
    for r in csv.DictReader(open("hot_queue.csv")):
        if r["status"].startswith("skip"): continue
        rows.append(dict(lab=r["company"], city=r["city"], country=r["country"], email=r["email"], src=f"hot#{r['priority']}", status=r["status"]))
    extra = [("Dentallabor Ramm", "Lennestadt", "info@dentallabor-ramm.de"), ("Schalow Dental-Technik", "Werne", "info@schalow-dentaltechnik.de"),
             ("SUTER Dental Labor", "Bremervörde", "info@suter.de"), ("Dentallabor Andrea Korndörfer", "Ludwigsfelde", "mail@dentallabor-ludwigsfelde.de"),
             ("Zahnärzte im Schloss", "Berlin", "info@zahnaerzte-im-schloss.de"), ("DentsPro", "Berlin", "pankow@dentspro.de"),
             ("Dentallabor Gadau", "Aschaffenburg", "info@gadau-dental.de"), ("Dentallabor Vill & Hapke", "Berlin", "kontakt@vill-hapke.de")]
    for lab, city, em in extra:
        rows.append(dict(lab=lab, city=city, country="Germany", email=em, src="stepstone-2026-09-30", status="sent 2026-09-30"))
    rows.append(dict(lab="Naturaleza Dental Lab", city="", country="Guatemala", email="naturalezadental@hotmail.com", src="naturaleza", status="replied; case links sent"))
    seen, out = set(), []
    for r in rows:
        if r["email"].lower() in seen: continue
        seen.add(r["email"].lower())
        r["lang"] = lang_for(r["country"]); r["iso"] = ISO.get(r["country"], "")
        r["id"] = hashlib.sha1(r["email"].lower().encode()).hexdigest()[:10]
        r["url"] = f"{BASE}/v/{r['id']}/"
        r["gif"] = f"{BASE}/v/{r['id']}/preview.gif"
        out.append(r)
    return out

def build(r):
    d = f"{REPO}/v/{r['id']}"
    os.makedirs(d, exist_ok=True)
    mp4 = f"{d}/video.mp4"
    if not os.path.exists(mp4):
        make(r["lab"], r["city"], r["lang"], mp4)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "12.8", "-i", mp4, "-frames:v", "1", "-q:v", "4", "-vf", "scale=720:-1", f"{d}/poster.jpg"], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf",
            "fps=8,scale=360:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
            "-loop", "0", f"{d}/preview.gif"], check=True)
    open(f"{d}/index.html", "w").write(page(clean_lab(r["lab"]), r["iso"], r["lang"]))
    return r["id"]

if __name__ == "__main__":
    L = leads()
    with open("video_links.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["src", "lab", "city", "country", "lang", "email", "status", "id", "url", "gif"])
        w.writeheader()
        for r in L: w.writerow({k: r[k] for k in w.fieldnames})
    print(len(L), "labs")
    with Pool(2) as p:
        for i, x in enumerate(p.imap_unordered(build, L)):
            print(i, x, flush=True)
