"""SATURNUS · EL OFICIANTE VACÍO · jefe de la fase 4 · propuestas (20 x 16 caracteres = 80 x 128 píxeles). Mira a la izquierda.
Colores de la fase 4: 1 = PF0 violeta · 2 = PF1 oro envejecido · 3 = PF2 jade pálido (bordes) · 4 = PF3 (sello / vacío que late)
Se dibuja con polígonos en coordenadas de pantalla (cada píxel ANTIC 4 es el doble de ancho que de alto: x de 0 a 160),
todo angular: nada redondeado.
"""
W, H = 80, 128


def blank(): return [['.'] * W for _ in range(H)]


def inside(pts, X, Y):
    c = False
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        if (y1 > Y) != (y2 > Y) and X < (x2 - x1) * (Y - y1) / (y2 - y1) + x1: c = not c
    return c


def poly(p, pts, fill='1', edge='3', pat=None):
    """rellena el polígono (x en unidades de pantalla 0-160, y en líneas); borde jade de un píxel"""
    m = [[inside(pts, 2 * x + 1, y + 0.5) for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            if not m[y][x]: continue
            border = any(not (0 <= y + dy < H and 0 <= x + dx < W and m[y + dy][x + dx])
                         for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if border and edge: p[y][x] = edge
            else: p[y][x] = pat(x, y) if pat else fill
    return m


def line(p, x0, y0, x1, y1, ch='3'):
    n = max(abs(x1 - x0) // 2, abs(y1 - y0), 1)
    for i in range(n + 1):
        x = round((x0 + (x1 - x0) * i / n - 1) / 2); y = round(y0 + (y1 - y0) * i / n)
        if 0 <= x < W and 0 <= y < H: p[y][x] = ch


def fix(p):  # ninguna celda 4x8 puede mezclar PF2 (3) y PF3 (4): el borde cede
    for cy in range(H // 8):
        for cx in range(W // 4):
            cell = [p[cy * 8 + y][cx * 4 + x] for y in range(8) for x in range(4)]
            if '4' in cell and '3' in cell:
                for y in range(8):
                    for x in range(4):
                        if p[cy * 8 + y][cx * 4 + x] == '3': p[cy * 8 + y][cx * 4 + x] = '2'


def tela(x, y):   # tela de la túnica: violeta con pliegues verticales de oro
    return '2' if x % 6 == 0 else '1'


def sillar(x, y):
    return '2' if y % 16 == 0 or (x + (y // 16) * 4) % 8 == 0 else '1'


def anillo(p, cx, cy, rx, ry, grosor=5, ch='2', inc=-0.35):
    """anillo de Saturno visto de canto: octágono alargado e inclinado (solo la banda)"""
    import math
    def octo(rx_, ry_):
        pts = []
        for k in range(8):
            a = math.pi / 8 + k * math.pi / 4
            x, y = rx_ * math.cos(a), ry_ * math.sin(a)
            pts.append((cx + x * math.cos(inc) - y * math.sin(inc), cy + x * math.sin(inc) + y * math.cos(inc)))
        return pts
    out = [[inside(octo(rx, ry), 2 * x + 1, y + .5) for x in range(W)] for y in range(H)]
    inn = [[inside(octo(rx - 2 * grosor, ry - grosor), 2 * x + 1, y + .5) for x in range(W)] for y in range(H)]
    band = [[out[y][x] and not inn[y][x] for x in range(W)] for y in range(H)]
    return band


def paint(p, mask, ch, only_empty=False, edge=None):
    for y in range(H):
        for x in range(W):
            if mask[y][x] and (not only_empty or p[y][x] == '.'):
                b = edge and any(not (0 <= y + dy < H and 0 <= x + dx < W and mask[y + dy][x + dx])
                                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                p[y][x] = edge if b else ch


# ===================================================================================================
def oficiante(st=0):
    """A · EL OFICIANTE: sacerdote con capucha-mitra de perfil, el anillo de Saturno como halo alrededor de la cabeza.
    Donde debería estar la cara solo hay VACÍO (un arco apuntado negro con un sello que late). Sostiene el cáliz."""
    p = blank()
    # túnica: exenta (no toca la pared), cae desde los hombros, frente y espalda inclinados; pliegues de oro cada dos caracteres (comprime bien)
    poly(p, [(64, 56), (122, 50), (134, 110), (40, 110), (50, 92)], pat=lambda x, y: '2' if x % 8 == 0 else '1')
    # estola de oro que baja por delante, con anillos bordados
    poly(p, [(60, 60), (76, 58), (68, 110), (50, 110)], fill='2')
    # brazo y manga hacia delante, puño de oro
    poly(p, [(60, 72), (104, 66), (100, 84), (40, 90)], fill='1')
    poly(p, [(34, 82), (46, 80), (44, 92), (32, 94)], fill='2')
    # cáliz: copa, nudo y pie (oro con borde jade)
    poly(p, [(2, 60), (40, 60), (30, 74), (12, 74)], fill='2')
    poly(p, [(18, 74), (24, 74), (24, 86), (18, 86)], fill='2')
    poly(p, [(8, 86), (34, 86), (28, 94), (14, 94)], fill='2')
    # capucha-mitra: punta alta, frente que cae hacia delante, nuca hasta los hombros
    poly(p, [(84, 0), (114, 12), (130, 58), (64, 62), (42, 46), (50, 16)], pat=lambda x, y: '2' if y % 16 == 0 else '1')
    # el VACÍO: arco apuntado negro donde estaría la cara
    poly(p, [(54, 22), (66, 14), (80, 22), (82, 52), (52, 54)], fill='.', edge='3')
    if st >= 1:                  # 1: dos puntos-ojo en el vacío; 2: el vacío arde entero (solo filas de carácter 3 y 4)
        for y in range(24, 40):
            for x in range(26, 41):
                if p[y][x] != '.': continue
                if st == 2 and abs(x - 33) * 2 + abs(y - 32) < 13: p[y][x] = '4'
                elif st == 1 and (y in (29, 30) and x in (29, 30, 35, 36) or y == 37 and 29 <= x <= 36): p[y][x] = '4'
    fix(p)
    return p


def sarcofago(st=0):
    """B · EL SARCÓFAGO: sarcófago antropomorfo en pie, de perfil; máscara de oro con tocado a rayas y brazos cruzados.
    La tapa se desliza hacia delante y deja ver el VACÍO del pecho: ese es el punto débil."""
    p = blank()
    # caja del sarcófago (detrás): bloque achaflanado de piedra violeta
    poly(p, [(84, 0), (160, 0), (160, 128), (84, 128), (76, 116), (76, 8)], pat=sillar)
    abre = (0, 6, 14)[st]          # la tapa se desplaza a la izquierda
    # tapa con forma de figura: cabeza, hombros, cuerpo que se estrecha hacia los pies
    tapa = [(92 - abre, 4), (118 - abre, 2), (122 - abre, 30), (128 - abre, 40), (124 - abre, 118), (96 - abre, 126),
            (70 - abre, 116), (60 - abre, 44), (66 - abre, 34)]
    poly(p, tapa, pat=lambda x, y: '2' if y % 6 < 2 else '1')               # tocado / vendas a rayas
    # máscara de perfil (oro macizo): frente, nariz, labios, barbilla y barba ceremonial
    poly(p, [(66, 8), (88, 6), (92, 30), (82, 34), (72, 34), (70, 28), (62, 24), (64, 18)], fill='2')
    poly(p, [(72, 34), (80, 34), (78, 46), (74, 46)], fill='2')                 # barba
    poly(p, [(70, 14), (78, 13), (78, 16), (70, 17)], fill='.', edge='3')       # ojo
    # brazos cruzados con el cayado y el mayal (oro)
    poly(p, [(58, 50), (104, 46), (102, 56), (56, 62)], fill='2')
    poly(p, [(60, 62), (104, 58), (100, 68), (56, 72)], fill='2')
    poly(p, [(46, 40), (54, 40), (62, 74), (56, 76)], fill='2')               # cayado
    poly(p, [(40, 46), (46, 46), (52, 76), (46, 78)], fill='2')               # mayal
    # el pecho: hueco del VACÍO entre la tapa y la caja (se ve más cuanto más se abre)
    if st >= 1:
        poly(p, [(74 - abre, 76), (96 - abre, 74), (98 - abre, 104), (76 - abre, 106)], fill='.', edge='3')
        for y in range(76, 106):
            for x in range(36 - abre // 2, 50 - abre // 2):
                if 0 <= x < W and p[y][x] == '.' and ((x + y) % 4 == 0 or st == 2 and (x * 2 + y) % 3 == 0):
                    p[y][x] = '4'
    # jeroglíficos de anillos en la caja
    for cy_ in (20, 52, 84, 108):
        paint(p, anillo(p, 140, cy_, 12, 4, 2, inc=-0.2), '3')
    fix(p)
    return p


def planeta(st=0):
    """C · EL ALTAR-PLANETA: Saturno como un altar: esfera facetada (octógono) cruzada por su anillo, sobre un zigurat
    escalonado. En la esfera, la máscara vacía del Oficiante; su ojo-pozo es el punto débil."""
    p = blank()
    # zigurat: tres gradas desde el suelo
    for i, (x0, y0) in enumerate(((40, 104), (60, 88), (84, 72))):
        poly(p, [(x0, y0), (160, y0), (160, 128 if i == 0 else y0 + 16), (x0, 128 if i == 0 else y0 + 16)], pat=sillar)
    # esfera facetada
    import math
    sph = [(96 + 46 * math.cos(math.pi / 8 + k * math.pi / 4), 46 + 40 * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    poly(p, sph, pat=lambda x, y: '2' if (y - 46) ** 2 // 30 % 7 == 0 else '1')
    # máscara: frente y cejas de oro, ojo-pozo
    poly(p, [(56, 28), (96, 22), (100, 34), (60, 38)], fill='2')
    poly(p, [(60, 54), (92, 52), (88, 70), (66, 72)], fill='2')                 # boca / mandíbula
    poly(p, [(64, 38), (90, 36), (88, 50), (66, 52)], fill='.', edge='3')       # ojo-pozo
    if st >= 1:
        for y in range(38, 52):
            for x in range(33, 45):
                if p[y][x] == '.' and ((x + y) % 3 == 0 or st == 2): p[y][x] = '4'
    # anillo de canto que cruza la esfera (por delante)
    band = anillo(p, 96, 50, 78, 14, 4, inc=-0.25)
    paint(p, band, '2', edge='3')
    fix(p)
    return p


DISENOS = [('A · EL OFICIANTE', oficiante,
            'Sacerdote encapuchado de perfil, con el anillo de Saturno como halo. Donde está la cara, solo hay vacío: '
            'un hueco negro con un sello que late. Sostiene el cáliz de las ofrendas.'),
           ('B · EL SARCÓFAGO', sarcofago,
            'Sarcófago antropomorfo en pie: máscara de oro de perfil, tocado a rayas y brazos cruzados. La tapa se '
            'desliza hacia delante y deja ver el vacío del pecho, el punto débil.'),
           ('C · EL ALTAR-PLANETA', planeta,
            'Saturno convertido en altar: esfera facetada cruzada por su anillo, sobre un zigurat. En la esfera, la '
            'máscara del Oficiante; su ojo-pozo se abre.')]


# ---- interfaz para el motor (diseño A elegido, sin anillo)
BOSS_K, BOSS_R = 23, 2
EXENTO = True                    # no está pegado a la pared: el suelo y el fondo se ven alrededor (levita sobre el suelo)
FILAS = 14                       # ocupa las filas 2-15; las 16-17 son el suelo de la arena
FACE = 20                        # frente de la capucha delante del vacío: desde ahí empieza la zona de impacto
EYE_CX, EYE_CY = 33, 32          # el VACÍO (punto débil)
EYE_ROWS, EYE_C0, EYE_NC = (3, 4), 5, 6
MOUTH_Y0, MOUTH_Y1 = 34, 56      # ofrendas: desde el vacío y desde el cáliz
POCKET_Y0, POCKET_Y1 = 56, 72


def boss(state=0):
    """0 vacío negro · 1 aparecen los ojos (aviso) · 2 el vacío arde: vulnerable"""
    from canvas import C
    c = C(W, H); c.p = oficiante(state)
    return c
