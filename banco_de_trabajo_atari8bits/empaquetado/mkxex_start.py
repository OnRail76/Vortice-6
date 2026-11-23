#!/usr/bin/env python3
"""Empaqueta build/init.bin ($0600, INITAD) y build/main.bin ($2000, RUNAD = etiqueta start) en un .xex"""
import sys, struct, re
init = open('build/init.bin', 'rb').read(); main = open('build/main.bin', 'rb').read()
lbl = open('build/game.lbl').read()
start = int(re.search(r'al ([0-9A-F]+) \.start\b', lbl).group(1), 16)
def seg(addr, data): return struct.pack('<HH', addr, addr + len(data) - 1) + data
x = b'\xff\xff' + seg(0x0600, init) + seg(0x02E2, struct.pack('<H', 0x0600)) + seg(0x2000, main) + seg(0x02E0, struct.pack('<H', start))
open(sys.argv[1], 'wb').write(x)
print('xex: %d bytes, $2000-$%04X, arranque $%04X' % (len(x), 0x2000 + len(main) - 1, start))
