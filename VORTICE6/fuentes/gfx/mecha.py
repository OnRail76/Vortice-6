"""UNIDAD CERO · mecha con propulsores y brazo-cañón (diseño propio). Mira a la izquierda.
Pareja P2 + P3 a +4 (como la nave): 'a' = P2 (columnas 0-7), 'b' = P3 (4-11), 'c' = los dos (4-7).
12 x 24 líneas. Enemigo común reutilizable en otras fases: sale de uno en uno.
"""


def g(t):
    return [l.strip() for l in t.strip('\n').split('\n')]


MECHA_A = g('''
......aab...
.....aaabb..
.....accbbb.
.....aaabb..
...aaaaabbbb
..aaaaaabbbb
aaaaaaaabbb.
a.aaaaaabbb.
aaaaaacabbb.
..aaaaccbbbb
.....aaabbbb
.....aaabbb.
.....aaab...
.....aa.bb..
....aa...bb.
....aa...bb.
...aa.....bb
...aa.....bb
..aaa....bbb
..aaa....bbb
............
..a......b..
.a.a....b.b.
............''')
MECHA_B = g('''
......aab...
.....aaabb..
.....acabbb.
.....aaabb..
...aaaaabbbb
..aaaaaabbbb
aaaaaaaabbb.
aaaaaaaabbb.
aaaaaacabbb.
..aaaaccbbbb
.....aaabbbb
.....aaabbb.
.....aaab...
.....aa.bb..
....aa...bb.
....aa...bb.
...aa.....bb
...aa.....bb
..aaa....bbb
..aaa....bbb
..a......b..
.aaa....bbb.
..a......b..
............''')
MECHA_COL = (0x0E, 0x3A)       # v4 más claro: acero blanco + armadura naranja -> zonas solapadas $3E
