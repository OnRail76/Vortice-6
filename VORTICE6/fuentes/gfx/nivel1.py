"""VÓRTICE 6 · FASE 1 · EL DESGUACE ESPACIAL · nivel jugable.

960 columnas (4 tramos de 240 + arena de FERRUM-9 al final). Cada píxel lleva además si es sólido:
las estrellas y los cascos lejanos se atraviesan; todo lo demás mata.
"""
import random
from world import (M, TRUSS, PLATE, CONTAINER, HULL, PIPES, REMACHADOR, GRUA, FARHULL)

COLS, ROWS = 960, 20
ARENA = 912          # desde aquí, solo techo y suelo: el scroll se para con la ventana en 912

FLOAT = M('''
.3333333333333..
32222222222222..
3211111111111211
3212121212121211
3211111111111211
32222222222222..
.1111111111111..
................''')
WRECK = M('''
................
................
................
................
................
.........1......
.......2.11.....
..2..1..2121....
...21.121.1.2...
....12211.11.1..
...1212221221...
..1111111111111.
..33333333333333
..21212121212121
..22222222222222
..11111111111111''')
SPIKES = M('''
.3...3...3...3..
.3...3...3...3..
323.323.323.323.
222222222222222.
1111111111111111
2121212121212121
1111111111111111
1111111111111111''')


DEBRIS = M('''
.3333...
32221...
3212211.
.32221..
..111...
........
........
........''')
DEBRIS2 = M('''
..33....
.3221.3.
32221.21
.2121221
..1..11.
........
........
........''')
ANTENNA = M('''
.33.....
.21.....
.21.....
.21.....
.21.....
.21.....
3333....
2222....
.21.....
.21.....
.21.....
.21.....
.21.....
.21.....
.11.....
........
.44.....
4444....
.44.....
........
........
........
........
........''')
PILE = M('''
................
................
................
................
................
................
.......3........
......321.......
....3.2121.3....
...3212211321...
..321212212121..
.32121222121221.
3212122121221211
2121212212121212
1212121121212121
1111111111111111''')
BEACON = M('''
........
........
........
...44...
..4444..
...44...
...11...
..1111..''')
 
BIGWRECK = M('''
........3333333333..............
......33222222222233............
....332211111111112233..........
...322111.1..1..1.111223........
..32211..............11223......
.322111...............1123......
32211..................11223....
3221....................1122333.
3221......................11122.
32211.....................11123.
.3221111111111111111111111111223
..33222222222222222222222222233.
....3333333333333333333333333...
........1..1........1..1........
........1..1........1..1........
................................''')
FARPLANET = M('''
..........111111111.............
.......111111111111111..........
.....1111111111111111111........
....11111111111111111111........
...111111111111111111111........
...11111111111111111111.........
..111111111111111111111.........
..11111111111111111111..........
..1111111111111111111...........
...111111111111111..............
....11111111111.................
................................
................................
................................
................................
................................''')
BEACON = M('''
........
........
........
...44...
..4444..
...44...
...11...
..1111..''')




# montañas de chatarra lejanas (no sólidas), en piezas de 16x16 que se repiten
JUNKA = M('''
................
................
................
.......1........
......111.......
.....11111......
...111111111....
..11111111111...
.1111111111111..
1111111111111111
1111111111111111
1111111111111111
1111111111111111
1111111111111111
1111111111111111
1111111111111111''')
JUNKB = M('''
..1.............
..1.............
..111111111.....
..1.......1.....
..1.......1.....
..1.......1.....
..1.............
.111............
11111.......1...
11111111..11111.
1111111111111111
1111111111111111
1111111111111111
1111111111111111
1111111111111111
1111111111111111''')
JUNKC = M('''
................
................
................
................
................
................
................
................
..........11....
.......1111111..
...111111111111.
1111111111111111
1111111111111111
1111111111111111
1111111111111111
1111111111111111''')




