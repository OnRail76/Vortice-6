#!/usr/bin/env python3
"""VÓRTICE 6 · PANEL DE MANDO (menú del disco y del cartucho): dibujo ANTIC E 160x192 con 4 colores por franja de 4 líneas.
Devuelve la imagen (índices 0-3), la paleta por franja y las piezas que el programa cambia en marcha.
Índices: 0 = fondo (COLBK), 1 = PF0, 2 = PF1, 3 = PF2."""
import os, sys, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx')]
import font, font3

W, H = 160, 192
NB = H // 4

# ---------------------------------------------------------------- composición (filas de pantalla)
LOGO_Y = 2                  # VÓRTICE 6: fuente del juego x2 de ancho y x3 de alto (24 líneas)
SUB_Y = 29                  # CORAZÓN DEL VACÍO (fuente del juego)
EURO_Y = 41                 # franja EUROSHOOTER (bandas 10-11)
MON_Y0, MON_Y1 = 48, 151    # monitor: marco arriba (48-50) y abajo (149-151)
ENT_Y = [60 + 18 * k for k in range(5)]
LBL_Y = 155                 # DIFICULTAD / MODO INVENCIBLE (fuente pequeña)
DIF_Y = 160                 # ◂ NORMAL ▸ (fuente grande)
FIRE_Y = 172                # PULSA FIRE
REC_Y = 181                 # RÉCORD · 2026 - TONY C. WARE
LED_Y = 188

WORLDS = [('EL DESGUACE ESPACIAL', 'JEFE: FERRUM-9', 0x28),
          ('LOS OCÉANOS ASTRALES', 'JEFE: THALASSA', 0x88),
          ('EL FUEGO INFERNAL DE HADES', 'JEFE: EL TRÍPTICO DE HADES', 0x38),
          ('EL SARCÓFAGO DE SACRIFICIOS', 'DE SATURNO · JEFE: SATURNUS', 0x1C),
          ('LA NAVE VIVIENTE', 'JEFE: EL CORAZÓN NULO', 0x46)]
PLANET = [0x26, 0x86, 0x34, 0x1A, 0x44]          # cuerpo del planeta (más oscuro que su rótulo)
PX = [16, 26, 16, 26, 16]                          # x del centro de cada planeta (la ruta zigzaguea)

img = [[0] * W for _ in range(H)]
pal = [[0x00, 0x00, 0x00, 0x00] for _ in range(NB)]


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H: img[y][x] = c


def big(t, x, y, c, sx=1, sy=1, shade=None, hi=None):
    """texto con la fuente del juego (8x8); sombra a la derecha/abajo y brillo en el borde superior"""
    for i, ch in enumerate(t):
        g = font._G.get(ch, font._G['?'])
        for gy, row in enumerate(g):
            for gx, b in enumerate(row):
                if b != 'X': continue
                for yy in range(sy):
                    for xx in range(sx):
                        X, Y = x + (i * 8 + gx) * sx + xx, y + gy * sy + yy
                        if shade is not None:
                            if img[Y + 1][X + 1] == 0: put(X + 1, Y + 1, shade)
                        put(X, Y, c)
                        if hi is not None and yy == 0 and (gy == 0 or g[gy - 1][gx] != 'X'): put(X, Y, hi)


def small(t, x, y, c):
    """fuente 3x5 (y-1 = fila del acento)"""
    for i, ch in enumerate(t):
        g = font3.glyph(ch)
        for gy, row in enumerate(g):
            for gx, b in enumerate(row):
                if b == 'X': put(x + 4 * i + gx, y - 1 + gy, c)


def bigw(t, sx=1): return 8 * len(t) * sx - 2 * sx


def setpal(b0, b1, bk=None, p0=None, p1=None, p2=None):
    for b in range(b0, b1 + 1):
        for k, v in enumerate((bk, p0, p1, p2)):
            if v is not None: pal[b][k] = v


# ---------------------------------------------------------------- 1 · VÓRTICE 6
logo = 'VÓRTICE 6'
lw = bigw(logo, 2)
lx = (W - lw) // 2
for i, ch in enumerate(logo):
    big(ch, lx + i * 16, LOGO_Y, 3 if ch == '6' else 2, sx=2, sy=3, shade=1, hi=None if ch == '6' else 3)
