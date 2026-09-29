import os, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, 'node_modules/@fontsource')
def f64(p): return base64.b64encode(open(os.path.join(FD, p), 'rb').read()).decode()
FONTS = f"""
@font-face{{font-family:Manrope;font-weight:500;src:url(data:font/woff2;base64,{f64('manrope/files/manrope-latin-500-normal.woff2')}) format('woff2')}}
@font-face{{font-family:Manrope;font-weight:700;src:url(data:font/woff2;base64,{f64('manrope/files/manrope-latin-700-normal.woff2')}) format('woff2')}}
@font-face{{font-family:Manrope;font-weight:800;src:url(data:font/woff2;base64,{f64('manrope/files/manrope-latin-800-normal.woff2')}) format('woff2')}}
@font-face{{font-family:'Instrument Serif';font-style:italic;font-weight:400;src:url(data:font/woff2;base64,{f64('instrument-serif/files/instrument-serif-latin-400-italic.woff2')}) format('woff2')}}
"""
NAVY, NAVY2, PANEL, TEAL, TEAL2, MINT, GOLD, TXT, MUTED = '#0b1826', '#0f2033', '#12263a', '#7FD1C7', '#4fb8ab', '#b9f0e8', '#f2c98a', '#e9f1f5', '#93a8b8'
TOOTH = 'M24 22c-3 0-5 3-5 6 0 5 2 7 3 11 1 4 2 7 3.5 7s2.5-3 3.2-6.5c.6-1.8 1.4-2.5 3.3-2.5s2.7.7 3.3 2.5c.7 3.5 1.7 6.5 3.2 6.5S43 43 44 39c1-4 3-6 3-11 0-3-2-6-5-6-2.5 0-4 1.6-9 1.6S26.5 22 24 22z'
def mark(ring=TEAL, tooth='#fff', bg=None, r=None):
    b = f'<circle cx="32" cy="32" r="32" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{b}<circle cx="32" cy="32" r="27" fill="none" stroke="{ring}" stroke-width="4" stroke-linecap="round" stroke-dasharray="118 52" transform="rotate(-20 32 32)"/><path d="{TOOTH}" fill="{tooth}"/></svg>'
def wordmark_html(size, c1, c2):
    return f'<span style="font-family:Manrope;font-weight:800;font-size:{size}px;letter-spacing:-.02em;color:{c1}">Boundless<span style="color:{c2}">CAD</span></span>'
def page(w, h, body, bg='transparent'):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}*{{margin:0;box-sizing:border-box}}html,body{{width:{w}px;height:{h}px;background:{bg};overflow:hidden}}body{{font-family:Manrope;color:{TXT};position:relative}}</style></head><body>{body}</body></html>'
DOTS = f'<div style="position:absolute;inset:0;background-image:radial-gradient({TEAL} 1.2px,transparent 1.6px);background-size:30px 30px;opacity:.12"></div>'
GRAD = f'radial-gradient(ellipse at 75% 30%,#1f4a68 0%,{PANEL} 50%,#0a1520 100%)'
jobs = []  # (name, w, h, html, transparent)
# --- logos
for nm, ring, tooth, bg in [('mark', TEAL, '#fff', None), ('mark-dark-bg', TEAL, '#fff', NAVY), ('mark-light', TEAL2, NAVY, None), ('mark-mono-white', '#fff', '#fff', None), ('mark-mono-navy', NAVY, NAVY, None)]:
    jobs.append((f'logo/{nm}-1024', 1024, 1024, page(1024, 1024, f'<div style="width:1024px;height:1024px">{mark(ring, tooth, bg)}</div>'), bg is None))
def full(c1, c2, ring, tooth, bg):
    return page(1600, 400, f'<div style="display:flex;align-items:center;gap:44px;height:400px;padding:0 80px">{mark(ring,tooth)}{wordmark_html(150,c1,c2)}</div>'.replace('<svg ', '<svg width="240" height="240" '), bg)
jobs.append(('logo/logo-horizontal-on-dark', 1600, 400, full('#fff', TEAL, TEAL, '#fff', NAVY), False))
jobs.append(('logo/logo-horizontal-transparent-white', 1600, 400, full('#fff', TEAL, TEAL, '#fff', 'transparent'), True))
jobs.append(('logo/logo-horizontal-transparent-navy', 1600, 400, full(NAVY, TEAL2, TEAL2, NAVY, 'transparent'), True))
jobs.append(('logo/logo-horizontal-on-light', 1600, 400, full(NAVY, TEAL2, TEAL2, NAVY, '#F5F3EE'), False))
# --- favicons / app icons
for s, nm in [(180, 'apple-touch-icon'), (192, 'icon-192'), (512, 'icon-512'), (32, 'favicon-32'), (16, 'favicon-16')]:
    jobs.append((f'icons/{nm}', s, s, page(s, s, f'<div style="width:{s}px;height:{s}px">{mark(TEAL, "#fff", NAVY)}</div>'), False))
