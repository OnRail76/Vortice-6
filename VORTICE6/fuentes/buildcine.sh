#!/bin/sh
# Vórtice 6 · programas de intro (1) y final (2)
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
mkdir -p build/cine
for C in 1 2; do
  V6CINE=$C python3 tools/gencine.py
  T=$( [ $C = 1 ] && echo intro || echo final )
  V6TEMAS=$T python3 tools/musica.py >/dev/null
  cp src/musdata.s build/cine/musdata.s
  $CC65/ca65 -g -D CINE=$C -I build/cine -I src -o build/cine$C.o src/cine.s
  CFG=src/cine.cfg; [ $C = 1 ] && CFG=src/cine1.cfg
  $CC65/ld65 -C $CFG -m build/cine$C.map -Ln build/cine$C.lbl -o build/dummy build/cine$C.o
  cp build/cine$C.lbl build/game.lbl
  python3 tools/mkxex.py build/vortice6_$T.xex
  cp build/main.bin build/cine$C.bin
done
python3 tools/musica.py >/dev/null
