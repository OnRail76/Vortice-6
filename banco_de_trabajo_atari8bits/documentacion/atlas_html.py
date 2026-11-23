#!/usr/bin/env python3
"""VÓRTICE 6 · Atlas del proyecto (memoria + instrucciones ilustradas) → build/atlas/atlas.html"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from atlas_title import atari
A = os.path.join(ROOT, 'build', 'atlas')
T = os.path.join(A, 'tit'); os.makedirs(T, exist_ok=True)
_n = [0]
def tit(text, grad='fuego', scale=4, cls='tit', maxw=150):
    _n[0] += 1
    f = 'tit/t%02d.png' % _n[0]
    atari(text, os.path.join(A, f), scale=scale, grad=grad)
    h = 9.5 if cls == 'tit' else 5.6
    h = min(h, maxw * 9.0 / (len(text) * 8 + 1))
    return '<img class="%s" src="%s" alt="%s" style="height:%.2fmm">' % (cls, f, text, h)
F = 'file:///usr/share/fonts/opentype/inter/'
CSS = """
@font-face{font-family:I;src:url('%(F)sInter-Regular.otf')}
@font-face{font-family:I;font-weight:500;src:url('%(F)sInter-Medium.otf')}
@font-face{font-family:I;font-weight:600;src:url('%(F)sInter-SemiBold.otf')}
@font-face{font-family:I;font-weight:700;src:url('%(F)sInter-Bold.otf')}
@font-face{font-family:I;font-style:italic;src:url('%(F)sInter-Italic.otf')}
@font-face{font-family:D;font-weight:800;src:url('%(F)sInterDisplay-ExtraBold.otf')}
@font-face{font-family:D;font-weight:900;src:url('%(F)sInterDisplay-Black.otf')}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#06060d}
body{font-family:I;color:#d9dbe8;font-size:9.6pt;line-height:1.45}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;
  background:radial-gradient(ellipse at 80%% -10%%,#1b1240 0,#0a0a18 45%%,#06060d 100%%);padding:16mm 15mm 18mm}
.page.full{padding:0;background:#000}
.page.full img.bg{width:100%%;height:100%%;object-fit:cover;display:block}
.foot{position:absolute;left:15mm;right:15mm;bottom:8mm;display:flex;justify-content:space-between;
  font-size:7pt;letter-spacing:.14em;color:#6c6f8f;text-transform:uppercase;border-top:1px solid #23243d;padding-top:2.2mm}
.foot b{color:#ff7a2a;font-weight:600}
img.tit{image-rendering:pixelated;height:9.5mm;display:block}
img.tit.s{height:5.6mm}
.kick{font-size:7.5pt;letter-spacing:.32em;text-transform:uppercase;color:#4fd6ff;font-weight:600;margin-bottom:2.5mm}
h2{font-family:D;font-weight:800;font-size:15pt;color:#fff;letter-spacing:.01em;margin:5mm 0 2mm}
h3{font-family:D;font-weight:800;font-size:11pt;color:#ffc23d;letter-spacing:.04em;text-transform:uppercase;margin:4mm 0 1.6mm}
p{margin:0 0 2.2mm}
.lead{font-size:11pt;line-height:1.55;color:#eceef7}
.dim{color:#8e91b0}
.acc{color:#ff7a2a}
.cy{color:#4fd6ff}
.rule{height:1.2mm;background:linear-gradient(90deg,#ff3d1a,#ff9a2a 35%%,#ffd23d 50%%,transparent);margin:3mm 0 5mm;border-radius:1mm;width:70mm}
.shot{image-rendering:pixelated;width:100%%;display:block;object-fit:contain;background:#000;border:1px solid #2b2d4a;border-radius:1.2mm}
.cap{font-size:7.4pt;color:#8e91b0;margin:1.2mm 0 3mm;line-height:1.35}
.cap b{color:#d9dbe8}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}
.card{background:linear-gradient(180deg,rgba(40,42,80,.45),rgba(18,18,36,.55));border:1px solid #26284a;border-radius:2mm;padding:3.4mm 3.8mm}
.card h4{font-family:D;font-weight:800;font-size:10pt;color:#fff;letter-spacing:.03em;text-transform:uppercase;margin-bottom:1mm}
.card .tag{font-size:7pt;letter-spacing:.2em;color:#ff7a2a;text-transform:uppercase;font-weight:600}
.en{display:grid;grid-template-columns:24mm 1fr;gap:3.5mm;align-items:center}
.spr{height:22mm;display:flex;align-items:center;justify-content:center;background:#05050b;border:1px solid #23243d;border-radius:1.5mm}
.spr img{image-rendering:pixelated;max-width:20mm;max-height:19mm}
table{width:100%%;border-collapse:collapse;font-size:8.4pt}
th{font-family:D;font-weight:800;text-align:left;color:#ffc23d;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid #3a3c62;padding:1.6mm 2mm}
td{border-bottom:1px solid #1d1f38;padding:1.5mm 2mm;vertical-align:top}
td:first-child{color:#fff;font-weight:600}
ul{margin:0 0 2.4mm 4.5mm}
li{margin-bottom:1.1mm}
li::marker{color:#ff7a2a}
.hdr{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:1mm}
.num{font-family:D;font-weight:900;font-size:46pt;line-height:.8;color:transparent;-webkit-text-stroke:1.2px #ff7a2a;opacity:.9}
.phase-band{height:2mm;border-radius:1mm;margin:2.5mm 0 4mm}
.tip{border-left:1.2mm solid #4fd6ff;background:rgba(79,214,255,.07);padding:2.4mm 3.4mm;border-radius:0 1.5mm 1.5mm 0;font-size:8.8pt;margin-top:3mm}
.tip b{color:#4fd6ff}
.quote{font-size:12.2pt;line-height:1.62;color:#eef0fa}
.quote p{margin-bottom:3.6mm}
.mono{font-family:'DejaVu Sans Mono',monospace;font-size:8pt;color:#c9cbe0}
.stat{font-family:D;font-weight:900;font-size:21pt;color:#fff;line-height:1}
.stat small{display:block;font-family:I;font-weight:500;font-size:7pt;letter-spacing:.16em;color:#8e91b0;text-transform:uppercase;margin-top:1.4mm}
.toc{font-size:10.5pt}
.toc div{display:flex;justify-content:space-between;border-bottom:1px dotted #2d2f50;padding:1.7mm 0}
.toc span:last-child{color:#ff7a2a;font-family:D;font-weight:800}
""" % {'F': F}

pages = []
pn = [0]
def page(body, cls='', foot=True, sec=''):
    pn[0] += 1
    f = ('<div class="foot"><span><b>VÓRTICE 6</b> · CORAZÓN DEL VACÍO · ATLAS DEL PROYECTO</span><span>%s · %d</span></div>'
         % (sec, pn[0])) if foot else ''
    pages.append('<section class="page %s">%s%s</section>' % (cls, body, f))
def img(src, cap=None, cls='shot'):
    s = '<img class="%s" src="img/%s">' % (cls, src)
    return s + ('<div class="cap">%s</div>' % cap if cap else '')
def enemy(spr, name, tag, text):
    return ('<div class="card en"><div class="spr"><img src="spr_%s.png"></div><div><div class="tag">%s</div><h4>%s</h4>'
            '<div>%s</div></div></div>' % (spr, tag, name, text))

# ===================================================================== 1 · portada
page('<img class="bg" src="img/cover_caja.jpg">', 'full', foot=False)

# ===================================================================== 2 · ficha e índice
page(f'''
{tit('VÓRTICE 6', 'fuego', 6)}
<div style="height:3mm"></div>{tit('CORAZÓN DEL VACÍO', 'acero', 4, 'tit s')}
<div class="rule"></div>
<p class="lead">Un <b>euroshooter</b> de scroll horizontal para Atari de 8 bits: cinco fases, cinco guardianes, una piloto y un único caza estelar
contra el regreso de Leviatán V. Rápido, duro y justo, en la tradición de los matamarcianos que se hacían en Alemania y el Reino Unido.</p>
<div class="g3" style="margin:6mm 0 7mm">
 <div class="card"><div class="stat">5<small>fases</small></div></div>
 <div class="card"><div class="stat">5<small>jefes</small></div></div>
 <div class="card"><div class="stat">3<small>dificultades</small></div></div>
</div>
<div class="g2">
<div>
<div class="kick">Este Atlas</div>
<div class="toc">
<div><span>La historia</span><span>3</span></div>
<div><span>Antes de jugar · carga y formatos</span><span>4</span></div>
<div><span>Controles, pantalla y dificultad</span><span>5</span></div>
<div><span>La Vórtice 6, armas y cápsulas</span><span>6</span></div>
<div><span>Unidad Cero · Compuzoide del Vacío</span><span>7</span></div>
<div><span>Fases 1 a 5 y sus jefes</span><span>8–17</span></div>
<div><span>Prólogo y epílogo</span><span>18</span></div>
<div><span>Secretos y consejos</span><span>19</span></div>
<div><span>Memoria del proyecto</span><span>20–23</span></div>
<div><span>Inspiración</span><span>24</span></div>
<div><span>Créditos</span><span>25</span></div>
</div></div>
<div>
<div class="kick">Ficha</div>
<table>
<tr><td>Título</td><td>VÓRTICE 6 · Corazón del Vacío</td></tr>
<tr><td>Género</td><td>Shoot ’em up horizontal (euroshooter)</td></tr>
<tr><td>Sistema</td><td>Atari XL/XE · 64 KB · NTSC (también funciona en PAL)</td></tr>
<tr><td>Formatos</td><td>Disco ATR · Cartucho CAR (AtariMax 8 Mbit) · XEX por fase</td></tr>
<tr><td>Jugadores</td><td>1 · joystick</td></tr>
<tr><td>Año</td><td>2026</td></tr>
<tr><td>Dirección y diseño</td><td>Tony C. Ware</td></tr>
<tr><td>Gráficos, fases y música</td><td>Tony C. Ware</td></tr>
<tr><td>Programa y asistencia</td><td>GPT y Claude</td></tr>
</table>
</div></div>
<div class="kick" style="margin-top:7mm">Las cinco fases</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2.5mm">
{''.join("<div>%s</div>" % img('f%d_j1.png' % k, ['El Desguace Espacial','Los Océanos Astrales','El Fuego Infernal de Hades','El Sarcófago de Saturno','La Nave Viviente'][k-1]) for k in range(1,6))}
</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2.5mm">
{''.join("<div>%s</div>" % img('f%d_b2.png' % k, ['FERRUM-9','THALASSA','El Tríptico de Hades','SATURNUS','El Corazón Nulo'][k-1]) for k in range(1,6))}
</div>
''', sec='Ficha')

# ===================================================================== 3 · historia
page(f'''
<div class="kick">Prólogo</div>
{tit('LA HISTORIA')}
<div class="rule"></div>
<div style="display:grid;grid-template-columns:1.12fr .88fr;gap:7mm">
<div class="quote">
<p>Tras la caída del <b class="acc">Corazón de Acero</b>, Leviatán V, a manos del misterioso piloto de la Vórtice 5, vivimos dos mil años de paz.</p>
<p>Hasta ahora. El Emperador <b>Xor VII</b>, de la Federación Europea Galáctica, reinaba en paz… hasta que misteriosos seres provenientes de Saturno lo asesinaron.</p>
<p>El <b class="acc">Sarcófago de Sacrificios de Saturno</b> vuelve a palpitar con rituales prohibidos. El <b>Oficiante Vacío</b>, nigromante cósmico,
está decidido a resucitar al Ordenador Loco que quiso destruir la galaxia… <b class="acc">Leviatán V</b>.</p>
<p>Por esa razón, la Federación envía a la descendiente directa del misterioso piloto que nos salvó una vez, la <b class="cy">Comandante Elara Voss</b>,
a bordo del nuevo caza estelar <b>Vórtice 6</b>.</p>
<p style="font-family:D;font-weight:800;font-size:14pt;color:#fff;margin-top:6mm">Su misión: destruir al Corazón del Vacío.</p>
</div>
<div>{img('cover_elara.jpg', '<b>Comandante Elara Voss.</b> Carátula oficial.', 'shot')}</div>
</div>
<div class="g2" style="margin-top:4mm">
<div>{img('historia1.png', 'La historia aparece en el título si nadie toca el mando durante 13 segundos.')}</div>
<div>{img('historia2.png', 'Segunda página. FIRE vuelve al título.')}</div>
</div>
''', sec='Historia')

# ===================================================================== 4 · antes de jugar
page(f'''
<div class="kick">Instrucciones</div>
{tit('ANTES DE JUGAR')}
<div class="rule"></div>
<p class="lead">Vórtice 6 se publica en tres formatos. El <b>disco</b> y el <b>cartucho</b> contienen el juego completo: la intro, las cinco fases
encadenadas y el final. Los <b>XEX</b> cargan cada parte por separado.</p>
<div class="g3" style="margin:5mm 0">
<div class="card"><div class="tag">Juego completo</div><h4>Disco · vortice6.atr</h4>
<p>Doble densidad (180 KB), arranca solo, sin DOS. Usa 668 de sus 717 sectores. Cada carga tarda unos segundos.</p>
<p class="dim">Disquetera de doble densidad (XF551, 1050 ampliada) o SIO2SD, SIO2PC, FujiNet o emulador.</p></div>
<div class="card"><div class="tag">Juego completo</div><h4>Cartucho · vortice6.car</h4>
<p>AtariMax 8 Mbit (1 MB), tipo 42 del formato CAR. Cargas instantáneas: el cargador copia cada parte de los bancos a la memoria y desconecta el cartucho.</p>
<p class="dim">Cartucho flash AtariMax de 8 Mbit (o compatible) o emulador.</p></div>
<div class="card"><div class="tag">Por partes</div><h4>Ficheros XEX</h4>
<p><span class="mono">vortice6_intro</span>, <span class="mono">vortice6_fase1…5</span> y <span class="mono">vortice6_final</span>. Cada fase empieza en su propio título y se juega suelta.</p>
<p class="dim">Cualquier DOS, cargador de XEX o emulador.</p></div>
</div>
<h3>Cómo arrancarlo</h3>
<ul>
<li><b>Disco:</b> enciende el Atari con el disco en la unidad 1.</li>
<li><b>Cartucho:</b> enciende con el cartucho puesto. Si usas emulador, elige el tipo <b>AtariMax 8 Mbit</b>.</li>
<li><b>XEX:</b> cárgalo desde tu DOS o tu cargador habitual.</li>
</ul>
<h3>Requisitos</h3>
<table>
<tr><th>Máquina</th><th>Vídeo</th><th>Mando</th></tr>
<tr><td>Atari XL/XE con 64 KB</td><td>Diseñado a 60 Hz (NTSC). En PAL funciona, algo más lento y con tonos un poco distintos.</td><td>Joystick en el puerto 1</td></tr>
</table>
<h3>Al encenderlo</h3>
<div class="g2">
<div>{img('intro_frase.png', 'La intro: tres frases que se encienden sobre negro.')}</div>
<div>{img('intro_nave.png', 'La Vórtice 6, redibujada de la carátula, con la música de la intro. FIRE la salta.')}</div>
</div>
<p class="dim" style="font-size:8pt">Probado en el emulador atari800: una partida completa encadenada en disco y en cartucho, de la intro al título.</p>
''', sec='Instrucciones')

# ===================================================================== 5 · controles, pantalla, dificultad
page(f'''
<div class="kick">Instrucciones</div>
{tit('CONTROLES Y PANTALLA')}
<div class="rule"></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm">
<div>
{img('titulo.png', '<b>Título.</b> Mueve el mando a izquierda o derecha para elegir la dificultad; FIRE empieza.')}
<h3>Controles</h3>
<table>
<tr><td>Joystick</td><td>Mueve la Vórtice 6 en las ocho direcciones.</td></tr>
<tr><td>FIRE</td><td>Dispara. <b>Mantenlo pulsado</b>: disparo automático.</td></tr>
<tr><td>◂ ▸ en el título</td><td>FÁCIL · NORMAL · HARDCORE</td></tr>
<tr><td>FIRE en rótulos</td><td>Empezar o saltar</td></tr>
</table>
</div>
<div>
{img('f1_j1.png', '<b>En juego.</b> Arriba: puntos, récord y naves (V6 ×3). Abajo: la fase, el nivel de disparo (▸ ▸▸ ▸▸▸) y el escudo (■ si lo llevas).')}
<h3>Reglas</h3>
<ul>
<li>Un golpe de bala, enemigo o decorado destruye la nave, salvo que lleves escudo.</li>
<li>Al volver, la nave parpadea y es invulnerable 3 segundos.</li>
<li>Se gana una fase destruyendo a su jefe. Después, la siguiente se carga sola y la partida continúa.</li>
<li>El récord se guarda mientras el Atari siga encendido.</li>
</ul>
</div>
</div>
<h3>Dificultad</h3>
<table>
<tr><th></th><th>Fácil</th><th>Normal</th><th>Hardcore</th></tr>
<tr><td>Naves</td><td>5</td><td>3</td><td>3</td></tr>
<tr><td>Balas enemigas</td><td>más lentas y nacen más lejos</td><td>la curva de cada fase</td><td>más rápidas y algo más cerca</td></tr>
<tr><td>Vida de los enemigos</td><td>−1 (mínimo 1)</td><td>normal</td><td>+1</td></tr>
<tr><td>Oleadas</td><td>25 % más separadas</td><td>normales</td><td>más juntas</td></tr>
<tr><td>Ataques de los jefes</td><td>avisan antes y cierran más despacio</td><td>la curva de cada fase</td><td>avisan menos y cierran antes</td></tr>
<tr><td>Vida de los jefes</td><td>−25 %</td><td>normal</td><td>+25 %</td></tr>
<tr><td>Al morir</td><td>conservas el láser</td><td>bajas un nivel</td><td>pierdes láser y escudo</td></tr>
<tr><td>Cápsulas</td><td>más frecuentes</td><td>normales</td><td>normales</td></tr>
</table>
<p class="dim" style="margin-top:2mm;font-size:8pt">La dificultad sube fase a fase en las tres: balas más rápidas, enemigos más duros, oleadas más apretadas y jefes que avisan menos.</p>
''', sec='Instrucciones')

# ===================================================================== 6 · nave, armas, cápsulas
page(f'''
<div class="kick">Instrucciones</div>
{tit('LA VÓRTICE 6')}
<div class="rule"></div>
<div style="display:grid;grid-template-columns:.9fr 1.1fr;gap:6mm;align-items:start">
<div>{img('cover_caja.jpg', 'El caza Vórtice 6 en la carátula.')}</div>
<div>
<p class="lead">El nuevo caza estelar de la Federación. En pantalla es blanco y cian para verse siempre sobre cualquier fondo; con escudo se vuelve dorado.</p>
<div class="g2" style="margin:3mm 0">
<div class="card" style="text-align:center"><div class="spr" style="height:26mm"><img src="spr_nave.png"></div><div class="cap" style="margin-top:2mm"><b>Vórtice 6</b></div></div>
<div class="card" style="text-align:center"><div class="spr" style="height:26mm"><img src="spr_nave_escudo.png"></div><div class="cap" style="margin-top:2mm"><b>Con escudo</b></div></div>
</div>
<h3>El láser cápsula</h3>
<p>Un disparo gordo, de cola azul y punta blanca, con dos misiles. Mejora por niveles con las cápsulas P:</p>
<table>
<tr><td>P1</td><td>un láser</td></tr>
<tr><td>P2</td><td>dos láseres en paralelo</td></tr>
<tr><td>P3</td><td>tres láseres en abanico</td></tr>
</table>
</div>
</div>
{img('laser.png', '<b>P1, P2 y P3.</b> El marcador de abajo muestra el nivel con una, dos o tres flechas.')}
<div class="g2" style="margin-top:2mm">
{enemy('capsula_p', 'Cápsula P', 'Potencia', 'Sube un nivel el láser. Con el nivel 3 ya conseguido, da <b>500</b> puntos.')}
{enemy('capsula_s', 'Cápsula S', 'Escudo', 'La nave aguanta un impacto (se vuelve dorada). Si ya llevas escudo, da <b>500</b> puntos.')}
</div>
<p class="dim" style="margin-top:3mm;font-size:8.4pt">Las cápsulas caen al limpiar ciertas oleadas enteras y siempre al destruir una Unidad Cero. Nacen siempre por delante de ti
y nunca dentro ni junto a un obstáculo: si no hay sitio, esperan en pantalla a que lo haya.</p>
''', sec='Instrucciones')

# ===================================================================== 7 · Unidad Cero
page(f'''
<div class="hdr"><div><div class="kick">Enemigo recurrente</div>{tit('UNIDAD CERO')}</div></div>
<div style="font-family:D;font-weight:800;font-size:13pt;color:#ff3d3d;letter-spacing:.18em;margin-top:2mm">— COMPUZOIDE DEL VACÍO —</div>
<div class="rule"></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm">
<div>{img('uc_concepto.jpg', '<b>Concepto.</b> Armadura blanca y roja, cúpula de cristal y brazos-cañón de energía.')}</div>
<div>{img('uc_batalla.jpg', '<b>Concepto de batalla.</b> La Unidad Cero contra la Vórtice 6.')}</div>
</div>
<div style="display:grid;grid-template-columns:52mm 1fr;gap:6mm;margin-top:5mm;align-items:start">
<div class="g2" style="gap:3mm">
<div class="card" style="text-align:center;padding:2.5mm"><div class="spr" style="height:30mm"><img src="spr_unidad_cero.png" style="max-height:28mm"></div><div class="cap" style="margin:1.5mm 0 0">Fases 1–3</div></div>
<div class="card" style="text-align:center;padding:2.5mm"><div class="spr" style="height:30mm"><img src="spr_unidad_cero_f5.png" style="max-height:28mm"></div><div class="cap" style="margin:1.5mm 0 0">Fase 5</div></div>
</div>
<div>
<p class="lead">Un mecha de combate al estilo de los grandes shooters de recreativa, el enemigo común más peligroso del juego.</p>
<ul>
<li>Llega <b>de uno en uno</b>: hasta que no cae o se va, no entra el siguiente.</li>
<li>Flota balanceándose en su carril, <b>avisa con un destello blanco</b> y dispara tres veces con su brazo-cañón, apuntando. Después se retira.</li>
<li>Es duro: aguanta más golpes en cada fase (8 en la primera, 16 en la última) y dispara cada vez más deprisa.</li>
<li>Al destruirlo <b>siempre suelta cápsula</b>, P y S alternas. Vale <b>500</b> puntos.</li>
<li>Aparece en las fases 1, 2, 3 y 5. En la Nave Viviente vuelve en carne roja y acero gris.</li>
</ul>
</div></div>
''', sec='Unidad Cero')

# ===================================================================== fases y jefes
PH = [
 dict(n=1, name='EL DESGUACE ESPACIAL', lema='Óxido · Chatarra · Inercia', band='linear-gradient(90deg,#16206b,#5a2e8c,#a3401f)',
  intro='Un cementerio orbital de naves. Losas flotantes, torres de chatarra, grúas y contenedores sobre un cielo que pasa del azul noche al violeta y al rojo óxido. Es la fase para aprender.',
  tramos=['<b>A · Patio de restos.</b> Chatarra suelta y balizas con luz roja.', '<b>B · Trituradora orbital.</b> Un pasillo que se estrecha.', '<b>C · Campo magnético.</b> Placas flotantes y grúas.', '<b>D · Dársena central.</b> La antesala de FERRUM-9.'],
  peligros='Todo el decorado sólido mata. Las estrellas y el horizonte de chatarra del fondo se atraviesan. La grúa-araña es decorado: no dispara, pero no la toques.',
  music='Re menor, 138 BPM. Tecno oscuro: batería, bajo zumbón y una melodía de sierra con eco.',
  en=[('carronero', 'Carroñero', 'Pez cíborg', 'Aleta-cuchilla y fauces. Entra en arco, hace un quiebro y regresa. 100 puntos.'),
      ('chatarrin', 'Chatarrín', 'Nave orgánica', 'Alienígena morado con cola de metal y núcleo que late. Avanza en zigzag. 150 puntos.'),
      ('unidad_cero', 'Unidad Cero', 'Mecha', 'Avisa con un destello y dispara apuntando. Siempre suelta cápsula. 500 puntos.')],
  boss='FERRUM-9', blema='El Compactador Soberano', bhp=40,
  bdesc='Una prensa industrial con mandíbulas de acero y un ojo tras persianas blindadas. Solo se le hiere con el ojo abierto. Al caer: 5.000 puntos.',
  att=[('I · Recolección', 'Escupe chatarra por las mandíbulas. El ojo sigue cerrado.'),
       ('II · Compactación', '«¡COMPACTACIÓN! ENTRA ENTRE SUS PINZAS». Las paredes se cierran hasta tapar la pantalla. El único refugio es el hueco entre sus mandíbulas, delante del ojo.'),
       ('III · Exposición', 'El ojo se abre en tres tiempos (persianas, rendija roja, iris) y dispara un abanico de tres balas.')],
  tip='Durante la compactación, métete entre las pinzas pronto: desde ahí le das al ojo a bocajarro en cuanto se abre.',
  cap=('Patio de restos: chatarra flotante y el Carroñero.', 'El campo magnético, con la Unidad Cero.', '¡Compactación! Las paredes se cierran.', 'El ojo, abierto: es el momento de disparar.')),
 dict(n=2, name='LOS OCÉANOS ASTRALES', lema='Bioluminiscencia · Presión · Corrientes', band='linear-gradient(90deg,#0b1a6b,#1b6fa8,#2e9a5a)',
  intro='Un mar sin horizonte en pleno espacio. Bolsas de agua hexagonales, jardines de coral orbital hechos de enredadera marina con bulbos y ojos, y un leviatán que pasa al fondo.',
  tramos=['<b>A · Mar sin horizonte.</b> Bolsas de agua y medusas lejanas.', '<b>B · Jardines de coral orbital.</b> Masas de enredadera que crecen del suelo y del techo.', '<b>C · Tormenta gravitacional.</b> Tubos de presión y corrientes.', '<b>D · Abismo de marea.</b> El leviatán al fondo.'],
  peligros='<b>Corrientes</b> (tramo C): las líneas de partículas avisan, y la corriente te empuja hacia arriba o hacia abajo. Tu nave es más rápida: siempre se puede vencer.',
  music='Fa sostenido dórico, 112 BPM.',
  en=[('medusa', 'Medusa de Vacío', 'Deriva', 'Campana de tres colores. Deriva con vaivén y suelta una esfera lenta apuntada.'),
      ('raya', 'Raya Fotónica', 'Manta', 'Entra en arco y sale de la pantalla. Rápida.'),
      ('anguila', 'Anguila de Marea', 'Larga', 'Sigue una ruta fija ondulante. Aguanta más golpes.'),
      ('unidad_cero', 'Unidad Cero', 'Mecha', 'También aquí, de una en una.')],
  boss='THALASSA', blema='La Madre de las Mareas', bhp=60,
  bdesc='Una diosa de mármol de perfil, con diadema; su pelo, en mechones ondulados, es la propia pared del final del océano. Su punto débil es el ojo-perla.',
  att=[('I · Canto', 'Canta burbujas desde la boca a velocidades alternas. Abre el ojo un momento tras cada tercer pulso.'),
       ('II · Corriente', '«¡CORRIENTE! BUSCA EL CARRIL LIBRE». Mechones de pelo cruzan la pantalla y llenan dos de los tres carriles. El libre cambia cada vez.'),
       ('III · Remolino', '«¡LA DIOSA ABRE EL OJO! DISPARA AL OJO». El ojo se queda abierto más tiempo y suelta crías en abanico.')],
  tip='En la corriente, el carril libre rota: medio, abajo, arriba. Colócate antes de que llegue el pelo.',
  cap=('Los jardines de coral orbital.', 'La tormenta gravitacional: corrientes y tubos de presión.', '¡Corriente! Solo un carril queda libre.', 'Thalassa abre el ojo.')),
 dict(n=3, name='EL FUEGO INFERNAL DE HADES', lema='Ceniza · Fuego · Erupción', band='linear-gradient(90deg,#1a0606,#7a1010,#d24a10)',
  intro='Columnas de basalto, estatuas demoníacas al fondo y un río de lava. La primera fase en la que el propio escenario te ataca.',
  tramos=['<b>A · Cenizas exteriores.</b> Columnas de basalto.', '<b>B · Hornos gemelos.</b> Fumarolas arriba y abajo que se alternan.', '<b>C · Garganta de brasas.</b> Techo y suelo se acercan; muros de fuego con una sola compuerta.', '<b>D · Trono de escoria.</b> Una cadena de fuegos por el suelo.'],
  peligros='<b>Géiseres</b>: todos laten a la vez. Brasa oscura (dormidos), amarillo que parpadea (aviso) y fuego blanco (erupción, mata). Las <b>pinzas</b> de suelo y techo solo dejan un hueco de tres filas.',
  music='La frigio, 150 BPM. Bajo martilleante y percusión dura.',
  en=[('ascoria', 'Ascoria', 'Roca', 'Roca facetada que deriva y, a mitad de camino, se abre en dos fragmentos.'),
      ('serafin', 'Serafín Negro', 'Caza', 'Vuelo en S. Dispara dos veces apuntando y se retira.'),
      ('martir', 'Mártir de Plasma', 'Espectro', 'Se acerca despacio mientras se materializa y luego cruza en línea recta, muy deprisa.'),
      ('unidad_cero', 'Unidad Cero', 'Mecha', 'Ocupa el lugar del antiguo Incinerador.')],
  boss='EL TRÍPTICO DE HADES', blema='Altar de tres rostros', bhp=110,
  bdesc='Tres máscaras apiladas delante de un pilar de basalto: FURIA (cuernos y dientes), HAMBRE (boca-horno) y CENIZA (ojos cerrados). El punto débil es el horno de HAMBRE.',
  att=[('I · Furia', 'Ráfagas de brasas desde las bocas de FURIA y CENIZA. Entre ráfagas, el horno se abre un instante.'),
       ('II · Hambre', '«¡HAMBRE TE ASPIRA! DISPARA AL HORNO». El horno se abre y te aspira hacia el altar. Aguantando a la izquierda se escapa.'),
       ('III · Ceniza', '«¡CENIZA! EL REACTOR ESTÁ EXPUESTO». El horno queda abierto más tiempo y lanza abanicos de brasas.')],
  tip='Cuando HAMBRE aspira, no luches solo contra la succión: tira a la izquierda y no dejes de disparar, el horno está abierto.',
  cap=('Los hornos gemelos y sus géiseres.', 'La garganta de brasas.', 'El Tríptico despierta.', '¡Ceniza! El reactor está expuesto.')),
 dict(n=4, name='EL SARCÓFAGO DE SACRIFICIOS DE SATURNO', lema='Oro · Jade · Sacrificio', band='linear-gradient(90deg,#1c0b3b,#5a2a8c,#b08a2a)',
  intro='Violeta profundo, oro envejecido y jade pálido. Saturno anillado al fondo, polvo de oro y oficiantes de piedra. Aquí se celebra el rito que quiere traer de vuelta a Leviatán V.',
  tramos=['<b>A · Anillos de entrada.</b> La abertura sube, baja y se estrecha.', '<b>B · Galería de ofrendas.</b> Altares, lámparas y puertas ceremoniales.', '<b>C · Cámara de las máscaras.</b> Máscaras rituales de oro con ojos y boca.', '<b>D · Sala del sarcófago.</b> Tapas de sarcófago que forman tres carriles.'],
  peligros='<b>Puertas ceremoniales</b>: rejillas de energía de todo el alto con una sola compuerta. Destruye sus dos <b>nodos de jade</b> (arriba y abajo) y la rejilla se apaga: +1.000 puntos y paso libre.',
  music='Do menor, 100 BPM. Coro sintético, campanas y un bombo a medio tiempo: un rito lento y pesado.',
  en=[('acolito', 'Acólito Orbital', 'Rombo', 'Entra deprisa, se planta, se carga destellando y suelta un disparo lento apuntado.'),
      ('guardian', 'Guardián de Anillo', 'Armadura', 'Pesado: necesita cuatro golpes. Cruza en arco.'),
      ('vaso', 'Vaso Votivo', 'Urna', 'Deriva meciéndose. Al romperlo suelta una cápsula o un alma que va hacia ti.'),
      ('escriba', 'Escriba Autómata', 'Pulso de luz', 'Marca su fila en violeta y, medio segundo después, toda la fila arde en blanco. ¡Sal de ella!')],
  boss='SATURNUS', blema='El Oficiante Vacío', bhp=140,
  bdesc='Un sacerdote encapuchado con túnica violeta y oro que levita sobre la arena, cáliz en mano. Donde debería estar su cara solo hay vacío, y ese vacío es su punto débil.',
  att=[('I · Ofrenda', 'Lanza ofrendas desde el vacío y desde el cáliz. Entre ráfagas, dos ojos se asoman y el vacío se abre un instante.'),
       ('II · El Rito', '«¡EL RITO! BUSCA LA FILA LIBRE». Bandas rituales llenan la pantalla de fuera hacia dentro hasta dejar un solo carril. Cada vez, uno distinto.'),
       ('III · El Cáliz se abre', '«¡EL CÁLIZ SE ABRE! DISPARA AL VACÍO». El vacío arde en jade, es vulnerable y dispara en abanico.')],
  tip='Los Escribas avisan siempre: la fila parpadea en violeta antes de arder. Muévete en cuanto la veas.',
  cap=('El pulso de luz de los Escribas.', 'La cámara de las máscaras.', '¡El Rito! Busca la fila libre.', 'El cáliz se abre: el vacío arde en jade.')),
 dict(n=5, name='LA NAVE VIVIENTE', lema='Carne · Hueso · Latido', band='linear-gradient(90deg,#1a0004,#6a0c18,#c8c8d0)',
  intro='El interior de una nave que está viva. Tejido con venas, arterias, mandíbulas de hueso y ojos inyectados en sangre enterrados en la carne. Al fondo late el corazón de Leviatán V.',
  tramos=['<b>A · Boca.</b> Mandíbulas de hueso con dientes.', '<b>B · Conductos.</b> Carne, arterias y paredes que respiran.', '<b>C · Cámara de los ojos.</b> Masas llenas de ojos arriba y abajo.', '<b>D · Ventrículo.</b> Pinzas de músculo.'],
  peligros='<b>Paredes respirantes</b>: relajadas no hacen nada, al avisar parpadean y contraídas vibran en rosa y blanco y matan. Las <b>pinzas</b> cierran techo y suelo a la vez y dejan un hueco de tres filas.',
  music='Si menor, 128 BPM. El bombo doble es el latido; hay un tramo en el que solo suena el corazón.',
  en=[('globulo', 'Glóbulo Cazador', 'Perseguidor', 'Memoriza dónde estabas y va hacia allí. Dispara apuntando.'),
      ('larva', 'Larva Mecánica', 'Veloz', 'Cruza muy deprisa y hace un único cambio de altura.'),
      ('unidad_cero_f5', 'Unidad Cero', 'Mecha', 'Vuelve, en carne roja y acero. La más dura: 16 golpes.'),
      ('escriba_f5', 'Escriba fantasma', 'Pulso de luz', 'Los Escribas de Saturno, ahora espectros. Avisan menos.')],
  boss='EL CORAZÓN NULO', blema='Leviatán V resucitado', bhp=180,
  bdesc='Un ojo-válvula enorme en una arena biomecánica: paneles de acero con LEDs rojos que laten con él, tubos de acero que lo sujetan al techo y al suelo, y un iris de pétalos de músculo.',
  att=[('I · Defensa', 'Dos nodos de energía, arriba y abajo, protegen el ojo. Mientras quede alguno, el ojo no recibe daño. Con los dos caídos: +1.000.'),
       ('II · Mutación', '«¡MUTACIÓN! LEE EL LATIDO Y ESQUIVA». Alterna bandas de tejido que dejan un solo carril libre y una válvula que te aspira hacia el ojo.'),
       ('III · Último latido', '«¡NÚCLEO EXPUESTO! DISPARA AL REACTOR». La válvula se abre del todo y el reactor dispara en abanico.')],
  tip='Primero los nodos. Sin ellos, el Corazón Nulo es invulnerable por mucho que le dispares.',
  cap=('Los conductos: tejido, venas y un ojo enterrado.', 'La cámara de los ojos.', '¡Mutación! Un solo carril libre.', 'Núcleo expuesto: dispara al reactor.')),
]
for ph in PH:
    n = ph['n']
    ens = ''.join(enemy(*e) for e in ph['en'])
    page(f'''
<div class="hdr"><div><div class="kick">Fase {n} · {ph['lema']}</div>{tit(ph['name'] if len(ph['name']) <= 26 else 'EL SARCÓFAGO DE SATURNO', 'fuego', 4, maxw=148)}</div><div class="num">0{n}</div></div>
<div class="phase-band" style="background:{ph['band']}"></div>
<p class="lead">{ph['intro']}</p>
<div class="g2" style="margin-top:3mm">
<div>{img('f%d_j1.png' % n, ph['cap'][0])}</div>
<div>{img('f%d_j2.png' % n, ph['cap'][1])}</div>
</div>
<div class="g2">
<div><h3>El recorrido</h3><ul>{''.join('<li>%s</li>' % t for t in ph['tramos'])}</ul>
<h3>Peligros</h3><p>{ph['peligros']}</p>
<h3>Música</h3><p>{ph['music']}</p></div>
<div><h3>Enemigos</h3><div style="display:grid;gap:2.4mm">{ens}</div></div>
</div>
''', sec='Fase %d' % n)
    atts = ''.join('<div class="card"><div class="tag">%s</div><div>%s</div></div>' % a for a in ph['att'])
    page(f'''
<div class="hdr"><div><div class="kick">Jefe de la fase {n}</div>{tit(ph['boss'], 'acero', 5 if len(ph['boss']) <= 12 else 4)}</div><div class="num">0{n}</div></div>
<div style="font-family:D;font-weight:800;font-size:12pt;color:#ff7a2a;letter-spacing:.16em;text-transform:uppercase;margin-top:2mm">{ph['blema']}</div>
<div class="rule"></div>
<p class="lead">{ph['bdesc']}</p>
<div class="g2" style="margin-top:3mm">
<div>{img('f%d_b1.png' % n, ph['cap'][2])}</div>
<div>{img('f%d_b2.png' % n, ph['cap'][3])}</div>
</div>
<h3>El combate</h3>
<div style="display:grid;gap:2.6mm">{atts}</div>
<div class="g2" style="margin-top:3mm;align-items:stretch">
<div class="tip"><b>Consejo.</b> {ph['tip']}</div>
<div class="card" style="display:flex;gap:6mm;align-items:center"><div class="stat">{ph['bhp']}<small>puntos de vida (Normal)</small></div>
<div class="dim" style="font-size:8pt">Antes de su arena suena una sirena y su nombre aparece en el marcador. Los ataques se repiten hasta que cae.</div></div>
</div>
''', sec='Jefe %d' % n)

# ===================================================================== prólogo y epílogo
page(f'''
<div class="kick">Cinemáticas</div>
{tit('PRÓLOGO Y EPÍLOGO')}
<div class="rule"></div>
<p class="lead">El juego empieza y termina con una pieza de cine: frases que se encienden sobre negro, una ilustración a pantalla completa
redibujada a partir de las carátulas y su propia música.</p>
<div class="g2" style="margin-top:4mm">
<div>{img('intro_nave.png', '<b>Intro.</b> «Cuando cayó el Corazón de Acero… El vacío tomó su lugar… El alma del universo pide tu ayuda…». Música en Re menor que estalla en Re mayor.')}</div>
<div>{img('final_frase.png', '<b>Final.</b> «El vacío da paso al silencio. El silencio es la paz. La galaxia recupera la esperanza.» Y «FIN».')}</div>
<div>{img('elara_destello.png', '<b>Elara Voss.</b> Al final aparece la comandante; un destello le cruza el ojo con un «tilín» antes del fundido a negro.')}</div>
<div>{img('creditos.png', '<b>Créditos.</b> Suben despacio desde abajo con la música del final (La mayor, piano y coro). Después, tu puntuación final.')}</div>
</div>
<p class="dim" style="font-size:8pt">Las dos ilustraciones usan el modo de mapa de bits del Atari (160 × 192) con cuatro colores por cada franja de cuatro líneas, cambiados en cada franja por interrupciones de pantalla.</p>
''', sec='Cinemáticas')

# ===================================================================== secretos y consejos
page(f'''
<div class="kick">Para pilotos</div>
{tit('SECRETOS Y CONSEJOS')}
<div class="rule"></div>
<div class="g2">
<div>
<h3>Consejos generales</h3>
<ul>
<li><b>Mantén FIRE pulsado.</b> El disparo es automático y no hay motivo para soltarlo.</li>
<li><b>Todo lo que dispara fuerte avisa.</b> La Unidad Cero, el Acólito y los Escribas destellan antes de atacar.</li>
<li><b>Ninguna bala nace pegada a ti.</b> Siempre aparecen con margen por delante: mira el carril, no la nave.</li>
<li><b>Las balas son de colores vivos.</b> Amarillas en los carriles libres; del color de su enemigo en los ocupados.</li>
<li><b>Limpia oleadas enteras.</b> Algunas sueltan cápsula al caer el último enemigo.</li>
<li><b>Prioriza la Unidad Cero.</b> Siempre deja cápsula.</li>
<li><b>Los jefes siempre dejan hueco.</b> Compactación, corriente, rito y mutación cierran la pantalla, pero nunca del todo.</li>
<li>En <b>Hardcore</b>, morir te deja sin láser ni escudo: juega a no perder la primera nave.</li>
</ul>
</div>
<div>
<h3>Puntuación</h3>
<table>
<tr><td>Carroñero</td><td>100</td></tr>
<tr><td>Chatarrín</td><td>150</td></tr>
<tr><td>Unidad Cero</td><td>500</td></tr>
<tr><td>Cápsula sobrante</td><td>500</td></tr>
<tr><td>Puerta ceremonial abierta · nodos del Corazón</td><td>1.000</td></tr>
<tr><td>FERRUM-9</td><td>5.000</td></tr>
</table>
<h3>Modo invencible</h3>
<div class="card">
<p>En el título: <b class="cy">abajo, abajo y FIRE</b>, con menos de cuatro segundos entre pulsaciones. Aparece «MODO INVENCIBLE ACTIVADO».
La misma secuencia lo desactiva. El modo se mantiene de fase en fase.</p>
</div>
<h3>La historia</h3>
<p>Deja el título sin tocar el mando 13 segundos y la historia aparecerá en dos páginas.</p>
</div>
</div>
<div style="margin-top:3mm;width:118mm">{img('muerte.png', '<b>Muerte de un jefe:</b> el fondo destella, explosiones por todo el cuerpo y el jefe se desmorona fila a fila hasta desaparecer.')}</div>
''', sec='Consejos')

# ===================================================================== memoria (4 páginas)
page(f'''
<div class="kick">Memoria del proyecto · 1</div>
{tit('ORIGEN Y DIRECCIÓN')}
<div class="rule"></div>
<p class="lead">Vórtice 6 es la continuación de Vórtice 5, el shooter vertical en el que cayó el Corazón de Acero. Esta vez el scroll es horizontal
y el modelo, el euroshooter de finales de los ochenta: rapidez, dificultad dura pero justa y una curva que sube fase a fase.</p>
<h3>El punto de partida</h3>
<p>Tony C. Ware escribió el documento de diseño (GDD), dibujó el atlas visual previo y encargó las carátulas: la piloto con casco junto a la nave
y la caja con el caza ante el Corazón del Vacío. Los nombres de la nave, las fases, los jefes y los enemigos vienen de ese diseño y se han mantenido.</p>
<h3>Decisiones de dirección</h3>
<ul>
<li><b>Ajustado al Atari:</b> un solo disparo que mejora con la cápsula P, escudo con la cápsula S, y tres o cuatro enemigos por fase.</li>
<li><b>Pantalla limpia:</b> balas siempre visibles, nada de parpadeos y ningún sprite cortado. Se trató la pantalla como en Vórtice 5 y Zak Attack.</li>
<li><b>Sin torretas:</b> los enemigos fijos del GDD se cambiaron por voladores; el mecha Remachador se convirtió en la <b>Unidad Cero</b> y se repite por el juego.</li>
<li><b>Obstáculos grandes y angulosos</b>, con borde claro para verse sobre cualquier fondo.</li>
<li><b>Nombres íntegros:</b> cada fase muestra su nombre completo antes de empezar, como «El Sarcófago de Sacrificios de Saturno».</li>
<li><b>Jefes espectaculares:</b> cada uno con tres fases de ataque, un punto débil visible y una muerte a lo grande, sin dejar restos en pantalla.</li>
<li><b>Morir con dignidad:</b> tres segundos de invulnerabilidad al volver y un GAME OVER centrado: «El vacío ha reclamado tu alma».</li>
</ul>
<h3>Cómo se hizo</h3>
<p>Tony dirigió todo el proceso pieza a pieza: eligió entre propuestas de diseño para cada enemigo y jefe (dibujadas en hojas comparativas
con su aspecto real en pantalla), pidió cambios después de jugar cada versión y fijó la paleta, la música y la dificultad. El programa se escribió
con la asistencia de GPT y Claude, y cada versión se probó con partidas automáticas en un emulador antes de entregarse.</p>
<div class="g3" style="margin-top:4mm">
<div class="card"><div class="tag">Fase 2</div><p>La diosa Thalassa se rehízo como un perfil femenino de escultura clásica, con el pelo unido a la pared.</p></div>
<div class="card"><div class="tag">Fase 4</div><p>Los Escribas dejaron de disparar balas: su pulso de luz es el ataque. Las jarras del escenario pasaron a ser máscaras rituales.</p></div>
<div class="card"><div class="tag">Fase 5</div><p>Fuera los verdes y las formas de árbol: carne, hueso y ojos enterrados en las venas, y una arena final biomecánica.</p></div>
</div>
''', sec='Memoria')

page(f'''
<div class="kick">Memoria del proyecto · 2</div>
{tit('LA TÉCNICA')}
<div class="rule"></div>
<div class="g2">
<div>
<h3>Escenarios</h3>
<p>Modo de caracteres de cuatro colores (ANTIC 4) con scroll fino horizontal sobre un búfer de 64 columnas. Cada fase tiene su juego de
128 caracteres; el generador se niega a compilar si un dibujo no cabe. El mapa se guarda en cuatro trozos de cinco filas con su propio diccionario.</p>
<p>Los degradados del cielo, el agua o la lava cambian el color de fondo fila a fila con interrupciones de pantalla (DLI).</p>
<h3>Sprites sin parpadeo</h3>
<p>El campo se divide en <b>cuatro franjas fijas</b> con dos huecos de sprite cada una. Cada enemigo recibe un hueco al nacer y lo conserva hasta morir.
Nunca hay más sprites que huecos, así que no hay parpadeo: si una oleada no cabe, el siguiente enemigo espera.</p>
<p>Los enemigos de tres colores son parejas de sprites superpuestos o desplazados; algunos usan doble ancho, cambiado por franja en la DLI.</p>
<h3>Doble búfer</h3>
<p>Dos zonas de sprites y dos bancos de tablas de color: el programa dibuja en el oculto y la interrupción vertical solo cambia punteros. Nada se dibuja a medias.</p>
</div>
<div>
<h3>Balas siempre visibles</h3>
<p>Cuatro puntos de ancho y tres líneas de alto, en amarillo vivo o en el color claro del enemigo de su franja. Ninguna nace a menos de 32 puntos por delante de la nave.
Se comprobó en partidas automáticas completas: todas las balas activas se veían en su sitio en las cinco fases.</p>
<h3>Jefes</h3>
<p>Cada jefe es un dibujo de caracteres de hasta 20 × 16 con su propio juego de caracteres, que cambia al entrar en la arena. Sus ataques
de pantalla completa (compactación, corriente, rito, mutación) se dibujan con el decorado.</p>
<h3>Música y efectos</h3>
<p>Un reproductor propio de cuatro voces en el chip POKEY: synth, bajo con distorsión, batería y eco. Los efectos ocupan un canal un momento y la música sigue.
La afinación se midió en el emulador, y la tonalidad de cada fase se eligió para que el bajo caiga en notas afinadas.</p>
<table style="margin-top:2mm">
<tr><th>Tema</th><th>Tono</th><th>Tempo</th></tr>
<tr><td>Intro</td><td>Re menor → Re mayor</td><td>90</td></tr>
<tr><td>Fase 1 · Desguace</td><td>Re menor</td><td>138</td></tr>
<tr><td>Fase 2 · Océanos</td><td>Fa# dórico</td><td>112</td></tr>
<tr><td>Fase 3 · Hades</td><td>La frigio</td><td>150</td></tr>
<tr><td>Fase 4 · Saturno</td><td>Do menor</td><td>100</td></tr>
<tr><td>Fase 5 · Nave Viviente</td><td>Si menor</td><td>128</td></tr>
<tr><td>Jefes</td><td>Mi frigio</td><td>150</td></tr>
<tr><td>Final</td><td>La mayor</td><td>64</td></tr>
</table>
</div>
</div>
''', sec='Memoria')

page(f'''
<div class="kick">Memoria del proyecto · 3</div>
{tit('DISCO Y CARTUCHO')}
<div class="rule"></div>
<p class="lead">El juego completo son siete programas que no caben a la vez en 64 KB: intro, cinco fases y final. Un pequeño cargador residente
los trae uno a uno y les pasa la partida.</p>
<div class="g2">
<div>
<h3>El bloque compartido</h3>
<p>Catorce bytes de la página 5 sobreviven entre programas: dificultad, puntos, naves, nivel del láser, escudo, récord, truco y si la partida viene encadenada.
Al superar una fase se guardan y se carga la siguiente; si pierdes, vuelves al título.</p>
<h3>Disco</h3>
<p>Doble densidad, arranque propio sin DOS. El cargador vive en $0710 y lee cada programa por el SIO del sistema a partir de $2000.</p>
<table>
<tr><th>Programa</th><th>Sectores</th></tr>
<tr><td>Intro</td><td>80</td></tr>
<tr><td>Fase 1 (con el título)</td><td>108</td></tr>
<tr><td>Fases 2 · 3 · 4 · 5</td><td>98 · 99 · 100 · 103</td></tr>
<tr><td>Final</td><td>80</td></tr>
<tr><td>Total</td><td>668 de 717</td></tr>
</table>
</div>
<div>
<h3>Cartucho</h3>
<p>AtariMax 8 Mbit: 128 bancos de 8 KB en la ventana $A000–$BFFF. El banco de arranque copia el mismo cargador a $0700, con la misma interfaz que el del disco,
así que los programas son idénticos en los dos formatos.</p>
<p>Para cada carga, el cargador va cambiando de banco y copiando páginas a la memoria; al terminar, <b>desconecta el cartucho</b> para que el juego tenga RAM en $A000–$BFFF
y avisa al sistema del cambio. Usa 22 bancos; el de arranque está repetido en el último para que funcione tanto con el arranque «antiguo» como con el «nuevo» de estos cartuchos.</p>
<h3>Pruebas</h3>
<p>Partidas automáticas encadenadas de la intro al título, en disco y en cartucho, comprobando que pasan puntos, naves, láser, escudo, dificultad y récord.
También se probó el arranque en un sistema PAL.</p>
</div>
</div>
<h3>Pantallas de enlace</h3>
<div class="g3">
<div>{img('superada.png', '<b>Fase superada.</b> Se guarda la partida y se carga la siguiente.')}</div>
<div>{img('gameover.png', '<b>Game over.</b> «El vacío ha reclamado tu alma».')}</div>
<div>{img('puntuacion.png', '<b>Fin de la partida.</b> Puntuación final y vuelta al título.')}</div>
</div>
''', sec='Memoria')

page(f'''
<div class="kick">Memoria del proyecto · 4</div>
{tit('HERRAMIENTAS')}
<div class="rule"></div>
<p class="lead">Todo el juego sale de ficheros de texto. Los gráficos se dibujan como rejillas de caracteres en Python, un generador los
comprueba contra los límites del hardware y produce los datos en ensamblador, y el ensamblador ca65 monta cada programa.</p>
<div class="g2">
<div>
<h3>La cadena</h3>
<ul>
<li><span class="mono">gfx/*.py</span>: escenarios, enemigos, jefes, paletas y fuente, dibujados en texto.</li>
<li><span class="mono">tools/gen1.py</span>: genera los datos de cada fase y valida colores, caracteres y textos.</li>
<li><span class="mono">tools/musica.py</span>: compone y empaqueta los temas para el reproductor.</li>
<li><span class="mono">tools/atpic.py</span>: convierte las ilustraciones de las carátulas al modo de mapa de bits.</li>
<li><span class="mono">src/g1.s</span>: el motor del juego; <span class="mono">src/cine.s</span>, la intro y el final.</li>
<li><span class="mono">mkdisk.py</span> y <span class="mono">mkcart.py</span>: montan el disco y el cartucho.</li>
</ul>
<h3>Probar sin manos</h3>
<p>Un arnés sobre la biblioteca del emulador atari800 juega partidas con guiones de joystick, captura pantallas, lee la memoria y graba el sonido.
Con él se midieron la visibilidad de las balas, las cápsulas, el tiempo por cuadro y la afinación.</p>
</div>
<div>
<h3>En cifras</h3>
<div class="g2" style="gap:3mm">
<div class="card"><div class="stat">7<small>programas</small></div></div>
<div class="card"><div class="stat">167 KB<small>de juego</small></div></div>
<div class="card"><div class="stat">8<small>temas de música</small></div></div>
<div class="card"><div class="stat">3<small>formatos</small></div></div>
<div class="card"><div class="stat">20 × 16<small>caracteres por jefe</small></div></div>
<div class="card"><div class="stat">0<small>parpadeos</small></div></div>
</div>
<h3>Ficheros del paquete</h3>
<table>
<tr><td>vortice6.atr</td><td>Disco, juego completo</td></tr>
<tr><td>vortice6.car</td><td>Cartucho, juego completo</td></tr>
<tr><td>*.xex</td><td>Intro, cada fase y final</td></tr>
<tr><td>*_PRUEBA.xex</td><td>Cada fase con la nave invencible</td></tr>
<tr><td>musica/</td><td>Los temas grabados del emulador</td></tr>
<tr><td>fuentes/</td><td>Todo el código y los dibujos</td></tr>
</table>
</div>
</div>
<h3>Bestiario: los sprites tal y como los monta el juego</h3>
<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:2mm">
{''.join('<div class="spr" style="height:17mm"><img src="spr_%s.png" style="max-height:14mm;max-width:17mm"></div>' % k for k in ['nave','carronero','chatarrin','unidad_cero','medusa','raya','anguila','ascoria','serafin','martir','acolito','guardian','vaso','escriba','globulo','larva'])}
</div>
<p class="dim" style="font-size:7.6pt;margin-top:1.5mm">Formas y colores sacados de los mismos datos con los que se construye el juego, ampliados con la proporción de píxel de un televisor NTSC.</p>
''', sec='Memoria')

# ===================================================================== inspiración
INSP = [('DEFCOM 1', 'MSX', 'Ibersoft'), ('Meganova', 'MSX', 'Dinamic'), ('Gradius', 'NES', 'Konami'), ('Star Soldier', 'NES', 'Hudson Soft'),
        ('X-Out', 'Amiga', 'Rainbow Arts'), ('Saint Dragon', 'Spectrum', 'The Sales Curve, basado en el arcade de Jaleco')]
cards = ''.join('<div class="card"><div class="tag">%s</div><h4 style="font-size:14pt;margin:1.5mm 0">%s</h4><div class="dim">%s</div></div>' % (s, t, c) for t, s, c in INSP)
page(f'''
<div class="kick">Homenaje</div>
{tit('INSPIRACIÓN')}
<div class="rule"></div>
<p class="lead">Vórtice 6 ha sido inspirado por grandes obras como estas:</p>
<div class="g2" style="margin-top:5mm;gap:5mm">{cards}</div>
<p class="dim" style="margin-top:6mm">De ellas viene el pulso del juego: la dureza justa de los shooters europeos, los jefes con fases y punto débil de los arcades japoneses,
y el gusto por los mundos biomecánicos que se respiraba en los 8 y 16 bits.</p>
<h3 style="margin-top:8mm">Los cinco guardianes</h3>
<div class="g3">
<div>{img('f1_b2.png', 'FERRUM-9')}</div><div>{img('f2_b2.png', 'THALASSA')}</div><div>{img('f3_b1.png', 'El Tríptico de Hades')}</div>
<div>{img('f4_b2.png', 'SATURNUS')}</div><div>{img('f5_b2.png', 'El Corazón Nulo')}</div><div>{img('elara_destello.png', 'Elara Voss')}</div>
</div>
''', sec='Inspiración')

# ===================================================================== créditos
page(f'''
<div style="text-align:center;padding-top:22mm">
{tit('VÓRTICE 6', 'fuego', 7, 'tit').replace('class="tit"', 'class="tit" style="margin:0 auto;height:13mm"')}
<div style="height:4mm"></div>
{tit('CORAZÓN DEL VACÍO', 'acero', 4, 'tit s').replace('class="tit s"', 'class="tit s" style="margin:0 auto"')}
<div class="rule" style="margin:8mm auto"></div>
<div style="font-size:8pt;letter-spacing:.3em;color:#4fd6ff;text-transform:uppercase;margin-top:10mm">Dirigido y diseñado por</div>
<div style="font-family:D;font-weight:900;font-size:24pt;color:#fff;margin:2mm 0 9mm">TONY C. WARE</div>
<div style="font-size:8pt;letter-spacing:.3em;color:#4fd6ff;text-transform:uppercase">Gráficos, fases y música</div>
<div style="font-family:D;font-weight:900;font-size:24pt;color:#fff;margin:2mm 0 9mm">TONY C. WARE</div>
<div style="font-size:8pt;letter-spacing:.3em;color:#4fd6ff;text-transform:uppercase">Programa y asistencia</div>
<div style="font-family:D;font-weight:900;font-size:24pt;color:#fff;margin:2mm 0 12mm">GPT Y CLAUDE</div>
<div class="dim" style="font-size:9pt;line-height:1.8">Protagonista: la Comandante Elara Voss, a bordo del Vórtice 6<br>
Los guardianes del vacío: FERRUM-9 · THALASSA · el Tríptico de Hades · SATURNUS · el Corazón Nulo</div>
<div style="font-family:D;font-weight:800;font-size:12pt;color:#ff7a2a;letter-spacing:.24em;margin-top:16mm">© 2026 · TONY C. WARE</div>
</div>
''', sec='Créditos')

# ===================================================================== contraportada
page('<img class="bg" src="img/cover_elara.jpg">', 'full', foot=False)

html = '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>VÓRTICE 6 · Atlas del proyecto</title><style>%s</style></head><body>%s</body></html>' % (CSS, '\n'.join(pages))
open(os.path.join(A, 'atlas.html'), 'w').write(html)
print('páginas:', len(pages))
