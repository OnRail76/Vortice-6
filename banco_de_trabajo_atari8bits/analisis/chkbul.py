#!/usr/bin/env python3
"""Visibilidad de las balas enemigas: en cada captura, busca píxeles de bala donde dice la memoria."""
import re, glob, sys
lbl = {m.group(2): int(m.group(1), 16) for m in re.finditer(r'al ([0-9A-F]+) \.(\w+)', open('build/game.lbl').read())}
def z(b, n, k=0): return b[lbl[n] - 0x80 + k]
tot = vis = 0; miss = []
for zf in sorted(glob.glob(sys.argv[1] + '/z*.bin')):
    b = open(zf, 'rb').read(); fr = zf[-9:-4]
    raw = open(sys.argv[1] + '/f%s.raw' % fr, 'rb').read()
    for k in ('e0', 'e1'):
        x, y = z(b, k + 'x'), z(b, k + 'y')
        if not x: continue
        tot += 1
        # la imagen va un cuadro por detrás de la lógica: ventana amplia
        found = False
        for yy in range(y - 6, y + 9):
            r = yy - 8
            if not 0 <= r < 240: continue
            for xx in range(x - 4, x + 14):
                px = 2 * xx - 64
                if 0 <= px < 384 and raw[r * 384 + px] != 0:
                    c = raw[r * 384 + px]
                    if (c & 15) >= 10: found = True
        vis += found
        if not found: miss.append((fr, k, x, y))
print('balas activas en capturas: %d · visibles: %d' % (tot, vis))
for m in miss[:10]: print('  no vista:', m)
