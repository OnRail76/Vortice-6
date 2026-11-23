"""EL TRÍPTICO DE HADES · propuestas (20 x 16 caracteres, como THALASSA). Mira a la izquierda.
Tres rostros apilados: FURIA (arriba), HAMBRE (centro, boca-horno), CENIZA (abajo); cada uno con su SELLO (PF3 que late).
Colores de la fase 3: 1 = PF0 basalto · 2 = PF1 lava naranja · 3 = PF2 amarillo caliente · 4 = PF3 sello / brasa
"""
W, H = 80, 128

FURIA = [
    "3..............3",
    "33............33",
    ".322........223.",
    "..221111111122..",
    ".12222244222221.",
    ".12333244233321.",
    ".12223322332221.",
    ".12144222244121.",
    ".12111222211121.",
    ".12222211222221.",
    ".12222111122221.",
    ".12111111111121.",
    ".11332332332311.",
    ".13111111111131.",
    ".11332332332311.",
    ".12111111111121.",
    "..122222222221..",
    "...1222222221...",
    "....11111111....",
    "................"]
HAMBRE = [  # boca de horno; estado 0 cerrada, 1 abierta (rejilla y fuego dentro)
    "....2222222222....",
    "..22111144111122..",
    ".2211111441111122.",
    ".2112222222222112.",
    "21122442222442112.",
    "211224422224421122",
    "211222222222222112",
    "211122222222221112",
    "211113333333311112",
    "211131111111131112",
    "211311111111113112",
    "213111111111111312",
    "213111111111111312",
    "211311111111113112",
    "211131111111131112",
    "211113333333311112",
    ".2111111111111112.",
    ".2211111111111122.",
    "..22111111111122..",
    "....2222222222....",
    "..................",
    ".................."]
HAMBRE_ABIERTA_CENTRO = ["31313131", "13131313", "4444444.", "44.44444", "4444444.", "13131313"]  # filas 9-14, cols 5-12
CENIZA = [
    "................",
    "....11111111....",
    "...1222222221...",
    "..122224422221..",
    ".12222244222221.",
    ".12222222222221.",
    ".12111222211121.",
    ".12333222233321.",
    ".12222211222221.",
    ".12212211221221.",
    ".12222111122221.",
    ".12222222222221.",
    ".12211111111221.",
    ".12222222222221.",
    "..122221222221..",
    "...1222122221...",
    "....11112111....",
    "......1.1.......",
    ".....1...1......",
    "................"]


