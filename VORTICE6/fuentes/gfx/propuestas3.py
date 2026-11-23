"""FASE 2 · LOS OCÉANOS ASTRALES · propuestas de enemigos (Atari 8 bits, mismas reglas que la fase 1).

Enemigos (miran a la izquierda):
  N   = 1 player, 1 color, 8 de ancho (caben 2 por franja)
  M12 = P2 + P3 a +4 -> 12 de ancho, 3 colores: 'a' P2 (col 0-7), 'b' P3 (col 4-11), 'c' los dos (col 4-7, OR)
  M8  = P2 + P3 en la misma x -> 8 de ancho, 3 colores libres: 'a' P2, 'b' P3, 'c' los dos (OR)
  M8x2 = como M8 pero a doble ancho (16 de ancho, píxel doble); necesita SIZEP por franja en la DLI
Truco de color: P3 en gris/blanco (tono 0) -> el solape 'c' es el color de P2 más claro (sin tonos raros).
"""


def g(t):
    return [l.strip() for l in t.strip('\n').split('\n')]


# Regla aprendida en la fase 1: las balas enemigas toman el color de P2/P3 de su franja,
# así que los dos colores tienen que ser claros (luminancia >= $A). P3 blanco/gris claro.
# ------------------------------------------------------------------ MEDUSA DE VACÍO
MEDUSA = {
 'A · campana, 1 color (8x13, 2 por franja)': ('N', 0xAC, g("""
..XXXX..
.XXXXXX.
XX.XX.XX
XXXXXXXX
XXXXXXXX
X.XXXX.X
.X.XX.X.
.X.X..X.
X..X.X..
.X..X.X.
..X.X..X
.X..X.X.
X....X.."""), g("""
..XXXX..
.XXXXXX.
XX.XX.XX
XXXXXXXX
XXXXXXXX
X.XXXX.X
X.X..X.X
.X.X.X..
.X..X.X.
X..X..X.
.X.X.X..
..X..X.X
.X..X...""")),
 'B · campana, 3 colores (8x14)': ('M8', (0xAA, 0x0E), g("""
..cccc..
.caaaac.
caaaaaac
caacacac
aaaaaaaa
aacaacaa
a.a..a.a
.b.bb.b.
.b.b..b.
b..b.b..
.b..b.b.
..b.b..b
.b..b.b.
b....b.."""), g("""
..cccc..
.caaaac.
caaaaaac
cacacaac
aaaaaaaa
aacaacaa
a.a..a.a
b.b..b.b
.b.b.b..
.b..b.b.
b..b..b.
.b.b.b..
..b..b.b
.b..b...""")),
 'C · campana grande (12x15)': ('M12', (0xAA, 0x0C), g("""
....XXXX....
..XXXXXXXX..
.XXXXXXXXXX.
XXXXX..XXXXX
XXXX.XX.XXXX
XXXX.XX.XXXX
XXXXX..XXXXX
.XXXXXXXXXX.
X.X.X..X.X.X
.X.X.X..X.X.
X..X..X.X..X
.X..X.X..X..
X..X..X..X.X
.X..X..X..X.
..X..X..X..."""), g("""
....XXXX....
..XXXXXXXX..
.XXXXXXXXXX.
XXXXX..XXXXX
XXXX.XX.XXXX
XXXX.XX.XXXX
XXXXX..XXXXX
.XXXXXXXXXX.
.X.X.XX.X.X.
X.X..X.X..X.
.X..X..X.X..
X..X..X..X.X
.X..X.X.X..X
X..X..X..X..
.X..X..X..X.""")),
}

# ------------------------------------------------------------------ RAYA FOTÓNICA (vista de arriba, nada hacia la izquierda)
RAYA = {
 'A · manta de alas anchas (12x13)': ('M12', (0x9A, 0x0E), g("""
......XX....
.....XXXX...
....XXXXX...
...XXXXXXX..
.XXXXXXXXXX.
XXX.XXXXXXXX
XXXXXXXXXXXX
XXX.XXXXXXXX
.XXXXXXXXXX.
...XXXXXXX..
....XXXXX...
.....XXXX...
......XX...."""), g("""
............
.......X....
.....XXXX...
...XXXXXXX..
.XXXXXXXXXXX
XXX.XXXXXXXX
XXXXXXXXXXXX
XXX.XXXXXXXX
.XXXXXXXXXXX
...XXXXXXX..
.....XXXX...
.......X....
............""")),
 'B · manta, 3 colores, doble ancho (16x9)': ('M8x2', (0x9A, 0x0E), g("""
....cc..
...caab.
..caaab.
.caaaaab
caacaaab
.caaaaab
..caaab.
...caab.
....cc.."""), g("""
........
....ccb.
..caaab.
.caaaaab
caacaaab
.caaaaab
..caaab.
....ccb.
........""")),
 'C · raya flecha con cola (12x9)': ('M12', (0x6A, 0x0C), g("""
.....XX.....
...XXXXX....
.XXXXXXXX...
XX.XXXXXXXXX
XXXXXXXXXX.X
.XXXXXXXX...
...XXXXX....
.....XX.....
............"""), g("""
............
....XXX.....
.XXXXXXXX...
XX.XXXXXXXXX
XXXXXXXXXX.X
.XXXXXXXX...
....XXX.....
............
............""")),
}

# ------------------------------------------------------------------ ANGUILA DE MAREA (de perfil, cabeza a la izquierda)
ANGUILA = {
 'A · anguila compacta (12x9)': ('M12', (0xCA, 0x0C), g("""
.XXX........
XX.XX.......
XXXXXX....XX
.XXXXXX..XXX
...XXXXXXXX.
....XXXXXX..
......XX....
............
............"""), g("""
............
.XXX........
XX.XX.....XX
XXXXXX...XX.
.XXXXXXXXXX.
...XXXXXXX..
.....XXX....
............
............""")),
 'B · anguila, 3 colores, doble ancho (16x6)': ('M8x2', (0xCA, 0x0E), g("""
.cc.....
c.ca...b
ccaab.bb
.caabbb.
...ab...
........"""), g("""
.cc.....
c.ca....
ccaab..b
.caabbbb
...abb..
........""")),
 'C · anguila larga, doble ancho (24x8)': ('M24', (0xCA, 0x0C), g("""
.XX.........
X.XX......XX
XXXXX....XX.
.XXXXXX.XX..
...XXXXXX...
.....XX.....
............
............"""), g("""
.XX.........
X.XX........
XXXXX......X
.XXXXX....XX
...XXXXXXXX.
.....XXXX...
............
............""")),
}

# ------------------------------------------------------------------ escenario (bloques de 4 x 8, colores 1-4)
# 1 = PF0 azul profundo · 2 = PF1 cian · 3 = PF2 blanco perla (bordes, siempre visibles) · 4 = PF3 corriente (late)
PAL_F2 = dict(pf0=0x94, pf1=0xA8, pf2=0x0E, pf3=0x9C)
BKGRAD_F2 = [0x00, 0x00, 0x80, 0x80, 0x80, 0x90, 0x90, 0x90, 0xA0, 0xA0, 0xA0, 0xA2, 0xB0, 0xB2, 0xC0, 0xC2, 0xC2, 0xC4, 0x00, 0x00]
