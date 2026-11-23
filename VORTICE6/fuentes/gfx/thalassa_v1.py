"""THALASSA · la Madre de las Mareas. Leviatán transparente de aspecto crustáceo con un corazón de perla
dentro de una concha. Mira a la izquierda. 64 x 112 píxeles (16 x 14 caracteres): mismo marco que FERRUM-9.

La perla está en las celdas del "ojo" (x 24-43, y 48-63): tres estados (concha cerrada, entreabierta, abierta).
Entre las dos pinzas queda libre la línea de tiro hacia la perla.
Colores (los de la fase 2): 1 = PF0 verde (órganos, sombra) · 2 = PF1 cian (cuerpo transparente)
3 = PF2 blanco perla (contornos) · 4 = PF3 corriente que late (perla, luces internas)
"""
from canvas import C

W, H = 64, 112
FACE = 24
EYE_CX, EYE_CY = 33, 56
POCKET_Y0, POCKET_Y1 = 46, 65


def _poly(c, pts, col):
    for y in range(H):
        xs = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(round(xs[i])), int(round(xs[i + 1])) + 1):
                if 0 <= x < W: c.p[y][x] = col


def body():
    c = C(W, H)
    # aletas exteriores (abanicos con radios), arriba y abajo a la derecha
    for top in (True, False):
        def Y(y): return y if top else 111 - y
        for k in range(7):
            x0 = 44 + k * 3
            for y in range(0, 22 - k):
                c.p[Y(y)][min(63, x0 + y // 4)] = '2' if k % 2 else '3'
    # caparazón: arco de placas (elipse) y cabeza que rodea la concha
    c.ell(48, 56, 16, 50, '2')
    c.ell(36, 56, 13, 20, '2')
    # pinzas: brazo curvo, pinza grande con dientes en el borde interior
    for top in (True, False):
        def Y(y): return y if top else 111 - y
        _poly(c, [(26, Y(30)), (14, Y(24)), (4, Y(18)), (0, Y(22)), (2, Y(28)), (10, Y(34)), (22, Y(40)), (28, Y(40))], '2')
        _poly(c, [(12, Y(36)), (4, Y(40)), (0, Y(44)), (3, Y(45)), (10, Y(42)), (18, Y(40))], '2')
        for x in range(2, 14, 3): c.p[Y(30 if x < 6 else 32)][x] = '1'
        for x in range(3, 12, 3): c.p[Y(42)][x + 1] = '1'      # dientes
    # contorno blanco perla de todo lo que es cuerpo
    for y in range(H):
        for x in range(W):
            if c.p[y][x] == '2' and any(c.get(x + dx, y + dy) in (None, '.') for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                c.p[y][x] = '3'
    # placas del caparazón (arcos) y órganos vistos por transparencia
    for y0 in range(14, 104, 13):
        for x in range(40, 63):
            yy = y0 + (x - 52) * (x - 52) // 24
            if 0 <= yy < H and c.p[yy][x] == '2': c.p[yy][x] = '3'
    for (x, y, rx, ry) in ((52, 30, 4, 7), (54, 82, 4, 7), (56, 56, 3, 12)):
        c.ell(x, y, rx, ry, '1')
    for y in range(20, 92, 4):                            # cordón nervioso
        if c.p[y][46] == '2': c.p[y][46] = '1'
    # antenas largas
    for top in (True, False):
        for k in range(28):
            x = 30 - k; y = (34 - k) if top else (77 + k)
            if 0 <= x < W and 0 <= y < H and c.p[y][x] == '.': c.p[y][x] = '3'
    # luces internas (PF3) en celdas sin contorno
    for (x, y) in ((52, 44), (52, 64)):
        c.rect(x, y, x + 3, y + 3, '4')
    return c


def shell(c, state):
    """0 concha cerrada · 1 entreabierta (brillo dentro) · 2 abierta: la perla"""
    cx, cy = EYE_CX, EYE_CY
    for y in range(48, 64):                              # celdas de la perla: sin blanco (PF2) para usar PF3
        for x in range(24, 44):
            if c.p[y][x] == '3': c.p[y][x] = '2'
    c.ell(cx, cy, 9, 8, '1')
    def valva(arriba, gap):
        for y in range(48, 64):
            d = (cy - y) if arriba else (y - cy)
            if d < gap: continue
            w = int(8 * (1 - ((d - gap) / (9 - gap + 0.01)) ** 2) ** 0.5) if d - gap < 9 - gap else 0
            for x in range(cx - w, cx + w + 1):
                c.p[y][x] = '1' if (x - cx) % 3 == 0 else '2'   # estrías de la concha
    if state == 0:
        valva(True, 0); valva(False, 1)
        for x in range(cx - 8, cx + 9): c.p[cy][x] = '1'
    elif state == 1:
        valva(True, 2); valva(False, 2)
        for x in range(cx - 6, cx + 7): c.p[cy][x] = '4'
    else:
        valva(True, 6); valva(False, 6)
        c.ell(cx, cy, 5, 5, '4')
        c.rect(cx - 2, cy - 3, cx - 1, cy - 2, '2')      # brillo de la perla
    return c


def boss(state=0):
    c = shell(body(), state)
    # ninguna celda puede mezclar PF2 y PF3
    for cy in range(H // 8):
        for cx in range(W // 4):
            cell = [c.p[cy * 8 + y][cx * 4 + x] for y in range(8) for x in range(4)]
            if '4' in cell and '3' in cell:
                for y in range(8):
                    for x in range(4):
                        if c.p[cy * 8 + y][cx * 4 + x] == '3': c.p[cy * 8 + y][cx * 4 + x] = '2'
    return c
