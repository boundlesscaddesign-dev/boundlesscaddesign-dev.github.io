"""BoundlessCAD QC report — one A4 PDF that ships with every delivered case.
usage: python3 qc_report.py case.json out.pdf
case.json keys: case_code, lab, date, designer_id (internal, not printed), items[{teeth,type,material}],
params (str), checks{margin,contacts,occlusion,thickness,contour,insertion: {ok: bool, note: str}},
images [paths, up to 3], qc_by, lang (en|de|es), notes."""
import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

FD = "/usr/share/fonts/truetype/google-fonts/"
for w in ("Regular", "Medium", "Bold"):
    pdfmetrics.registerFont(TTFont(f"P-{w}", FD + f"Poppins-{w}.ttf"))
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo-white.png")
NAVY, TEAL, INK, MUT, LINE, OKC, BAD = map(HexColor, ("#0B1826", "#20C9BB", "#10243A", "#5B6B7F", "#D9E2EC", "#0E9F8F", "#C0392B"))

L = {
 "en": dict(title="Design QC Report", case="Case", lab="Lab", date="Delivered", items="Restorations", teeth="Teeth (FDI)", type="Type", mat="Material",
            params="Parameters used", checks="6-point quality check", shots="Design views", sign="QC approved by", role="Dentist · BoundlessCAD",
            names=dict(margin="Margin line", contacts="Proximal contacts", occlusion="Occlusion", thickness="Minimum thickness & connectors",
                       contour="Contour / emergence profile", insertion="Insertion path & files"),
            ok="PASS", no="CHECK", notes="Notes", foot="Questions or adjustments? Reply to our email — revisions within 12 h."),
 "de": dict(title="Qualitätsbericht Konstruktion", case="Fall", lab="Labor", date="Geliefert", items="Restaurationen", teeth="Zähne (FDI)", type="Art", mat="Material",
            params="Verwendete Parameter", checks="6-Punkte-Qualitätskontrolle", shots="Ansichten", sign="Freigegeben von", role="Zahnarzt · BoundlessCAD",
            names=dict(margin="Präparationsgrenze", contacts="Approximalkontakte", occlusion="Okklusion", thickness="Mindeststärke & Verbinder",
                       contour="Kontur / Emergenzprofil", insertion="Einschubrichtung & Dateien"),
            ok="OK", no="PRÜFEN", notes="Hinweise", foot="Fragen oder Änderungen? Antworten Sie auf unsere E-Mail — Überarbeitung innerhalb von 12 h."),
 "es": dict(title="Informe de control de calidad", case="Caso", lab="Laboratorio", date="Entregado", items="Restauraciones", teeth="Dientes (FDI)", type="Tipo", mat="Material",
            params="Parámetros usados", checks="Control de calidad de 6 puntos", shots="Vistas del diseño", sign="Aprobado por", role="Odontólogo · BoundlessCAD",
            names=dict(margin="Línea de margen", contacts="Contactos proximales", occlusion="Oclusión", thickness="Espesor mínimo y conectores",
                       contour="Contorno / perfil de emergencia", insertion="Eje de inserción y archivos"),
            ok="OK", no="REVISAR", notes="Notas", foot="¿Dudas o ajustes? Respondan a nuestro correo — revisiones en 12 h."),
}
ORDER = ["margin", "contacts", "occlusion", "thickness", "contour", "insertion"]

