"""THALASSA · la Madre de las Mareas (versión 2: la diosa).
Perfil femenino de mármol mirando a la izquierda; el pelo, en mechones ondulados, ES la pared del final del nivel
(llena todo el alto del campo y se funde con el borde derecho). 80 x 128 píxeles = 20 x 16 caracteres.

El punto débil es el ojo-perla (3 estados: cerrado, entreabierto con destello, abierto = vulnerable).
I Canto: canta burbujas desde la boca · II Corriente: mechones de pelo cruzan la pantalla dejando un carril libre
III Remolino: el ojo-perla se abre más tiempo y suelta crías.
Colores de la fase 2: 1 = PF0 verde (sombras) · 2 = PF1 cian · 3 = PF2 blanco perla (mármol, contornos)
4 = PF3 que late (la perla). Una celda no puede tener PF2 y PF3 a la vez: el destello solo aparece al abrirse.
"""
import math
from canvas import C

W, H = 80, 128
BOSS_K, BOSS_R = 23, 2          # byte de la ventana y fila de campo donde empieza
FACE = 2                        # x de la piel más adelantada a la altura del ojo (la nariz): ahí empieza la zona de impacto
EYE_CX, EYE_CY = 16, 46
EYE_ROWS, EYE_C0, EYE_NC = (5, 6), 2, 3
MOUTH_Y0, MOUTH_Y1 = 66, 80     # de dónde salen las burbujas del canto
POCKET_Y0, POCKET_Y1 = 40, 56

# perfil (borde izquierdo de la piel) por y: frente, entrecejo, nariz, labios, barbilla, cuello
K = [(0, 22), (8, 16), (20, 12), (34, 10), (40, 9), (46, 7), (52, 4), (58, 1), (62, 0), (64, 3), (67, 6), (70, 5),
     (73, 7), (75, 8), (78, 6), (81, 7), (86, 9), (92, 10), (97, 13), (101, 18), (106, 21), (127, 23)]


def edge(y):
    for (y0, x0), (y1, x1) in zip(K, K[1:]):
        if y0 <= y <= y1:
            return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def pelo(x, y):                  # mechones en S: baldosa de 16 x 16 que se repite
    t = (y + 5 * math.sin(2 * math.pi * x / 16)) % 16
    return '3' if t < 2 else '2' if t < 9 else '1' if t < 11 else '2'


def body():
    c = C(W, H)
    p = c.p
    for y in range(H):
        e = edge(y)
        nuca = 38 if y < 96 else 32
        for x in range(W):
            casco = y < 34 and x >= e + 6 and y < 10 + (x - e) * 1.2      # pelo que cubre la cabeza
            if x >= nuca or casco:
                p[y][x] = pelo(x, y)
            elif x >= e:
                p[y][x] = '3' if x - e < 16 else '2'                      # mármol con sombra hacia la nuca
    for y in range(12, 17):                                              # diadema
        for x in range(int(edge(y)) + 6, 40):
            if p[y][x] != '.':
                p[y][x] = '3' if y in (12, 16) else '1'
    ex, ey = EYE_CX, EYE_CY
    for x in range(ex - 5, ex + 3): p[ey - 5][x] = '2'                    # ceja
    for y in range(ey - 3, ey + 5):                                      # cuenca del ojo en sombra suave
        for x in range(ex - 5, ex + 3):
            if p[y][x] == '3' and (y - ey - 1) ** 2 / 16 + (x - ex + 1) ** 2 / 16 < 1: p[y][x] = '2'
    for x in range(int(edge(63)) + 2, int(edge(63)) + 5): p[63][x] = '1'   # aleta de la nariz
    for x in range(int(edge(73)) + 1, int(edge(73)) + 8): p[73][x] = '1'   # labios
    for x in range(int(edge(76)) + 2, int(edge(76)) + 6): p[76][x] = '2'
    for y in range(86, 99):                                              # sombra bajo la barbilla
        for x in range(int(edge(y)) + 5, int(edge(y)) + 16): p[y][x] = '2'
    for y in range(104, 128, 6):                                         # pliegues del cuello
        for x in range(int(edge(y)) + 3, int(edge(y)) + 7): p[y][x] = '2'
    return c


def eye(c, st):
    p = c.p
    ex, ey = EYE_CX, EYE_CY
    if st:                                                               # con destello: las celdas del ojo sin PF2
        for y in range(EYE_ROWS[0] * 8, EYE_ROWS[-1] * 8 + 8):
            for x in range(EYE_C0 * 4, (EYE_C0 + EYE_NC) * 4):
                if p[y][x] == '3': p[y][x] = '2'
    if st == 0:
        for x in range(ex - 4, ex + 2): p[ey + 1][x] = '1'               # párpado cerrado
        for x in range(ex - 3, ex + 1): p[ey + 2][x] = '2'
    elif st == 1:
        for x in range(ex - 3, ex + 2): p[ey][x] = '1'; p[ey + 1][x] = '4'
    else:
        for y in range(ey - 1, ey + 4):
            for x in range(ex - 3, ex + 2):
                if abs(y - ey - 1) * 2 + abs(x - ex + 1) * 2 <= 5: p[y][x] = '4'
        p[ey][ex - 2] = '2'                                              # brillo de la perla
    return c


def boss(state=0):
    return eye(body(), state)
