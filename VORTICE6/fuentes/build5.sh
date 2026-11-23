#!/bin/sh
# Vórtice 6 · fase 5 jugable (mismo motor; datos de la fase 4)
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
V6FASE=5 python3 tools/gen1.py
V6FASE=5 python3 tools/musica.py
mkdir -p build
$CC65/ca65 -g -I src -o build/g5.o src/g1.s
$CC65/ld65 -C src/g1.cfg -m build/g5.map -Ln build/game5.lbl -o build/dummy build/g5.o
cp build/game5.lbl build/game.lbl
cp build/main.bin build/f5.bin
python3 tools/mkxex.py build/vortice6_fase5.xex
python3 tools/mkatr.py build/vortice6_fase5.atr
$CC65/ca65 -g -D PRUEBA=1 -I src -o build/g5p.o src/g1.s
$CC65/ld65 -C src/g1.cfg -Ln build/game5p.lbl -o build/dummy build/g5p.o
cp build/game5p.lbl build/game.lbl
python3 tools/mkxex.py build/vortice6_fase5_PRUEBA.xex
cp build/game5.lbl build/game.lbl
# deja los datos de la fase 1 como estaban
python3 tools/gen1.py >/dev/null; python3 tools/musica.py >/dev/null
