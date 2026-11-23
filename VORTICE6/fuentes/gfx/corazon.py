"""EL CORAZÓN NULO · jefe final (fase 5) · propuestas (20 x 16 caracteres = 80 x 128 píxeles). Mira a la izquierda.
Colores de la fase 5: 1 = PF0 carne roja · 2 = PF1 verde enfermizo · 3 = PF2 hueso (bordes) · 4 = PF3 (pupila / reactor que late)
Dibujado con polígonos angulares (nada redondeado), en coordenadas de pantalla (x 0-160, y 0-128).
"""
import math
from saturnus import W, H, blank, poly, paint, fix, inside


def octo(cx, cy, rx, ry, rot=math.pi / 8):
    return [(cx + rx * math.cos(rot + k * math.pi / 4), cy + ry * math.sin(rot + k * math.pi / 4)) for k in range(8)]


def carne(x, y):        # tejido: rojo con fibras verdes horizontales (alineadas a la celda: caben en el juego de caracteres)
    return '2' if y % 8 == 4 and x % 4 != 3 else '1'


def placa(x, y):        # blindaje: verde con remaches de hueso
    return '3' if x % 4 == 1 and y % 8 == 3 else '2'


def arteria(p, y0, y1, x0, fill='2'):
    """arteria: tubo de x0 hasta la pared derecha, con anillos de hueso cada 12"""
    poly(p, [(x0, y0), (160, y0 - 2), (160, y1 + 2), (x0, y1)], pat=lambda x, y: '3' if x % 8 == 0 else fill)


