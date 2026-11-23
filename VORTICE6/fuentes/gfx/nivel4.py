"""VÓRTICE 6 · FASE 4 · EL SARCÓFAGO DE SACRIFICIOS DE SATURNO · nivel jugable.

960 columnas: A Anillos de entrada · B Galería de ofrendas (puertas) · C Cámara de urnas · D Sala del sarcófago · arena desde la 912.
Colores: 1 = PF0 violeta profundo · 2 = PF1 oro envejecido · 3 = PF2 jade pálido (bordes: siempre visibles)
         4 = PF3 PUERTA CEREMONIAL: rejilla de energía; el motor la enciende (jade que late) o la apaga (abierta)
Las puertas no son sólidas en el mapa: cada una tiene dos NODOS de jade (enemigos 'N'); si caen los dos, la puerta
se apaga y se abre el paso ancho; si no, solo queda la compuerta estrecha de 3 filas. Lo comprueba el motor con GEYSERS.
"""
import random
from world import M
from nivel1 import Level, kit as _kit, STARP
import nivel1

COLS, ROWS = 960, 20
ARENA = 912

FILL_PIEDRA = ['1111', '1111', '1121', '1111', '1111', '1111', '1211', '1111']   # piedra violeta con vetas de oro
FILL_ORO = ['2222', '2122', '2222', '2222', '2222', '2212', '2222', '2222']      # oro envejecido (urnas, tapas)


def kit(mask, fill):
    old = nivel1.FILLPAT
    nivel1.FILLPAT = fill
    try:
        return _kit(mask)
    finally:
        nivel1.FILLPAT = old


def colgante(w, h, fill=FILL_PIEDRA):      # bloque que cuelga del techo; borde inferior achaflanado (mitad de anillo)
    return kit(['#' * w] * (h - 1) + ['c' + '#' * (w - 2) + 'd'], fill)


def torre(w, h, fill=FILL_PIEDRA):         # bloque desde el suelo; borde superior achaflanado
    return kit(['a' + '#' * (w - 2) + 'b'] + ['#' * w] * (h - 1), fill)


def altar(w):                              # altar escalonado de tres gradas
    return kit(['.' * 2 + 'a' + '#' * (w - 6) + 'b' + '.' * 2,
                '.a' + '#' * (w - 4) + 'b.',
                'a' + '#' * (w - 2) + 'b',
                '#' * w], FILL_PIEDRA)


def mascara(fill=FILL_ORO):                # MÁSCARA RITUAL angular (6x6): frente con cuernos, dos ojos y boca
    return kit(['a.##.b', '######', '#.##.#', '######', '##..##', '.c##d.'], fill)


def tapa(w):                               # tapa de sarcófago: losa larga achaflanada
    return kit(['a' + '#' * (w - 2) + 'b', 'c' + '#' * (w - 2) + 'd'], FILL_ORO)


# techo: cornisa de piedra con dientes escalonados · suelo: zócalo con gradas
TECHO = M('''
2222222222222222
2112211221122112
1111111111111111
1211111112111111
3333333333333333
3111111331111113
.311113..311113.
..3113....3113..''' + '\n' + '\n'.join(['................'] * 8))
SUELO = M('\n'.join(['................'] * 5) + '''
..3113....3113..
.311113..311113.
3111111331111113
3333333333333333
1111111111111111
1121112111211121
2222222222222222
1111111111111111
1211121112111211
1111111111111111
1111111111111111''')

REJA = ['.44..44.', '.44..44.', '4..44..4', '4..44..4', '.44..44.', '.44..44.', '4..44..4', '4..44..4']

GEYSERS = []                # tramos de puerta (columna, fila de arriba, fila de abajo) para el motor
PUERTAS = []                # (columna, primera fila del hueco) · los nodos se colocan en las oleadas


def reja(L, c, r0, r1):
    for r in range(r0, r1 + 1):
        for cc in (c, c + 1):   # una celda con borde jade (PF2) no puede llevar rejilla (PF3)
            assert not any('3' in ''.join(L.p[r * 8 + y][cc * 4:cc * 4 + 4]) for y in range(8)), ('reja sobre borde', c, r)
        for y in range(8):
            for x in range(8):
                if REJA[y][x] != '.' and L.p[r * 8 + y][c * 4 + x] == '.':
                    L.p[r * 8 + y][c * 4 + x] = '4'
    GEYSERS.append((c, r0, r1))


