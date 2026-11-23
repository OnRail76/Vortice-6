#!/usr/bin/env python3
"""Atlas final: los sprites tal y como los monta el juego (forma y colores), en PNG ampliado."""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx')]
from PIL import Image
from pal import atari_rgb
import sprites as S, mecha, hw, propuestas3 as P3, propuestas4 as P4, propuestas5 as P5, propuestas6 as P6
OUT = sys.argv[1]
SX, SY = 6, 4                      # un color clock = 6 px, una línea = 4 px (proporción NTSC)
def render(rows, c2, c3, dbl=False, single=False):
    w = max(len(r) for r in rows) * (2 if dbl else 1)
    h = len(rows)
    im = Image.new('RGBA', (w * SX, h * SY), (0, 0, 0, 0))
    px = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == '.': continue
            if single or ch in 'aX': col = c2
            elif ch == 'b': col = c3
            else: col = c2 | c3
            rgb = atari_rgb(col) + (255,)
            for xx in range((2 if dbl else 1) * SX):
                for yy in range(SY):
                    px[(x * (2 if dbl else 1)) * SX + xx, y * SY + yy] = rgb
    return im
def norm12(rows):
    out = []
    for r in rows:
        q = ''
        for x, ch in enumerate(r.ljust(12, '.')):
            q += '.' if ch == '.' else ('a' if x < 4 else 'b' if x > 7 else ('c' if ch == 'X' else ch))
        out.append(q)
    return out
def g(d, k): return d[[n for n in d if n.startswith(k)][0]]
items = {
    'nave': render(S.SHIP['A'], hw.SHIP['p0'], hw.SHIP['p1']),
    'nave_escudo': render(S.SHIP['A'], hw.SHIELD['p0'], hw.SHIELD['p1']),
    'capsula_p': render(S.PAIR['CAPSULA P'][0], 0x38, 0x0E),
    'capsula_s': render(S.PAIR['CAPSULA S'][0], 0x88, 0x0E),
    'carronero': render(S.FLY['CARROÑERO'][0], 0xAC, 0xAC, single=True),
    'chatarrin': render(S.CHATARRIN[0], *S.CHATARRIN_COL),
    'unidad_cero': render(mecha.MECHA_A, *mecha.MECHA_COL),
    'unidad_cero_f5': render(mecha.MECHA_A, 0x4A, 0x0C),
}
med = g(P3.MEDUSA, 'B'); ray = g(P3.RAYA, 'B'); ang = g(P3.ANGUILA, 'C')
items['medusa'] = render(med[2], *med[1]); items['raya'] = render(ray[2], *ray[1], dbl=True)
items['anguila'] = render(norm12(ang[2]), *ang[1], dbl=True)
asc = g(P4.ASCORIA, 'A'); ser = g(P4.SERAFIN, 'A'); mar = g(P4.MARTIR, 'A')
items['ascoria'] = render(asc[2], *asc[1]); items['serafin'] = render(norm12(ser[2]), *ser[1]); items['martir'] = render(mar[2], *mar[1])
aco = g(P5.ACOLITO, 'B'); gua = g(P5.GUARDIAN, 'A'); vas = g(P5.VASO, 'A'); esc = g(P5.ESCRIBA, 'B')
items['acolito'] = render(aco[2], *aco[1], dbl=True); items['guardian'] = render(norm12(gua[2]), *gua[1])
items['vaso'] = render(vas[2], *vas[1]); items['escriba'] = render(norm12(esc[2]), *esc[1])
glo = g(P6.GLOBULO, 'B'); lar = g(P6.LARVA, 'A')
items['globulo'] = render(norm12(glo[2]), 0x4A, 0x0E); items['larva'] = render(norm12(lar[2]), 0x3C, 0x0E)
items['escriba_f5'] = render(norm12(esc[2]), 0x0C, 0x5C)
for k, im in items.items():
    im.save(os.path.join(OUT, 'spr_%s.png' % k))
print(len(items), 'sprites')
