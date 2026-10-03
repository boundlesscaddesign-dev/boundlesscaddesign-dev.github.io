#!/usr/bin/env python3
"""Build check/es/index.html and check/de/index.html from the English source check/index.html.

Run after every change to check/index.html:  python3 tools/check_i18n.py
UI strings created by JavaScript live in check/i18n.js (all languages).
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'check', 'index.html')
BASE = 'https://boundlesscaddesign-dev.github.io/check/'

# (english, spanish, german) — static text in the page
T = [
 ('<title>Free STL Check for dental scans — BoundlessCAD</title>',
  '<title>STL Check gratis para escaneos dentales — BoundlessCAD</title>',
  '<title>Kostenloser STL Check für Dentalscans — BoundlessCAD</title>'),
 ('content="Free STL check for dental scans and models: finds holes, non-manifold edges, flipped normals, floating debris and wrong units in seconds. Runs in your browser; your file is never uploaded."',
  'content="Comprobación STL gratuita para escaneos y modelos dentales: detecta agujeros, aristas no-manifold, normales invertidas, restos sueltos y unidades incorrectas en segundos. Funciona en su navegador; el archivo nunca se sube."',
  'content="Kostenloser STL-Check für Dentalscans und Modelle: findet Löcher, nicht-mannigfaltige Kanten, gedrehte Normalen, lose Scan-Reste und falsche Einheiten in Sekunden. Läuft im Browser; die Datei wird nie hochgeladen."'),
 ('content="Free STL Check — is your scan ready for design?"',
  'content="STL Check gratis — ¿su escaneo está listo para diseñar?"',
  'content="Kostenloser STL Check — ist Ihr Scan bereit für die Konstruktion?"'),
 ('content="Drop an STL or PLY. Get holes, broken edges, debris and unit problems in seconds. Nothing is uploaded."',
  'content="Suelte un STL o PLY. Agujeros, aristas rotas, restos y problemas de unidades en segundos. No se sube nada."',
  'content="STL oder PLY ablegen. Löcher, defekte Kanten, Scan-Reste und Einheitenfehler in Sekunden. Nichts wird hochgeladen."'),
 ('>Send a case</a>', '>Enviar un caso</a>', '>Fall senden</a>'),
 ('STL CHECK BY BOUNDLESSCAD · FREE · NO SIGN-UP', 'STL CHECK DE BOUNDLESSCAD · GRATIS · SIN REGISTRO', 'STL CHECK VON BOUNDLESSCAD · KOSTENLOS · OHNE ANMELDUNG'),
 ('<h1>Is your scan <span class="serif">ready for design?</span></h1>',
  '<h1>¿Su escaneo está <span class="serif">listo para diseñar?</span></h1>',
  '<h1>Ist Ihr Scan <span class="serif">bereit für die Konstruktion?</span></h1>'),
 ('Drop an STL or PLY. In a few seconds you see holes, broken edges, flipped normals, floating debris and unit problems, marked in 3D.',
  'Suelte un STL o PLY. En pocos segundos verá agujeros, aristas rotas, normales invertidas, restos sueltos y problemas de unidades, marcados en 3D.',
  'Legen Sie eine STL- oder PLY-Datei ab. In wenigen Sekunden sehen Sie Löcher, defekte Kanten, gedrehte Normalen, lose Scan-Reste und Einheitenfehler – markiert in 3D.'),
 ('<b>Drop your scan here, or click to choose</b>', '<b>Suelte aquí su escaneo o haga clic para elegirlo</b>', '<b>Scan hier ablegen oder klicken zum Auswählen</b>'),
 ('STL (binary or ASCII) or PLY · intraoral scans, models, dies, designs',
  'STL (binario o ASCII) o PLY · escaneos intraorales, modelos, muñones, diseños',
  'STL (binär oder ASCII) oder PLY · Intraoralscans, Modelle, Stümpfe, Konstruktionen'),
 ('No scan at hand? <button id="sample" type="button">Try it with a sample arch</button>',
  '¿No tiene un escaneo a mano? <button id="sample" type="button">Pruebe con una arcada de ejemplo</button>',
  'Kein Scan zur Hand? <button id="sample" type="button">Mit einem Beispielkiefer testen</button>'),
 ('<span>Runs in your browser</span><span>Your file is never uploaded</span><span>No account, no email</span>',
  '<span>Funciona en su navegador</span><span>El archivo nunca se sube</span><span>Sin cuenta, sin email</span>',
  '<span>Läuft in Ihrem Browser</span><span>Die Datei wird nie hochgeladen</span><span>Kein Konto, keine E-Mail</span>'),
 ('<span id="busyT">Reading file…</span>', '<span id="busyT">Leyendo el archivo…</span>', '<span id="busyT">Datei wird gelesen…</span>'),
 ('<h2 id="vt">Checking…</h2>', '<h2 id="vt">Comprobando…</h2>', '<h2 id="vt">Wird geprüft…</h2>'),
 ('<h3 id="ctaH">Want us to fix it, or design on it?</h3>', '<h3 id="ctaH">¿Lo reparamos o diseñamos sobre él?</h3>', '<h3 id="ctaH">Sollen wir reparieren oder darauf konstruieren?</h3>'),
 ('We repair holes and debris and design crowns, abutments, bars and dentures in exocad. Your first case is free.',
  'Reparamos agujeros y restos, y diseñamos coronas, pilares, barras y prótesis removibles en exocad. Su primer caso es gratis.',
  'Wir reparieren Löcher und Scan-Reste und konstruieren Kronen, Abutments, Stege und Prothesen in exocad. Ihr erster Fall ist kostenlos.'),
 ('>Email us this report</a>', '>Envíenos este informe</a>', '>Bericht an uns senden</a>'),
 ('>Download report card</button>', '>Descargar la ficha</button>', '>Berichtskarte herunterladen</button>'),
 ('>Copy report</button>', '>Copiar informe</button>', '>Bericht kopieren</button>'),
 ('>Share this tool</button>', '>Compartir la herramienta</button>', '>Tool teilen</button>'),
 ('>Check another file</button>', '>Comprobar otro archivo</button>', '>Andere Datei prüfen</button>'),
 ('<h3>1 · Drop the file</h3><p>Scans from any intraoral or lab scanner, exported as STL or PLY. Large full-arch scans work too.</p>',
  '<h3>1 · Suelte el archivo</h3><p>Escaneos de cualquier escáner intraoral o de laboratorio, exportados como STL o PLY. También arcadas completas grandes.</p>',
  '<h3>1 · Datei ablegen</h3><p>Scans aus jedem Intraoral- oder Laborscanner, als STL oder PLY exportiert. Auch große Ganzkieferscans.</p>'),
 ('<h3>2 · We read the mesh</h3><p>Every edge and triangle is checked in your browser: open edges, edges shared by three or more triangles, flipped triangles, separate pieces, size.</p>',
  '<h3>2 · Leemos la malla</h3><p>Cada arista y triángulo se comprueba en su navegador: aristas abiertas, aristas compartidas por tres o más triángulos, triángulos invertidos, piezas separadas, tamaño.</p>',
  '<h3>2 · Wir lesen das Netz</h3><p>Jede Kante und jedes Dreieck wird in Ihrem Browser geprüft: offene Kanten, Kanten mit drei oder mehr Dreiecken, gedrehte Dreiecke, separate Teile, Größe.</p>'),
 ('<h3>3 · See it in 3D</h3><p>Problems are marked on the model, with a plain-English report you can copy or send to your designer.</p>',
  '<h3>3 · Véalo en 3D</h3><p>Los problemas se marcan en el modelo, con un informe claro que puede copiar o enviar a su diseñador.</p>',
  '<h3>3 · In 3D ansehen</h3><p>Probleme werden am Modell markiert, mit einem verständlichen Bericht zum Kopieren oder Weitersenden.</p>'),
 ('<h2>Questions</h2>', '<h2>Preguntas</h2>', '<h2>Fragen</h2>'),
 ('<summary>Is my file uploaded anywhere?</summary><p>No. The file is read by your own browser and never sent to a server. You can disconnect from the internet after the page has loaded and it still works.</p>',
  '<summary>¿Se sube mi archivo a algún sitio?</summary><p>No. Su propio navegador lee el archivo y nunca se envía a un servidor. Puede desconectarse de internet después de cargar la página y sigue funcionando.</p>',
  '<summary>Wird meine Datei irgendwo hochgeladen?</summary><p>Nein. Ihr eigener Browser liest die Datei, sie wird nie an einen Server gesendet. Nach dem Laden der Seite funktioniert es sogar offline.</p>'),
 ('<summary>My intraoral scan shows an open border. Is that a problem?</summary><p>No. A scan of a jaw is an open surface, so one outer border per piece is normal. The tool counts that border separately and only flags extra holes inside the surface.</p>',
  '<summary>Mi escaneo intraoral muestra un borde abierto. ¿Es un problema?</summary><p>No. El escaneo de una arcada es una superficie abierta, así que un borde exterior por pieza es normal. La herramienta lo cuenta aparte y solo marca los agujeros adicionales dentro de la superficie.</p>',
  '<summary>Mein Intraoralscan hat einen offenen Rand. Ist das ein Problem?</summary><p>Nein. Ein Kieferscan ist eine offene Fläche, ein Außenrand pro Teil ist normal. Das Tool zählt diesen Rand separat und markiert nur zusätzliche Löcher in der Oberfläche.</p>'),
 ('<summary>What does "non-manifold" mean?</summary><p>An edge shared by three or more triangles. Many CAD and slicing programs cannot handle it, and it often comes from merged or badly repaired scans.</p>',
  '<summary>¿Qué significa «no-manifold»?</summary><p>Una arista compartida por tres o más triángulos. Muchos programas CAD y de laminado no pueden procesarla; suele venir de escaneos fusionados o mal reparados.</p>',
  '<summary>Was bedeutet „nicht-mannigfaltig“?</summary><p>Eine Kante, die von drei oder mehr Dreiecken geteilt wird. Viele CAD- und Slicer-Programme können damit nicht umgehen; sie entsteht oft durch zusammengeführte oder schlecht reparierte Scans.</p>'),
 ('<summary>Does a high score mean the scan is clinically good?</summary><p>No. The tool checks the mesh, not the clinical content. A clean mesh can still have an unclear margin or a missing contact. For that, a designer has to look at it.</p>',
  '<summary>¿Una puntuación alta significa que el escaneo es clínicamente bueno?</summary><p>No. La herramienta comprueba la malla, no el contenido clínico. Una malla limpia puede tener un margen poco claro o un contacto ausente. Para eso tiene que verlo un diseñador.</p>',
  '<summary>Bedeutet eine hohe Wertung, dass der Scan klinisch gut ist?</summary><p>Nein. Das Tool prüft das Netz, nicht den klinischen Inhalt. Auch ein sauberes Netz kann eine unklare Präparationsgrenze oder einen fehlenden Kontakt haben. Das muss ein Konstrukteur beurteilen.</p>'),
 ('<summary>Can you fix my file?</summary><p>Yes. Hole repair, debris removal, merging and model preparation are part of our <a href="../services/" style="color:var(--teal)">design services</a>, and the first case is free.</p>',
  '<summary>¿Pueden reparar mi archivo?</summary><p>Sí. Reparación de agujeros, eliminación de restos, fusión y preparación de modelos forman parte de nuestros <a href="../services/" style="color:var(--teal)">servicios de diseño</a>, y el primer caso es gratis.</p>',
  '<summary>Können Sie meine Datei reparieren?</summary><p>Ja. Lochreparatur, Entfernen von Scan-Resten, Zusammenführen und Modellvorbereitung gehören zu unseren <a href="../services/" style="color:var(--teal)">Konstruktionsleistungen</a>, und der erste Fall ist kostenlos.</p>'),
 ('© 2026 BoundlessCAD · remote exocad design for dental labs · boundlesscad.design@gmail.com',
  '© 2026 BoundlessCAD · diseño remoto en exocad para laboratorios dentales · boundlesscad.design@gmail.com',
  '© 2026 BoundlessCAD · Remote-exocad-Konstruktion für Dentallabore · boundlesscad.design@gmail.com'),
]

def build(lang, col):
    s = open(SRC, encoding='utf-8').read()
    for row in T:
        if row[0] not in s:
            sys.exit('missing source string: ' + row[0][:70])
        s = s.replace(row[0], row[col])
    s = s.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    s = s.replace(f'<link rel="canonical" href="{BASE}">', f'<link rel="canonical" href="{BASE}{lang}/">', 1)
    # one directory deeper: fix relative paths
    s = s.replace('"../', '"../../').replace("'../", "'../../")
    s = s.replace('<script src="i18n.js">', '<script src="../i18n.js">')
    s = s.replace("const SAMPLE='sample-arch.stl'", "const SAMPLE='../sample-arch.stl'")
    os.makedirs(os.path.join(ROOT, 'check', lang), exist_ok=True)
    open(os.path.join(ROOT, 'check', lang, 'index.html'), 'w', encoding='utf-8').write(s)
    print('built check/%s/index.html' % lang)

build('es', 1)
build('de', 2)