# ---- obstáculos nuevos (v3): angulosos, más grandes y con borde claro para que se vean siempre
GIRDER = M('''
3333333333333333333333333333333333333...
2222222222222222222222222222222222222.3.
1221122112211221122112211221122112213...
.22..22..22..22..22..22..22..22..22.2...
.22..22..22..22..22..22..22..22..22..1..
1221122112211221122112211221122112213...
2222222222222222222222222222222222222.3.
3333333333333333333333333333333333333...''')
ENGINE = M('''
3333333333333333
3222222222222223
3211111111111123
3212222222222123
3211111111111123
3212222222222123
3211111111111123
3222222222222223
3333333333333333
.1222222222222..
.1233333333332..
.123......1.32..
.123..........1.
.12...........2.
.1.............1
................''')
SHARD = M('''
333333333333333333333333
322222222222222222222223
.32121212121212121212123
..3222222222222222222223
...321111111111111111123
....32222222222222222223
.....3211111111111111123
......322222222222222223
.......32121212121212123
........3222222222222223
.........321111111111123
..........32222222222223
...........3333333333333
............1..1..1..1..
................1.....1.
........................''')
MAGPLATE = M('''
333333333333333333333333
322222222222222222222223
321212121212121212121223
322222222222222222222223
321111111111111111111123
321111111111111111111123
322222222222222222222223
333333333333333333333333''')
HULKSEC = M('''
........333333333333333333333...
.......32222222222222222222223..
......3221111111111111111111223.
.....32211.11.11.11.11.11.11123.
....322222222222222222222222223.
...3221212121212121212121212123.
..32222222222222222222222222223.
.3333333333333333333333333333333
..1111111111111111111111111111..
...1..1........1......1....1....
...1..1........1......1....1....
...2..2........2......2....2....
..333.33......333....333..333...
................................
................................
................................''')



# ---- KIT de obstáculos grandes (v4): piezas achaflanadas por celdas 4x8, borde claro (PF2) y anillo óxido
#   máscara por celdas: '#' llena · 'a' esquina cortada arriba-izq · 'b' arriba-der · 'c' abajo-izq · 'd' abajo-der
#   Todo cae en celdas enteras y el relleno se repite por celda, así que cuestan pocos caracteres.
FILLPAT = ['1111', '1111', '1121', '1111', '2222', '1111', '1111', '1111']
def kit(mask):
    H, W = len(mask) * 8, len(mask[0]) * 4
    def inside(x, y):
        if not (0 <= x < W and 0 <= y < H): return False
        k = mask[y // 8][x // 4]; cx, cy = x % 4, y % 8
        if k == '#': return True
        if k == 'a': return 2 * cx + cy >= 7
        if k == 'b': return 2 * (3 - cx) + cy >= 7
        if k == 'c': return 2 * cx + (7 - cy) >= 7
        if k == 'd': return 2 * (3 - cx) + (7 - cy) >= 7
        return False
    out = []
    for y in range(H):
        row = ''
        for x in range(W):
            if not inside(x, y): row += '.'; continue
            n4 = [inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            n8 = n4 + [inside(x + dx, y + dy) for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1))]
            if not all(n4): row += '3'
            elif not all(n8): row += '2'
            else: row += FILLPAT[y % 8][x % 4]
        out.append(row)
    return out

def losa(w, h):            # placa flotante achaflanada
    if h == 1: return kit(['a' + '#' * (w - 2) + 'b'])
    m = ['a' + '#' * (w - 2) + 'b'] + ['#' * w] * (h - 2) + ['c' + '#' * (w - 2) + 'd']
    return kit(m)
def torre(w, h):           # pilar desde el suelo, techo achaflanado
    return kit(['a' + '#' * (w - 2) + 'b'] + ['#' * w] * (h - 1))
def colgante(w, h):        # bloque que cuelga del techo
    return kit(['#' * w] * (h - 1) + ['c' + '#' * (w - 2) + 'd'])
def cuna(w, h, lado='izq'):  # esquirla en cuña: un lado en rampa (una celda por fila)
    m = []
    for r in range(h):
        if lado == 'izq': m.append('.' * (h - 1 - r) + 'a' + '#' * (w - h + r))
        else: m.append('#' * (w - h + r) + 'b' + '.' * (h - 1 - r))
    m.append('c' + '#' * (w - 1) if lado == 'izq' else '#' * (w - 1) + 'd') if False else None
    return kit(m)
def viga(w):               # viga larga de una fila con remate en punta
    return kit(['a' + '#' * (w - 2) + 'b'])

