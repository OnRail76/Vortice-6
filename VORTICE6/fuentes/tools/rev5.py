#!/usr/bin/env python3
"""FASE 5 · revisión: paleta sin verdes, escenario orgánico (venas, arterias, ojo), enemigos nuevos y jefe recoloreado."""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx'), os.path.join(ROOT, 'tools')]
from PIL import Image, ImageDraw, ImageFont
from pal import atari_rgb as A
import venas as V, mecha, propuestas5 as P5, propuestas6 as P6, corazon, hw, sprites as S
DJ = '/usr/share/fonts/truetype/dejavu/'
FT = ImageFont.truetype(DJ + 'DejaVuSans-Bold.ttf', 30); FB = ImageFont.truetype(DJ + 'DejaVuSans-Bold.ttf', 20)
FR = ImageFont.truetype(DJ + 'DejaVuSans.ttf', 15); FM = ImageFont.truetype(DJ + 'DejaVuSansMono-Bold.ttf', 13)
BG = (14, 14, 22); TX = (232, 232, 242); DIM = (165, 168, 190); ORO = (255, 200, 90)
NEW = dict(bk=[0x00] * 20,
           pf0=0x42, pf1=0x46, pf2=0x0C, pf3=0x4E)
OLD = dict(pf0=0x32, pf1=0xC6, pf2=0x0C, pf3=0x3A)

# ---------------- escenario de muestra (200 columnas)
COLS = 200
P = [['.'] * (COLS * 4) for _ in range(160)]
def put(rows, c, r, solid_only=False):
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            yy, xx = r * 8 + y, c * 4 + x
            if ch != '.' and 0 <= yy < 160 and 0 <= xx < COLS * 4: P[yy][xx] = ch
techo = ['1111111111111111', '1121111111112111', '1111111111111111', '3333333333333333']
for c in range(0, COLS, 4):
    put(techo + ['.' * 16] * 12, c, 0)
    put(['.' * 16] * 12 + techo[::-1], c, 16)
