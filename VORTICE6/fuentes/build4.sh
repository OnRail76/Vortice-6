#!/bin/sh
# Vórtice 6 · fase 4 jugable (mismo motor; datos de la fase 4)
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
V6FASE=4 python3 tools/gen1.py
V6FASE=4 python3 tools/musica.py
mkdir -p build
$CC65/ca65 -g -I src -o build/g4.o src/g1.s
$CC65/ld65 -C src/g1.cfg -m build/g4.map -Ln build/game4.lbl -o build/dummy build/g4.o
cp build/game4.lbl build/game.lbl
cp build/main.bin build/f4.bin
python3 tools/mkxex.py build/vortice6_fase4.xex
python3 tools/mkatr.py build/vortice6_fase4.atr
$CC65/ca65 -g -D PRUEBA=1 -I src -o build/g4p.o src/g1.s
$CC65/ld65 -C src/g1.cfg -Ln build/game4p.lbl -o build/dummy build/g4p.o
cp build/game4p.lbl build/game.lbl
python3 tools/mkxex.py build/vortice6_fase4_PRUEBA.xex
cp build/game4.lbl build/game.lbl
# deja los datos de la fase 1 como estaban
python3 tools/gen1.py >/dev/null; python3 tools/musica.py >/dev/null
