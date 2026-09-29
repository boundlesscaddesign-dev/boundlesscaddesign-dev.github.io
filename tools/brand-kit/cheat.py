"""Build the exocad parameter cheat sheet: a web page (/cheatsheet/index.html) and a print HTML for PDF."""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
d = json.load(open(os.path.join(SP, 'cheatsheet.json')))
E = html.escape
def short_src(u):
    from urllib.parse import urlparse
    return urlparse(u).netloc.replace('www.', '')
rows = []
for m in d['materials']:
    rows.append(f"""<tr><td><b>{E(m['material'])}</b><small>{E(m['manufacturer'])} · {E(m['type'])}</small></td>
<td>{E(m['crown_min_occlusal_mm']) or '—'}</td><td>{E(m['crown_min_axial_mm']) or '—'}</td><td>{E(m['connector_mm2']) or '—'}</td>
<td class="ind">{E(m['indications'])}</td><td class="src"><a href="{E(m['source_url'])}" target="_blank" rel="noopener">{E(m['source_title'])}</a></td></tr>""")
notes = ''.join(f'<li>{E(n["text"])} <a href="{E(n["source_url"])}" target="_blank" rel="noopener">[source]</a></li>' for n in d['general_notes'])
LOGO = '<svg width="30" height="30" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="27" fill="none" stroke="#7FD1C7" stroke-width="4" stroke-linecap="round" stroke-dasharray="118 52"/><path d="M24 22c-3 0-5 3-5 6 0 5 2 7 3 11 1 4 2 7 3.5 7s2.5-3 3.2-6.5c.6-1.8 1.4-2.5 3.3-2.5s2.7.7 3.3 2.5c.7 3.5 1.7 6.5 3.2 6.5S43 43 44 39c1-4 3-6 3-11 0-3-2-6-5-6-2.5 0-4 1.6-9 1.6S26.5 22 24 22z" fill="#fff"/></svg>'
TABLE = f"""<div class="tw"><table>
<thead><tr><th>Material</th><th>Min. occlusal / incisal (mm)</th><th>Min. axial / circular (mm)</th><th>Connector (mm²)</th><th>Indications & limits</th><th>Source</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""
WEB = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>exocad design cheat sheet: minimum thickness & connector sizes by material — BoundlessCAD</title>
<meta name="description" content="Minimum wall thickness, connector cross-sections and indication limits for zirconia, lithium disilicate, ZLS, hybrid ceramic, PMMA and CoCr — taken from manufacturer instructions for use, with sources. Free PDF.">
<link rel="canonical" href="https://boundlesscaddesign-dev.github.io/cheatsheet/">
<meta property="og:title" content="exocad design cheat sheet — min. thickness & connectors by material">
<meta property="og:description" content="Manufacturer values for 11 materials in one table, with sources. Free PDF.">
<meta property="og:image" content="https://boundlesscaddesign-dev.github.io/og.png">
<meta name="theme-color" content="#0b1826">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"TechArticle","headline":"exocad design cheat sheet: minimum thickness and connector sizes by material","author":{"@type":"Organization","name":"BoundlessCAD"},"datePublished":"2026-09-29","inLanguage":"en","about":["dental CAD design","minimum wall thickness","connector cross-section","zirconia","lithium disilicate"]})}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../cases/shared.css">
<style>
header{{position:sticky;top:0;z-index:20;background:rgba(11,24,38,.85);backdrop-filter:blur(14px) saturate(1.3);border-bottom:1px solid var(--line)}}
.bar{{max-width:1240px;margin:0 auto;padding:0 22px;height:66px;display:flex;align-items:center;justify-content:space-between;gap:12px}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 22px}}
.hero{{padding:54px 0 16px}}
h1{{font-size:clamp(30px,4.4vw,50px);line-height:1.06;letter-spacing:-1.3px;margin:12px 0 12px;max-width:900px}}
.lead{{color:var(--muted);font-size:16.5px;max-width:720px}}
.ctas{{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0 8px}}
.warn{{margin:18px 0 22px;padding:14px 16px;border-radius:14px;background:rgba(242,201,138,.08);border:1px solid rgba(242,201,138,.3);color:#f0dcb8;font-size:14px;max-width:900px}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:16px;background:var(--panel)}}
table{{width:100%;border-collapse:collapse;font-size:14px;min-width:1000px}}
th,td{{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{color:var(--mint);font-size:11.5px;letter-spacing:1px;text-transform:uppercase;position:sticky;top:0;background:#132b41}}
td b{{color:#fff;display:block}}td small{{color:var(--muted);font-size:12px}}
td.ind{{color:#c9d6df;font-size:13px;max-width:320px}}td.src{{font-size:12px;max-width:220px}}td.src a{{color:var(--teal)}}
tr:last-child td{{border-bottom:0}}
h2{{font-size:24px;letter-spacing:-.5px;margin:34px 0 12px}}
ul.n{{margin:0 0 20px 20px;display:grid;gap:8px;color:#c9d6df;font-size:15px;max-width:900px}}ul.n a{{color:var(--teal)}}
.cta{{margin:34px 0 70px;padding:28px;border-radius:22px;background:linear-gradient(135deg,#12324a,#0f2033);border:1px solid rgba(127,209,199,.22);display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between}}
.cta h2{{margin:0}}.cta p{{color:#b6c7d3;margin-top:4px}}
footer{{border-top:1px solid var(--line);padding:24px 0;color:var(--muted);font-size:13px}}
</style></head><body>
<header><div class="bar"><a class="logo" href="../" aria-label="BoundlessCAD home">{LOGO}<span>Boundless<b>CAD</b></span></a><a class="btn" href="../send/">Free first case →</a></div></header>
<section class="hero"><div class="wrap">
<div class="eyebrow">Free cheat sheet</div>
<h1>Minimum thickness & connectors, <span class="serif">by material.</span></h1>
<p class="lead">The numbers you check before every design, collected from the manufacturers' own instructions for use — 11 materials in one table, each with its source. Print it, pin it next to your exocad screen.</p>
<div class="ctas"><a class="btn" href="boundlesscad-exocad-cheatsheet.pdf" download>Download the PDF →</a><a class="btn ghost" href="../review/">Get a free design review</a></div>
<div class="warn">Values are copied from the manufacturer documents linked in each row (compiled 29 Sep 2026). Materials and IFUs change between generations and lots — always confirm against the instructions supplied with the material you use.</div>
</div></section>
<main class="wrap">{TABLE}
<h2>Good to know</h2><ul class="n">{notes}</ul>
<div class="cta"><div><h2>Short on design capacity this week?</h2><p>We design crowns, bridges, abutments and full-arch cases in exocad — overnight option, first case free.</p></div><a class="btn" href="../send/">Send a case →</a></div>
</main>
<footer><div class="wrap">© 2026 BoundlessCAD · boundlesscad.design@gmail.com · Product names are trademarks of their respective owners; BoundlessCAD is not affiliated with the manufacturers listed.</div></footer>
</body></html>"""
os.makedirs(os.path.join(HERE, 'site_cheatsheet'), exist_ok=True)
open(os.path.join(HERE, 'site_cheatsheet', 'index.html'), 'w').write(WEB)
# print version (A4 landscape) with embedded fonts
exec(open(os.path.join(HERE, 'gen.py')).read().split('NAVY, NAVY2')[0])  # loads FONTS
TOOTH = 'M24 22c-3 0-5 3-5 6 0 5 2 7 3 11 1 4 2 7 3.5 7s2.5-3 3.2-6.5c.6-1.8 1.4-2.5 3.3-2.5s2.7.7 3.3 2.5c.7 3.5 1.7 6.5 3.2 6.5S43 43 44 39c1-4 3-6 3-11 0-3-2-6-5-6-2.5 0-4 1.6-9 1.6S26.5 22 24 22z'
PR_ROWS = []
for m in d['materials']:
    PR_ROWS.append(f"<tr><td><b>{E(m['material'])}</b><small>{E(m['manufacturer'])} · {E(m['type'])}</small></td><td>{E(m['crown_min_occlusal_mm']) or '—'}</td><td>{E(m['crown_min_axial_mm']) or '—'}</td><td>{E(m['connector_mm2']) or '—'}</td><td class='ind'>{E(m['indications'])}</td><td class='src'>{E(short_src(m['source_url']))}</td></tr>")
