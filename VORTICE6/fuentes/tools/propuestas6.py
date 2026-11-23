#!/usr/bin/env python3
"""Hoja de propuestas de la fase 2: enemigos (2 variantes de 3 enemigos) y maqueta del escenario."""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx')]
from PIL import Image, ImageDraw, ImageFont
from pal import atari_rgb as A
import propuestas6 as P, sprites as S
DJ = '/usr/share/fonts/truetype/dejavu/'
FT = ImageFont.truetype(DJ + 'DejaVuSans-Bold.ttf', 26); FB = ImageFont.truetype(DJ + 'DejaVuSans-Bold.ttf', 18)
FS = ImageFont.truetype(DJ + 'DejaVuSans.ttf', 14)


def norm(rows):
    """columnas 0-3 solo P2, 8-11 solo P3: se corrige el dibujo a lo que el hardware puede mostrar"""
    out = []
    for r in rows:
        s = ''
        for x, ch in enumerate(r.ljust(12, '.')):
            if ch == '.': s += '.'
            elif x < 4: s += 'a'
            elif x > 7: s += 'b'
            else: s += 'c' if ch == 'X' else ch
        out.append(s)
    return out


def draw(rows, cmap, sx, sy):
    w = max(len(r) for r in rows)
    im = Image.new('RGBA', (w * sx, len(rows) * sy), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in cmap: d.rectangle((x * sx, y * sy, (x + 1) * sx - 1, (y + 1) * sy - 1), fill=A(cmap[ch]))
    return im


def boxed(im, pad=8, bg=(0, 0, 0)):
    b = Image.new('RGB', (im.width + 2 * pad, im.height + 2 * pad), bg); b.paste(im, (pad, pad), im); return b


img = Image.new('RGB', (1600, 3200), (14, 15, 26)); d = ImageDraw.Draw(img)
d.text((30, 18), 'FASE 5 · LA NAVE VIVIENTE · enemigos (los 4 del GDD)', font=FT, fill=(120, 220, 255))
d.text((30, 54), 'Mismas reglas que la fase 1: franjas fijas, sin parpadeo. Colores siempre claros: las balas de cada franja usan los colores de su enemigo.', font=FS, fill=(170, 175, 200))
d.text((30, 72), '12 de ancho = dos players desplazados como la nave (tres zonas de color en vertical) · 8 de ancho = superpuestos (3 colores donde quieras) · doble ancho = píxel doble.', font=FS, fill=(170, 175, 200))
SHIPC = {'a': 0x9C, 'b': 0x0E, 'c': 0x9E}
y = 104
for titulo, grupo, nota in (('GLÓBULO CAZADOR', P.GLOBULO, 'persigue despacio una posición pasada de la nave (no corrige cada cuadro)'),
                            ('ESPINA MOTRIZ', P.ESPINA, 'avisa con una burbuja, sale de la pared y se retrae'),
                            ('LARVA MECÁNICA', P.LARVA, 'atraviesa un carril y hace un único cambio de altura'),
                            ('NODO PARÁSITO', P.PARASITO, 'acelera los disparos de los cercanos; destruirlo calma la sala')):
    d.text((30, y), titulo, font=FT, fill=(255, 190, 70)); d.text((330, y + 8), nota, font=FS, fill=(170, 175, 200))
    y += 44
    for name, (k, c, fa, fb) in grupo.items():
        if k == 'N':
            cm = {'X': c}; sx = 1
        elif k.startswith('M8'):
            cm = {'a': c[0], 'b': c[1], 'c': c[0] | c[1]}; sx = 2 if k == 'M8x2' else 1
        else:
            fa, fb = norm(fa), norm(fb)
            cm = {'a': c[0], 'b': c[1], 'c': c[0] | c[1]}; sx = 2 if k == 'M24' else 1
        h = max(len(fa) * 9 + 30, 140)
        d.rounded_rectangle((20, y - 6, 1580, y + h), 8, fill=(26, 28, 46))
        d.text((36, y), name, font=FB, fill=(230, 230, 240))
        col = ('color $%02X' % c) if k == 'N' else ('P2 $%02X · P3 $%02X · solape $%02X' % (c[0], c[1], c[0] | c[1]))
        col += {'N': ' · un player', 'M8': ' · pareja superpuesta', 'M8x2': ' · pareja superpuesta a doble ancho', 'M12': ' · pareja desplazada', 'M24': ' · pareja desplazada a doble ancho'}[k]
        d.text((36, y + 26), col, font=FS, fill=(160, 165, 190))
        x = 560
        for f in (fa, fb):
            b = boxed(draw(f, cm, 9 * sx, 9)); img.paste(b, (x, y)); x += b.width + 14
        # a tamaño de pantalla (x2) junto a la nave, sobre el degradado del agua
        bg = Image.new('RGB', (300, 120), A(0x90)); bd = ImageDraw.Draw(bg)
        for i in range(6): bd.rectangle((0, i * 20, 300, i * 20 + 19), fill=A(P.BKGRAD_F5[6 + i]))
        s = draw(fa, cm, 2 * sx, 2); bg.paste(s, (190, 30), s)
        sh = draw(S.SHIP['A'], SHIPC, 2, 2); bg.paste(sh, (30, 40), sh)
        bd.text((6, 4), 'en pantalla (x2)', font=FS, fill=(220, 220, 240))
        img.paste(bg, (1260, y))
        y += h + 14
    y += 6
img = img.crop((0, 0, 1600, y))
img.save(os.path.join(ROOT, 'docs', 'fase5_enemigos.png')); print(img.size)
