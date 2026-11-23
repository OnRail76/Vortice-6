#!/bin/sh
# Vórtice 6 · juego completo: disco (doble densidad) y cartucho (AtariMax 8 Mbit), con intro, 5 fases y final
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
for F in 2 3 4 5 1; do sh build$F.sh; done
sh buildcine.sh
$CC65/ca65 -o build/boot.o src/boot.s
$CC65/ld65 -t none -o build/boot.bin build/boot.o
python3 tools/mkdisk.py build/vortice6_disco.atr
sh build_cartucho.sh
