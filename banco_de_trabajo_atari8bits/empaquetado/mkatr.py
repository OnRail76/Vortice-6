#!/usr/bin/env python3
"""ATR autoarrancable sin DOS (del banco: mkpack.py) con salto a la etiqueta start."""
import struct, sys, re
main = open('build/main.bin', 'rb').read()
start = int(re.search(r'al ([0-9A-F]+) \.start\b', open('build/game.lbl').read()).group(1), 16)
LOAD = 0x1FF6
body = bytes([0x4C, start & 255, start >> 8, 0x60])   # $1FFC: JMP start ; $1FFF: RTS (DOSINI)
img = bytearray(6) + body + main
nsec = (len(img) + 127) // 128
assert nsec <= 255, 'ATR: %d sectores (> 255)' % nsec
img[0] = 0; img[1] = nsec; img[2:4] = struct.pack('<H', LOAD); img[4:6] = struct.pack('<H', 0x1FFF)
img += bytes(nsec * 128 - len(img))
disk = img + bytes(720 * 128 - len(img))
par = len(disk) // 16
hdr = struct.pack('<HHHB', 0x0296, par & 0xFFFF, 128, par >> 16) + bytes(9)
open(sys.argv[1], 'wb').write(hdr + disk)
print('atr: %d sectores de arranque (tope 255)' % nsec)
