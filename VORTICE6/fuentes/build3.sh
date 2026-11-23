#!/bin/sh
# Vórtice 6 · fase 3 jugable (mismo motor; datos de la fase 2)
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
V6FASE=3 python3 tools/gen1.py
V6FASE=3 python3 tools/musica.py
mkdir -p build
$CC65/ca65 -g -I src -o build/g3.o src/g1.s
$CC65/ld65 -C src/g1.cfg -m build/g3.map -Ln build/game3.lbl -o build/dummy build/g3.o
cp build/game3.lbl build/game.lbl
cp build/main.bin build/f3.bin
python3 tools/mkxex.py build/vortice6_fase3.xex
python3 tools/mkatr.py build/vortice6_fase3.atr
mv build/vortice6_fase3.atr build/vortice6_fase3.atr 2>/dev/null || true
$CC65/ca65 -g -D PRUEBA=1 -I src -o build/g3p.o src/g1.s
$CC65/ld65 -C src/g1.cfg -Ln build/game3p.lbl -o build/dummy build/g3p.o
cp build/game3p.lbl build/game.lbl
python3 tools/mkxex.py build/vortice6_fase3_PRUEBA.xex
cp build/game3.lbl build/game.lbl
# deja los datos de la fase 1 como estaban
python3 tools/gen1.py >/dev/null; python3 tools/musica.py >/dev/null