FACE = [0x0E, 0x0C, 0x1E, 0x1C, 0x2A, 0x38, 0x46]          # plata -> oro -> naranja -> rojo, como la carátula
SIX = [0x4E, 0x4C, 0x3A, 0x48, 0x46, 0x44, 0x42]
for b in range(7):
    setpal(b, b, 0x00, 0x42 if b > 2 else 0x04, FACE[b], SIX[b] if b > 0 else 0x0E)
# el brillo superior de las letras va en el índice 3 (comparte color con el 6: el 6 brilla en rojo-oro)

# ---------------------------------------------------------------- 2 · CORAZÓN DEL VACÍO
sub = 'CORAZÓN DEL VACÍO'
big(sub, (W - bigw(sub)) // 2, SUB_Y, 2, shade=1)
setpal(7, 9, 0x00, 0x22, 0x1C, 0x00)
pal[7][2] = 0x1E; pal[9][2] = 0x2A

# ---------------------------------------------------------------- 3 · franja EUROSHOOTER (el fondo late)
eu = 'EUROSHOOTER EN 8 BITS REDEFINIDO'
small(eu, (W - font3.width(eu)) // 2, EURO_Y + 1, 2)
for x in range(W):                                  # filos de la placa
    put(x, 40, 1); put(x, 47, 1)
for k in range(6):                                  # puntas en flecha a los lados
    for y in range(41 + k // 2, 47 - k // 2):
        put(2 + k, y, 1); put(W - 3 - k, y, 1)
setpal(10, 11, 0x32, 0x44, 0x0E, 0x00)

# ---------------------------------------------------------------- 4 · monitor de navegación
BEZ = 0x08
for x in range(2, W - 2):
    for y in (MON_Y0, MON_Y0 + 1, MON_Y1 - 1, MON_Y1):
        put(x, y, 1)
    put(x, MON_Y0 + 2, 2 if x % 8 < 4 else 1)      # remaches del marco
for y in range(MON_Y0, MON_Y1 + 1):
    for x in (2, 3, 4, W - 5, W - 4, W - 3):
        put(x, y, 1)
setpal(12, 12, 0x00, BEZ, 0x0C, 0x00)
setpal(37, 37, 0x00, BEZ, 0x0C, 0x00)
tit = 'RUTA DE NAVEGACIÓN · 5 MUNDOS'
small(tit, (W - font3.width(tit)) // 2, 54, 3)
SCR = 0x90                                          # pantalla: azul noche (la VBI le pasa el barrido)
setpal(13, 36, SCR, BEZ, 0x0C, 0x9C)
# retícula tenue: puntos cada 8 píxeles
for y in range(61, 146, 8):
    for x in range(40, W - 8, 8):
        if img[y][x] == 0: put(x, y, 1)
for k, (n1, n2, col) in enumerate(WORLDS):
    y0 = ENT_Y[k]
    cx, cy = PX[k], y0 + 5
    # planeta: círculo de 11 líneas (proporción NTSC: 1 píxel = 1,6 líneas)
    for y in range(-5, 6):
        for x in range(-4, 5):
            if (x * 1.6) ** 2 + y ** 2 <= 5.4 ** 2:
                put(cx + x, cy + y, 2)
                if (x * 1.6 + 2) ** 2 + (y + 2) ** 2 <= 2.6 ** 2: put(cx + x, cy + y, 3)
    if k == 3:                                      # Saturno: anillo
        for x in range(-7, 8):
            y = round(-x * 0.25)
            if abs(x) > 3: put(cx + x, cy + y, 1)
    if k == 0:                                      # el desguace: chatarra orbitando
        for dx, dy in ((-7, -4), (6, 3), (7, -2)): put(cx + dx, cy + dy, 1)
    if k == 4:                                      # la nave viviente: latido (vetas)
        for dy in (-2, 0, 2): put(cx - 1, cy + dy, 1); put(cx + 1, cy + dy - 1, 1)
    small(n1, 44, y0 + 1, 3)
    small(n2, 44, y0 + 8, 2)
    small(str(k + 1), 34, y0 + 4, 2)
    b0, b1 = (y0 - 1) // 4, (y0 + 12) // 4
    setpal(b0, b1, SCR, BEZ, col, 0x9C)
    # ruta: puntos hasta el siguiente
    if k < 4:
        x0, x1, ya, yb = cx, PX[k + 1], cy + 7, ENT_Y[k + 1] + 5 - 7
        for y in range(ya, yb + 1, 2):
            t = (y - ya) / max(1, yb - ya)
            put(round(x0 + (x1 - x0) * t), y, 1)
# las franjas de los planetas tienen su color en el índice 2; las de en medio, el gris del rótulo
# ---------------------------------------------------------------- 5 · consola
for x in range(W):
    put(x, 153, 1)
setpal(38, 47, 0x00, 0x06, 0x0E, 0x9A)
LBL = 'DIFICULTAD'
LBL_INV = 'DIFICULTAD · MODO INVENCIBLE'
DIFS = ['◂  FÁCIL  ▸', '◂  NORMAL  ▸', '◂ HARDCORE ▸']
fire = 'PULSA FIRE'
big(fire, (W - bigw(fire)) // 2, FIRE_Y, 2)
REC = 'RÉCORD 000000'
REC_X = 8
small(REC, REC_X, REC_Y, 3)
cr = '2026 - TONY C. WARE'
small(cr, W - 8 - font3.width(cr), REC_Y, 2)
setpal(45, 46, 0x00, 0x06, 0x08, 0x9C)
LEDX = list(range(6, W - 6, 8))
for i, x in enumerate(LEDX):
    for y in range(LED_Y, LED_Y + 2):
        for xx in range(3): put(x + xx, y, 1 + i % 3)
setpal(47, 47, 0x00, 0x34, 0xC6, 0x1A)


def rows_of(y0, n, draw):
    """bytes (40 por fila) de las filas y0..y0+n-1 tras dibujar con draw() sobre un lienzo limpio de esas filas"""
    save = [r[:] for r in img[y0:y0 + n]]
    for r in range(y0, y0 + n): img[r] = [0] * W
    draw()
    out = tobytes_rows(y0, n)
    for i, r in enumerate(save): img[y0 + i] = r
    return out


def tobytes_rows(y0, n):
    b = bytearray()
    for y in range(y0, y0 + n):
        for x in range(0, W, 4):
            v = 0
            for k in range(4): v = (v << 2) | img[y][x + k]
            b.append(v)
    return bytes(b)


# piezas variables
DIFROWS = [rows_of(DIF_Y, 8, lambda t=t: big(t, (W - bigw(t)) // 2, DIF_Y, 2)) for t in DIFS]
LBLROWS = [rows_of(LBL_Y - 1, 6, lambda t=t: small(t, (W - font3.width(t)) // 2, LBL_Y, 3)) for t in (LBL, LBL_INV)]
# dígitos del récord (fuente pequeña, índice 3): 5 filas por dígito, 1 byte cada una
DIGB = []
for d in '0123456789':
    g = font3.glyph(d)[1:]
    for row in g:
        v = 0
        for k in range(4):
            v = (v << 2) | (3 if k < 3 and row[k] == 'X' else 0)
        DIGB.append(v)
REC_DX = (REC_X + 4 * REC.index('0')) // 4      # byte del primer dígito
# estado inicial: NORMAL, sin truco
for i, r in enumerate(range(DIF_Y, DIF_Y + 8)):
    pass


def apply(rows, y0):
    for i in range(len(rows) // 40):
        for xb in range(40):
            v = rows[i * 40 + xb]
            for k in range(4): img[y0 + i][xb * 4 + k] = (v >> (6 - 2 * k)) & 3


apply(DIFROWS[1], DIF_Y)
apply(LBLROWS[0], LBL_Y - 1)

# franjas del monitor (para el barrido) y de cada mundo (para resaltar el rótulo)
MON_B0, MON_B1 = 13, 36
ENT_B = [((y0 - 1) // 4, (y0 + 12) // 4) for y0 in ENT_Y]
SHIP_PATH = [(PX[k], ENT_Y[k] + 5) for k in range(5)]


def check():
    for b in range(NB):
        used = {img[y][x] for y in range(4 * b, 4 * b + 4) for x in range(W)}
        assert used <= {0, 1, 2, 3}


def preview(path, scale=4):
    from PIL import Image
    from pal import atari_rgb
    im = Image.new('RGB', (W, H))
    for y in range(H):
        p = pal[y // 4]
        for x in range(W):
            im.putpixel((x, y), atari_rgb(p[img[y][x]]))
    im.resize((W * scale, int(H * scale * 0.625 * 1.6)), Image.NEAREST).save(path)


if __name__ == '__main__':
    check()
    preview(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'build', 'menu_prev.png'))
    print('ok')
