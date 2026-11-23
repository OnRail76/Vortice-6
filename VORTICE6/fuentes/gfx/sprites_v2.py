"""VÓRTICE 6 · sprites (player/missile graphics).

Nave: P0 en x, P1 en x+4 (modo OR de GTIA).
  'a' = solo P0 (rojo)   'b' = solo P1 (gris)   'c' = P0+P1 (blanco rosado)
  Columnas 0-3 solo 'a'; 4-7 cualquiera; 8-11 solo 'b'.
Voladores: 8 de ancho, 1 color ('X'), dos cuadros.  Miran a la izquierda (llegan por la derecha).
Parejas (cápsulas): 'a' = P2, 'b' = P3, 'c' = los dos.
"""

def g(t):
    r = [l.strip() for l in t.strip('\n').split('\n')]
    return [l.replace(' ', '') for l in r]

# ---------------------------------------------------------------- VÓRTICE 6
SHIP = {   # E3: casco y alas blancos en el solape, motores y bordes naranja (P0), morro plateado (P1)
 'A': g('''
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
.aa.cc......'''),
 'B': g('''
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
.aa.cc......'''),
}
# CHATARRÍN: nave orgánica alienígena, pareja P2 + P3 a +4 (como la nave): 'a' P2, 'b' P3, 'c' núcleo
CHATARRIN = (g('''
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
..aaaa......'''))
CHATARRIN_COL = (0x64, 0x0A)
SHIP_W, SHIP_H = 12, 11
# Explosión de la nave (solo P0, 8x8, se colorea con el color de P0)
SHIP_BOOM = [g('''
...a....
.a.a.a..
..aaa...
aaa.aaa.
..aaa...
.a.a.a..
...a....
........'''), g('''
a..a..a.
.a...a..
...a....
aa.a.aa.
...a....
.a...a..
a..a..a.
........''')]