for c, a in ((0, 4), (36, 6), (116, 3), (150, 5)): put(V.tejido(V.monte(5, a), 18 - a), c, 18 - a)
for c, a in ((14, 3), (64, 6), (130, 4), (180, 3)): put(V.tejido(V.monte(4, a), 2, techo=True), c, 2)
put(V.ojo3(), 68, 3)                # ojo en la masa del techo
put(V.ojo3(), 40, 12)               # ojo en la masa del suelo
put(V.arteria3(18), 92, 8)
put(V.arteria3(12), 168, 10)
# pared respirante (PF3) de muestra
for y in range(56, 128):
    for x in range(8):
        if (x + y // 2) % 3: P[y][140 * 4 + x] = '4'

def render(pal, scale=2, c0=0, n=COLS):
    im = Image.new('RGB', (n * 4 * scale * 2, 160 * scale)); px = im.load()
    cm = {'1': A(pal['pf0']), '2': A(pal['pf1']), '3': A(pal['pf2']), '4': A(pal['pf3'])}
    bks = [A(v) for v in NEW['bk']]
    for y in range(160):
        for x in range(n * 4):
            c = cm.get(P[y][c0 * 4 + x], bks[y // 8])
            for dy in range(scale):
                for dx in range(2 * scale): px[x * 2 * scale + dx, y * scale + dy] = c
    return im

def sprite(rows, cm, sx=3, sy=3):
    w = max(len(r) for r in rows)
    im = Image.new('RGB', (w * sx + 16, len(rows) * sy + 16), (0, 0, 0)); d = ImageDraw.Draw(im)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in cm: d.rectangle((8 + x * sx, 8 + y * sy, 8 + (x + 1) * sx - 1, 8 + (y + 1) * sy - 1), fill=A(cm[ch]))
    return im

def norm(rows):
    out = []
    for r in rows:
        s = ''
        for x, ch in enumerate(r.ljust(12, '.')):
            s += '.' if ch == '.' else ('a' if x < 4 else 'b' if x > 7 else ('c' if ch == 'X' else ch))
        out.append(s)
    return out

def cmap(c): return {'a': c[0], 'b': c[1], 'c': c[0] | c[1]}

lvl1 = render(NEW, 2, 0, 100); lvl2 = render(NEW, 2, 100, 100)
lvl = Image.new('RGB', (lvl1.width, lvl1.height * 2 + 16), BG); lvl.paste(lvl1, (0, 0)); lvl.paste(lvl2, (0, lvl1.height + 16))
W = max(lvl.width + 80, 1700)
im = Image.new('RGB', (W, 2240), BG); d = ImageDraw.Draw(im)
d.text((40, 24), 'VÓRTICE 6 · FASE 5 · LA NAVE VIVIENTE · revisión', font=FT, fill=TX)
d.text((40, 66), 'Sin verdes · escenario orgánico (venas, arterias y ojos) · fuera NODO PARÁSITO y ESPINA · vuelven la UNIDAD CERO y los ESCRIBAS', font=FR, fill=DIM)
y = 110
d.text((40, y), '1 · PALETA (sin verdes: todo sangre, carne y hueso)', font=FB, fill=ORO); y += 34
for lab, pal in (('ahora', OLD), ('propuesta', NEW)):
    d.text((40, y + 12), lab, font=FR, fill=TX)
    for i, (k, nom) in enumerate((('pf0', 'carne'), ('pf1', 'cartílago → vena'), ('pf2', 'hueso / blanco del ojo'), ('pf3', 'músculo / latido'))):
        x = 180 + i * 300
        d.rectangle((x, y, x + 110, y + 44), fill=A(pal[k])); d.text((x + 120, y + 4), '%s $%02X' % (k.upper(), pal[k]), font=FM, fill=TX)
        d.text((x + 120, y + 22), nom, font=FR, fill=DIM)
    y += 60
y += 10
d.text((40, y), '2 · ESCENARIO ORGÁNICO: la enredadera de la fase 2 hecha venas que crecen del techo y del suelo y acaban en ojillos; ARTERIAS gruesas que cruzan;', font=FB, fill=ORO); y += 28
d.text((40, y), '    y OJOS grandes incrustados en la carne (blanco de hueso, iris rojo, pupila negra con brillo). A la derecha, una pared respirante (músculo).', font=FB, fill=ORO); y += 40
im.paste(lvl, (40, y)); y += lvl.height + 30
# ---------------- enemigos
d.text((40, y), '3 · ENEMIGOS DE LA FASE 5 (sin verdes; colores claros para que sus balas se vean)', font=FB, fill=ORO); y += 40
glo = P6.GLOBULO['B · glóbulo de membrana dentada (12x11)']
lar = P6.LARVA['A · dron segmentado con mandíbulas (12x8)']
esc = P5.ESCRIBA['B · escriba con tablilla (12x14)']
fichas = [('GLÓBULO (se queda)', norm(glo[2]), (0x4A, 0x0E), 'rojo sangre y blanco; persigue'),
          ('LARVA (se queda)', norm(lar[2]), (0x3C, 0x0E), 'era verde: ahora hueso salmón'),
          ('UNIDAD CERO · A', norm(mecha.MECHA_A), (0x4A, 0x0C), 'carne roja y acero gris'),
          ('UNIDAD CERO · B', norm(mecha.MECHA_A), (0x0E, 0x5A), 'hueso blanco y magenta'),
          ('UNIDAD CERO · C', norm(mecha.MECHA_A), (0x3E, 0x4A), 'crema y rojo (más «carne»)'),
          ('ESCRIBA · A', norm(esc[2]), (0x4C, 0x0E), 'rosa sangre y blanco'),
          ('ESCRIBA · B', norm(esc[2]), (0x0C, 0x5C), 'hueso y magenta (fantasma)')]
x = 40
for nom, rows, col, nota in fichas:
    sp = sprite(rows, cmap(col), 6, 3)
    im.paste(sp, (x, y + 26)); d.text((x, y), nom, font=FR, fill=TX)
    d.text((x, y + 34 + sp.height), nota, font=FR, fill=DIM); d.text((x, y + 54 + sp.height), '$%02X / $%02X' % col, font=FM, fill=DIM)
    x += max(sp.width, 200) + 30
y += 230
# ---------------- jefe recoloreado
d.text((40, y), '4 · EL CORAZÓN NULO con la paleta nueva: el globo deja de ser verde y el ojo se lee como ojo (blanco de hueso, iris de carne, reactor rosa-blanco)', font=FB, fill=ORO); y += 40
for st in range(3):
    p = corazon.valvula(st)
    cm = {'1': NEW['pf0'], '2': NEW['pf1'], '3': NEW['pf2'], '4': 0x0E if st == 2 else 0x4E}
    # el globo del ojo (antes verde, PF1) pasa a blanco de hueso
    sp = Image.new('RGB', (80 * 6 + 20, 128 * 3 + 20), (0, 0, 0)); dd = ImageDraw.Draw(sp)
    for yy, row in enumerate(p):
        for xx, ch in enumerate(row):
            if ch in cm: dd.rectangle((10 + xx * 6, 10 + yy * 3, 10 + xx * 6 + 5, 10 + yy * 3 + 2), fill=A(cm[ch]))
    im.paste(sp, (40 + st * (sp.width + 30), y))
    d.text((40 + st * (sp.width + 30), y + sp.height + 6), ('válvula cerrada', 'latido (aviso)', 'reactor expuesto')[st], font=FR, fill=DIM)
y += 128 * 3 + 70
im = im.crop((0, 0, W, y))
im.save(os.path.join(ROOT, 'build', 'fase5_revision.png'))
print(im.size)