class Level:
    def __init__(s):
        s.w = COLS * 4
        s.p = [['.'] * s.w for _ in range(ROWS * 8)]
        s.solid = [[False] * s.w for _ in range(ROWS * 8)]
        s.turrets = []

    def stamp(s, m, col, row, solid=True, over=True):
        if any('4' in l for l in m):          # una luz (PF3) no puede caer en una celda con PF2
            for y, l in enumerate(m):
                for x, ch in enumerate(l):
                    if ch == '.': continue
                    cy, cx = (row * 8 + y) // 8, (col * 4 + x) // 4
                    for yy in range(cy * 8, cy * 8 + 8):
                        if 0 <= yy < ROWS * 8 and '3' in ''.join(s.p[yy][cx * 4:cx * 4 + 4]): return
        for y, l in enumerate(m):
            for x, ch in enumerate(l):
                if ch == '.': continue
                yy, xx = row * 8 + y, col * 4 + x
                if 0 <= yy < ROWS * 8 and 0 <= xx < s.w:
                    if not over and s.p[yy][xx] != '.': continue
                    s.p[yy][xx] = ch
                    s.solid[yy][xx] = solid

    def stamp_bg(s, m, col, row):
        """fondo no sólido por celdas: solo copia celdas 4x8 enteras sobre celdas vacías"""
        for cy in range(len(m) // 8):
            for cx in range(len(m[0]) // 4):
                R0, C0 = (row + cy) * 8, (col + cx) * 4
                if R0 + 8 > ROWS * 8 or C0 + 4 > s.w: continue
                if any(s.p[R0 + y][C0 + x] != '.' for y in range(8) for x in range(4)): continue
                for y in range(8):
                    for x in range(4):
                        s.p[R0 + y][C0 + x] = m[cy * 8 + y][cx * 4 + x]

    def turret(s, col, row):
        pass                # (las torretas se quitaron: UNIDAD CERO es ahora un mecha volador)


STARP = 24        # el campo de estrellas se repite cada 24 columnas (así el mapa comprime bien)


def build():
    L = Level()
    R = random.Random(1986)
    for c in range(0, COLS, 4):
        L.stamp(TRUSS, c, 0)
        L.stamp(PLATE, c, 18)
    # ---------------- A · PATIO DE RESTOS (0-239): torres, losas y cuñas grandes
    for c in (36, 88, 156, 212): L.stamp(CONTAINER, c, 16)
    L.stamp(CONTAINER, 88, 14)
    L.stamp(BEACON, 89, 13)
    for c, w, h in ((24, 4, 5), (118, 5, 6), (176, 4, 4), (226, 6, 5)): L.stamp(torre(w, h), c, 18 - h)
    for c, w, h in ((50, 6, 3), (140, 8, 4), (196, 5, 3)): L.stamp(colgante(w, h), c, 2)
    for c, r, w, h in ((40, 9, 12, 2), (98, 7, 10, 3), (160, 10, 14, 2), (204, 8, 9, 2)): L.stamp(losa(w, h), c, r)
    for c, r, lado in ((70, 10, 'izq'), (186, 5, 'der')): L.stamp(cuna(8, 3, lado), c, r)
    # ---------------- B · TRITURADORA ORBITAL (240-479): pasillo que se estrecha y se cierra en dientes
    for i, c in enumerate(range(244, 476, 12)):
        top = 3 + (i % 3)
        L.stamp(colgante(6, top - 1), c, 2)
        h = 3 + (i + 1) % 3
        L.stamp(torre(6, h), c + 6, 18 - h)
        L.stamp(BEACON, c + 8, 17 - h)
    # ---------------- C · CAMPO MAGNÉTICO (480-719): losas flotantes grandes, grúas y púas
    plates = [(492, 6), (512, 11), (530, 4), (548, 9), (568, 13), (586, 6), (606, 10), (624, 4), (642, 12),
              (660, 7), (680, 11), (698, 5)]
    for k, (c, r) in enumerate(plates): L.stamp(losa(10 if k % 2 else 8, 2), c, r)
    for c in (500, 560, 620, 680): L.stamp(GRUA, c, 2)
    for c in (530, 590, 650, 710): L.stamp(SPIKES, c, 17)
    # ---------------- D · DÁRSENA CENTRAL (720-911): cascos enormes y vigas
    for c in (760, 820, 880): L.stamp(CONTAINER, c, 16)
    L.stamp(CONTAINER, 820, 14)
    L.stamp(BEACON, 821, 13)
    for c, w, h in ((730, 7, 4), (800, 5, 3), (850, 8, 4)): L.stamp(colgante(w, h), c, 2)
    for c, w, h in ((744, 5, 5), (790, 6, 4), (866, 5, 6)): L.stamp(torre(w, h), c, 18 - h)
    L.stamp(losa(16, 3), 768, 8)
    L.stamp(losa(12, 2), 834, 10)
    for c, r in ((722, 9), (812, 12), (892, 7)): L.stamp(viga(10), c, r)
    L.stamp(cuna(8, 3, 'der'), 896, 11)
    # antenas con luz de aviso colgando del techo, en todo el nivel
    for c in range(10, 900, 38):
        if all(L.p[y][x] == '.' for y in range(16, 140) for x in range(c * 4 - 4, c * 4 + 12)):
            L.stamp(ANTENNA, c, 2)
    # fondo lejano (se atraviesa), por celdas sobre lo vacío: montañas de chatarra y cascos a la deriva
    seq = [JUNKA, JUNKC, JUNKB, JUNKC, JUNKA, JUNKA, JUNKC]
    for i, c in enumerate(range(0, COLS, 4)):
        L.stamp_bg(seq[i % len(seq)], c, 16)
    for c in range(30, 900, 46):
        L.stamp_bg(FARHULL, c, 5 + (c // 7) % 5)
    # estrellas al final, solo en celdas vacías: 4 caracteres-estrella, patrón de 24 columnas
    STARS = [((1, 2), '3'), ((2, 5), '1'), ((0, 6), '1'), ((3, 1), '3')]
    vacio = [[all(L.p[q * 40 + y][c * 4 + x] == '.' for y in range(40) for x in range(4)) for q in range(4)] for c in range(COLS)]
    pat = [(R.randrange(STARP), R.randrange(2, 18), R.randrange(4)) for _ in range(150)]
    for c0 in range(0, COLS, STARP):
        for dc, r, k in pat:
            c = c0 + dc
            if c >= COLS: continue
            q0 = (r // 5) * 40
            if all(L.p[q0 + y][c * 4 + x] == '.' or (y // 8 != (r % 5) and L.p[q0 + y][c * 4 + x] in '13' and vacio[c][r // 5])
                   for y in range(40) for x in range(4)) and vacio[c][r // 5]:
                (sx, sy), ch = STARS[k]
                L.p[r * 8 + sy][c * 4 + sx] = ch
    return L


# degradado de fondo (COLBK por fila de campo): espacio azul arriba, resplandor de chatarra junto al suelo
BKGRAD = [0x00, 0x00, 0x80, 0x80, 0x80, 0x80, 0x82, 0x82, 0x72, 0x72, 0x62, 0x62, 0x52, 0x50, 0x40, 0x40, 0x30, 0x30, 0x00, 0x00]


# oleadas (7.º campo: patrón · D por detrás, B bucle, Q patrulla, C carga, E escalera): (columna de la cámara, tipo, cantidad, franja 0-3, separación en cuadros, cápsula al limpiarla)
#   R = CARROÑERO (antes RECORTADOR: arco, quiebro y regreso)  C = CHATARRÍN (zigzag)  M = UNIDAD CERO (mecha: se para, avisa y dispara apuntando)
#   Franjas: 0 = filas 2-5, 1 = 6-9, 2 = 10-13, 3 = 14-17.  Una oleada alterna entre su franja y la vecina.
WAVES = [
    (8, 'R', 4, 1, 18, '', ''),
    (40, 'R', 4, 2, 18, 'P', ''),
    (62, 'M', 1, 1, 1, '', ''),
    (80, 'C', 3, 1, 30, '', ''),
    (120, 'R', 4, 0, 14, '', 'B'),
    (130, 'M', 2, 2, 50, '', ''),
    (160, 'C', 4, 2, 24, '', ''),
    (190, 'M', 1, 0, 1, '', ''),
    (205, 'R', 4, 1, 18, 'S', ''),
    (250, 'C', 3, 1, 30, '', 'Q'),
    (272, 'M', 2, 0, 50, '', ''),
    (295, 'C', 3, 2, 30, '', ''),
    (330, 'R', 4, 1, 16, '', ''),
    (352, 'M', 1, 2, 1, '', ''),
    (372, 'C', 4, 1, 24, 'P', 'E'),
    (420, 'R', 4, 1, 14, '', ''),
    (442, 'M', 2, 1, 50, '', ''),
    (472, 'C', 3, 1, 28, '', ''),
    (520, 'R', 4, 1, 18, '', 'C'),
    (542, 'M', 1, 0, 1, '', ''),
    (562, 'C', 4, 1, 24, 'S', ''),
    (610, 'R', 4, 1, 14, '', ''),
    (632, 'M', 2, 2, 50, '', ''),
    (662, 'C', 4, 1, 24, '', 'D'),
    (700, 'R', 4, 1, 16, 'P', ''),
    (730, 'M', 1, 2, 1, '', ''),
    (752, 'C', 4, 0, 22, '', ''),
    (778, 'M', 1, 1, 1, '', ''),
    (792, 'R', 4, 2, 14, '', 'B'),
    (832, 'C', 4, 1, 20, 'S', ''),
    (848, 'M', 2, 0, 50, '', ''),
    (870, 'R', 4, 1, 14, '', ''),
    (884, 'M', 1, 2, 1, '', ''),
]
