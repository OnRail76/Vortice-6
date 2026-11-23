"""VÓRTICE 6 · FASE 5 · LA NAVE VIVIENTE · nivel jugable (versión orgánica, sin verdes).

960 columnas: A Boca de entrada · B Conductos vitales · C Cámara de los ojos · D Ventrículo · arena desde la 912.
Colores: 1 = PF0 carne oscura ($42) · 2 = PF1 vena roja viva ($46) · 3 = PF2 hueso / blanco del ojo ($0C)
         4 = PF3 PARED RESPIRANTE: músculo que el motor colorea según su estado (relajado · avisando · contraído)
Escenario: masas de tejido con venas que crecen del techo y del suelo y acaban en tentáculos con ojillos (la
enredadera de la fase 2 llevada a vasos sanguíneos), OJOS grandes inyectados en sangre ENTERRADOS en esas masas
(sin bloque alrededor: las venas los rodean), ARTERIAS que cruzan y paredes de músculo.
"""
import random
from world import M
from nivel1 import Level, kit as _kit, STARP
import nivel1
import venas as V

COLS, ROWS = 960, 20
ARENA = 912

FILL_DIENTE = ['3333', '3333', '3323', '3333', '3333', '3233', '3333', '3333']   # hueso con vetas


def kit(mask, fill):
    old = nivel1.FILLPAT
    nivel1.FILLPAT = fill
    try:
        return _kit(mask)
    finally:
        nivel1.FILLPAT = old


