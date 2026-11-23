#!/usr/bin/env python3
"""VÓRTICE 6 · atlas visual Atari 8 bits (A4 apaisado), desde los mismos datos y capturas de run8."""
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx'), os.path.join(ROOT, 'tools')]
from PIL import Image, ImageDraw, ImageFont
from pal import atari_rgb as A
import hw, sprites as S, world
from cells import Charset, scene_map

CAP = os.path.join(ROOT, 'build', 'cap')
OUT = os.path.join(ROOT, 'docs')
G = json.load(open(os.path.join(ROOT, 'build', 'gen.json')))
PW, PH = 1754, 1240
DJ = '/usr/share/fonts/truetype/dejavu/'
def F(n, s): return ImageFont.truetype(DJ + n, s)
FT = F('DejaVuSans-Bold.ttf', 44); FH = F('DejaVuSans-Bold.ttf', 26); FS = F('DejaVuSans-Bold.ttf', 19)
FR = F('DejaVuSans.ttf', 18); FRs = F('DejaVuSans.ttf', 15); FM = F('DejaVuSansMono.ttf', 15); FMb = F('DejaVuSansMono-Bold.ttf', 16)
BG = (12, 13, 24); PANEL = (24, 26, 44); EDGE = (70, 80, 130); GOLD = (255, 190, 70); TXT = (226, 228, 238); DIM = (150, 155, 180); RED = (235, 90, 80)
TIT = ['El Desguace Espacial', 'Los Océanos Astrales', 'El Fuego Infernal de Hades', 'El Sarcófago de Sacrificios de Saturno', 'La Nave Viviente']
PHC = [(150, 160, 175), (90, 190, 230), (240, 120, 50), (200, 150, 240), (230, 80, 110)]
pages = []

def page(num, kicker, title, accent=GOLD):
    im = Image.new('RGB', (PW, PH), BG); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, PW, 8), fill=accent)
    d.text((60, 34), kicker, font=FS, fill=accent)
    d.text((60, 60), title, font=FT, fill=TXT)
    d.line((60, 122, PW - 60, 122), fill=EDGE, width=2)
    d.text((60, PH - 40), 'VÓRTICE 6  ·  ATLAS VISUAL ATARI 8 BITS (NTSC)  ·  By Tony and Claude A.I.', font=FRs, fill=DIM)
    d.text((PW - 100, PH - 40), '%02d' % num, font=FS, fill=accent)
    return im, d

def panel(d, x0, y0, x1, y1, head=None, col=GOLD):
    d.rounded_rectangle((x0, y0, x1, y1), 10, fill=PANEL, outline=EDGE, width=2)
    if head: d.text((x0 + 16, y0 + 10), head, font=FS, fill=col); return y0 + 42
    return y0 + 14

def wrap(d, x, y, text, font=FR, w=600, fill=TXT, lh=None):
    lh = lh or int(font.size * 1.38)
    for para in text.split('\n'):
        line = ''
        for word in para.split(' '):
            t = (line + ' ' + word).strip()
            if d.textlength(t, font=font) > w and line:
                d.text((x, y), line, font=font, fill=fill); y += lh; line = word
            else: line = t
        d.text((x, y), line, font=font, fill=fill); y += lh
    return y

def bullets(d, x, y, items, w, font=FR, col=GOLD):
    for it in items:
        d.text((x, y), '▪', font=font, fill=col)
        y = wrap(d, x + 22, y, it, font, w - 22) + 4
    return y

def cap(name, w=None):
    im = Image.open(os.path.join(CAP, name + '.png'))
    if w: im = im.resize((w, int(im.height * w / im.width)), Image.NEAREST)
    return im

def frame(im, base, x, y, col=EDGE):
    d = ImageDraw.Draw(im); im.paste(base, (x, y)); d.rectangle((x - 2, y - 2, x + base.width + 1, y + base.height + 1), outline=col, width=2)

def swatch(d, x, y, code, label, w=150):
    d.rectangle((x, y, x + 44, y + 30), fill=A(code), outline=(0, 0, 0))
    d.text((x + 52, y - 1), '$%02X' % code, font=FMb, fill=TXT)
    d.text((x + 52, y + 16), label, font=FRs, fill=DIM)