def puerta(L, c, hueco):
    """PUERTA CEREMONIAL: dintel y zócalo de piedra, rejilla de energía de las filas 3 a 15 con una compuerta de 3 filas"""
    L.stamp(kit(['c' + '##' + 'd'], FILL_PIEDRA), c - 1, 2)          # dintel
    L.stamp(kit(['a' + '##' + 'b'], FILL_PIEDRA), c - 1, 15)         # zócalo
    reja(L, c, 3, hueco - 1)
    reja(L, c, hueco + 3, 14)
    PUERTAS.append((c, hueco))


def anillo(L, c, g0, g1, w=4):
    """ANILLO de entrada: dos medias piezas achaflanadas; el paso es la abertura entre las filas g0 y g1"""
    if g0 > 2: L.stamp(colgante(w, g0 - 2), c, 2)
    if g1 < 15: L.stamp(torre(w, 15 - g1), c, g1 + 1)


# fondo (no sólido, PF0 tramado): el planeta anillado de Saturno y figuras hieráticas
def saturno():
    s = ['.........1111111.........',
         '.......11111111111.......',
         '......1111111111111......',
         '11...111111111111111...11',
         '.1111111111111111111111..',
         '...111111111111111111....',
         '......1111111111111......',
         '.......11111111111.......',
         '.........1111111.........',
         '.........................']
    s += ['.' * 25] * 6
    return [''.join(ch if ch == '.' or (x + y) % 2 == 0 else '.' for x, ch in enumerate(r.ljust(28, '.')))
            for y, r in enumerate(s)]


def oficiante():
    s = ['....1111....',
         '...111111...',
         '...1.11.1...',
         '...111111...',
         '....1111....',
         '..11111111..',
         '.1111111111.',
         '11.111111.11',
         '1..111111..1',
         '...111111...',
         '...111111...',
         '..11111111..',
         '..11111111..',
         '.1111111111.',
         '.1111111111.',
         '............']
    return [''.join(ch if ch == '.' or (x + y) % 2 == 0 else '.' for x, ch in enumerate(r.ljust(12, '.')))
            for y, r in enumerate(s)]


