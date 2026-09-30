"""Compose a personalised 15-second BoundlessCAD video for one lab.
usage: python3 compose.py "<Lab name>" "<City>" <lang en|de|es> <out.mp4>"""
import sys, os, re, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from crown import margin_overlay
from cache_crown import yaw

W = H = 1080
FPS = 30
NF = 450
NAVY = (11, 27, 58); NAVY2 = (18, 44, 88); TEAL = (32, 201, 187); WHITE = (244, 248, 252)
MUTED = (160, 180, 205)
FD = "/usr/share/fonts/truetype/google-fonts/"
def F(w, s): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)

TXT = {
 "en": dict(hello="Hello,", made="We made this 15-second video just for you.",
   s2t="Your crowns, designed in exocad", s2s="Margins · contacts · occlusion — every case checked by a dentist",
   s3t="Designed while {city} sleeps", s3t0="Designed while you sleep", t1="18:00 in {city}", t10="18:00 your time",
   t1s="You send the scan", t2s="Ready-to-mill files in your inbox", foot="Crowns & bridges · standard service 24–48 h",
   free1="Your first case is", free2="FREE", res="RESERVED FOR", case="Case no.", cta="Just reply to our email with your scan."),
 "de": dict(hello="Hallo,", made="Dieses 15-Sekunden-Video haben wir nur für Sie gemacht.",
   s2t="Ihre Kronen, konstruiert in exocad", s2s="Ränder · Kontakte · Okklusion — jeder Fall von einem Zahnarzt geprüft",
   s3t="Konstruiert, während {city} schläft", s3t0="Konstruiert, während Sie schlafen", t1="18:00 in {city}", t10="18:00 Ihre Zeit",
   t1s="Sie senden den Scan", t2s="Fräsfertige Dateien im Postfach", foot="Kronen & Brücken · Standardservice 24–48 h",
   free1="Ihr erster Fall ist", free2="GRATIS", res="RESERVIERT FÜR", case="Fall-Nr.", cta="Einfach auf unsere E-Mail mit Ihrem Scan antworten."),
 "es": dict(hello="Hola,", made="Hicimos este video de 15 segundos solo para ustedes.",
   s2t="Sus coronas, diseñadas en exocad", s2s="Márgenes · contactos · oclusión — cada caso revisado por un odontólogo",
   s3t="Diseñado mientras {city} duerme", s3t0="Diseñado mientras ustedes duermen", t1="18:00 en {city}", t10="18:00 su hora",
   t1s="Ustedes envían el escaneo", t2s="Archivos listos para fresar en su correo", foot="Coronas y puentes · servicio estándar 24–48 h",
   free1="Su primer caso es", free2="GRATIS", res="RESERVADO PARA", case="Caso n.º", cta="Solo respondan a nuestro correo con su escaneo."),
}

def ease(t):
    t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
def out_back(t):
    t = min(max(t, 0.0), 1.0); c = 1.70158
    return 1 + (c+1)*(t-1)**3 + c*(t-1)**2
def win(f, a, b, fade=10):
    """1 inside [a,b], eased fade in/out over `fade` frames."""
    return ease((f-a)/fade) * (1-ease((f-(b-fade))/fade))

# ---------- static layers ----------
def background():
    y = np.linspace(0, 1, H)[:, None, None]
    g = np.array(NAVY2)*(1-y) + np.array(NAVY)*y
    img = np.repeat(g, W, 1)
    xx, yy = np.meshgrid(np.arange(W), np.arange(H))
    glow = np.exp(-(((xx-540)/420)**2 + ((yy-520)/380)**2))[..., None]
    img = img + glow*np.array([10, 40, 45])
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(im)
    for x in range(30, W, 40):
        for y2 in range(30, H, 40):
            d.point((x, y2), fill=(60, 95, 140, 255))
    return im
BG = background()

def logo():
    L = Image.open("logo.png").convert("RGBA")
    bb = L.getbbox(); L = L.crop(bb)
    h = 58; return L.resize((int(L.width*h/L.height), h), Image.LANCZOS)
LOGO = logo()

# ---------- text helpers ----------
def text_layer(canvas, xy, text, font, fill, alpha=1.0, anchor="la", dy=0):
    if alpha <= 0.01: return
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((xy[0], xy[1]+dy), text, font=font, fill=fill+(int(255*alpha),), anchor=anchor)
    canvas.alpha_composite(lay)

def fit_font(text, weight, maxw, start, minsize=34):
    s = start
    while s > minsize:
        f = F(weight, s)
        if f.getlength(text) <= maxw: return f, [text]
        s -= 4
    # wrap into two lines
    words = text.split(); best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        m = max(F(weight, 60).getlength(a), F(weight, 60).getlength(b))
        if best is None or m < best[0]: best = (m, a, b)
    lines = [best[1], best[2]] if best else [text]
    s = start
    while s > 30:
        f = F(weight, s)
        if max(f.getlength(l) for l in lines) <= maxw: return f, lines
        s -= 4
    return F(weight, 30), lines

