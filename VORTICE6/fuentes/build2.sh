#!/bin/sh
# Vórtice 6 · fase 2 jugable (mismo motor; datos de la fase 2)
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
V6FASE=2 python3 tools/gen1.py
V6FASE=2 python3 tools/musica.py
mkdir -p build
$CC65/ca65 -g -I src -o build/g2.o src/g1.s
$CC65/ld65 -C src/g1.cfg -m build/g2.map -Ln build/game2.lbl -o build/dummy build/g2.o
cp build/game2.lbl build/game.lbl
cp build/main.bin build/f2.bin
python3 tools/mkxex.py build/vortice6_fase2.xex
python3 tools/mkatr.py build/vortice6_fase2.atr
mv build/vortice6_fase2.atr build/vortice6_fase2.atr 2>/dev/null || true
$CC65/ca65 -g -D PRUEBA=1 -I src -o build/g2p.o src/g1.s
$CC65/ld65 -C src/g1.cfg -Ln build/game2p.lbl -o build/dummy build/g2p.o
cp build/game2p.lbl build/game.lbl
python3 tools/mkxex.py build/vortice6_fase2_PRUEBA.xex
cp build/game2.lbl build/game.lbl
# deja los datos de la fase 1 como estaban
python3 tools/gen1.py >/dev/null; python3 tools/musica.py >/dev/null
