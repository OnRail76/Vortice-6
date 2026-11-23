"""FERRUM-9 · el compactador soberano (versión 2). Mira a la izquierda. 64 x 112 píxeles (16 x 14 caracteres).

Dos mandíbulas largas con dientes; entre ellas, la "boca" (el único refugio durante la compactación).
El ojo está al fondo de la boca, en la cara del cuerpo: tres estados (cerrado, entreabierto, abierto).
PF0 = sombra, PF1 = óxido, PF2 = acero, PF3 = rojo (luces y pupila; late).
"""
from canvas import C

W, H = 64, 112
FACE = 24            # x de la cara del cuerpo
EYE_CX, EYE_CY = 32, 56
POCKET_Y0, POCKET_Y1 = 46, 65     # hueco entre los dientes


def body():
    c = C(W, H)
    # cuerpo blindado
    c.rect(FACE, 0, 63, 111, '1')
    c.box(FACE, 0, 63, 111, '3')
    c.box(FACE + 2, 2, 61, 109, '2')
    for y in range(8, 104, 16):                 # placas del blindaje
        c.rect(FACE + 6, y, 58, y, '2')
    for y in (14, 40, 70, 96):                  # rejillas
        c.rect(50, y, 58, y + 1, '3')
        c.rect(50, y + 3, 58, y + 4, '3')
    # pistones hidráulicos que sujetan las mandíbulas
    for k in range(3):
        c.line(10 + k, 26, FACE + 2 + k, 8, '3')
        c.line(10 + k, 85, FACE + 2 + k, 103, '3')
    # mandíbula superior
    c.rect(0, 26, FACE + 2, 41, '2')
    c.rect(0, 26, FACE + 2, 27, '3')
    c.rect(2, 30, FACE, 33, '1')
    c.rect(0, 26, 3, 41, '3')
    for x in range(1, FACE, 4):                 # dientes hacia abajo
        c.rect(x, 42, x + 2, 43, '3')
        c.rect(x + 1, 44, x + 1, 45, '3')
    # mandíbula inferior (simétrica)
    c.rect(0, 70, FACE + 2, 85, '2')
    c.rect(0, 84, FACE + 2, 85, '3')
    c.rect(2, 78, FACE, 81, '1')
    c.rect(0, 70, 3, 85, '3')
    for x in range(1, FACE, 4):
        c.rect(x, 68, x + 2, 69, '3')
        c.rect(x + 1, 66, x + 1, 67, '3')
    # luces de aviso rojas (PF3) en celdas sin acero
    for (x, y) in ((44, 20), (44, 88)):
        c.rect(x, y, x + 3, y + 3, '4')
    # cuenca del ojo
    c.ell(EYE_CX, EYE_CY, 10, 10, '1')
    return c


def eye(c, state):
    """0 cerrado (persianas de acero), 1 entreabierto (rendija roja), 2 abierto (iris rojo y pupila)"""
    cx, cy = EYE_CX, EYE_CY
    for y in range(48, 64):                    # celdas del ojo: sin acero (PF2) para poder usar el rojo (PF3)
        for x in range(24, 44):
            if c.p[y][x] == '3': c.p[y][x] = '2'
    c.ell(cx, cy, 8, 8, '1')
    if state == 0:
        for y in range(cy - 7, cy + 8, 3):
            c.rect(cx - 6, y, cx + 6, y + 1, '2')
    elif state == 1:
        for y in list(range(cy - 7, cy - 2, 3)) + list(range(cy + 3, cy + 8, 3)):
            c.rect(cx - 6, y, cx + 6, y + 1, '2')
        c.rect(cx - 6, cy - 1, cx + 6, cy + 1, '4')
    else:
        c.ell(cx, cy, 7, 7, '4')
        c.ell(cx - 1, cy, 3, 4, '.')
    return c


def boss(state=0):
    return eye(body(), state)