# ---------------------------------------------------------------- voladores (2 por fase)
FLY = {
 # FASE 1 · DESGUACE
 'RECORTADOR': (g('''
XX....XX
.X...XXX
..XXXXXX
...XX.XX
..XXXXXX
.X...XXX
XX....XX
........'''), g('''
......XX
XX...XXX
.XXXXXXX
...XX.XX
.XXXXXXX
XX...XXX
......XX
........''')),
 'CHATARRIN': (g('''
..XXXXX.
.X.X.X.X
.XXXXXXX
XX.XX.X.
.XXXXXXX
.X.X.X.X
..XXXXX.
........'''), g('''
..XXXXX.
.XX.X.XX
.XXXXXXX
XX.XX.XX
.XXXXXXX
.XX.X.XX
..XXXXX.
........''')),
 # CARROÑERO (antes RECORTADOR): pez cíborg con aleta-cuchilla, ojo-visor y fauces
 'CARROÑERO': (g('''
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
 # REMACHADOR volador (cañón a la izquierda)
 'REMACHADOR': (g('''
....XXXX
...XXXXX
XXXXX..X
XXXXX..X
...XXXXX
...XX.XX
..XXXXXX
.XX...XX'''), g('''
....XXXX
...XXXXX
.XXXX..X
.XXXX..X
...XXXXX
...XX.XX
..XXXXXX
.XX...XX''')),
 # FASE 2 · OCÉANOS
 'MEDUSA DE VACIO': (g('''
..XXXX..
.XXXXXX.
XX.XX.XX
XXXXXXXX
X.X..X.X
.X.XX.X.
.X.X..X.
X..X.X..
...X..X.
..X.....'''), g('''
..XXXX..
.XXXXXX.
XX.XX.XX
XXXXXXXX
X.X..X.X
X.X..X.X
.X..X..X
.X..X.X.
..X..X..
.....X..''')),
 'RAYA FOTONICA': (g('''
.....XX.
...XXXX.
.XXXXXXX
XXX.XXXX
.XXXXXXX
...XXXX.
.....XX.
........'''), g('''
........
...XXX..
.XXXXXXX
XXX.XXXX
.XXXXXXX
...XXX..
........
........''')),
 # FASE 3 · HADES
 'ASCORIA': (g('''
..XXXX..
.XXX.XX.
XXX.XXXX
XX.X.XXX
XXXX.X.X
XXX.XXXX
.XX.XXX.
..XXXX..'''), g('''
..XXXX..
.XX.XXX.
XXXX.XXX
XXX.X.XX
X.X.XXXX
XXXX.XXX
.XXX.XX.
..XXXX..''')),
 'SERAFIN NEGRO': (g('''
......XX
....XXX.
..XXXX..
XXXXXXXX
.XX.XXXX
..XXXX..
....XXX.
......XX'''), g('''
........
.....XXX
..XXXXX.
XXXXXXXX
.XX.XXXX
..XXXXX.
.....XXX
........''')),
 # FASE 4 · SATURNO
 'ACOLITO ORBITAL': (g('''
...XX...
..XXXX..
.XX..XX.
XX.XX.XX
XX.XX.XX
.XX..XX.
..XXXX..
...XX...'''), g('''
...XX...
..XXXX..
.XXXXXX.
XXX..XXX
XXX..XXX
.XXXXXX.
..XXXX..
...XX...''')),
 'GUARDIAN DE ANILLO': (g('''
..XXXXX.
.XXXXXXX
XXX...XX
XX.....X
XX......
XXX.....
.XXX....
..XX....'''), g('''
..XXXXX.
.XX.X.XX
XXX...XX
XX.....X
XX......
XXX.....
.X.X....
..XX....''')),
 # FASE 5 · NAVE VIVIENTE
 'GLOBULO CAZADOR': (g('''
..XXXX..
.XXXXXX.
XXX..XXX
XX....XX
XX....XX
XXX..XXX
.XXXXXX.
..XXXX..'''), g('''
..XXXX..
.XXXXXX.
XXXXXXXX
XXX..XXX
XXX..XXX
XXXXXXXX
.XXXXXX.
..XXXX..''')),
 'LARVA MECANICA': (g('''
.X......
X.XX.XX.
.XXXXXXX
XX.X.X.X
.XXXXXXX
X.XX.XX.
.X......
........'''), g('''
........
XXXX.XX.
.XXXXXXX
.X.X.X.X
.XXXXXXX
XXXX.XX.
........
........''')),
}
# colores de los voladores por fase (P2, P3) y variante (nombre sobrante del GDD)
FLY_PHASE = [
  (('CARROÑERO', 0xAC), ('CHATARRIN', 0x36), ('GRUA-ARANA', 'decorado: gancho colgante del techo')),
  (('MEDUSA DE VACIO', 0xAE), ('RAYA FOTONICA', 0x9A), ('ANGUILA DE MAREA', 'RAYA en cadena de 4 por franjas, color $C8')),
  (('ASCORIA', 0x26), ('SERAFIN NEGRO', 0x06), ('MARTIR DE PLASMA', 'SERAFIN en $48, cruza en línea recta')),
  (('ACOLITO ORBITAL', 0x2C), ('GUARDIAN DE ANILLO', 0xBA), ('VASO VOTIVO', 'ACOLITO en $58, suelta una cápsula al morir')),
  (('GLOBULO CAZADOR', 0x48), ('LARVA MECANICA', 0xEC), ('NODO PARASITO', 'decorado: pústula verde del tendón')),
]

# ---------------------------------------------------------------- objetos de pareja P2+P3
PAIR = {
 'CAPSULA P': (g('''
.aaaaaa.
aaccccaa
aacaacaa
aaccccaa
aacaaaaa
aacaaaaa
.aaaaaa.
........'''), (0x34, 0x0A)),
 'CAPSULA S': (g('''
.aaaaaa.
aaaccaaa
aacaaaaa
aaacaaaa
aaaacaaa
aaccaaaa
.aaaaaa.
........'''), (0x84, 0x0A)),
}
# explosión de enemigo: 3 cuadros, 1 color, el color sube de luminancia
BOOM = [g('''
........
........
...XX...
..XXXX..
..XXXX..
...XX...
........
........'''), g('''
........
..X..X..
.X.XX.X.
..XXXX..
..XXXX..
.X.XX.X.
..X..X..
........'''), g('''
X..X...X
...X.X..
.X.....X
X..X....
.......X
.X...X..
...X..X.
X...X...''')]
BOOM_COL = [0x3E, 0x3A, 0x34]
# bala enemiga (en la galería) y bala de jefe
ORB = g('''
........
..XXX...
.XXXXX..
.XX.XX..
.XXXXX..
..XXX...
........
........''')
