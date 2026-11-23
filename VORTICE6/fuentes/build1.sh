#!/bin/sh
# Vórtice 6 · fase 1 jugable: genera datos, ensambla, enlaza y empaqueta
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
python3 tools/gen1.py
V6FASE=1 python3 tools/musica.py
mkdir -p build
$CC65/ca65 -g -I src -o build/g1.o -l build/g1.lst src/g1.s
$CC65/ld65 -C src/g1.cfg -m build/g1.map -Ln build/game1.lbl -o build/dummy build/g1.o
cp build/game1.lbl build/game.lbl
cp build/main.bin build/f1.bin
python3 tools/mkxex.py build/vortice6_fase1.xex
python3 tools/mkatr.py build/vortice6_fase1.atr
# versión de prueba (nave invencible) para las partidas automáticas
$CC65/ca65 -g -D PRUEBA=1 -I src -o build/g1p.o src/g1.s
$CC65/ld65 -C src/g1.cfg -Ln build/game.lbl -o build/dummy build/g1p.o
python3 tools/mkxex.py build/vortice6_fase1_PRUEBA.xex
$CC65/ld65 -C src/g1.cfg -m build/g1.map -Ln build/game.lbl -o build/dummy build/g1.o