def mandibula(w, h, arriba=True):
    """MANDÍBULA: bloque de hueso con una fila de dientes en punta (desde el techo o desde el suelo)"""
    dientes = ('cd' if arriba else 'ab') * (w // 2)
    m = ['#' * w] * (h - 1) + [dientes]
    if not arriba: m = m[::-1]
    return kit(m, FILL_DIENTE)


# techo y suelo: banda de carne con venas y borde de hueso
TECHO = M('''
1111111111111111
1121111112111111
1112111121111211
1111211211112111
1111122111121111
2111112111211111
3333333333333333
.3...3.....3...3''' + '\n' + '\n'.join(['................'] * 8))
SUELO = M('\n'.join(['................'] * 8) + '''
..3.....3...3...
3333333333333333
1111211111112111
1112121111121211
1121112111211121
1211111212111112
1111111121111111
1111111111111111''')

MUSCULO = ['4444.444', '4.44444.', '44.44444', '444.4444', '4444.444', '44444.44', '.4444444', '444444.4']
ANCLA = M('''
.3333333
31111113
31211213
31111113
.3111113
..31113.
...313..
....3...''')

# ---- ARENA BIOMECÁNICA (desde la columna 896): el ventrículo acaba en una cámara de máquinas.
# En la arena el color 2 (PF1) pasa a acero oscuro; los LEDs son PF3 y laten con el corazón.
# Las celdas con LED (4) no llevan bordes (3): regla del hardware.
_A = ['2222', '2332', '2322', '2322', '2322', '2322', '2332', '2222']        # placa atornillada
_B = ['2222', '2222', '2442', '2442', '2222', '2112', '2112', '2222']        # LED y rejilla roja
_D = ['2222', '2112', '2112', '2222', '2442', '2442', '2222', '2222']
_L = ['2222', '2222', '3333', '3..3', '.33.', '....', '....', '....']        # labio inferior del panel
TECHO_T = [_A[y] + _B[y] + _A[y] + _D[y] for y in range(8)] + [_L[y] * 4 for y in range(8)]
SUELO_T = TECHO_T[::-1]

GEYSERS = []


def musculo(L, c, r0, r1):
    for r in range(r0, r1 + 1):
        for cc in (c, c + 1):
            assert not any('3' in ''.join(L.p[r * 8 + y][cc * 4:cc * 4 + 4]) for y in range(8)), ('músculo sobre hueso', c, r)
        for y in range(8):
            for x in range(8):
                if MUSCULO[y][x] != '.' and L.p[r * 8 + y][c * 4 + x] == '.':
                    L.p[r * 8 + y][c * 4 + x] = '4'
    GEYSERS.append((c, r0, r1))


def pared(L, c, desde_techo, hasta):
    if desde_techo:
        L.stamp(ANCLA, c, 2); musculo(L, c, 3, hasta)
    else:
        L.stamp(ANCLA[::-1], c, 15); musculo(L, c, hasta, 14)


def pinza(L, c, hueco):
    L.stamp(ANCLA, c, 2); L.stamp(ANCLA[::-1], c, 15)
    musculo(L, c, 3, hueco - 1); musculo(L, c, hueco + 3, 14)


def masa(L, c, n, alto, techo=False):
    """masa de tejido con venas: n columnas de 16 píxeles; alto en filas (desde el suelo o desde el techo)"""
    alts = V.monte(n, alto)
    if techo: L.stamp(V.tejido(alts, 2, techo=True), c, 2)
    else: L.stamp(V.tejido(alts, 18 - alto), c, 18 - alto)
    return alts


_OJO = None


def ojo(L, c, r):
    """OJO grande enterrado en la carne: solo se dibuja la almendra (con venillas fijas en el párpado);
    alrededor quedan las venas de la masa, sin bloque. Siempre en la misma fase de la baldosa (caracteres compartidos)."""
    global _OJO
    if _OJO is None:
        o = [list(r_) for r_ in V.ojo3()]
        cx, cy = 19.5, 15.5
        for y in range(32):
            for x in range(40):
                vx, vy = (x - cx) * 2, (y - cy)
                lim = (32 / 2 - 2) * (1 - (vx / 39) ** 2)
                if abs(vy) >= lim + .5: o[y][x] = '.'
        for (x0, y0, dx, dy) in ((8, 6, 1, 1), (14, 3, 0, 1), (24, 3, 0, 1), (30, 5, -1, 1), (9, 25, 1, -1), (20, 28, 0, -1), (31, 26, -1, -1)):
            x, y = x0, y0                       # venillas que entran desde el párpado
            for t in range(4):
                if o[y][x] in '13': o[y][x] = '2'
                x += dx if t % 2 else 0; y += dy
        _OJO = [''.join(r_) for r_ in o]
    L.stamp(_OJO, c, r)


def masa_ojo(L, c, techo):
    """masa de tejido de alto fijo con su ojo dentro, siempre igual (así comparte caracteres)"""
    masa(L, c, 4, 6, techo)
    ojo(L, c + 3, 2 if techo else 14)


def build():
    GEYSERS.clear()
    L = Level()
    R = random.Random(5005)
    for c in range(0, COLS, 4):
        if c < 896:
            L.stamp(TECHO, c, 0)
            L.stamp(SUELO, c, 16)
        else:
            L.stamp(TECHO_T, c, 0)
            L.stamp(SUELO_T, c, 16)
    # --- dónde van las piezas grandes (lo demás se rellena de tejido)
    paredes = [(258, True, 8), (320, False, 9), (392, True, 7), (440, False, 10), (600, True, 8), (664, False, 9)]
    pinzas = [(c, 8) for k, c in enumerate(range(730, 900, 24))]     # hueco siempre en medio
    ojos = [(214, False), (290, True), (330, False), (400, False), (444, True), (486, False), (506, True),
            (526, False), (546, True), (566, False), (586, True), (626, False), (646, True), (686, False), (706, True),
            (780, False), (852, True)]
    arterias = [(282, 9, 14), (352, 9, 12), (424, 9, 12), (520, 9, 10), (614, 9, 8), (700, 9, 8), (770, 9, 6), (842, 9, 6)]
    jaws = list(range(20, 120, 16))
    libre = set()
    for c, _, _ in paredes: libre.update(range(c - 2, c + 4))
    for c, _ in pinzas: libre.update(range(c - 2, c + 4))
    ocupado_suelo = set(); ocupado_techo = set()
    for c, t in ojos: (ocupado_techo if t else ocupado_suelo).update(range(c, c + 16))
    for i, c in enumerate(jaws): (ocupado_techo if i % 2 == 0 else ocupado_suelo).update(range(c, c + 8))
    # ---------------- A · BOCA DE ENTRADA: mandíbulas de hueso
    for i, c in enumerate(jaws):
        if i % 2 == 0: L.stamp(mandibula(8, 3 + i % 3), c, 2)
        else: L.stamp(mandibula(8, 3 + i % 3, arriba=False), c, 15 - (3 + i % 3) + 1)
    # ---------------- alfombra de tejido con venas en techo y suelo, todo el nivel (la carne crece desde la boca)
    for techo, occ, fase in ((False, ocupado_suelo, 0), (True, ocupado_techo, 6)):
        c = 8 + fase
        while c < 904:
            n = R.choice((2, 3, 3, 4))
            span = range(c, c + 4 * n)
            if any(x in libre or x in occ for x in span):
                c += 4
                continue
            prof = 1 if c < 120 else 2 if c < 240 else 3
            alto = R.randrange(prof, prof + 3) if c >= 120 else 2
            masa(L, c, n, alto, techo)
            c += 4 * n + R.choice((0, 0, 4, 8))
    # ---------------- ojos enterrados en masas grandes (B y sobre todo C, la cámara de los ojos)
    for c, t in ojos: masa_ojo(L, c, t)
    # ---------------- arterias que cruzan por el centro
    for c, r, w in arterias: L.stamp(V.arteria3(w), c, r)
    # ---------------- músculo: paredes respirantes (B y C) y pinzas (D, el ventrículo)
    for c, t, h in paredes: pared(L, c, t, h)
    for c, h in pinzas: pinza(L, c, h)
    return L


BKGRAD = [0x00] * 20
PAL = dict(bk=0x00, pf0=0x42, pf1=0x46, pf2=0x0C, pf3=0x44)

# oleadas (7.º campo: patrón · D por detrás, B bucle, Q patrulla, C carga, E escalera): G = GLÓBULO CAZADOR · L = LARVA MECÁNICA · M = UNIDAD CERO (de una en una) · S = ESCRIBA (fantasmas de Saturno)
WAVES = [
    (6, 'G', 3, 1, 32, '', ''), (26, 'L', 4, 2, 24, 'P', 'Q'), (44, 'M', 1, 1, 1, '', ''), (64, 'G', 3, 0, 30, '', ''),
    (84, 'S', 2, 1, 32, '', ''), (96, 'L', 4, 1, 22, 'S', 'B'), (118, 'G', 4, 2, 28, '', ''), (140, 'M', 1, 2, 1, '', ''),
    (158, 'L', 5, 0, 20, '', 'D'), (180, 'S', 2, 2, 30, 'P', ''), (192, 'G', 4, 1, 26, '', ''), (214, 'L', 5, 2, 20, '', 'C'),
    (236, 'M', 1, 1, 1, '', ''), (258, 'G', 4, 0, 24, '', ''), (280, 'S', 3, 1, 28, '', ''), (300, 'L', 5, 1, 18, '', 'E'),
    (312, 'G', 4, 2, 24, 'P', ''), (336, 'M', 1, 0, 1, '', ''), (356, 'L', 5, 0, 18, '', 'B'), (380, 'S', 2, 2, 26, 'S', ''),
    (404, 'G', 5, 1, 22, '', ''), (416, 'L', 5, 2, 18, '', 'Q'), (440, 'M', 1, 2, 1, 'P', ''), (462, 'G', 5, 0, 22, '', ''),
    (488, 'L', 6, 1, 16, '', 'D'), (510, 'S', 3, 0, 24, '', ''), (520, 'G', 5, 2, 20, 'S', ''), (546, 'M', 1, 1, 1, '', ''),
    (566, 'L', 6, 0, 16, '', 'Q'), (590, 'G', 5, 1, 20, 'P', ''), (612, 'S', 3, 2, 22, '', ''), (624, 'M', 1, 2, 1, '', ''),
    (648, 'L', 6, 2, 16, '', 'B'), (670, 'G', 5, 0, 18, 'S', ''), (694, 'S', 3, 1, 22, '', ''), (706, 'L', 6, 1, 16, '', 'D'),
    (730, 'G', 6, 2, 18, 'P', ''), (752, 'M', 1, 1, 1, '', ''), (772, 'L', 6, 0, 14, '', 'C'), (796, 'S', 3, 2, 20, '', ''),
    (808, 'G', 6, 1, 18, 'S', ''), (832, 'L', 6, 2, 14, '', 'E'), (856, 'M', 1, 0, 1, '', ''), (876, 'G', 6, 0, 18, '', ''),
]
# segunda capa: más glóbulos, larvas y escribas en otras franjas
WAVES += [(c + 10, t, n, (b + 2) % 4, g, '', pat) for (c, t, n, b, g, cap, pat) in WAVES if c + 10 < 896 and t in 'GLS']
WAVES.sort()