def build():
    GEYSERS.clear()
    PUERTAS.clear()
    L = Level()
    R = random.Random(4004)
    for c in range(0, COLS, 4):
        L.stamp(TECHO, c, 0)
        L.stamp(SUELO, c, 16)
    # ---------------- A · ANILLOS DE ENTRADA (0-239): la abertura sube y baja, cada vez más estrecha
    for c, g0, g1 in ((28, 6, 12), (58, 4, 10), (88, 8, 14), (116, 5, 10), (146, 9, 14),
                      (174, 4, 9), (200, 8, 13), (226, 6, 10)):
        anillo(L, c, g0, g1)
    for c, r in ((42, 9), (102, 7), (160, 11), (214, 4)): L.stamp(tapa(6), c, r)
    # ---------------- B · GALERÍA DE OFRENDAS (240-479): altares, lámparas colgantes y tres puertas
    for c in (246, 286, 330, 372, 420, 462): L.stamp(altar(8), c, 12)
    for c in (264, 312, 352, 400, 438): L.stamp(colgante(3, 3), c, 2)
    for c in (300, 384, 446): puerta(L, c, 8)       # compuerta en medio; la rejilla se enciende y se apaga
    # ---------------- C · CÁMARA DE LAS MÁSCARAS (480-719): máscaras rituales flotantes en dos alturas, techo y suelo que se cierran
    for i, c in enumerate(range(486, 712, 14)):
        L.stamp(mascara(), c, (4, 9, 7, 10, 5, 8)[i % 6])
        if i % 3 == 2: L.stamp(colgante(4, 3), c + 7, 2)
        if i % 3 == 0: L.stamp(torre(4, 3), c + 8, 13)
    # ---------------- D · SALA DEL SARCÓFAGO (720-911): tapas largas que hacen tres carriles y dos puertas
    for c, r in ((726, 7), (744, 12), (790, 6), (806, 12), (880, 8)): L.stamp(tapa(14), c, r)
    for c in (772, 848): puerta(L, c, 8)
    for c in (830, 896): L.stamp(altar(8), c, 12)
    # ---------------- fondo (se atraviesa): Saturno anillado y oficiantes
    sat, ofi = saturno(), oficiante()
    for c in (10, 250, 520, 760): L.stamp_bg(sat, c, 4)
    for c in (140, 410, 640, 870): L.stamp_bg(ofi, c, 6)
    # polvo de oro solo en trozos vacíos (comprime bien)
    vacio = [[all(L.p[q * 40 + y][c * 4 + x] == '.' for y in range(40) for x in range(4)) for q in range(4)] for c in range(COLS)]
    CH = ['....', '..2.', '....', '....', '....', '.3..', '....', '....']
    pat = [(R.randrange(STARP), R.randrange(3, 15)) for _ in range(22)]
    for c0 in range(0, COLS, STARP):
        for dc, r in pat:
            c = c0 + dc
            if c < COLS and vacio[c][r // 5] and all(L.p[r * 8 + y][c * 4 + x] == '.' for y in range(8) for x in range(4)):
                for y in range(8):
                    for x in range(4):
                        if CH[y][x] != '.': L.p[r * 8 + y][c * 4 + x] = CH[y][x]
    return L


# negro arriba -> violeta -> púrpura -> violeta -> negro junto al zócalo
BKGRAD = [0x00, 0x00, 0x00, 0x50, 0x50, 0x60, 0x60, 0x60, 0x62, 0x62, 0x70, 0x70, 0x72, 0x72, 0x60, 0x60, 0x50, 0x50, 0x00, 0x00]
PAL = dict(bk=0x00, pf0=0x64, pf1=0x28, pf2=0xBA, pf3=0xBC)

# oleadas (7.º campo: patrón · D por detrás, B bucle, Q patrulla, C carga, E escalera): A = ACÓLITO · G = GUARDIÁN · V = VASO · E = ESCRIBA · (los NODOS de las puertas los pone el motor)
#   (columna, tipo, cuántos, franja, separación, cápsula al limpiar la oleada)
WAVES = [
    (6, 'A', 3, 1, 34, '', ''), (30, 'G', 3, 2, 30, 'P', 'Q'), (54, 'V', 3, 0, 40, '', ''), (76, 'A', 3, 2, 30, '', 'B'),
    (100, 'E', 2, 1, 40, '', ''), (120, 'G', 4, 0, 28, 'S', ''), (146, 'V', 3, 2, 36, '', 'D'), (168, 'A', 4, 1, 28, '', ''),
    (192, 'E', 1, 2, 1, '', ''), (210, 'G', 4, 1, 26, 'P', 'C'), (234, 'A', 4, 0, 26, '', ''),
    (258, 'V', 4, 1, 32, '', 'E'), (280, 'E', 2, 0, 36, '', ''), (296, 'G', 4, 2, 26, '', ''), (322, 'A', 4, 1, 24, 'S', 'B'),
    (344, 'E', 1, 2, 1, '', ''), (362, 'V', 4, 0, 30, '', ''), (402, 'G', 4, 1, 24, 'P', 'Q'), (424, 'A', 4, 2, 24, '', ''),
    (468, 'E', 2, 1, 32, '', ''), (488, 'V', 4, 1, 28, '', 'D'), (508, 'A', 4, 0, 24, '', ''), (530, 'G', 4, 2, 24, 'S', 'Q'),
    (552, 'V', 4, 2, 28, '', ''), (574, 'E', 1, 1, 1, '', ''), (594, 'A', 4, 1, 22, '', 'B'), (616, 'V', 4, 0, 26, 'P', ''),
    (640, 'G', 5, 1, 22, '', 'D'), (664, 'E', 2, 2, 30, '', ''), (684, 'A', 5, 2, 22, '', ''), (706, 'V', 4, 1, 26, '', 'C'),
    (730, 'G', 5, 0, 22, 'S', ''), (754, 'E', 1, 1, 1, '', ''), (790, 'A', 5, 1, 20, '', 'E'), (812, 'V', 4, 2, 24, 'P', ''),
    (830, 'E', 3, 0, 28, '', ''), (866, 'G', 5, 2, 20, '', 'B'), (884, 'A', 5, 1, 20, '', ''),
]
# segunda capa: presión en otras franjas (también escribas: varias rayas a la vez)
WAVES += [(c + 12, t, n, (b + 2) % 4, g, '', pat) for (c, t, n, b, g, cap, pat) in WAVES if c + 12 < 896]
# los NODOS de jade no van en las oleadas: el motor los coloca junto a su puerta cuando esta entra en pantalla
WAVES.sort()
WAVES += [(c, 'E', 1, b, 1, '', '') for c, b in ((150, 3), (236, 2), (378, 1), (548, 3), (616, 2), (742, 0), (884, 3))]
WAVES.sort()
