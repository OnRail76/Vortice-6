"""FASE 5 · prototipo del escenario orgánico: VENAS (la enredadera de la fase 2 llevada a vasos sanguíneos),
ARTERIAS y el OJO. Colores: 1 = PF0 carne oscura · 2 = PF1 vena roja viva · 3 = PF2 hueso / blanco del ojo · 4 = PF3 (latido)
"""
U = 16

# malla de venas: troncos que se ramifican, con bulbos-ojo pequeños (como las bolitas de la enredadera de la fase 2)
VENAS = ['..2...12..2...21', '..21..2...21..2.', '...2.21....2.12.', '...221......22..',
         '....2...333..2..', '...12..31113.2..', '..2.2..31.13.12.', '.2..21.31113..2.',
         '2....2..333...2.', '.....21..2...21.', '......2..21..2..', '.....12...2.12..',
         '....2.2...221...', '...2...2...2....', '..2....21..2....', '.21.....2..21...']
# remate: puntas de vena que acaban en un ojillo
FLECO = [['................', '...333......333.', '..31113....31113', '..31.13....31.13',
          '..31113.2..31113', '...333..2...333.', '....2..2.....2..', '...21.21....21..'],
         ['................', '.......333......', '.333..31113.....', '31113.31.13..333',
          '31.13.31113.3111', '31113..333..31.1', '.333....2...3111', '..2....21....333']]


def venas(alturas, row, techo=False):
    """montaña de venas: alturas en celdas por cada columna de 16 píxeles"""
    H = max(alturas)
    out = [['.'] * (U * len(alturas)) for _ in range(8 * H)]
    for k, h in enumerate(alturas):
        for cy in range(h):
            r = (H - 1 - cy) if not techo else cy
            tope = cy == h - 1
            for y in range(8):
                yy = r * 8 + y
                if tope:
                    f = FLECO[k % 2]
                    ch = f[y] if not techo else f[7 - y]
                else:
                    ch = VENAS[(row * 8 + yy) % 16]
                for x in range(U):
                    out[yy][k * U + x] = ch[x]
    return [''.join(l) for l in out]


def monte(n, alto):
    import math
    return [max(1, round(alto * (0.55 + 0.45 * math.sin(math.pi * (i + 0.5) / n)))) for i in range(n)]


