"""VÓRTICE 6 · FASE 3 · EL FUEGO INFERNAL DE HADES · nivel jugable.

960 columnas: A Cenizas exteriores · B Hornos gemelos · C Garganta de brasas · D Trono de escoria · arena desde la 912.
Colores: 1 = PF0 basalto rojo oscuro · 2 = PF1 lava naranja · 3 = PF2 amarillo caliente (bordes: siempre visibles)
         4 = PF3 GÉISER: el motor cambia su color al ritmo de las erupciones (brasa -> aviso amarillo -> fuego blanco)
Los géiseres no son sólidos en el mapa: matan solo cuando están en erupción (lo comprueba el motor con GEYSERS).
"""
import random
from world import M
from nivel1 import Level, kit as _kit, STARP
import nivel1

COLS, ROWS = 960, 20
ARENA = 912

FILL_ROCA = ['1111', '1121', '1111', '2111', '1111', '1112', '1111', '1211']
FILL_CENIZA = ['1111', '1111', '1211', '1111', '1111', '1111', '1112', '1111']


def kit(mask, fill):
    old = nivel1.FILLPAT
    nivel1.FILLPAT = fill
    try:
        return _kit(mask)
    finally:
        nivel1.FILLPAT = old


def columna(w, h):          # columna de basalto desde el suelo, remate achaflanado
    return kit(['a' + '#' * (w - 2) + 'b'] + ['#' * w] * (h - 1), FILL_ROCA)


def estalactita(w, h):      # basalto que cuelga del techo, se estrecha en dos escalones
    m = ['#' * w] * max(1, h - 2) + ['c' + '#' * (w - 2) + 'd', '.' + 'c' + '#' * max(0, w - 4) + 'd' + '.']
    return kit(m[:h], FILL_ROCA)


def losa(w, h):             # placa de escoria flotante
    m = ['a' + '#' * (w - 2) + 'b'] + ['#' * w] * (h - 2) + ['c' + '#' * (w - 2) + 'd']
    return kit(m, FILL_CENIZA)


# techo: roca volcánica dentada · suelo: costra con lava
TECHO = M('''
1111111111111111
1211111112111111
1111211111111211
3111111311111131
.311113.311113..
..3113...3113...
...33.....33....
................''' + '\n' + '\n'.join(['................'] * 8))
SUELO = M('''
................
................
................
................
......3....3....
.....313..313...
....31113311113.
3333111111111133
2222222222222222
2122222122222222
2222212222221222
2222222222222222
1111111111111111
1211112111121111
1111111111111111
1111111111111111''')

# boquilla del géiser (sólida, en el suelo o en el techo) y columna de fuego (PF3, no sólida)
BOQUILLA = M('''
........
.33..33.
.31331.3
3111111.
31111113
11111111
11111111
11111111''')
FUEGO = ['4..44..4', '.4.44.4.', '..4444..', '.444.44.', '44..4.44', '.44.444.', '4.444..4', '.44.4.4.']

# estatua demoníaca de fondo (no sólida, PF0 tramado): torso con cuernos
def estatua():
    s = ['......1.........1......',
         '.....11.........11.....',
         '....11...11111...11....',
         '....1...1111111...1....',
         '.......111.1.111.......',
         '.......1111111111......',
         '........1111111........',
         '.....111111111111111...',
         '...1111.111111111.1111.',
         '..111...111111111...111',
         '.11.....111111111.....1',
         '........111111111......',
         '........111...111......',
         '........111...111......',
         '.......1111...1111.....',
         '.......................']
    return [''.join(ch if ch == '.' or (x + y) % 2 == 0 else '.' for x, ch in enumerate(r.ljust(24, '.')))
            for y, r in enumerate(s)]


GEYSERS = []                # (columna, fila de arriba, fila de abajo) del fuego, para el motor


def fuego(L, c, r0, r1):
    for r in range(r0, r1 + 1):
        for y in range(8):
            for x in range(8):
                if FUEGO[y][x] != '.' and L.p[r * 8 + y][c * 4 + x] == '.':
                    L.p[r * 8 + y][c * 4 + x] = '4'
    GEYSERS.append((c, r0, r1))


def geiser(L, c, desde_techo=False, alto=8):
    if not desde_techo:
        L.stamp(BOQUILLA, c, 16)
        fuego(L, c, 16 - alto, 15)
    else:
        L.stamp([r for r in BOQUILLA[::-1]], c, 2)
        fuego(L, c, 3, 2 + alto)


def pinza(L, c, hueco):          # géiser de suelo + géiser de techo: en erupción solo queda el hueco (3 filas)
    L.stamp(BOQUILLA, c, 16)
    L.stamp([r for r in BOQUILLA[::-1]], c, 2)
    fuego(L, c, 3, hueco - 1)
    fuego(L, c, hueco + 3, 15)


def muro(L, c, hueco, arriba=3):  # MURO INFERNAL: cortina de fuego de todo el alto con una sola compuerta
    L.stamp(BOQUILLA, c, 16)
    fuego(L, c, arriba, hueco - 1)
    fuego(L, c, hueco + 3, 15)


