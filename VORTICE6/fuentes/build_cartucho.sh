#!/bin/sh
# Vórtice 6 · cartucho AtariMax 8 Mbit (1 MB) con el juego completo (necesita build_disco.sh antes)
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
$CC65/ca65 -o build/cartldr.o src/cartldr.s
$CC65/ld65 -t none -o build/cartldr.bin build/cartldr.o
python3 tools/mkcart.py build/vortice6.car