PRINT = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
@page{{size:A4 landscape;margin:0}}*{{margin:0;box-sizing:border-box}}
body{{font-family:Manrope;color:#0b1826;width:297mm;min-height:210mm;background:#fff}}
.top{{background:#0b1826;color:#fff;padding:9mm 12mm 7mm;display:flex;justify-content:space-between;align-items:flex-end}}
.brand{{display:flex;align-items:center;gap:10px;font-weight:800;font-size:17px}}.brand b{{color:#7FD1C7}}
h1{{font-weight:800;font-size:25px;letter-spacing:-.4px;margin-top:6mm}}h1 i{{font-family:'Instrument Serif';font-weight:400;color:#b9f0e8;font-size:28px}}
.top p{{color:#b6c7d3;font-size:10.5px;margin-top:2mm;max-width:170mm}}
.badge{{background:#7FD1C7;color:#06241f;font-weight:800;font-size:10px;padding:5px 10px;border-radius:999px;white-space:nowrap}}
.body{{padding:5mm 12mm 0}}
table{{width:100%;border-collapse:collapse;font-size:8.6px}}th,td{{text-align:left;padding:4px 5px;border-bottom:.6px solid #d6dde3;vertical-align:top}}
th{{background:#eaf6f4;color:#0f3b44;font-size:7.6px;letter-spacing:.6px;text-transform:uppercase}}td b{{display:block;font-size:9.2px}}td small{{color:#5b6f7e;font-size:7.4px}}
td.ind{{width:78mm;color:#23384a}}td.src{{color:#5b6f7e;font-size:7.4px;width:26mm}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 8mm;margin-top:4mm;font-size:8px;color:#23384a}}.notes div::before{{content:"▸ ";color:#4fb8ab}}
.foot{{position:absolute;left:0;right:0;bottom:0;padding:4mm 12mm;display:flex;justify-content:space-between;align-items:center;font-size:8.6px;color:#5b6f7e;border-top:2px solid #7FD1C7}}
.foot b{{color:#0b1826}}
</style></head><body style="position:relative;height:210mm">
<div class="top"><div><div class="brand"><svg width="24" height="24" viewBox="0 0 64 64"><circle cx="32" cy="32" r="27" fill="none" stroke="#7FD1C7" stroke-width="5" stroke-linecap="round" stroke-dasharray="118 52"/><path d="{TOOTH}" fill="#fff"/></svg>Boundless<b>CAD</b></div>
<h1>exocad design cheat sheet · <i>min. thickness & connectors by material</i></h1>
<p>Values copied from each manufacturer's instructions for use (compiled 29 Sep 2026). Always confirm with the IFU supplied with your material lot — values differ between material generations.</p></div><span class="badge">FREE · keep next to your screen</span></div>
<div class="body"><table><thead><tr><th>Material</th><th>Min. occlusal / incisal (mm)</th><th>Min. axial / circular (mm)</th><th>Connector (mm²)</th><th>Indications & limits</th><th>Source</th></tr></thead><tbody>{''.join(PR_ROWS)}</tbody></table>
<div class="notes">{''.join(f'<div>{E(n["text"])}</div>' for n in d['general_notes'])}</div></div>
<div class="foot"><span><b>Short on design capacity?</b> BoundlessCAD designs crowns, bridges, abutments and full-arch cases in exocad — overnight option · first case free.</span><span><b>boundlesscad.design@gmail.com</b> · boundlesscaddesign-dev.github.io/cheatsheet</span></div>
</body></html>"""
open(os.path.join(HERE, 'cheatsheet_print.html'), 'w').write(PRINT)
print('ok', len(d['materials']))