def wrap(c, text, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def build(d, out):
    T = L.get(d.get("lang", "en"), L["en"])
    W, H = A4; m = 40
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle(f"{T['title']} {d['case_code']}")
    # header band
    c.setFillColor(NAVY); c.rect(0, H-110, W, 110, stroke=0, fill=1)
    if os.path.exists(LOGO):
        img = ImageReader(LOGO); iw, ih = img.getSize(); h = 30
        c.drawImage(img, m, H-62, width=iw*h/ih, height=h, mask="auto")
    c.setFillColor(white); c.setFont("P-Bold", 20); c.drawRightString(W-m, H-52, T["title"])
    c.setFillColor(TEAL); c.setFont("P-Medium", 11); c.drawRightString(W-m, H-72, d["case_code"])
    c.setFillColor(TEAL); c.rect(0, H-114, W, 4, stroke=0, fill=1)
    y = H-150
    # meta
    c.setFont("P-Medium", 9); c.setFillColor(MUT)
    for i, (k, v) in enumerate([(T["case"], d["case_code"]), (T["lab"], d["lab"]), (T["date"], d["date"])]):
        x = m + i*((W-2*m)/3)
        c.drawString(x, y, k.upper()); c.setFont("P-Bold", 12); c.setFillColor(INK); c.drawString(x, y-16, v)
        c.setFont("P-Medium", 9); c.setFillColor(MUT)
    y -= 46
    # items table
    c.setFont("P-Bold", 11); c.setFillColor(INK); c.drawString(m, y, T["items"]); y -= 18
    cols = [m, m+140, m+300]
    c.setFont("P-Medium", 8.5); c.setFillColor(MUT)
    for x, k in zip(cols, (T["teeth"], T["type"], T["mat"])): c.drawString(x, y, k.upper())
    y -= 6; c.setStrokeColor(LINE); c.line(m, y, W-m, y); y -= 14
    c.setFont("P-Regular", 10); c.setFillColor(INK)
    for it in d["items"]:
        for x, k in zip(cols, ("teeth", "type", "material")): c.drawString(x, y, str(it[k]))
        y -= 16
    y -= 6
    c.setFont("P-Medium", 8.5); c.setFillColor(MUT); c.drawString(m, y, T["params"].upper()); y -= 13
    c.setFont("P-Regular", 9.5); c.setFillColor(INK)
    for ln in wrap(c, d["params"], "P-Regular", 9.5, W-2*m): c.drawString(m, y, ln); y -= 13
    y -= 12
    # checks
    c.setFont("P-Bold", 11); c.drawString(m, y, T["checks"]); y -= 10
    for k in ORDER:
        ck = d["checks"][k]; ok = ck.get("ok", False)
        y -= 26
        c.setFillColor(HexColor("#F4F8FB")); c.roundRect(m, y-6, W-2*m, 24, 6, stroke=0, fill=1)
        c.setFillColor(OKC if ok else BAD); c.roundRect(m+8, y-1, 46, 14, 7, stroke=0, fill=1)
        c.setFillColor(white); c.setFont("P-Bold", 7.5); c.drawCentredString(m+31, y+2.5, T["ok"] if ok else T["no"])
        c.setFillColor(INK); c.setFont("P-Medium", 10); c.drawString(m+66, y+2, T["names"][k])
        c.setFillColor(MUT); c.setFont("P-Regular", 8.5)
        note = ck.get("note", "")
        if note: c.drawRightString(W-m-10, y+2, note[:70])
    y -= 30
    # images
    imgs = [p for p in d.get("images", []) if os.path.exists(p)][:3]
    if imgs:
        c.setFont("P-Bold", 11); c.setFillColor(INK); c.drawString(m, y, T["shots"]); y -= 10
        gw = (W-2*m-20)/3; gh = gw
        for i, p in enumerate(imgs):
            x = m + i*(gw+10)
            c.setFillColor(HexColor("#0E2236")); c.roundRect(x, y-gh, gw, gh, 8, stroke=0, fill=1)
            ir = ImageReader(p); iw, ih = ir.getSize(); s = min(gw/iw, gh/ih)*0.94
            c.drawImage(ir, x+(gw-iw*s)/2, y-gh+(gh-ih*s)/2, iw*s, ih*s, mask="auto")
        y -= gh + 16
    if d.get("notes"):
        c.setFont("P-Medium", 8.5); c.setFillColor(MUT); c.drawString(m, y, T["notes"].upper()); y -= 13
        c.setFont("P-Regular", 9.5); c.setFillColor(INK)
        for ln in wrap(c, d["notes"], "P-Regular", 9.5, W-2*m): c.drawString(m, y, ln); y -= 13
    # sign-off
    c.setStrokeColor(LINE); c.line(m, 92, W-m, 92)
    c.setFont("P-Medium", 8.5); c.setFillColor(MUT); c.drawString(m, 76, T["sign"].upper())
    c.setFont("P-Bold", 12); c.setFillColor(INK); c.drawString(m, 60, d["qc_by"])
    c.setFont("P-Regular", 9); c.setFillColor(MUT); c.drawString(m, 47, T["role"])
    c.setFont("P-Regular", 8.5); c.drawRightString(W-m, 60, "boundlesscad.design@gmail.com")
    c.drawRightString(W-m, 47, "boundlesscaddesign-dev.github.io")
    c.setFillColor(TEAL); c.setFont("P-Medium", 8.5); c.drawCentredString(W/2, 24, T["foot"])
    c.showPage(); c.save()

if __name__ == "__main__":
    build(json.load(open(sys.argv[1])), sys.argv[2])