def arteria(w):
    """ARTERIA: tubo grueso horizontal (2 filas) con pared de hueso, sangre que corre a tramos y anillos"""
    top = '3' * (4 * w)
    rows = [top]
    for y in range(1, 15):
        r = ''
        for x in range(4 * w):
            if x % 16 in (0, 1): r += '3'                       # anillos de cartílago
            elif y in (1, 14): r += '1'
            elif 5 <= y <= 9 and (x // 4 + y) % 6 < 3: r += '2'  # pulsos de sangre
            else: r += '1'
        rows.append(r)
    rows.append(top)
    return rows


OJO = '''
..............33333333333333333333..............
..........33333111111111111111111333333.........
.......3333111122222222222222222211113333.......
.....33311122222222333333333322222222111333.....
...333112222222333333333333333333322222211333...
..33112222223333333333111111113333333222221133..
.3311222223333333331111.......111133333322221133
331122222333333333111...........111333332222113.
3311222233333333311.......33.....11333332222113.
3311222233333333311......3333....11333332222113.
3311222233333333311.......33.....11333332222113.
331122222333333333111...........111333332222113.
.3311222223333333331111.......111133333322221133
..33112222223333333333111111113333333222221133..
...333112222222333333333333333333322222211333...
.....33311122222222333333333322222222111333.....
.......3333111122222222222222222211113333.......
..........33333111111111111111111333333.........
..............33333333333333333333..............
................................................'''


def ojo():
    """el OJO incrustado en la carne: párpados de vena, blanco de hueso, iris rojo, pupila negra con brillo"""
    rows = [r for r in OJO.strip('\n').split('\n')]
    w = max(len(r) for r in rows)
    rows = [r.ljust(w, '.') for r in rows]
    # se centra en 8 filas de carácter (64 líneas): carne alrededor
    pad = (40 - len(rows)) // 2
    carne = []
    for y in range(40):
        if pad <= y < pad + len(rows):
            r = rows[y - pad]
            carne.append(''.join(ch if ch != '.' or (x in range(18, 30) and 6 <= y - pad <= 12) else '1' for x, ch in enumerate(r)))
        else:
            carne.append('1' * w)
    return carne


# ===================================================================== versión 2: tejido denso, ojo inyectado en sangre
import random as _r


def _tile(seed=7):
    """baldosa 16x16 de tejido: carne con venas que se ramifican (se repite sin costuras), algún hueco y un ojillo"""
    R = _r.Random(seed)
    t = [['1'] * 16 for _ in range(16)]
    for tronco in range(3):
        x, y = R.randrange(16), 0
        for y in range(16):
            t[y][x % 16] = '2'
            if R.random() < .35: t[y][(x + 1) % 16] = '2'
            if R.random() < .18:                       # rama
                bx = x
                for k in range(R.randrange(2, 5)):
                    bx += R.choice((-1, 1)); t[(y + k) % 16][bx % 16] = '2'
            x += R.choice((-1, 0, 0, 1))
    for (hx, hy) in ((5, 3), (12, 11)):                 # huecos oscuros entre venas
        for dy in range(2):
            for dx in range(3 - dy):
                if t[(hy + dy) % 16][(hx + dx) % 16] == '1': t[(hy + dy) % 16][(hx + dx) % 16] = '.'
    ojillo = ['.333.', '31113', '31.13', '31113', '.333.']
    for dy, row in enumerate(ojillo):
        for dx, ch in enumerate(row):
            if ch != '.': t[(9 + dy) % 16][(1 + dx) % 16] = ch
            else: t[(9 + dy) % 16][(1 + dx) % 16] = '.' if (dy, dx) == (2, 2) else t[(9 + dy) % 16][(1 + dx) % 16]
    return [''.join(r) for r in t]


TEJIDO = _tile()
FLECO2 = [['................', '.....2.......3..', '....2.2.....313.', '.3..2..2....33..',
           '313.21..2..2.2..', '.3.211..21.2..2.', '..2111.2211211.2', '.21111211111112.'],
          ['................', '..3...........2.', '.313......2..2..', '..33.2...2.2.2..',
           '..2.2.2..2..21..', '.2..21.2211.21..', '2..2111211121112', '1211111111111111']]


def tejido(alturas, row, techo=False):
    """masa de tejido con venas; en lo alto, tentáculos de vena con ojillos"""
    H = max(alturas)
    out = [['.'] * (U * len(alturas)) for _ in range(8 * H)]
    for k, h in enumerate(alturas):
        for cy in range(h):
            r = (H - 1 - cy) if not techo else cy
            tope = cy == h - 1
            for y in range(8):
                yy = r * 8 + y
                ch = (FLECO2[k % 2][y] if not techo else FLECO2[k % 2][7 - y]) if tope else TEJIDO[(row * 8 + yy) % 16]
                for x in range(U): out[yy][k * U + x] = ch[x]
    return [''.join(l) for l in out]


OJO2 = """
..........................1111111111111..........................
...................1111111222222222222211111111...................
..............11112222222233333333333332222222221111..............
..........1112222223333333333332333333333333333222222111..........
.......1122222333333233333333332333333332333333333332222211.......
.....11222333333333332333333111111111333332333333333333322211.....
...112223333323333333333331112222222211133333333233333333332211...
..122233333332333333333311222111111222211333332233333333333322211.
.122333333333323333333112221111...111122211333233333333233333332221
1222333332333333333331122111........1112211333333333332333333333221
1223333333233333333311221111....33...111221133333333233333333333322
1223333333323333333311221111...3333..111221133333332333333333333322
1222333333333233333331122111....33...1112211333333233333333333333221
.1223333333333233333331122211........11122211333323333333333333332221
..12223333333333233333331122211111111122211333333333333333333322211.
...112223333333332333333331112222222211133333333333323333333332211...
.....11222333333333333233333111111111333333333233333333333322211.....
.......1122222333333333323333333333333333333233333333332222211.......
..........1112222223333333333333332333333333333333222222111..........
..............11112222222233333333333332222222221111..............
...................1111111222222222222211111111...................
..........................1111111111111.........................."""


def ojo_grande():
    """OJO enorme inyectado en sangre: párpados de carne y vena, blanco de hueso con venillas rojas, iris de carne
    con anillo de vena y pupila negra con brillo. 16 x 3 caracteres (64 x 21 líneas, se centra en 24)."""
    rows = [r for r in OJO2.strip('\n').split('\n')]
    w = 64
    rows = [r[:w].ljust(w, '.') for r in rows]
    out = ['1' * w] + [''.join('1' if (ch == '.' and not (28 <= x <= 40 and 6 <= y <= 15)) else ch for x, ch in enumerate(r)) for y, r in enumerate(rows)]
    out += ['1' * w] * (24 - len(out))
    return out


def arteria2(w):
    """ARTERIA de 3 filas: pared de cartílago, sangre que fluye en vetas, extremos que se estrechan como raíces"""
    H = 24
    rows = []
    for y in range(H):
        r = ''
        for x in range(4 * w):
            e = min(x, 4 * w - 1 - x)                     # distancia al extremo: se estrecha
            top, bot = max(0, 6 - e // 2), H - 1 - max(0, 6 - e // 2)
            if y < top or y > bot: r += '.'
            elif y in (top, bot): r += '3'
            elif y in (top + 1, bot - 1): r += '1'
            elif (x // 3 + y // 2) % 7 == 0 or (x + 2 * y) % 23 == 0: r += '3'
            elif abs(y - H // 2) < 4 and (x // 4 + y) % 5 < 3: r += '2'
            else: r += '1'
        rows.append(r)
    return rows


# ===================================================================== versión 3: ojo y arteria pensados para el píxel doble del Atari
import math as _m


def ojo3(w=40, h=32, seed=3):
    """OJO inyectado en sangre en píxeles ANTIC 4 (cada píxel es el doble de ancho que de alto):
    almendra de 80 x 32 a la vista; párpado de vena, blanco de hueso con venillas, iris de carne, pupila y brillo"""
    R = _r.Random(seed)
    cx, cy = w / 2 - .5, h / 2 - .5
    out = [['1'] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            vx, vy = (x - cx) * 2, (y - cy)                 # coordenadas a la vista
            lim = (h / 2 - 2) * (1 - (vx / (w - 1)) ** 2)  # almendra
            if abs(vy) < lim - 1.5:
                out[y][x] = '3'
            elif abs(vy) < lim + .5:
                out[y][x] = '2'                            # borde del párpado (vena)
    for k in range(9):                                     # venillas rojas en el blanco, desde los lados hacia el iris
        ang = R.uniform(-.9, .9) + (_m.pi if k % 2 else 0)
        rr = R.uniform(30, 36)
        x, y = cx * 2 + _m.cos(ang) * rr, cy + _m.sin(ang) * rr * .35
        for t in range(14):
            xx, yy = int(round(x / 2)), int(round(y))
            if 0 <= xx < w and 0 <= yy < h and out[yy][xx] == '3': out[yy][xx] = '2'
            x += (cx * 2 - x) * .09 + R.uniform(-1, 1); y += (cy - y) * .09 + R.uniform(-.6, .6)
    for y in range(h):                                     # iris, anillo y pupila
        for x in range(w):
            vx, vy = (x - cx) * 2, (y - cy)
            d = _m.hypot(vx, vy * 1.0)
            if d < 13: out[y][x] = '2' if d > 11 else '1'
            if d < 6: out[y][x] = '.'
    out[int(cy) - 3][int(cx) - 1] = '3'                   # brillo (un punto)
    return [''.join(r) for r in out]


def arteria3(w, h=24):
    """ARTERIA orgánica: tubo de carne con pared de cartílago fina, sangre en el centro y extremos que se
    abren en raíces; sin rayas rectas"""
    out = []
    for y in range(h):
        r = ''
        for x in range(4 * w):
            e = min(x, 4 * w - 1 - x)
            m = max(0, 7 - e)                              # se estrecha en las puntas
            top, bot = m // 2 + 1, h - 2 - m // 2
            if y < top or y > bot:
                r += '.'
            elif y in (top, bot): r += '3'
            elif abs(y - h // 2) <= 3 and x % 16 not in (0, 1, 2, 3): r += '2'     # sangre (período de 4 celdas)
            elif abs(y - h // 2) == 5 and x % 16 in (6, 7, 8): r += '3'            # brillo de la pared
            else: r += '1'
        out.append(r)
    return out
