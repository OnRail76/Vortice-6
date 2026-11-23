"""Segunda tanda: VÓRTICE 6 al estilo de la carátula y CHATARRÍN como nave alienígena.

Nave (mira a la derecha): P0 en x, P1 en x+4 -> 12 color clocks de ancho.
  'a' = solo P0 (columnas 0-7)  'b' = solo P1 (columnas 4-11)  'c' = los dos (columnas 4-7)
  El blanco del casco y las alas va en el solape ('c'); P0 solo para motores, bordes y cabina; P1 para el morro.
Alienígenas (miran a la izquierda): N = 1 player, 1 color (2 por franja); M12 = P2+P3 a +4 (1 por franja).
"""


def g(t):
    return [l.strip() for l in t.strip('\n').split('\n')]


NAVE_FORMA = (g('''
.aa.cc......
..aacc......
...accc.....
aaaaccccbb..
aa.acca.bbb.
aaaaccccbbbb
aa.acccbbbb.
aaaaccccbb..
...accc.....
..aacc......
.aa.cc......'''), g('''
.aa.cc......
..aacc......
...accc.....
.aaaccccbb..
aaaacca.bbb.
.aaaccccbbbb
aaaacccbbbb.
.aaaccccbb..
...accc.....
..aacc......
.aa.cc......'''))

NAVE = {
 'E1 · blanco con motores y bordes rojos': (0x44, 0x0A),
 'E2 · blanco con cabina, motores y bordes azules (lo más parecido a la carátula)': (0x84, 0x0A),
 'E3 · blanco con acentos naranja (llama caliente)': (0x34, 0x0A),
 'E4 · todo blanco y plata (la silueta clara de la carátula, sin acento de color)': (0x0C, 0x0A),
}

ALIEN = {
 'A · garra insectoide (N, 8x7)': ('N', 0x5A, g('''
XX......
.XX.XXX.
..XXXXXX
.XX.X.XX
..XXXXXX
.XX.XXX.
XX......'''), g('''
........
XXX.XXX.
..XXXXXX
.XX.X.XX
..XXXXXX
XXX.XXX.
........''')),
 'B · dardo alienígena con aletas (N, 8x7)': ('N', 0xC8, g('''
......XX
....XXX.
..XXXX.X
XXX.XXXX
..XXXX.X
....XXX.
......XX'''), g('''
.....XX.
....XXXX
..XXXX..
XXX.XXXX
..XXXX..
....XXXX
.....XX.''')),
 'C · nave orgánica con núcleo que late (M12, 12x7, 3 colores)': ('M', (0x64, 0x0A), g('''
..aaaa......
.aaaaaab..b.
aaa.cc.bbbb.
aaaaccccbbbb
aaa.cc.bbbb.
.aaaaaab..b.
..aaaa......'''), g('''
..aaaa......
.aaaaaab.b..
aaa.aa.bbbbb
aaaacaacbbb.
aaa.aa.bbbbb
.aaaaaab.b..
..aaaa......''')),
}
