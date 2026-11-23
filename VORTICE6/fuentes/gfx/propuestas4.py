"""FASE 3 · EL FUEGO INFERNAL DE HADES · propuestas de enemigos (mismas reglas que la fase 2).
Paleta: negro carbón, carmesí, naranja llama, amarillo caliente. Colores claros (las balas usan los de su franja).
P3 en gris/blanco (tono 0): el solape 'c' es el color de P2 más claro."""


def g(t):
    return [l.strip() for l in t.strip('\n').split('\n')]


# ASCORIA: roca facetada (angulosa, nada de patatas) con grieta viva; se abre y suelta dos fragmentos
ASCORIA = {
 'A · roca facetada, 3 colores (8x8)': ('M8', (0x2A, 0x0C), g("""
..bbbb..
.bbabbb.
bbbcabbb
bbacbabb
bbbacbbb
bbabcabb
.bbbabb.
..bbbb.."""), g("""
..bbbb..
.bbcbbb.
bbacabbb
bbccbcbb
bbbcabbb
bbacccbb
.bbbcbb.
..bbbb..""")),
 'B · roca grande que se abre (8x12, doble ancho)': ('M8x2', (0x2A, 0x0C), g("""
...bbb..
..bbbbb.
.bbbabbb
bbbacbbb
bbbcabbb
bbacabbb
bbbacbbb
.bbbcabb
.bbbbabb
..bbbbb.
...bbb..
........"""), g("""
..bbb...
.bbbb.b.
bbbba.bb
bbbac.bb
bbbca..b
bbac.cbb
bbbc..bb
.bbbc.bb
.bbbbcb.
..bbb.b.
...bb...
........""")),
 'C · roca con lava (12x10)': ('M12', (0x3A, 0x0C), g("""
....XXXX....
..XXXXXXXX..
.XXXccXXXXX.
XXXXXcXXXXXX
XXXXcXcXXXXX
XXXccXXcXXXX
XXXXXcXXXXXX
.XXXXcXXXXX.
..XXXXXXXX..
....XXXX...."""), g("""
....XXXX....
..XXXXXXXX..
.XXXccXXXXX.
XXXXcXcXXXXX
XXXcXXXcXXXX
XXXccXXcXXXX
XXXXcXcXXXXX
.XXXXcXXXXX.
..XXXXXXXX..
....XXXX....""")),
}

# SERAFÍN NEGRO: caza alado de metal quemado; vuelo en S, dispara una vez y se retira
SERAFIN = {
 'A · caza de alas en flecha (12x11)': ('M12', (0x3A, 0x0C), g("""
........XX..
......XXXX..
....XXXXX...
..XXXXXX....
XXXXcXXXXXXX
.XXXXXXXXXX.
XXXXcXXXXXXX
..XXXXXX....
....XXXXX...
......XXXX..
........XX.."""), g("""
............
.......XXX..
....XXXXX...
..XXXXXX....
XXXXcXXXXXXX
.XXXXXXXXXX.
XXXXcXXXXXXX
..XXXXXX....
....XXXXX...
.......XXX..
............""")),
 'B · serafín de 6 alas, 3 colores (16x11, doble ancho)': ('M8x2', (0x3A, 0x0C), g("""
.....bb.
...bbb..
..cbb...
.caabbbb
caaacccb
.caabbbb
..cbb...
...bbb..
.....bb.
....bb..
...bb..."""), g("""
....bbb.
..bbbb..
..cbb...
.caabbbb
caaacccb
.caabbbb
..cbb...
..bbbb..
....bbb.
........
........""")),
 'C · caza pequeño, 1 color (8x9, 2 por franja)': ('N', 0x3C, g("""
.....XX.
...XXX..
.XXXXXXX
XX.XXXX.
.XXXXXXX
...XXX..
.....XX.
........
........"""), g("""
......X.
...XXXX.
.XXXXXXX
XX.XXXX.
.XXXXXXX
...XXXX.
......X.
........
........""")),
}

# MÁRTIR DE PLASMA: figura espectral roja; se materializa, espera y cruza en línea recta
MARTIR = {
 'A · espectro encapuchado, 3 colores (8x16)': ('M8', (0x4A, 0x0E), g("""
..aaaa..
.aaaaaa.
aac..caa
aaaccaaa
.aaaaaa.
..aaaa..
.aaccaa.
aacccca.
aaccccaa
.acccca.
.aaccaa.
.aaaaaa.
a.aaaa.a
.a.aa.a.
a..a..a.
.a..a..a"""), g("""
..aaaa..
.aaaaaa.
aac..caa
aaaccaaa
.aaaaaa.
..aaaa..
.aaccaa.
aacccca.
aaccccaa
.acccca.
.aaccaa.
.aaaaaa.
.a.aa.a.
a..aa..a
.a.a.a..
a...a.a.""")),
 'B · mártir con brazos abiertos (12x16)': ('M12', (0x4A, 0x0E), g("""
....XXXX....
...XXXXXX...
...XcXXcX...
....XXXX....
X....XX....X
XX..XXXX..XX
.XXXXccXXXX.
..XXXccXXX..
....XccX....
....XXXX....
...XXXXXX...
...XXXXXX...
..XX.XX.XX..
..X..XX..X..
.X..X..X..X.
X..X....X..X"""), g("""
....XXXX....
...XXXXXX...
...XcXXcX...
....XXXX....
.X...XX...X.
XX..XXXX..XX
XXXXXccXXXXX
..XXXccXXX..
....XccX....
....XXXX....
...XXXXXX...
...XXXXXX...
..XX.XX.XX..
...X.XX.X...
..X..XX..X..
.X..X..X..X.""")),
 'C · llama con rostro, 1 color (8x14, 2 por franja)': ('N', 0x4C, g("""
...X....
..XX..X.
.XXX.XX.
.XXXXXX.
XX.XX.XX
XXXXXXXX
XX....XX
.XXXXXX.
..XXXX..
.XXXXXX.
X.XXXX.X
..X..X..
.X....X.
X......X"""), g("""
....X...
.X..XX..
.XX.XXX.
.XXXXXX.
XX.XX.XX
XXXXXXXX
XX....XX
.XXXXXX.
..XXXX..
.XXXXXX.
X.XXXX.X
.X.XX.X.
X..X...X
...X....""")),
}
BKGRAD_F3 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x20, 0x20, 0x30, 0x30, 0x30, 0x32, 0x40, 0x40, 0x42, 0x42, 0x44, 0x44, 0x00, 0x00]