# --- social covers
def cover(w, h, head, sub, pad, show_pills=True, hs=0.15, mw=0.62):
    pills = ''.join(f'<span style="padding:{h*0.03:.0f}px {h*0.06:.0f}px;border-radius:999px;border:1.5px solid rgba(127,209,199,.4);background:rgba(127,209,199,.1);color:{MINT};font-weight:700;font-size:{h*0.052:.0f}px">{t}</span>' for t in ['Crowns & bridges', 'Custom abutments', 'Full-arch implant', 'Surgical guides'])
    return page(w, h, f'''{DOTS}<div style="position:absolute;right:{w*0.04:.0f}px;top:50%;transform:translateY(-50%);width:{h*1.05:.0f}px;height:{h*1.05:.0f}px;border-radius:50%;border:2px dashed rgba(127,209,199,.22)"></div>
<div style="position:absolute;right:{w*0.075:.0f}px;top:50%;transform:translateY(-50%);width:{h*0.7:.0f}px;height:{h*0.7:.0f}px">{mark()}</div>
<div style="position:absolute;left:{pad}px;top:50%;transform:translateY(-50%);max-width:{w*mw:.0f}px">
<div style="font-weight:800;font-size:{h*hs:.0f}px;line-height:1.05;letter-spacing:-.02em;color:#fff">{head}</div>
<div style="font-size:{h*0.075:.0f}px;color:#b6c7d3;margin-top:{h*0.04:.0f}px">{sub}</div>
<div style="display:{'flex' if show_pills else 'none'};gap:{h*0.025:.0f}px;flex-wrap:wrap;margin-top:{h*0.06:.0f}px">{pills}</div></div>''', GRAD)
jobs.append(('social/linkedin-cover-1584x396', 1584, 396, cover(1584, 396, 'Remote exocad design <span style="font-family:\'Instrument Serif\';font-style:italic;font-weight:400;color:#b9f0e8">for dental labs.</span>', 'Scan tonight · mill at 8 am · first case free', 470, hs=0.105, mw=0.5), False))
jobs.append(('social/facebook-cover-1640x624', 1640, 624, cover(1640, 624, 'Remote exocad design <span style="font-family:\'Instrument Serif\';font-style:italic;font-weight:400;color:#b9f0e8">for dental labs.</span>', 'Scan tonight · mill at 8 am · first case free', 120), False))
jobs.append(('social/x-header-1500x500', 1500, 500, cover(1500, 500, 'Remote exocad design <span style="font-family:\'Instrument Serif\';font-style:italic;font-weight:400;color:#b9f0e8">for dental labs.</span>', 'Scan tonight · mill at 8 am · first case free', 90), False))
jobs.append(('social/profile-picture-1080', 1080, 1080, page(1080, 1080, f'<div style="width:1080px;height:1080px">{mark(TEAL, "#fff", NAVY)}</div>'), False))
# --- IG highlight covers (1080x1920, icon centered in safe circle)
ICONS = {
 'services': '<path d="M60 70c-10 0-16 9-16 18 0 15 6 21 9 33 3 12 6 21 10 21s7-9 9-19c2-6 4-8 10-8s8 2 10 8c2 10 5 19 9 19s7-9 10-21c3-12 9-18 9-33 0-9-6-18-15-18-8 0-12 5-27 5S68 70 60 70z" fill="none" stroke="#b9f0e8" stroke-width="7" stroke-linejoin="round"/>',
 '3d': '<g fill="none" stroke="#b9f0e8" stroke-width="7" stroke-linejoin="round"><path d="M100 40 50 68v64l50 28 50-28V68z"/><path d="m50 68 50 28 50-28M100 96v64"/></g>',
 'send': '<g fill="none" stroke="#b9f0e8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M100 140V60"/><path d="m68 90 32-32 32 32"/><path d="M50 130v20h100v-20"/></g>',
 'plans': '<g fill="none" stroke="#b9f0e8" stroke-width="7" stroke-linejoin="round"><rect x="52" y="52" width="96" height="96" rx="16"/><path d="M52 84h96M84 52v96"/></g>',
 'faq': '<g fill="none" stroke="#b9f0e8" stroke-width="7" stroke-linecap="round"><circle cx="100" cy="100" r="52"/><path d="M84 86c0-10 8-17 17-17s17 7 17 16c0 12-17 13-17 25"/></g><circle cx="101" cy="130" r="5" fill="#b9f0e8"/>',
 'review': '<g fill="none" stroke="#b9f0e8" stroke-width="7" stroke-linecap="round"><circle cx="90" cy="90" r="36"/><path d="m116 116 34 34"/><path d="m74 90 11 11 22-22"/></g>',
}
for k, ic in ICONS.items():
    jobs.append((f'instagram/highlight-{k}', 1080, 1920, page(1080, 1920, f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:760px;height:760px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#1f4a68,{PANEL} 70%);border:6px solid rgba(127,209,199,.35);display:grid;place-items:center"><svg width="420" height="420" viewBox="0 0 200 200">{ic}</svg></div>', NAVY), False))
json.dump([(n, w, h, t) for n, w, h, _, t in jobs], open(os.path.join(HERE, 'jobs.json'), 'w'))
os.makedirs(os.path.join(HERE, 'html'), exist_ok=True)
for n, w, h, html, t in jobs:
    p = os.path.join(HERE, 'html', n.replace('/', '__') + '.html'); open(p, 'w').write(html)
# svg sources
os.makedirs(os.path.join(HERE, 'out/logo'), exist_ok=True)
open(os.path.join(HERE, 'out/logo/mark.svg'), 'w').write(mark())
open(os.path.join(HERE, 'out/logo/mark-dark-bg.svg'), 'w').write(mark(bg=NAVY))
open(os.path.join(HERE, 'out/logo/mark-light.svg'), 'w').write(mark(TEAL2, NAVY))
open(os.path.join(HERE, 'out/logo/mark-mono-white.svg'), 'w').write(mark('#fff', '#fff'))
print(len(jobs), 'jobs')
