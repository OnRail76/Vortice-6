"""VÓRTICE 6 · FASE 2 · LOS OCÉANOS ASTRALES · nivel jugable.

960 columnas: A Mar sin horizonte · B Jardines de coral orbital (enredadera marina) · C Tormenta gravitacional · D Abismo de marea
· arena de THALASSA desde la 912. Mismo formato que el nivel 1 (ANTIC 4, 4 cuartos de 5 filas).
Colores: 1 = PF0 verde acuático · 2 = PF1 cian · 3 = PF2 blanco perla (bordes: siempre visibles) · 4 = PF3 corriente (late)
Todo lo grande es anguloso (achaflanado por celdas), sin formas de "patata"; las burbujas son decorado pequeño.
"""
import random
from world import M, SURF, SEABED
from nivel1 import Level, kit as _kit, STARP
import nivel1

COLS, ROWS = 960, 20
ARENA = 912

# relleno de agua: cian con motas verdes (se repite por celda: cuesta pocos caracteres)
FILL_AGUA = ['2222', '2212', '2222', '1222', '2222', '2221', '2222', '2122']
FILL_CORAL = ['1111', '1121', '1111', '1111', '2111', '1111', '1111', '1111']


def kit(mask, fill):
    old = nivel1.FILLPAT
    nivel1.FILLPAT = fill
    try:
        return _kit(mask)
    finally:
        nivel1.FILLPAT = old


def bolsa(w, h):                  # bolsa de agua luminosa: hexágono achaflanado
    m = ['a' + '#' * (w - 2) + 'b'] + ['#' * w] * (h - 2) + ['c' + '#' * (w - 2) + 'd']
    return kit(m, FILL_AGUA)


def tubo(w):                      # tubo líquido de presión (horizontal, 2 filas)
    return kit(['a' + '#' * (w - 2) + 'b', 'c' + '#' * (w - 2) + 'd'], FILL_AGUA)


# ENREDADERA MARINA (estilo fondos orgánicos): malla de lianas con bulbos-ojo; crece del suelo o del techo
# en columnas de 4 celdas (16 píxeles) con alturas que suben y bajan suave; arriba remata en lianas con bolitas.
MALLA = ['1..11..111..11.1', '.11..11...11..1.', '11.1..1.333.1.11', '..1.11.31113.1..',
         '.1.1..131213..1.', '1..1.1.31113.1.1', '.11.1...333.1.1.', '1..1.11.....1..1',
         '.11..1.11.11.11.', '1.333..1.1..1..1', '.31113.1..11.11.', '131213..11..1..1',
         '.31113.11..1.11.', '1.333.1..11.1..1', '.1...1.11..1.1..', '1.11..1..11..1.1']
FLECO = [['................', '..33.......33...', '.3223.....3223..', '.3223..33.3223..',
          '..33..3223.33...', '..1...3223..1...', '.1.1...33..1.1..', '1...1..1..1...11'],
         ['................', '......33........', '.33..3223....33.', '3223.3223...3223',
          '3223..33..1.3223', '.33...1..1...33.', '..1.1..11...1.1.', '.1...1....11...1']]
U = 16


def enredadera(alturas, row, techo=False):
    """alturas en celdas por cada columna de 16 píxeles; row = fila donde se estampa (para alinear la malla)"""
    H = max(alturas)
    out = [['.'] * (U * len(alturas)) for _ in range(8 * H)]
    for k, h in enumerate(alturas):
        for cy in range(h):
            r = (H - 1 - cy) if not techo else cy          # celda desde el suelo (o desde el techo)
            tope = cy == h - 1
            for y in range(8):
                yy = r * 8 + y
                if tope:
                    f = FLECO[k % 2]
                    ch = f[y] if not techo else f[7 - y]
                else:
                    ch = MALLA[(row * 8 + yy) % 16]
                for x in range(U):
                    out[yy][k * U + x] = ch[x]
    return [''.join(l) for l in out]


def monte(n, alto):            # perfil suave: sube, meseta y baja
    import math
    return [max(1, round(alto * (0.55 + 0.45 * math.sin(math.pi * (i + 0.5) / n)))) for i in range(n)]


def cristal(w, h, lado='izq'):    # cristal de perla en cuña (suelo)
    m = []
    for r in range(h):
        if lado == 'izq': m.append('.' * (h - 1 - r) + 'a' + '#' * (w - h + r))
        else: m.append('#' * (w - h + r) + 'b' + '.' * (h - 1 - r))
    return kit(m, FILL_AGUA)


