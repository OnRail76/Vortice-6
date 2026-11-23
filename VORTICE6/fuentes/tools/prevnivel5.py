#!/usr/bin/env python3
"""vista previa del nivel 5 con la paleta real y la proporción del Atari (píxel doble de ancho)"""
import sys; sys.path.insert(0, 'gfx')
from PIL import Image
from pal import atari_rgb
import nivel5 as N
L = N.build(); P = N.PAL
rgb = {'1': atari_rgb(P['pf0']), '2': atari_rgb(P['pf1']), '3': atari_rgb(P['pf2']), '4': atari_rgb(0x4E)}
bks = [atari_rgb(v) for v in N.BKGRAD]
tramos = []
for c0 in range(0, 960, 160):
    W = 160 * 4
    im = Image.new('RGB', (W * 2, 160)); px = im.load()
    for y in range(160):
        for x in range(W):
            ch = L.p[y][c0 * 4 + x]
            c = rgb[ch] if ch in rgb else bks[y // 8]
            px[2 * x, y] = c; px[2 * x + 1, y] = c
    tramos.append(im)
S = Image.new('RGB', (tramos[0].width, len(tramos) * 168), (20, 20, 30))
for i, t in enumerate(tramos): S.paste(t, (0, i * 168))
S.save(sys.argv[1])
