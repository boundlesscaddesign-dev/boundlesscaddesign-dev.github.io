"""Build the per-lab video page: v/<id>/index.html (+ video.mp4, poster.jpg, preview.gif)."""
import html, urllib.parse

COPY = {
 "en": dict(title="A video for {lab}", h="We made this for {lab}", p="15 seconds on how we'd work as your overnight exocad design team.",
            b1="Send your first case — free", b2="See your lab's overview", b3="Browse 15 real 3D cases", note="Reply to our email or write to boundlesscad.design@gmail.com"),
 "de": dict(title="Ein Video für {lab}", h="Für {lab} gemacht", p="15 Sekunden darüber, wie wir als Ihr nächtliches exocad-Konstruktionsteam arbeiten würden.",
            b1="Ersten Fall gratis senden", b2="Übersicht für Ihr Labor", b3="15 echte 3D-Fälle ansehen", note="Antworten Sie auf unsere E-Mail oder schreiben Sie an boundlesscad.design@gmail.com"),
 "es": dict(title="Un video para {lab}", h="Hecho para {lab}", p="15 segundos sobre cómo trabajaríamos como su equipo nocturno de diseño en exocad.",
            b1="Envíen su primer caso gratis", b2="Ver la página de su laboratorio", b3="Ver 15 casos 3D reales", note="Respondan a nuestro correo o escriban a boundlesscad.design@gmail.com"),
}

def page(lab, iso2, lang):
    C = COPY.get(lang, COPY["en"])
    L = html.escape(lab)
    q = urllib.parse.quote(lab)
    forlink = f"/for/?lab={q}&c={iso2}&lang={lang}"
    send = "/send/"
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{C['title'].format(lab=L)} — BoundlessCAD</title>
<meta name="robots" content="noindex,nofollow">
<meta property="og:title" content="{C['title'].format(lab=L)}"><meta property="og:image" content="poster.jpg"><meta property="og:video" content="video.mp4">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#0b1826">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0b1826;--ink:#eef4f8;--mut:#9fb3c8;--teal:#7FD1C7;--card:#10243a}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(1200px 700px at 50% 0,#14304d,var(--bg));color:var(--ink);font-family:Manrope,system-ui,sans-serif;min-height:100vh}}
main{{max-width:620px;margin:0 auto;padding:28px 16px 48px;text-align:center}}
.logo{{height:34px;margin:4px auto 22px;display:block}}
h1{{font-size:clamp(24px,6vw,34px);margin:0 0 8px;font-weight:800;letter-spacing:-.01em}}
p{{color:var(--mut);margin:0 0 20px;line-height:1.5}}
video{{width:100%;aspect-ratio:1;border-radius:20px;background:#081320;box-shadow:0 20px 60px rgba(0,0,0,.45),0 0 0 1px rgba(127,209,199,.25);display:block}}
.btns{{display:grid;gap:10px;margin:22px 0 14px}}
a.b{{display:block;padding:15px 18px;border-radius:14px;text-decoration:none;font-weight:700;color:var(--ink);background:var(--card);border:1px solid rgba(127,209,199,.25)}}
a.b.p{{background:var(--teal);color:#06231f;border:0}}
small{{color:var(--mut)}}
</style></head><body><main>
<img class="logo" src="/brand/logo/logo-horizontal-transparent-white.png" alt="BoundlessCAD">
<h1>{C['h'].format(lab=L)}</h1><p>{C['p']}</p>
<video src="video.mp4" poster="poster.jpg" autoplay muted loop playsinline controls></video>
<div class="btns"><a class="b p" href="{send}">{C['b1']}</a><a class="b" href="{forlink}">{C['b2']}</a><a class="b" href="/cases/">{C['b3']}</a></div>
<small>{C['note']}</small>
</main></body></html>
"""