# medusas lejanas (fondo, no sólidas): silueta en PF0, por celdas
MEDUSA_LEJOS = M('''
..1111..
.111111.
11111111
11111111
1.1..1.1
.1.11.1.
1..1..1.
.1..1...''')
# leviatán gigante que pasa tras el escenario en el abismo (fondo, no sólido)
def leviatan():
    L = [
        '................................................................................................',
        '...........................1111111111111111111111111............................................',
        '.....................11111111111111111111111111111111111111.....................................',
        '................111111111111111111111111111111111111111111111111111.............................',
        '............11111111..1111111111111111111111111111111111111111111111111111......................',
        '.........111111111....1111111111111111111111111111111111111111111111111111111111................',
        '.......1111111111111111111111111111111111111111111111111111111111111111111111111111111..........',
        '.....111111111111111111111111111111111111111111111111111111111111111111111111111111111111111....',
        '...11111111111111111111111111111111111111111111111111111111111111111111111.....11111111111111111',
        '..1111111111111111111111111111111111111111111111111111111111111111111111.........11111111111111.',
        '.11111111111111111111111111111111111111111111111111111111111111111111..............11111111111..',
        '111111111111111111111111111111111111111111111111111111111111111111..................111111111...',
        '1111111111111111111111111111111111111111111111111111111111111111.....................1111111....',
        '.1111111111111111111111111111111111111111111111111111111111111.........................111.....',
        '..111111111111111111111111111111111111111111111111111111111.....................................',
        '....11111111111111111111111111111111111111111111111111111.......................................',
        '.......1111111111111111111111111.....1111111111111111...........................................',
        '..........11111111111111111111.........11111111111..............................................',
        '..............1111111111111...............1111..................................................',
        '...................11111........................................................................',
        '................................................................................................',
        '................................................................................................',
        '................................................................................................',
        '................................................................................................']
    L = [l.ljust(96, '.')[:96] for l in L]
    # cuerpo macizo (se ve claro tras el escenario), solo el borde tramado; ojo y línea del vientre en blanco perla
    out = []
    for y, l in enumerate(L):
        r = ''
        for x, ch in enumerate(l):
            if ch == '.': r += '.'; continue
            edge = any(not (0 <= y + dy < len(L) and 0 <= x + dx < 96) or L[y + dy][x + dx] == '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            r += ('1' if (x + y) % 2 == 0 else '.') if edge else '1'
        out.append(r)
    out = [list(r) for r in out]
    for x, y in ((10, 8), (11, 8), (10, 9), (11, 9)): out[y][x] = '3'           # ojo
    for x in range(14, 60, 2): out[13 + (x > 40)][x] = '2'                        # vientre
    return [''.join(r) for r in out]


# corrientes: rayas de partículas PF3 (no sólidas), dos sentidos
CORR_BAJA = M('''
4.......
.4......
..4.....
........
....4...
.....4..
......4.
........''')
CORR_SUBE = M('''
......4.
.....4..
....4...
........
..4.....
.4......
4.......
........''')
BURBUJA = M('''
....
.33.
3..3
.33.
....
..3.
....
....''')


def build():
    L = Level()
    R = random.Random(2002)
    for c in range(0, COLS, 4):
        L.stamp(SURF, c, 0)
        L.stamp(SEABED, c, 18)
    # ---------------- A · MAR SIN HORIZONTE (0-239): espacio abierto, bolsas de agua flotando y medusas lejanas
    for c, r, w, h in ((30, 7, 8, 3), (70, 11, 10, 2), (104, 5, 7, 3), (140, 10, 12, 3), (182, 6, 9, 2), (214, 11, 8, 3)):
        L.stamp(bolsa(w, h), c, r)
    for c, a in ((46, 5), (116, 4), (192, 6), (228, 4)):
        L.stamp(enredadera(monte(3, a), 18 - a), c, 18 - a)
    # ---------------- B · JARDINES DE CORAL ORBITAL (240-479): bosque de corales arriba y abajo, carriles amplios
    for i, c in enumerate(range(244, 470, 22)):
        a = 4 + (i % 3)
        L.stamp(enredadera(monte(3, a), 18 - a), c, 18 - a)
        t = 3 + (i + 1) % 3
        L.stamp(enredadera(monte(3, t), 2, techo=True), c + 11, 2)
    # ---------------- C · TORMENTA GRAVITACIONAL (480-719): tubos de presión y bandas de corriente
    for c, r in ((490, 6), (530, 11), (570, 5), (610, 12), (650, 7), (690, 10)):
        L.stamp(tubo(14), c, r)
    for c in (510, 590, 670): L.stamp(cristal(8, 3, 'izq'), c, 15)
    for c in (550, 630, 706): L.stamp(cristal(8, 3, 'der'), c, 15)
    # ---------------- D · ABISMO DE MAREA (720-911): menos luz, bolsas grandes y corales gruesos
    #     el leviatán pasa por el centro: nada delante de él (bolsas abajo, corales bajos y techo corto)
    for c, r, w, h in ((726, 13, 10, 2), (800, 12, 12, 2), (880, 11, 10, 2)):
        L.stamp(bolsa(w, h), c, r)
    for c, a in ((768, 4), (824, 3), (896, 4)): L.stamp(enredadera(monte(3, a), 18 - a), c, 18 - a)
    for c, a in ((722, 3), (800, 2)): L.stamp(enredadera(monte(3, a), 2, techo=True), c, 2)
    # ---------------- fondo (se atraviesa)
    for c in range(8, 240, 26):                       # medusas lejanas en el mar abierto
        L.stamp_bg(MEDUSA_LEJOS, c, 3 + (c * 7) % 11)
    lev = leviatan()
    L.stamp_bg(lev, 736, 7)
    L.stamp_bg(lev, 840, 5)
    # corrientes en la tormenta: banda alta baja, banda baja sube (se ven antes de que empujen)
    for c in range(480, 720, 2):
        for r in (3, 4):
            if all(L.p[r * 8 + y][c * 4 + x] == '.' for y in range(8) for x in range(8)):
                L.stamp(CORR_BAJA, c, r, solid=False)
        for r in (14, 15):
            if all(L.p[r * 8 + y][c * 4 + x] == '.' for y in range(8) for x in range(8)):
                L.stamp(CORR_SUBE, c, r, solid=False)
    # burbujas (pequeñas, decorado) solo en trozos vacíos, patrón de 24 columnas como las estrellas
    vacio = [[all(L.p[q * 40 + y][c * 4 + x] == '.' for y in range(40) for x in range(4)) for q in range(4)] for c in range(COLS)]
    pat = [(R.randrange(STARP), R.randrange(2, 18)) for _ in range(40)]
    for c0 in range(0, COLS, STARP):
        for dc, r in pat:
            c = c0 + dc
            if c < COLS and vacio[c][r // 5] and all(L.p[r * 8 + y][c * 4 + x] == '.' for y in range(8) for x in range(4)):
                for y in range(8):
                    for x in range(4):
                        if BURBUJA[y][x] != '.': L.p[r * 8 + y][c * 4 + x] = BURBUJA[y][x]
    return L


# degradado: azul noche arriba -> cian frío -> verde acuático junto al fondo
BKGRAD = [0x00, 0x00, 0x80, 0x80, 0x80, 0x82, 0x90, 0x90, 0x92, 0x92, 0xA0, 0xA0, 0xA2, 0xA2, 0xA2, 0xB2, 0xB2, 0xB2, 0x00, 0x00]
PAL = dict(bk=0x00, pf0=0xC6, pf1=0xA8, pf2=0x0E, pf3=0x9C)   # verde acuático, cian frío, blanco perla, corriente


# oleadas (7.º campo: patrón · D por detrás, B bucle, Q patrulla, C carga, E escalera): (columna de la cámara, tipo, cantidad, franja 0-3, separación en cuadros, cápsula al limpiarla)
#   J = MEDUSA DE VACÍO (vaivén y esfera lenta) · R = RAYA FOTÓNICA (manta: arco y sale) · A = ANGUILA DE MAREA
#   M = UNIDAD CERO (mecha común, de uno en uno, siempre suelta cápsula)
WAVES = [
    (8, 'J', 3, 1, 40, '', ''),
    (36, 'R', 4, 0, 24, 'P', 'Q'),
    (60, 'J', 3, 2, 40, '', ''),
    (84, 'M', 1, 1, 1, '', ''),
    (104, 'R', 4, 2, 22, '', 'B'),
    (130, 'A', 3, 1, 40, '', ''),
    (156, 'J', 4, 0, 34, 'S', 'D'),
    (182, 'R', 4, 1, 22, '', ''),
    (206, 'M', 1, 2, 1, '', ''),
    (226, 'A', 3, 0, 40, '', 'C'),
    (250, 'J', 3, 1, 40, '', ''),
    (276, 'A', 3, 2, 36, 'P', 'E'),
    (302, 'R', 4, 0, 20, '', ''),
    (330, 'M', 1, 1, 1, '', ''),
    (352, 'J', 4, 2, 34, '', 'B'),
    (380, 'A', 4, 1, 34, '', ''),
    (410, 'R', 4, 1, 20, 'S', 'Q'),
    (440, 'M', 1, 0, 1, '', ''),
    (470, 'J', 3, 1, 40, '', ''),
    (500, 'R', 4, 1, 20, '', 'D'),
    (530, 'A', 3, 2, 36, '', ''),
    (560, 'M', 1, 1, 1, '', ''),
    (586, 'R', 4, 2, 20, 'P', 'Q'),
    (616, 'J', 4, 1, 34, '', ''),
    (646, 'A', 4, 0, 34, '', 'B'),
    (676, 'M', 1, 2, 1, '', ''),
    (700, 'R', 4, 1, 18, '', ''),
    (730, 'J', 4, 0, 32, 'S', 'D'),
    (760, 'A', 4, 2, 32, '', ''),
    (790, 'M', 1, 1, 1, '', ''),
    (816, 'R', 4, 1, 18, '', 'C'),
    (846, 'A', 4, 1, 30, 'P', ''),
    (874, 'J', 4, 2, 30, '', 'E'),
]