def pupila(p, st, cx, cy, h):
    """0 cerrada (rendija) · 1 se dilata (latido) · 2 abierta: reactor expuesto"""
    w = (4, 10, 16)[st]
    pts = [(cx, cy - h), (cx + w, cy - h // 2), (cx + w, cy + h // 2), (cx, cy + h), (cx - w, cy + h // 2), (cx - w, cy - h // 2)]
    m = poly(p, pts, fill='.', edge='3')
    if st >= 1:
        for y in range(H):
            for x in range(W):
                if m[y][x] and p[y][x] == '.' and (st == 2 or (x + y) % 3 == 0): p[y][x] = '4'


def blindado(st=0):
    """A · EL CORAZÓN BLINDADO: esfera facetada de carne y blindaje con tres arterias hacia la pared;
    las uniones de las arterias son los NODOS de energía; la pupila mira a la nave"""
    p = blank()
    for y0, y1 in ((14, 26), (58, 70), (102, 114)): arteria(p, y0, y1, 110)
    poly(p, octo(84, 64, 64, 58), pat=carne)
    # placas de blindaje angulares alrededor (arriba, abajo y atrás)
    poly(p, [(40, 14), (84, 4), (128, 14), (116, 28), (84, 20), (52, 28)], pat=placa)
    poly(p, [(40, 114), (84, 124), (128, 114), (116, 100), (84, 108), (52, 100)], pat=placa)
    poly(p, [(30, 40), (44, 34), (44, 94), (30, 88)], pat=placa)
    # nodos de energía en las uniones
    for yc in (20, 64, 108):
        poly(p, octo(136, yc, 10, 9), fill='2')
    # ojo: párpado de hueso y pupila
    poly(p, [(48, 46), (96, 42), (112, 64), (96, 86), (48, 82), (40, 64)], fill='.', edge='3')
    pupila(p, st, 74, 64, 16)
    fix(p)
    return p


def valvula(st=0):
    """B · EL OJO-VÁLVULA: un ojo enorme sujeto por cuatro tendones al techo y al suelo; el iris son pétalos de
    músculo que se abren como un diafragma (solo cambian las dos filas centrales: el resto es fijo)"""
    p = blank()
    tend = lambda x, y: '3' if y % 8 == 0 else ('1' if x % 6 == 0 else '2')   # tubos de acero con anillos
    for x0 in (64, 112):                                                                   # tendones (alineados a celdas)
        poly(p, [(x0, 0), (x0 + 24, 0), (x0 + 24, 24), (x0 + 16, 32), (x0 + 8, 32), (x0, 24)], pat=tend)
        poly(p, [(x0 + 8, 96), (x0 + 16, 96), (x0 + 24, 104), (x0 + 24, 128), (x0, 128), (x0, 104)], pat=tend)
    poly(p, [(16, 64), (56, 24), (136, 24), (160, 48), (160, 80), (136, 104), (56, 104)], pat=carne)   # párpados de carne
    poly(p, [(28, 64), (64, 34), (120, 34), (144, 64), (120, 94), (64, 94)], fill='2')                   # globo
    poly(p, [(56, 64), (72, 40), (104, 40), (120, 64), (104, 88), (72, 88)], fill='1')                  # iris
    for (ax, ay, bx, by, cx, cy) in ((72, 40, 104, 40, 88, 56), (72, 88, 104, 88, 88, 72),            # pétalos: arriba, abajo
                                     (56, 64, 72, 40, 80, 56), (56, 64, 72, 88, 80, 72),               # y los cuatro laterales
                                     (120, 64, 104, 40, 96, 56), (120, 64, 104, 88, 96, 72)):
        poly(p, [(ax, ay), (bx, by), (cx, cy)], fill='1')
    # las dos filas del ojo (56-71): 0 válvula cerrada (rendija) · 1 se entreabre y late · 2 abierta: reactor
    for y in range(56, 72):
        for x in range(30, 58):
            if p[y][x] == '.': continue
            d = abs(y - 63.5)
            if st == 0 and d < 1 and 36 <= x <= 51: p[y][x] = '3'
            elif st == 1 and d < 3 and 34 <= x <= 53: p[y][x] = '4' if (x + y) % 2 else '.'
            elif st == 2 and d < 7 and 32 <= x <= 55: p[y][x] = '4'
    fix(p)
    return p


def cosido(st=0):
    """C · EL NÚCLEO COSIDO: masa de carne cosida con grapas de hueso y trozos de los cuatro jefes caídos:
    placa de FERRUM-9 arriba, mechones de THALASSA detrás, cuernos del TRÍPTICO y la capucha de SATURNUS;
    en el centro, la pupila-reactor"""
    p = blank()
    poly(p, [(30, 60), (52, 14), (110, 6), (156, 30), (156, 100), (112, 122), (54, 116)], pat=carne)
    poly(p, [(56, 8), (112, 2), (118, 24), (60, 28)], pat=lambda x, y: '3' if y % 8 == 4 and x % 4 == 1 else '2')   # placa FERRUM
    for k in range(4):                                                                      # mechones THALASSA
        y = 40 + 18 * k
        poly(p, [(132, y), (160, y - 6), (160, y + 2), (138, y + 8)], fill='2')
    poly(p, [(36, 30), (50, 24), (44, 44)], fill='3', edge='3'); poly(p, [(40, 100), (54, 106), (46, 88)], fill='3', edge='3')  # cuernos TRÍPTICO
    poly(p, [(66, 86), (96, 80), (112, 120), (58, 124)], pat=lambda x, y: '2' if x % 8 == 0 else '1')            # capucha SATURNUS
    for x0 in range(50, 150, 16):                                                           # grapas de hueso (costura)
        for y in (34, 35, 94, 95):
            xx = x0 // 2
            if 0 <= xx < W and p[y][xx] in '12': p[y][xx] = '3'
    poly(p, [(48, 46), (96, 40), (108, 62), (96, 84), (48, 80), (40, 62)], fill='.', edge='3')
    pupila(p, st, 72, 62, 16)
    fix(p)
    return p


DISENOS = [('A · EL CORAZÓN BLINDADO', blindado,
            'Esfera facetada de carne y blindaje con tres arterias que la unen a la pared. Donde entran las arterias hay '
            'tres NODOS de energía (fase I: hay que destruir dos). La pupila mira a la nave y se abre sobre el reactor.'),
           ('B · EL OJO-VÁLVULA', valvula,
            'Un ojo enorme encajado entre tendones; el iris son seis pétalos de músculo que se abren como un diafragma. '
            'Las válvulas abiertas dejan ver el reactor.'),
           ('C · EL NÚCLEO COSIDO', cosido,
            'La criatura se ha cosido con lo que le quitaste: placa de FERRUM-9, mechones de THALASSA, cuernos del '
            'TRÍPTICO, la capucha de SATURNUS. Grapas de hueso, y en el centro la pupila-reactor.')]


# ---- interfaz para el motor (diseño B elegido: el OJO-VÁLVULA)
BOSS_K, BOSS_R = 23, 2
EXENTO = True                    # se ve el fondo alrededor; los tendones lo sujetan al techo y al suelo
FACE = 8                         # punta del párpado delante de la válvula: desde ahí empieza la zona de impacto
EYE_CX, EYE_CY = 44, 64          # la válvula / el reactor (punto débil)
EYE_ROWS, EYE_C0, EYE_NC = (7, 8), 7, 8
MOUTH_Y0, MOUTH_Y1 = 36, 84      # proyectiles desde los pétalos de arriba y de abajo
POCKET_Y0, POCKET_Y1 = 56, 72


def boss(state=0):
    """0 válvula cerrada · 1 se entreabre y late (aviso) · 2 abierta: reactor expuesto"""
    from canvas import C
    c = C(W, H); c.p = valvula(state)
    return c
