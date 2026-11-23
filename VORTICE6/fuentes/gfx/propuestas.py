"""Propuestas de RECORTADOR (pez cíborg) y CHATARRÍN (cabeza moái de perfil). Miran a la izquierda.

  N   = 1 player, ancho normal (8 color clocks), 1 color  -> caben 2 por franja (como hoy)
  M12 = P2 + P3 desplazado 4 cc, modo OR (como la nave): 12 de ancho, 3 colores -> 1 por franja
        'a' = solo P2 (columnas 0-7), 'b' = solo P3 (columnas 4-11), 'c' = los dos (columnas 4-7)
"""


def g(t):
    return [l.strip() for l in t.strip('\n').split('\n')]


PEZ = {
 'A · pez cíborg (N, 8x7)': ('N', 0x0C, g('''
.XXX....
XXXXX.XX
X.XXXXX.
XXX.XX..
XXXXXXX.
.XXX..XX
........'''), g('''
.XXX....
XXXXX...
X.XXXXXX
XXX.XXX.
XXXXXX..
.XXX.XXX
........''')),
 'B · pez cíborg con aleta-cuchilla y fauces (N, 8x10)': ('N', 0xAC, g('''
...XX...
..XXX...
.XXXXX.X
X.X.XXXX
XXXXXXX.
X...XX..
XXXXXXX.
.XXXXXXX
..XX...X
...X....'''), g('''
...XX...
..XXX...
.XXXXX..
X.X.XXXX
XXXXXXXX
XX..XX..
XXXXXXX.
.XXXXXX.
..XX..XX
...X....''')),
 'C · pez cíborg grande: carne + cola de metal (M12, 12x7, 3 colores)': ('M', (0x36, 0x0A), g('''
..aaaa......
.aaaaaab..bb
a.aaacabbbb.
aaaaaaabbb..
aaaaacabbbb.
.aaaaaab..bb
..aaaa......'''), g('''
..aaaa......
.aaaaaab....
a.aaacabbbbb
aaaaaaabbb..
aaaaacabbbbb
.aaaaaab....
..aaaa......''')),
}

# El moái se dibuja a doble altura (cada fila = 2 líneas): con píxeles anchos y líneas finas,
# solo así la cabeza sale alta y se distinguen ceja, ojo, nariz, labios y oreja. Sigue siendo 1 player.
MOAI = {
 'A · moái de piedra (N, 8x18 líneas)': ('N2', 0x0A, g('''
..XXXXX.
.XXXXXXX
XXXXXXXX
...XXXXX
..XXXX.X
XXXXXX.X
..XXXX.X
.XXXXXXX
..XXXXXX'''), g('''
..XXXXX.
.XXXXXXX
XXXXXXXX
..X.XXXX
..XXXX.X
XXXXXX.X
..XXXX.X
.XXX.XXX
..XXXXXX''')),
 'B · moái de piedra sombreado, ojo que se enciende (M12, 12x16 líneas, 3 colores)': ('M2', (0x0A, 0x04), g('''
.aaaaaab....
ccaaaaabbb..
..a.aaabbb..
.aaaaaabbbb.
caaaaaab.bb.
.aaaaaab.bb.
ccaaaaabbbb.
.aaaaaabbb..'''), g('''
.aaaaaab....
ccaaaaabbb..
..acaaabbb..
.aaaaaabbbb.
caaaaaab.bb.
.aaaaaab.bb.
ccaaaaabbbb.
.aaaaaabbb..''')),
 'C · moái de chatarra: piedra y nuca oxidada (M12, 12x16 líneas, 3 colores)': ('M2', (0x08, 0x34), g('''
.aaaaaab....
aaaaaacbb...
..a.aaabbb..
.aaaaaabbbb.
aaaaaacb.bb.
.aaaaaab.bb.
aaaaaacbbbb.
.aaaaaabbb..'''), g('''
.aaaaaab....
aaaaaacbb...
..acaaabbb..
.aaaaaabbbb.
aaaaaacb.bb.
.aaaaaab.bb.
aaaaaacbbbb.
.aaaaaabbb..''')),
}