# ---------------------------------------------------------------- render de datos
def render_grid(rows, colmap, cw=2, scale=4):
    """rows de texto; cada carácter = 1 color clock (cw px de ancho) x 1 línea"""
    h = len(rows); w = max(len(r) for r in rows)
    im = Image.new('RGBA', (w * cw * scale, h * scale), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            c = colmap.get(ch)
            if c is None: continue
            d.rectangle((x * cw * scale, y * scale, (x + 1) * cw * scale - 1, (y + 1) * scale - 1), fill=A(c))
    return im

def on_bg(img, bg=(0, 0, 0), pad=10, grid=False, cw=2, scale=4):
    o = Image.new('RGB', (img.width + 2 * pad, img.height + 2 * pad), bg)
    o.paste(img, (pad, pad), img)
    if grid:
        d = ImageDraw.Draw(o)
        for x in range(0, img.width + 1, cw * scale): d.line((pad + x, pad, pad + x, pad + img.height), fill=(40, 40, 60))
        for y in range(0, img.height + 1, scale): d.line((pad, pad + y, pad + img.width, pad + y), fill=(40, 40, 60))
        o2 = Image.new('RGB', o.size); o2.paste(o); o2.paste(img, (pad, pad), img); return o2
    return o

def ship_img(scale=6, colors=hw.SHIP):
    a, b = colors['p0'], colors['p1']
    rows = S.SHIP['A']
    return render_grid(rows, {'a': a, 'b': b, 'c': a | b}, 2, scale)

def phase_cmap(i):
    p = hw.PHASES[i]
    return {'1': p['pf0'], '2': p['pf1'], '3': p['pf2'], '4': p['pf3']}

def meta_img(m, i, scale=4):
    return render_grid(m, phase_cmap(i), 2, scale)

def charset_sheet(i, boss=False, scale=3):
    cs = Charset('x')
    sc = world.boss_scene(i) if boss else world.PHASES[i]()
    scene_map(sc, cs)
    cm = phase_cmap(i)
    n = len(cs.glyphs); cols = 16
    cell_w, cell_h = 4 * 2 * scale, 8 * scale
    im = Image.new('RGB', (cols * (cell_w + 2) + 2, ((n + cols - 1) // cols) * (cell_h + 2) + 2), (30, 30, 46))
    d = ImageDraw.Draw(im)
    bk = A(hw.PHASES[i]['bk'][10])
    for k, g in enumerate(cs.glyphs):
        X = 2 + (k % cols) * (cell_w + 2); Y = 2 + (k // cols) * (cell_h + 2)
        d.rectangle((X, Y, X + cell_w - 1, Y + cell_h - 1), fill=bk)
        for y in range(8):
            v = g[y]
            for x in range(4):
                pv = (v >> (6 - 2 * x)) & 3
                if pv:
                    d.rectangle((X + x * 2 * scale, Y + y * scale, X + (x + 1) * 2 * scale - 1, Y + (y + 1) * scale - 1), fill=A(cm[str(pv)]))
    return im, n

def boss_img(i, scale=4):
    c = world.BOSSES[i]()
    rows = [''.join(r) for r in c.p]
    return render_grid(rows, phase_cmap(i), 2, scale)

# ================================================================= 1 · PORTADA
im, d = page(1, 'ATLAS VISUAL · VERSIÓN ATARI 8 BITS', 'VÓRTICE 6')
t = cap('00_titulo', 960)
frame(im, t, 60, 160)
x = 1060
y = panel(d, x, 160, PW - 60, 880, 'QUÉ ES ESTE ATLAS')
y = wrap(d, x + 16, y, 'Tu diseño de VÓRTICE 6 redibujado con los límites reales del Atari 400/800/XL/XE: '
         'ANTIC 4 (4 colores + fondo por carácter), 128 caracteres por juego, 4 players de 8 píxeles y 4 misiles, '
         'NTSC a 60 Hz.\n\nTodas las imágenes de pantalla son capturas de atari800 ejecutando el visor '
         '(vortice6_visor.xex) y todos los dibujos salen de los mismos datos que usa ese programa. '
         'Lo que ves aquí es lo que se ve en el Atari.', FR, 600)
y += 16
d.text((x + 16, y), 'SE MANTIENE', font=FS, fill=GOLD); y += 32
y = bullets(d, x + 16, y, ['Todos los nombres: VÓRTICE 6, las cinco fases, los cinco jefes y los veinte enemigos.',
                           'Shooter horizontal de 5 fases con jefe, estructura A-B-C-D + jefe y avisos legibles.'], 600, FRs)
y += 10
d.text((x + 16, y), 'SE AJUSTA AL HARDWARE', font=FS, fill=GOLD); y += 32
y = bullets(d, x + 16, y, ['Un solo disparo + cápsula P (2 niveles) + cápsula S (escudo).',
                           '3 enemigos por fase: 2 voladores (PMG) y 1 de decorado (caracteres). El 4.º nombre pasa a variante.',
                           'Jefes de 12 × 10 caracteres, con el scroll parado.'], 600, FRs)
y = panel(d, 60, 900, PW - 60, 1180, 'ÍNDICE')
idx = ['01 Portada', '02 Evaluación del diseño', '03 Reglas del hardware', '04 La nave y el armamento', '05 Bestiario',
       '06 Fase 1 · El Desguace Espacial', '07 Fase 2 · Los Océanos Astrales', '08 Fase 3 · El Fuego Infernal de Hades',
       '09 Fase 4 · El Sarcófago de Saturno', '10 Fase 5 · La Nave Viviente', '11 Galería PMG y marcador', '12 Notas técnicas']
for k, s in enumerate(idx):
    d.text((80 + (k // 4) * 540, y + (k % 4) * 30), s, font=FR, fill=TXT)
pages.append(im)

# ================================================================= 2 · EVALUACIÓN
im, d = page(2, 'DEL DOCUMENTO DE DISEÑO AL ATARI', 'Evaluación: qué cabe, qué cambia y qué sale')
cols = [('SE QUEDA TAL CUAL', (110, 210, 140), [
    'Scroll horizontal fino con HSCROL sobre ANTIC 4.',
    'Nave en player/missile graphics; jefes hechos con caracteres.',
    'Una paleta por fase, cambiada por bandas con DLI.',
    'Carga por fases desde disco en el juego final (48 KB).',
    'Estructura de fase A-B-C-D + jefe con 3 etapas.',
    'La "sintaxis" de avisos: color + sonido + tile + ataque.',
    'Biblioteca de movimientos: RECTO, SENO, ZIGZAG, TURRETA, ARCOS, SEGMENTOS y ZONA.',
    'Los cinco jefes con su punto débil (pulso de PF3).']),
  ('SE ADAPTA', GOLD, [
    'Armas: de 6 módulos (o 5 niveles en la lámina) a 1 disparo + P (cadencia y doble cañón) + S (escudo de 1 impacto).',
    'Enemigos: de 4 por fase a 3 (2 voladores PMG + 1 de decorado). El 4.º nombre queda como variante de color/conducta o como decorado.',
    'Voladores: 8 píxeles de ancho y 1 color, multiplexados en P2/P3 por franjas horizontales.',
    'Nave: 12 × 11 píxeles y 3 colores (P0 y P1 desplazados 4 píxeles, modo OR).',
    'Jefes: 48 × 80 píxeles (12 × 10 caracteres), con el scroll detenido.',
    'Paletas de 8 tonos → 4 colores + fondo por banda; los degradados, con DLI fila a fila.']),
  ('SE QUEDA FUERA', RED, [
    'Las 4 opciones/satélites: no quedan players libres.',
    'El láser a pantalla completa y la onda en arco.',
    'El doble toque de FIRE para elegir mejora (el "plan B" del GDD lo confirma).',
    'Degradados y brillos del arte de concepto dentro de un mismo carácter.',
    'Ataques simultáneos de muchos sprites por línea: máx. 2 voladores por franja.'])]
for k, (h, c, items) in enumerate(cols):
    x0 = 60 + k * 550
    yy = panel(d, x0, 150, x0 + 530, 900, h, c)
    bullets(d, x0 + 16, yy + 4, items, 490, FR, c)
yy = panel(d, 60, 920, PW - 60, 1180, 'CONTRADICCIONES DEL MATERIAL ORIGINAL QUE HE RESUELTO')
bullets(d, 76, yy + 4, [
    'La lámina tiene 5 niveles de disparo y cápsulas P/S/Opción/Rapidez/Bonus; el GDD, una barra de 6 módulos. Me quedo con P + S, más sencillo y legible con un botón.',
    'La lámina tiene 8 enemigos comunes + 1 especial por fase; el GDD, 4 propios por fase. Me quedo con los 20 nombres del GDD, 3 activos por fase.',
    'El GDD pide PAL; tus ports van en NTSC primero. Colores, velocidad y capturas son NTSC (60 Hz). PAL, después.'], PW - 160, FR)
pages.append(im)

# ================================================================= 3 · HARDWARE
im, d = page(3, 'LAS REGLAS ANTES DE DIBUJAR', 'Reglas del hardware de este diseño')
yy = panel(d, 60, 150, 860, 700, 'PANTALLA DE JUEGO (DISPLAY LIST)')
rows = [('24 líneas en blanco', (40, 40, 60), 34), ('Marcador · ANTIC 2 · fuente ROM  (DLI)', (80, 110, 200), 34),
        ('2 líneas en blanco: cambio de juego y colores', (40, 40, 60), 22),
        ('20 filas ANTIC 4 + HSCROL + LMS por fila\n160 líneas · DLI en cada fila:\nfondo, X y color de P2/P3', (150, 90, 40), 210),
        ('2 líneas en blanco: vuelta a la fuente ROM', (40, 40, 60), 22), ('Marcador inferior · ANTIC 2', (80, 110, 200), 34)]
y = yy + 6
for t, c, h in rows:
    d.rectangle((80, y, 840, y + h), fill=c)
    wrap(d, 96, y + 6, t, FRs, 720)
    y += h + 6
yy = panel(d, 880, 150, PW - 60, 700, 'REPARTO DE SPRITES (PMG DE 1 LÍNEA)')
tab = [('P0 + P1', 'VÓRTICE 6: 12 × 11, P1 desplazado 4 cc, modo OR → 3 colores'),
       ('P2, P3', 'voladores, 1 color, multiplexados por franjas con DLI (2 por franja)'),
       ('P2 + P3', 'cápsulas P y S, ojo/bala de jefe: objeto de 3 colores'),
       ('M0, M1', 'disparo de la nave (ancho ×4 = 8 cc); M1 solo con doble cañón'),
       ('M2, M3', 'balas enemigas (color del volador de su franja)'),
       ('PRIOR $21', 'players sobre el campo + OR en parejas')]
y = yy + 4
for a, b in tab:
    d.text((900, y), a, font=FMb, fill=GOLD); y = wrap(d, 1040, y, b, FR, 620) + 10
yy = panel(d, 60, 720, PW - 60, 1180, 'CELDA ANTIC 4 Y COLORES')
y = bullets(d, 76, yy + 4, [
    'Carácter de 4 × 8 píxeles; cada píxel mide 1 color clock (resolución 160). Valores: fondo (COLBK), PF0, PF1, PF2.',
    'Con el bit 7 del código (carácter invertido), PF2 se sustituye por PF3: el quinto color. Una celda no puede mezclar PF2 y PF3; el generador lo comprueba.',
    'Un juego de 128 caracteres por fase y otro por jefe. Uso real: ' + ', '.join('%s %d' % (k.title(), v) for k, v in G['charsets'].items()) + '.',
    'Colores con códigos de la paleta NTSC ($HL: tono H, luminancia L). PF0–PF3 fijos por fase; el fondo cambia fila a fila con DLI (degradados de agua, bandas de lava y de templo).',
    'Pulso de PF3 cada 16 cuadros: ojos de torretas, sellos, perla y pupila "laten" sin coste de CPU.'], PW - 160, FR)
pages.append(im)

# ================================================================= 4 · NAVE Y ARMAS
im, d = page(4, '01 · PROTAGONISTA Y ARSENAL', 'La VÓRTICE 6 y su armamento')
yy = panel(d, 60, 150, 900, 760, 'VÓRTICE 6 · P0 + P1 EN MODO OR')
s1 = on_bg(ship_img(14), (0, 0, 0), 14, True, 2, 14)
im.paste(s1, (80, yy + 6))
x = 80 + s1.width + 30
y = yy + 10
for code, lab in ((hw.SHIP['p0'], 'P0 (solo): motor y aletas'), (hw.SHIP['p1'], 'P1 (solo): casco y morro'),
                  (hw.SHIP['p0'] | hw.SHIP['p1'], 'P0 OR P1: cabina y brillos')):
    swatch(d, x, y, code, lab); y += 52
y += 10
ty = wrap(d, x, y, 'Columnas 0-3: solo P0. Columnas 4-7: los tres colores. Columnas 8-11: solo P1. Dos cuadros (A/B) para la llama del motor.', FRs, 380)
y = max(yy + s1.height + 20, ty + 14)
d.text((80, y), 'ESTADOS', font=FS, fill=GOLD)
sx = 80
for lab, colors in (('NORMAL', hw.SHIP), ('ESCUDO', hw.SHIELD)):
    s = on_bg(ship_img(5, colors), (0, 0, 0), 8)
    im.paste(s, (sx, y + 34)); d.text((sx, y + 40 + s.height), lab, font=FRs, fill=DIM); sx += s.width + 30
b = on_bg(render_grid(S.SHIP_BOOM[0], {'a': 0x3E}, 2, 5), (0, 0, 0), 8); im.paste(b, (sx, y + 34)); d.text((sx, y + 40 + b.height), 'IMPACTO', font=FRs, fill=DIM)
sx += b.width + 20
b = on_bg(render_grid(S.SHIP_BOOM[1], {'a': 0x34}, 2, 5), (0, 0, 0), 8); im.paste(b, (sx, y + 34))
yy = panel(d, 920, 150, PW - 60, 760, 'UN SOLO DISPARO, DOS MEJORAS')
y = yy + 6
def shot_demo(y, double):
    o = Image.new('RGB', (740, 90), (0, 0, 0))
    s = ship_img(4); o.paste(s, (20, 22), s)
    dd = ImageDraw.Draw(o)
    if double:
        for xs in (160, 330, 500):
            dd.rectangle((xs, 22 + 3 * 4, xs + 63, 22 + 3 * 4 + 7), fill=A(hw.SHIP['p0']))
            dd.rectangle((xs, 22 + 7 * 4, xs + 63, 22 + 7 * 4 + 7), fill=A(hw.SHIP['p1']))
    else:
        for xs in (160, 330, 500):
            dd.rectangle((xs, 22 + 5 * 4, xs + 63, 22 + 5 * 4 + 7), fill=A(hw.SHIP['p0']))
    im.paste(o, (940, y))
d.text((940, y), 'Nivel 1 · cañón base (M0)', font=FS, fill=TXT); shot_demo(y + 30, False)
y += 140
d.text((940, y), 'Nivel 2 · cápsula P: doble cañón (M0 + M1) y más cadencia', font=FS, fill=TXT); shot_demo(y + 30, True)
y += 140
for k, (n, (rows, (ca, cb))) in enumerate(S.PAIR.items()):
    g = render_grid(rows, {'a': ca, 'b': cb, 'c': ca | cb}, 2, 6)
    o = on_bg(g, (0, 0, 0), 10); im.paste(o, (940 + k * 400, y))
    wrap(d, 940 + k * 400 + o.width + 14, y + 4, n + ('\n+1 nivel de disparo\n(máx. 2)' if 'P' in n[-1] else '\nescudo: 1 impacto'), FRs, 220)
y += 130
wrap(d, 940, y, 'Al morir se vuelve al nivel 1. Las cápsulas son una pareja P2+P3 (cáscara + letra en OR).', FRs, 760, DIM)
yy = panel(d, 60, 780, PW - 60, 1180, 'POR QUÉ ASÍ')
bullets(d, 76, yy + 4, [
    'Con P0 y P1 en la nave y P2/P3 para los enemigos no quedan players para las opciones/satélites, ni para un láser o una onda. Los misiles son lo único libre: el disparo se hace con ellos y no gasta CPU de dibujo.',
    'La nave en dos players solapados da 12 píxeles de ancho y 3 colores sin perder ningún player más.',
    'Escudo = cambio de colores de P0/P1 (cian y blanco): se ve, no tapa la nave y no cuesta nada.',
    'Con un solo botón no hay selección de mejoras: recoger es activar. Es el "plan B" del propio GDD (riesgo R2).'], PW - 160, FR)
pages.append(im)

# ================================================================= 5 · BESTIARIO
im, d = page(5, '02 · ENEMIGOS', 'Bestiario: 3 por fase (2 voladores PMG + 1 de decorado)')
DECOR = [('REMACHADOR', world.REMACHADOR, 'TURRETA'), ('POLIPO TORRE', world.POLIPO, 'TURRETA'),
         ('INCINERADOR', world.INCINERADOR, 'TURRETA/ZONA'), ('ESCRIBA AUTOMATA', world.ESCRIBA, 'TURRETA'),
         ('ESPINA MOTRIZ', world.ESPINA, 'ZONA')]
MOV = [('ARCOS', 'ZIGZAG'), ('SENO', 'ARCOS'), ('RECTO', 'SENO'), ('RECTO + PARADA', 'ARCOS'), ('PERSIGUE (SENO)', 'ZIGZAG')]
NICE = {'CHATARRIN': 'CHATARRÍN', 'MEDUSA DE VACIO': 'MEDUSA DE VACÍO', 'RAYA FOTONICA': 'RAYA FOTÓNICA', 'SERAFIN NEGRO': 'SERAFÍN NEGRO',
        'ACOLITO ORBITAL': 'ACÓLITO ORBITAL', 'GUARDIAN DE ANILLO': 'GUARDIÁN DE ANILLO', 'GLOBULO CAZADOR': 'GLÓBULO CAZADOR',
        'LARVA MECANICA': 'LARVA MECÁNICA', 'POLIPO TORRE': 'PÓLIPO TORRE', 'ESCRIBA AUTOMATA': 'ESCRIBA AUTÓMATA',
        'GRUA-ARANA': 'GRÚA-ARAÑA', 'MARTIR DE PLASMA': 'MÁRTIR DE PLASMA', 'NODO PARASITO': 'NODO PARÁSITO'}
def nice(n): return NICE.get(n, n)
for i in range(5):
    y0 = 140 + i * 208
    d.rounded_rectangle((60, y0, PW - 60, y0 + 196), 10, fill=PANEL, outline=EDGE, width=2)
    d.rectangle((60, y0, 74, y0 + 196), fill=PHC[i])
    d.text((92, y0 + 12), 'FASE %d' % (i + 1), font=FS, fill=PHC[i])
    wrap(d, 92, y0 + 40, TIT[i], FRs, 200, DIM)
    (n1, c1), (n2, c2), (n4, note) = S.FLY_PHASE[i]
    x = 310
    for n, c, mv in ((n1, c1, MOV[i][0]), (n2, c2, MOV[i][1])):
        fa, fb = S.FLY[n]
        for f in (fa, fb):
            g = on_bg(render_grid(f, {'X': c}, 2, 7), A(hw.PHASES[i]['bk'][8]), 8)
            im.paste(g, (x, y0 + 14)); x += g.width + 8
        d.text((x - 2 * (16 * 7 + 16 + 8), y0 + 104), nice(n), font=FS, fill=TXT)
        d.text((x - 2 * (16 * 7 + 16 + 8), y0 + 130), 'PMG · $%02X · %s' % (c, mv), font=FM, fill=DIM)
        x += 34
    nm, m, mv = DECOR[i]
    g = on_bg(meta_img(m, i, 4), A(hw.PHASES[i]['bk'][16]), 8)
    if g.height > 170: g = g.resize((int(g.width * 170 / g.height), 170), Image.NEAREST)
    im.paste(g, (x, y0 + 12)); xx = x + g.width + 16
    d.text((xx, y0 + 16), nice(nm), font=FS, fill=TXT)
    d.text((xx, y0 + 42), 'caracteres · %s' % mv, font=FM, fill=DIM)
    d.text((xx, y0 + 90), 'VARIANTE: ' + nice(n4), font=FS, fill=GOLD)
    wrap(d, xx, y0 + 116, note.replace('ARANA', 'ARAÑA'), FRs, PW - 80 - xx, DIM)
pages.append(im)

# ================================================================= 6-10 · FASES
REC = [
 ('A · Patio de restos: cascos lejanos, primeras patrullas de RECORTADOR y REMACHADOR en el suelo.\nB · Trituradora orbital: contenedores y tuberías estrechan el paso.\nC · Campo magnético: CHATARRÍN en zigzag entre placas que cruzan.\nD · Dársena central: cápsula final y aviso de FERRUM-9.',
  ['FERRUM-9 · I Recolección: los brazos (mandíbulas) recogen chatarra; dispara al ojo entre recogidas.',
   'II Compactación: las placas superior e inferior se cierran; el hueco cambia de altura.',
   'III Exposición: el ojo turquesa (PF3, pulsa) se abre y lanza 3 balas lentas: ventana de daño.']),
 ('A · Mar sin horizonte: degradado de azules por DLI fila a fila, burbujas y MEDUSAS lejanas.\nB · Jardines de coral: PÓLIPO TORRE dispara si ocupas su carril.\nC · Tormenta gravitacional: las líneas de corriente avisan del empuje (una suma a la velocidad de la nave).\nD · Abismo de marea: el fondo se oscurece y llega THALASSA.',
  ['THALASSA · I Canto: burbujas grandes (pareja P2+P3) a velocidades alternas.',
   'II Corriente: dos chorros contrarios; tres carriles libres.',
   'III Remolino: la concha abre una ventana larga; la perla blanca (PF3) es el punto débil.']),
 ('A · Cenizas exteriores: chispas y bandas de fondo rojo oscuro (DLI).\nB · Hornos gemelos: géiseres de plasma alternan en el suelo.\nC · Garganta de brasas: ASCORIA y SERAFÍN NEGRO entre agujas de roca.\nD · Trono de escoria: INCINERADOR en el suelo y entrada del tríptico.',
  ['EL TRÍPTICO DE HADES · tres rostros apilados, uno por carril.',
   'I Furia (arriba): ráfagas horizontales cortas; después revela su sello.',
   'II Hambre (centro): la boca de horno aspira suavemente.  III Ceniza (abajo): lluvia de brasas por columnas.']),
 ('A · Entrada de los anillos: Saturno lejano y columnas de jade.\nB · Galería de ofrendas: sellos de jade en el suelo; ESCRIBA AUTÓMATA en el friso.\nC · Cámara de las urnas: ACÓLITO ORBITAL se para y dispara; GUARDIÁN DE ANILLO en arco.\nD · Sala del sarcófago: las bandas violetas anuncian a SATURNUS.',
  ['SATURNUS · I Liturgia: los anillos fijan tres posiciones y disparan en simetría.',
   'II Ofrenda: el sarcófago se abre y marca zonas peligrosas.',
   'III Profanación: la máscara se agrieta; los ojos magenta (PF3) son el corazón expuesto.']),
 ('A · Boca de entrada: dientes de hueso y paredes de carne.\nB · Conductos vitales: arterias rojas y ESPINA MOTRIZ que nace del suelo y del techo.\nC · Cámara de memoria: GLÓBULO CAZADOR y LARVA MECÁNICA; pústulas verdes del NODO PARÁSITO.\nD · Ventrículo: el pasillo se abre y solo queda el latido.',
  ['EL CORAZÓN NULO · I Defensa: tres arterias alimentan el blindaje; destrúyelas.',
   'II Mutación: la pupila verde (PF3, late) dispara dos patrones por ciclo.',
   'III Último latido: el reactor queda expuesto con ventanas de daño cada vez más largas.']),
]
for i in range(5):
    p = hw.PHASES[i]
    im, d = page(6 + i, 'FASE %d · ESCENARIO Y JEFE' % (i + 1), TIT[i], PHC[i])
    a = cap('%02d_fase%d' % (2 * i + 1, i + 1), 820); frame(im, a, 60, 150, PHC[i])
    b = cap('%02d_jefe%d' % (2 * i + 2, i + 1), 820); frame(im, b, 874, 150, PHC[i])
    d.text((60, 772), 'Captura de atari800 · scroll fino, 2 voladores por franja, cápsula y disparo', font=FRs, fill=DIM)
    d.text((874, 772), 'Captura de atari800 · %s, scroll parado' % hw.JEFES_DOC[i], font=FRs, fill=DIM)
    yy = panel(d, 60, 805, 600, 1180, 'PALETA NTSC', PHC[i])
    y = yy + 4
    for code, lab in ((p['pf0'], 'PF0 · masa / sombra'), (p['pf1'], 'PF1 · estructura'), (p['pf2'], 'PF2 · luz / borde'),
                      (p['pf3'], 'PF3 · foco (pulsa)'), (p['luz'], 'pulso PF3 / marcador')):
        swatch(d, 80, y, code, lab); y += 44
    bks = sorted(set(p['bk']), key=p['bk'].index)
    d.text((340, yy + 4), 'FONDO POR FILA (DLI)', font=FRs, fill=DIM)
    for k, c in enumerate(bks[:5]): swatch(d, 340, yy + 30 + k * 44, c, 'COLBK')
    cs, n = charset_sheet(i, False, 2)
    cb, nb = charset_sheet(i, True, 2)
    yy = panel(d, 620, 805, 1100, 1180, 'CARACTERES · FASE %d / 128 · JEFE %d / 128' % (n, nb), PHC[i])
    sc = min(1.0, 450 / cs.width)
    cs2 = cs.resize((int(cs.width * sc), int(cs.height * sc)), Image.NEAREST); im.paste(cs2, (636, yy + 4))
    yy2 = yy + 8 + cs2.height
    if yy2 < 1100:
        cb2 = cb.resize((int(cb.width * sc), int(cb.height * sc)), Image.NEAREST)
        cb2 = cb2.crop((0, 0, cb2.width, min(cb2.height, 1170 - yy2)))
        im.paste(cb2, (636, yy2))
    yy = panel(d, 1120, 805, PW - 60, 1180, 'RECORRIDO Y JEFE', PHC[i])
    y = wrap(d, 1136, yy + 2, REC[i][0], FRs, 560)
    y += 6
    bullets(d, 1136, y, REC[i][1], 560, FRs, PHC[i])
    pages.append(im)

# ================================================================= 11 · GALERÍA + JEFES AMPLIADOS
im, d = page(11, 'SPRITES Y JEFES', 'Galería PMG y los cinco jefes en caracteres')
g = cap('11_galeria', 700); frame(im, g, 60, 150)
d.text((60, 682), 'Captura de atari800 · los cuatro players multiplexados por franjas (P0-P3 en cada banda).', font=FRs, fill=DIM)
x = 860
for i in range(5):
    bi = boss_img(i, 3)
    o = on_bg(bi, A(hw.PHASES[i]['bk'][9]), 4)
    xx = 790 + (i % 3) * 300; yy = 150 + (i // 3) * 318
    im.paste(o, (xx, yy))
    d.text((xx, yy + o.height + 6), hw.JEFES_DOC[i], font=FS, fill=PHC[i])
    d.text((xx, yy + o.height + 30), '48 × 80 · 12 × 10 car.', font=FRs, fill=DIM)
yy = panel(d, 60, 800, PW - 60, 1180, 'MARCADOR (HUD)')
y = bullets(d, 76, yy + 4, [
    'Arriba: SCORE · HI · VIDAS (V6×3) · FASE.  Abajo: P (nivel de disparo) · S (escudo) · nombre de la fase o del jefe.',
    'Dos líneas ANTIC 2 con la fuente de la ROM: 40 columnas nítidas que no gastan caracteres del juego de la fase. La fuente de la ROM no tiene tildes: en pantalla, OCEANOS, CORAZON NULO…',
    'Fondo del marcador = tono de la fase con luminancia 2; texto con luminancia 14. Una DLI en la línea en blanco cambia de fuente y de colores sin tirones.',
    'Del HUD de la lámina original se quitan la barra de nivel 1-5 y los iconos de opciones (no existen ya); quedan P y S.'], PW - 160, FR)
pages.append(im)

# ================================================================= 12 · NOTAS TÉCNICAS
im, d = page(12, 'CÓMO ESTÁ HECHO', 'Notas técnicas del visor y siguientes pasos')
yy = panel(d, 60, 150, 860, 760, 'MAPA DE MEMORIA (VISOR)')
mm = [('$0080-$00A1', 'página cero del visor'), ('$2000-$4BFF', '11 juegos de caracteres (5 fases, 5 jefes, logotipo)'),
      ('$4C00-$%s' % G['end'], '%d filas de pantalla únicas + textos (ninguna ventana cruza 4 KB)' % G['rows']),
      ('…-$8F33', 'sprites, láminas, código'), ('$A000-$A7FF', 'PMG de 1 línea (PMBASE $A0)'),
      ('$A800-$AB4F', 'display list, 15 tablas DLI, actores')]
y = yy + 4
for a, b in mm:
    d.text((80, y), a, font=FMb, fill=GOLD); y = wrap(d, 260, y, b, FR, 580) + 8
y = wrap(d, 80, y + 6, 'El visor desconecta el BASIC de los XL/XE (PORTB) para usar $A000-$BFFF como RAM. En un 400/800, sin cartucho de BASIC puesto.', FRs, 760, DIM)
yy = panel(d, 880, 150, PW - 60, 760, 'CÓMO FUNCIONA')
bullets(d, 896, yy + 4, [
    'Escenario de 64 columnas por fila (+48 repetidas): la ventana de ANTIC nunca da la vuelta; la VBI solo suma el desplazamiento grueso a 20 LMS.',
    'HSCROL = 3 − (camx & 3); 1 color clock cada 2 cuadros.',
    'DLI con 15 tablas (una por campo): modo ligero por fila (fondo, X y color de P2/P3) y completo en los cambios de zona (juego de caracteres, PF0-3, los 4 players).',
    'Cada volador conserva su player y su franja; la lógica solo escribe su X en las entradas de esa franja.',
    'ATRACT = 0 en cada VBI: el modo atracción del SO nunca entra.',
    'Generado desde texto (gfx/*.py → tools/gen.py → ca65/ld65), como en el banco de trabajo. Capturas con run8.'], 800, FRs)
yy = panel(d, 60, 780, PW - 60, 1180, 'LO QUE TODAVÍA NO HACE (SIGUIENTE PASO: PROTOTIPO P0/P1 DEL GDD)')
bullets(d, 76, yy + 4, [
    'Es un visor: no hay colisiones, puntuación, oleadas por guion, sonido POKEY ni lógica de jefes. Los voladores cruzan en línea recta para enseñar el multiplexado.',
    'Siguiente paso propuesto: el "primer prototipo" del propio GDD: Desguace con 3 drones, 2 balas, un pasillo, scroll fino y FERRUM-9, midiendo tiempo por cuadro con PROF.',
    'Juego completo: carga de cada fase desde el ATR (charset + mapa largo + jefe ≈ 6-7 KB por fase), como prevé el GDD en su presupuesto de 36 KB.',
    'Formatos del visor: .xex y .atr autoarrancable (223 de 255 sectores). El .car, al final del proyecto, con el resto del paquete.'], PW - 160, FR)
pages.append(im)

pdf = os.path.join(OUT, 'VORTICE_6_Atlas_Atari8bits.pdf')
pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=150)
for k, p in enumerate(pages): p.save(os.path.join(OUT, 'atlas_%02d.png' % (k + 1)))
print('atlas: %d páginas -> %s' % (len(pages), pdf))