def fix(p):  # ninguna celda 4x8 puede mezclar PF2 (3) y PF3 (4)
    for cy in range(len(p) // 8):
        for cx in range(len(p[0]) // 4):
            cell = [p[cy * 8 + y][cx * 4 + x] for y in range(8) for x in range(4)]
            if '4' in cell and '3' in cell:
                for y in range(8):
                    for x in range(4):
                        if p[cy * 8 + y][cx * 4 + x] == '3': p[cy * 8 + y][cx * 4 + x] = '2'


def paste(p, art, x0, y0):
    for y, r in enumerate(art):
        for x, ch in enumerate(r):
            if ch != '.' and 0 <= y0 + y < H and 0 <= x0 + x < W: p[y0 + y][x0 + x] = ch


def totem(boca=0):
    """A · TÓTEM: pilar de basalto con cuernos; los tres rostros salen hacia delante sobre ménsulas, unidos por cadenas"""
    p = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(36, W):
            v = '1'
            if y % 16 == 0 or (x - 36 + (y // 16) * 6) % 12 == 0: v = '2'          # sillares
            if x == 36: v = '3'
            p[y][x] = v
    for k in range(10):                                                     # cuernos del pilar
        for t in range(3):
            if 0 <= 10 - k < H: p[max(0, 9 - k)][32 - k + t] = '3'
    for (y0, art, x0) in ((6, FURIA, 18), (48, HAMBRE, 14), (96, CENIZA, 18)):
        for y in range(y0 + 6, y0 + 14):                                      # ménsula
            for x in range(x0 + 12, 37): p[y][x] = '1' if y not in (y0 + 6, y0 + 13) else '3'
        paste(p, art, x0, y0)
    if boca:
        paste(p, HAMBRE_ABIERTA_CENTRO, 14 + 5, 48 + 9)
    for y in range(26, 48, 2): p[y][24] = '3'                               # cadenas
    for y in range(70, 96, 2): p[y][24] = '3'
    fix(p)
    return p


def altar(boca=0):
    """B · RETABLO: tres hornacinas apiladas con arco apuntado (el retablo de un altar), la del centro más grande"""
    p = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(10, W):
            p[y][x] = '1' if (x + y) % 9 else '2'
    def nicho(x0, y0, w, h):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                d = min(x - x0, x0 + w - 1 - x)
                top = y0 + max(0, (w // 2 - d) - w // 4)
                if y < top: continue
                edge = d == 0 or y == top or y == y0 + h - 1
                p[y][x] = '3' if edge else '.'
    nicho(12, 2, 24, 30); nicho(8, 40, 28, 40); nicho(12, 92, 24, 30)
    paste(p, FURIA, 16, 10); paste(p, HAMBRE, 13, 54); paste(p, CENIZA, 16, 100)
    if boca: paste(p, HAMBRE_ABIERTA_CENTRO, 13 + 5, 54 + 9)
    for x in range(10, W, 6):                                               # pináculos
        p[0][x] = '3'; p[1][x] = '3'
    fix(p)
    return p


def x2(art):
    return [''.join(ch * 2 for ch in r) for r in art for _ in range(2)]


def totem2(boca=0):
    """A · TÓTEM grande: tres máscaras a doble tamaño apiladas sobre el pilar (cada una, un tercio del alto)"""
    p = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(44, W):
            v = '1'
            if y % 16 == 0 or (x - 44 + (y // 16) * 8) % 16 == 0: v = '2'
            if x == 44: v = '3'
            p[y][x] = v
    hb = [list(r) for r in HAMBRE]
    if boca:
        for dy, r in enumerate(HAMBRE_ABIERTA_CENTRO):
            for dx, ch in enumerate(r):
                if ch != '.': hb[9 + dy][5 + dx] = ch
    hb = [''.join(r) for r in hb]
    for (y0, art, x0) in ((0, FURIA, 10), (41, hb, 6), (88, CENIZA, 10)):
        a = x2(art)
        for y in range(y0 + 12, min(H, y0 + 28)):                       # ménsula hacia el pilar
            for x in range(x0 + 24, 45): p[y][x] = '1' if y not in (y0 + 12, y0 + 27) else '3'
        paste(p, a, x0, y0)
    fix(p)
    return p


def altar2(boca=0):
    """B · RETABLO grande: tres hornacinas con arco apuntado, máscaras a doble tamaño"""
    p = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(42, W):
            p[y][x] = '1' if (x // 4 + y // 8) % 2 else '2' if (y % 8 == 0 or x % 4 == 0) else '1'
    def nicho(x0, y0, w, h):
        for y in range(y0, min(H, y0 + h)):
            for x in range(x0, x0 + w):
                d = min(x - x0, x0 + w - 1 - x)
                top = y0 + max(0, (w // 2 - d) - w // 3)
                if y < top: continue
                edge = d <= 1 or y == top
                p[y][x] = '3' if edge else ('1' if (x + y) % 2 else '.')
    nicho(4, 0, 44, 42); nicho(0, 42, 48, 46); nicho(4, 88, 44, 40)
    hb = [list(r) for r in HAMBRE]
    if boca:
        for dy, r in enumerate(HAMBRE_ABIERTA_CENTRO):
            for dx, ch in enumerate(r):
                if ch != '.': hb[9 + dy][5 + dx] = ch
    paste(p, x2(FURIA), 10, 2); paste(p, x2([''.join(r) for r in hb]), 6, 43); paste(p, x2(CENIZA), 10, 88)
    fix(p)
    return p


# ---- interfaz para el motor (mismo marco que FERRUM-9 y THALASSA)
BOSS_K, BOSS_R = 23, 2
FACE = 6                         # x de la máscara de HAMBRE: delante empieza la zona de impacto
EYE_CX, EYE_CY = 24, 64          # boca-horno de HAMBRE (el punto débil)
EYE_ROWS, EYE_C0, EYE_NC = (7, 8), 3, 6
MOUTH_Y0, MOUTH_Y1 = 24, 110     # ráfagas desde la boca de FURIA y de CENIZA
POCKET_Y0, POCKET_Y1 = 56, 72


def boss(state=0):
    """0 boca cerrada · 1 el horno se calienta (brillo dentro) · 2 horno abierto: vulnerable"""
    p = totem2(1 if state == 2 else 0)
    if state == 1:
        for y in range(59, 70, 2):
            for x in range(16, 32):
                if p[y][x] == '1': p[y][x] = '4'
        fix(p)
    from canvas import C
    c = C(W, H); c.p = p
    return c