def build():
    GEYSERS.clear()
    L = Level()
    R = random.Random(3003)
    for c in range(0, COLS, 4):
        L.stamp(TECHO, c, 0)
        L.stamp(SUELO, c, 16)
    # ---------------- A · CENIZAS EXTERIORES (0-239): columnas, géiseres altos de suelo y de techo
    for c, w, h in ((30, 5, 4), (92, 4, 6), (150, 6, 5), (214, 5, 4)): L.stamp(columna(w, h), c, 16 - h)
    for c, w, h in ((60, 6, 3), (124, 5, 4), (186, 7, 3)): L.stamp(estalactita(w, h), c, 2)
    for c, r in ((44, 8), (170, 10)): L.stamp(losa(10, 2), c, r)
    for c in (76, 140, 200): geiser(L, c, alto=10)
    for c in (108, 228): geiser(L, c, desde_techo=True, alto=9)
    pinza(L, 166, 8)
    # ---------------- B · HORNOS GEMELOS (240-479): fumarolas arriba y abajo y pinzas que cierran el paso
    for i, c in enumerate(range(250, 470, 22)):
        if i % 3 == 2:
            pinza(L, c, 8)              # compuerta siempre en medio
        else:
            geiser(L, c, desde_techo=(i % 2 == 1), alto=9)
        L.stamp(columna(4, 3 + i % 2), c + 9, 13 - i % 2)
        L.stamp(estalactita(4, 3), c + 15, 2)
    # ---------------- C · GARGANTA DE BRASAS (480-719): techo y suelo se acercan; MUROS INFERNALES con compuerta
    for i, c in enumerate(range(484, 716, 12)):
        h = 4 + (i % 3)
        L.stamp(columna(6, h), c, 16 - h)
        L.stamp(estalactita(6, 3 + (i + 1) % 3), c + 6, 2)
        if i % 2 == 1:
            muro(L, c + 7, 10, arriba=7)  # compuerta siempre en medio
    # ---------------- D · TRONO DE ESCORIA (720-911): cadena de fuegos por el suelo, goteo del techo y pinzas
    for k, c in enumerate(range(726, 900, 12)):
        if k % 4 == 3:
            pinza(L, c, 8)
        else:
            geiser(L, c, alto=6)
            if k % 2: geiser(L, c + 6, desde_techo=True, alto=5)
    for c, r in ((760, 7), (840, 9)): L.stamp(losa(12, 2), c, r)
    # ---------------- fondo (se atraviesa): estatuas demoníacas y chispas
    est = estatua()
    for c in (10, 110, 200, 730, 800, 870): L.stamp_bg(est, c, 5)
    vacio = [[all(L.p[q * 40 + y][c * 4 + x] == '.' for y in range(40) for x in range(4)) for q in range(4)] for c in range(COLS)]
    CH = ['....', '..3.', '....', '....', '....', '.2..', '....', '....']
    pat = [(R.randrange(STARP), R.randrange(3, 15)) for _ in range(26)]
    for c0 in range(0, COLS, STARP):
        for dc, r in pat:
            c = c0 + dc
            if c < COLS and vacio[c][r // 5] and all(L.p[r * 8 + y][c * 4 + x] == '.' for y in range(8) for x in range(4)):
                for y in range(8):
                    for x in range(4):
                        if CH[y][x] != '.': L.p[r * 8 + y][c * 4 + x] = CH[y][x]
    return L


# negro carbón arriba -> rojo oscuro -> carmesí junto a la lava
BKGRAD = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x20, 0x20, 0x30, 0x30, 0x30, 0x40, 0x40, 0x42, 0x42, 0x42, 0x44, 0x00, 0x00]
PAL = dict(bk=0x00, pf0=0x32, pf1=0x38, pf2=0x1E, pf3=0x2C)

# oleadas (7.º campo: patrón · D por detrás, B bucle, Q patrulla, C carga, E escalera): A = ASCORIA · S = SERAFÍN NEGRO · P = MÁRTIR DE PLASMA · M = UNIDAD CERO
WAVES = [
    (8, 'A', 3, 1, 36, '', ''), (34, 'S', 3, 0, 30, 'P', 'Q'), (60, 'A', 3, 2, 36, '', ''), (84, 'M', 1, 1, 1, '', ''),
    (104, 'P', 2, 2, 60, '', 'B'), (128, 'S', 3, 1, 30, '', ''), (154, 'A', 4, 0, 32, 'S', 'D'), (180, 'P', 2, 1, 60, '', ''),
    (206, 'M', 1, 2, 1, '', ''), (228, 'S', 3, 2, 30, '', 'C'), (252, 'A', 3, 1, 36, '', ''), (278, 'P', 2, 0, 60, 'P', 'E'),
    (304, 'S', 4, 1, 26, '', ''), (330, 'M', 1, 1, 1, '', ''), (354, 'A', 4, 2, 32, '', 'B'), (380, 'P', 3, 1, 50, '', ''),
    (410, 'S', 4, 0, 26, 'S', 'Q'), (440, 'M', 1, 2, 1, '', ''), (470, 'A', 3, 1, 36, '', ''), (500, 'S', 4, 1, 26, '', 'D'),
    (530, 'P', 3, 1, 50, '', ''), (560, 'M', 1, 1, 1, '', ''), (586, 'A', 4, 1, 30, 'P', 'Q'), (616, 'S', 4, 1, 24, '', ''),
    (646, 'P', 3, 1, 46, '', 'B'), (676, 'M', 1, 1, 1, '', ''), (700, 'A', 4, 2, 30, '', ''), (730, 'S', 4, 0, 24, 'S', 'D'),
    (760, 'P', 3, 1, 46, '', ''), (790, 'M', 1, 2, 1, '', ''), (816, 'A', 4, 1, 28, '', 'C'), (846, 'S', 4, 2, 24, 'P', ''),
    (874, 'P', 3, 1, 44, '', 'E'),
]
# segunda capa: más presión en otras franjas, intercaladas con las de arriba
WAVES += [(c + 14, t, n, (b + 2) % 4, g, '', pat) for (c, t, n, b, g, cap, pat) in WAVES if c + 14 < 896 and t != 'M']
WAVES.sort()
