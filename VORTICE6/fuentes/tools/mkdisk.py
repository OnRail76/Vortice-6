#!/usr/bin/env python3
"""Disco de doble densidad (ATR, 720 sectores de 256 bytes) con arranque propio y los 7 programas:
0 intro · 1-5 fases · 6 final. Cada programa se carga desde $2000 y salta a su etiqueta start."""
import struct, re, sys
progs = [('build/cine1.bin', 'build/cine1.lbl')] + [('build/f%d.bin' % f, 'build/game%d.lbl' % f) for f in range(1, 6)] + \
        [('build/cine2.bin', 'build/cine2.lbl')]
boot = bytearray(open('build/boot.bin', 'rb').read())
assert len(boot) == 384
PTAB = 0x0809 - 0x0700
sectors = {}
nxt = 4
for i, (b, l) in enumerate(progs):
    data = open(b, 'rb').read()
    start = int(re.search(r'al ([0-9A-F]+) \.start\b', open(l).read()).group(1), 16)
    n = (len(data) + 255) // 256
    data += bytes(n * 256 - len(data))
    for k in range(n): sectors[nxt + k] = data[k * 256:(k + 1) * 256]
    boot[PTAB + 6 * i:PTAB + 6 * i + 6] = struct.pack('<HHH', nxt, n, start)
    print('programa %d: %-18s sectores %3d-%3d (%d) arranque $%04X' % (i, b, nxt, nxt + n - 1, n, start))
    nxt += n
assert nxt <= 721, 'no cabe: %d sectores' % nxt
img = bytes(boot)
for s in range(4, 721): img += sectors.get(s, bytes(256))
par = len(img) // 16
hdr = struct.pack('<HHHB', 0x0296, par & 0xFFFF, 256, par >> 16) + bytes(9)
open(sys.argv[1], 'wb').write(hdr + img)
print('disco: %d de 717 sectores de datos usados' % (nxt - 4))
