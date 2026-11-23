#!/usr/bin/env python3
"""Hoja de propuestas de SATURNUS (fase 4): tres diseños x tres estados, con los colores reales de la fase."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx'), os.path.join(ROOT, 'tools')]
from PIL import Image, ImageDraw, ImageFont
from pal import atari_rgb as A
import corazon as SA, propuestas6 as P6, sprites as S, hw
DJ = '/usr/share/fonts/truetype/dejavu/'
FT = ImageFont.truetype(DJ + 'DejaVuSans-Bold.ttf', 34); FH = ImageFont.truetype(DJ + 'DejaVuSans-Bold.ttf', 22)
FR = ImageFont.truetype(DJ + 'DejaVuSans.ttf', 16); FS = ImageFont.truetype(DJ + 'DejaVuSans.ttf', 14)
BG = (12, 13, 24); GOLD = (220, 170, 255); TXT = (226, 228, 238); DIM = (150, 155, 180)
PAL = dict(pf0=0x32, pf1=0xC6, pf2=0x0C)
CM = {'1': PAL['pf0'], '2': PAL['pf1'], '3': PAL['pf2'], '4': 0x3E}
SC = 3          # 1 línea = 3 px; 1 píxel ANTIC 4 = 6 px de ancho
BOSS_R = 2

def render(p, st):
    cw, ch = 2 * SC, SC
    im = Image.new('RGB', (SA.W * cw + 60 * cw // 2, SA.H * ch + 2 * 8 * ch), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for r in range(18):         # fondo: el degradado de la fase por filas
        d.rectangle((0, r * 8 * ch, im.width, (r + 1) * 8 * ch - 1), fill=A(P6.BKGRAD_F5[r + 1] if r + 1 < 20 else 0))
    ox = 30 * cw // 2 + 30 * cw // 2
    for y, row in enumerate(p):
        for x, c in enumerate(row):
            if c != '.':
                col = CM[c] if not (c == '4' and st == 1) else 0xDA
                d.rectangle((ox + x * cw, (y + 8) * ch, ox + (x + 1) * cw - 1, (y + 9) * ch - 1), fill=A(col))
    # la nave, a escala, delante
    for y, row in enumerate(S.SHIP['A']):
        for x, c in enumerate(row):
            if c in 'abc':
                col = hw.SHIP['p0'] if c == 'a' else hw.SHIP['p1'] if c == 'b' else hw.SHIP['p0'] | hw.SHIP['p1']
                d.rectangle((6 + x * SC, (70 + y) * ch, 6 + (x + 1) * SC - 1, (71 + y) * ch - 1), fill=A(col))
    return im

def cells(p):
    return len({tuple(''.join(p[cy * 8 + y][cx * 4:cx * 4 + 4]) for y in range(8)) for cy in range(16) for cx in range(20)})

def wrap(d, x, y, t, w, f=FR, fill=TXT):
    line = ''
    for wd in t.split():
        if d.textlength(line + ' ' + wd, font=f) > w:
            d.text((x, y), line.strip(), font=f, fill=fill); y += 21; line = ''
        line += ' ' + wd
    d.text((x, y), line.strip(), font=f, fill=fill); return y + 21

tiles = []
for nom, fn, txt in SA.DISENOS:
    row = [render(fn(st), st) for st in range(3)]
    tiles.append((nom, txt, row, max(cells(fn(st)) for st in range(3))))
tw, th = tiles[0][2][0].size
PW = 60 + 3 * (tw + 24) + 40
PH = 150 + len(tiles) * (th + 120)
im = Image.new('RGB', (PW, PH), BG); d = ImageDraw.Draw(im)
d.rectangle((0, 0, PW, 8), fill=GOLD)
d.text((40, 24), 'VÓRTICE 6 · FASE 5 · JEFE FINAL', font=FH, fill=GOLD)
d.text((40, 54), 'EL CORAZÓN NULO · propuestas', font=FT, fill=TXT)
d.text((40, 100), 'Colores de la fase 5 (carne roja, verde enfermizo, hueso) sobre su fondo. 20 x 16 caracteres, como el Tríptico. '
       'Estados: pupila cerrada · latido de aviso · reactor expuesto (vulnerable). Se ajustarán al límite de caracteres al elegir.', font=FS, fill=DIM)
y = 140
for nom, txt, row, nc in tiles:
    d.text((40, y), nom, font=FH, fill=GOLD)
    d.text((40 + d.textlength(nom, font=FH) + 20, y + 5), '%d caracteres distintos (hay que bajar a ~105 al construirlo)' % nc, font=FS, fill=DIM)
    wrap(d, 40, y + 32, txt, PW - 80)
    for k, t in enumerate(row):
        x = 40 + k * (tw + 24)
        im.paste(t, (x, y + 80))
        d.text((x, y + 84 + th), ('pupila cerrada', 'latido (aviso)', 'reactor expuesto: vulnerable')[k], font=FS, fill=DIM)
    y += th + 120
im.save(os.path.join(ROOT, 'build', 'corazon_propuestas.png'))
print(im.size, [t[3] for t in tiles])