def rounded(d, box, r, **kw): d.rounded_rectangle(box, r, **kw)

# ---------- scenes ----------
def crown_img(f):
    p = f"cache/c{f:04d}.png"
    return Image.open(p) if os.path.exists(p) else None

def frame(f, lab, city, T, code):
    im = BG.copy()
    im.alpha_composite(LOGO, (56, 48))

    # ---- S1 greeting (0-90)
    a1 = win(f, 0, 96, 14)
    if a1 > 0:
        up = (1-ease(f/18))*30
        text_layer(im, (540, 330), T["hello"], F("Medium", 56), MUTED, a1, "mm", up)
        fnt, lines = fit_font(lab, "Bold", 900, 104)
        y0 = 450 - (len(lines)-1)*fnt.size*0.55
        for i, l in enumerate(lines):
            t = ease((f-6-i*4)/18)
            text_layer(im, (540, y0 + i*fnt.size*1.1), l, fnt, WHITE, a1*t, "mm", (1-t)*40)
        last_y = y0 + (len(lines)-1)*fnt.size*1.1
        if city:
            text_layer(im, (540, last_y+95), city.upper(), F("Medium", 34), TEAL, a1*ease((f-18)/16), "mm")
        text_layer(im, (540, last_y+175), T["made"], F("Regular", 30), MUTED, a1*ease((f-30)/16), "mm")
        # orbit ring drawing around the name
        prog = ease((f-4)/60)
        if prog > 0:
            ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            rd = ImageDraw.Draw(ring)
            bw = min(1000, max(fnt.getlength(l) for l in lines) + 140)
            box = [540-bw/2, last_y-150-(len(lines)-1)*fnt.size*0.55, 540+bw/2, last_y+130]
            rd.arc(box, -200, -200+360*prog, fill=TEAL+(int(200*a1),), width=4)
            ring = ring.filter(ImageFilter.GaussianBlur(0.6))
            im.alpha_composite(ring)

    # ---- crown (78-380)
    c = crown_img(f) if 92 <= f < 353 else None
    if c is not None:
        ca = ease((f-92)/14) * (1-ease((f-334)/18))
        if f < 225:
            sc, cy = 1.2, 110
        else:
            t = ease((f-225)/30)
            sc, cy = 1.2 - 0.35*t, 110 + 0*t
        if f >= 345:
            t = ease((f-345)/35); sc -= 0.2*t; cy -= 40*t
        size = int(760*sc)
        ci = c
        if 238 <= f < 345:
            mo = margin_overlay(yaw(f), ease((f-240)/95), size=760, scale=200)
            ci = c.copy(); ci.alpha_composite(mo)
        ci = ci.resize((size, size), Image.LANCZOS)
        if ca < 1:
            ci.putalpha(ci.getchannel("A").point(lambda v: int(v*ca)))
        im.alpha_composite(ci, (540-size//2, int(cy)))

    # ---- S2 captions (95-230)
    a2 = win(f, 96, 232, 14)
    if a2 > 0:
        text_layer(im, (540, 170), T["s2t"], fit_font(T["s2t"], "Bold", 960, 54)[0], WHITE, a2, "mm", (1-ease((f-96)/16))*24)
        text_layer(im, (540, 935), T["s2s"], fit_font(T["s2s"], "Regular", 980, 30)[0], MUTED, a2*ease((f-120)/16), "mm")

    # ---- S3 overnight timeline (240-350)
    a3 = win(f, 238, 352, 14)
    if a3 > 0:
        h = T["s3t"].format(city=city) if city else T["s3t0"]
        text_layer(im, (540, 165), h, fit_font(h, "Bold", 960, 50)[0], WHITE, a3, "mm", (1-ease((f-238)/16))*24)
        card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        rounded(cd, [70, 700, 1010, 950], 28, fill=(9, 22, 48, int(235*a3)), outline=TEAL+(int(120*a3),), width=2)
        im.alpha_composite(card)
        t1 = T["t1"].format(city=city) if city else T["t10"]
        text_layer(im, (110, 745), t1, fit_font(t1, "Bold", 400, 40)[0], WHITE, a3)
        text_layer(im, (110, 800), T["t1s"], fit_font(T["t1s"], "Regular", 400, 28)[0], MUTED, a3)
        text_layer(im, (970, 745), "08:00", F("Bold", 40), TEAL, a3*ease((f-315)/12), "ra")
        text_layer(im, (970, 800), T["t2s"], fit_font(T["t2s"], "Regular", 440, 28)[0], MUTED, a3*ease((f-318)/12), "ra")
        # progress bar with moon -> sun
        p = ease((f-255)/70)
        bar = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bar)
        x0, x1, yb = 110, 970, 880
        bd.rounded_rectangle([x0, yb-5, x1, yb+5], 5, fill=(40, 70, 110, int(255*a3)))
        bd.rounded_rectangle([x0, yb-5, x0+(x1-x0)*p, yb+5], 5, fill=TEAL+(int(255*a3),))
        mx = x0+(x1-x0)*p
        if p < 1:
            bd.ellipse([mx-18, yb-18, mx+18, yb+18], fill=(235, 240, 255, int(255*a3)))
            bd.ellipse([mx-10, yb-24, mx+22, yb+8], fill=(9, 22, 48, int(255*a3)))  # crescent moon
        else:
            bd.ellipse([mx-20, yb-20, mx+20, yb+20], fill=TEAL+(int(255*a3),))
            bd.line([(mx-9, yb), (mx-2, yb+8), (mx+10, yb-8)], fill=(255, 255, 255, int(255*a3)), width=5)
        im.alpha_composite(bar)
        text_layer(im, (540, 985), T["foot"], F("Regular", 24), MUTED, a3*0.9, "mm")

    # ---- S4 free case ticket (350-450)
    if f >= 352:
        a4 = ease((f-352)/16)
        text_layer(im, (540, 250), T["free1"], F("Medium", 48), WHITE, a4, "mm", (1-a4)*24)
        s = out_back((f-362)/18)
        if s > 0:
            fr = F("Bold", int(130*max(s, 0.01)))
            text_layer(im, (540, 360), T["free2"], fr, TEAL, min(1, s), "mm")
        tt = ease((f-378)/18)
        if tt > 0:
            tk = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tk)
            top = 470 + (1-tt)*60
            rounded(td, [150, top, 930, top+300], 26, fill=(244, 248, 252, int(250*tt)))
            for cx in (150, 930):
                td.ellipse([cx-26, top+150-26, cx+26, top+150+26], fill=(0, 0, 0, 0))
            # punch notches: cut alpha
            a = np.array(tk)
            for cx in (150, 930):
                yy, xx = np.ogrid[:H, :W]
                a[((xx-cx)**2 + (yy-(top+150))**2) < 26**2] = 0
            tk = Image.fromarray(a)
            td = ImageDraw.Draw(tk)
            for x in range(190, 900, 22):
                td.line([(x, top+212), (x+10, top+212)], fill=(170, 185, 205, int(255*tt)), width=2)
            im.alpha_composite(tk)
            text_layer(im, (540, top+48), T["res"], F("Medium", 24), (90, 110, 140), tt, "mm")
            fnt, lines = fit_font(lab, "Bold", 700, 52, minsize=30)
            if len(lines) == 1:
                text_layer(im, (540, top+115), lab, fnt, NAVY, tt, "mm")
            else:
                for i, l in enumerate(lines):
                    text_layer(im, (540, top+95+i*fnt.size*1.05), l, fnt, NAVY, tt, "mm")
            text_layer(im, (540, top+255), f"{T['case']} {code}", F("Bold", 30), (20, 150, 140), tt, "mm")
        ce = ease((f-400)/16)
        text_layer(im, (540, 845), T["cta"], fit_font(T["cta"], "Regular", 960, 32)[0], WHITE, ce, "mm")
        text_layer(im, (540, 915), "boundlesscad.design@gmail.com", F("Medium", 30), TEAL, ce, "mm")
        text_layer(im, (540, 960), "boundlesscaddesign-dev.github.io", F("Regular", 26), MUTED, ce, "mm")
    return im.convert("RGB")

def clean_lab(s): return re.sub(r"\s*\(.*?\)", "", s).strip()
def clean_city(s):
    s = re.sub(r"\s*\(.*?\)", "", s or "").strip()
    s = s.split(",")[0].split("/")[0].strip()
    s = re.sub(r"\s+[A-Z]{1,2}\d.*$", "", s)  # UK postcodes
    return s
def case_code(lab):
    w = re.sub(r"[^A-Za-z0-9]", "", clean_lab(lab).split()[0] if clean_lab(lab).split() else "LAB").upper()
    return f"BC-{w[:6]}-001"

def make(lab, city, lang, out):
    lab_c, city_c = clean_lab(lab), clean_city(city)
    T = TXT.get(lang, TXT["en"]); code = case_code(lab)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(NF):
        p.stdin.write(frame(f, lab_c, city_c, T, code).tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    if sys.argv[1] == "--still":
        lab, city, lang = sys.argv[2:5]
        T = TXT[lang]
        for f in map(int, sys.argv[5:]):
            frame(f, clean_lab(lab), clean_city(city), T, case_code(lab)).save(f"still_{f}.png")
    else:
        make(*sys.argv[1:5])
