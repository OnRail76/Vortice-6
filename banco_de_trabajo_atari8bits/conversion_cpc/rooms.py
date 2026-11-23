#!/usr/bin/env python3
"""Reproduce el dibujo de las 8 salas del BASIC original (LOCATE/PRINT/PEN en MODE 0, 20x25)
y deja cada sala como rejilla [fila 1..25][col 1..20] = (código CPC, pen)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
LST = open(os.path.join(HERE, '..', 'orig', 'BOLONPRG.BAS.txt'), encoding='latin1').read().splitlines()
LINES = {}
for l in LST:
    n, _, rest = l.partition(' ')
    if n.isdigit(): LINES[int(n)] = rest

def s(line, k=0):
    """k-ésima cadena entre comillas de una línea del listado."""
    return re.findall(r'"([^"]*)"', LINES[line])[k]

class Scr:
    def __init__(s_):
        s_.g = [[(32, 0)] * 21 for _ in range(26)]
        s_.c, s_.r, s_.pen = 1, 1, 1
    def locate(s_, c, r): s_.c, s_.r = c, r
    def pr(s_, txt, nl=True):
        for ch in txt:
            code = ch if isinstance(ch, int) else ord(ch)
            if s_.c > 20: s_.c = 1; s_.r += 1
            if 1 <= s_.r <= 25: s_.g[s_.r][s_.c] = (code, s_.pen)
            s_.c += 1
        if nl: s_.c = 1; s_.r += 1

FLOOR = s(1700)        # suelo de 80 caracteres, filas 21-24
TOP = s(1760)          # techo de 40 caracteres, filas 3-4

def room(f):
    S = Scr()
    def col_ab(c, a0, a1, b0, b1):
        for a in range(a0, a1 + 1, 2): S.locate(c, a); S.pr('ab')
        for a in range(b0, b1 + 1, 2): S.locate(c, a); S.pr('`d')
    if f == 1:
        S.pen = 4; S.locate(1, 21); S.pr(FLOOR)
        S.locate(11, 14); S.pr('ababababab'); S.locate(11, 15); S.pr('`d`d`d`d`d')
        S.locate(12, 12); S.pr('ababababa'); S.locate(12, 13); S.pr('`d`d`d`d`')
        S.locate(13, 10); S.pr('abababab'); S.locate(13, 11); S.pr('`d`d`d`d')
    elif f == 2:
        S.pen = 6; S.locate(1, 3); S.pr(TOP); S.locate(1, 21); S.pr(FLOOR)
        col_ab(1, 5, 13, 6, 14); col_ab(19, 11, 19, 12, 20)
        S.locate(3, 13); S.pr('abababab'); S.locate(3, 14); S.pr('`d`d`d`d')
        S.locate(10, 15); S.pr('abab'); S.locate(10, 16); S.pr('`d`d')
        S.locate(16, 19); S.pr('ababa'); S.locate(16, 20); S.pr('cdcdc')
        S.locate(12, 9); S.pr('ababababa'); S.locate(12, 10); S.pr('`d`d`d`d`')
        S.locate(17, 11); S.pr('ab'); S.locate(17, 12); S.pr('`d')
        S.locate(1, 5); S.pr('aabab'); S.locate(1, 6); S.pr('ccdcd')
    elif f == 3:
        S.pen = 2; S.locate(1, 21); S.pr(FLOOR); S.locate(1, 3); S.pr(TOP)
        S.locate(1, 11); S.pr(s(1900))
        col_ab(1, 9, 19, 10, 20); col_ab(19, 5, 15, 6, 16)
        S.locate(3, 9); S.pr('abab'); S.locate(3, 10); S.pr('cdcd')
        S.locate(4, 12); S.pen = 15; S.pr('*')
        for a in range(17, 21): S.locate(17, a); S.pr('@@')
    elif f == 4:
        S.pen = 10; S.locate(1, 21); S.pr(FLOOR); S.locate(1, 3); S.pr(TOP)
        col_ab(1, 5, 15, 6, 16); col_ab(19, 9, 19, 10, 20)
        S.locate(1, 9); S.pr(s(2010))
        S.locate(3, 11); S.pen = 15; S.pr('*')
        for a in range(5, 9): S.locate(18, a); S.pr('@@')
    elif f == 5:
        S.pen = 5; S.locate(1, 21); S.pr(FLOOR); S.locate(1, 3); S.pr(TOP)
        col_ab(1, 9, 19, 10, 20); col_ab(19, 5, 15, 6, 17)
        S.locate(1, 9); S.pr(s(2100))
        S.locate(4, 10); S.pr([137] * 6); S.locate(6, 20); S.pr([137] * 6)
        S.locate(3, 15); S.pen = 15; S.pr('*')
        for a in range(17, 21): S.locate(19, a); S.pr('@@')
    elif f == 6:
        S.pen = 11; S.locate(1, 21); S.pr(FLOOR); S.locate(1, 3); S.pr(TOP)
        col_ab(1, 5, 15, 6, 16); col_ab(19, 5, 15, 6, 16)
        S.locate(1, 9); S.pr(s(2190))
    elif f == 7:
        S.pen = 2; S.locate(1, 21); S.pr(FLOOR); S.locate(1, 3); S.pr(TOP)
        col_ab(1, 5, 15, 6, 16); col_ab(19, 9, 19, 10, 20)
        S.locate(1, 9); S.pr(s(2280))
    elif f == 8:
        S.pen = 8; S.locate(1, 21); S.pr(FLOOR); S.locate(1, 3); S.pr(TOP)
        col_ab(1, 9, 19, 10, 20); col_ab(19, 5, 19, 6, 20)
        S.locate(1, 9); S.pr(s(2370))
        S.pen = 2; S.locate(16, 19); S.pr('ef'); S.locate(16, 20); S.pr('uv')
        S.locate(18, 5); S.pen = 15; S.pr('*')
    return S.g

# Tablas de objetos (DATA 940-1140): tipo, fila, col, dirF, minF, maxF, dirC, minC, maxC, pen, carA, carB
def tables():
    vals = []
    for n in range(940, 1141, 10):
        vals += [int(v) for v in LINES[n].replace('DATA', '').split(',')]
    rooms, cur = [], []
    i = 0
    while i < len(vals):
        if vals[i] == 255: rooms.append(cur); cur = []; i += 1; continue
        cur.append(vals[i:i + 12]); i += 12
    return rooms

# Caracteres redefinidos (SYMBOL) del cargador
def symbols():
    out = {}
    for l in open(os.path.join(HERE, '..', 'orig', 'BOLONCIO.BAS.txt'), encoding='latin1'):
        m = re.match(r'\d+\s+SYMBOL\s+([\d,\s]+)$', l.strip())
        if m:
            v = [int(x) for x in m.group(1).replace(' ', '').split(',') if x]
            out[v[0]] = v[1:9]
    return out

if __name__ == '__main__':
    t = tables()
    for f in range(1, 9):
        g = room(f)
        print('== sala', f, t[f - 1])
        for r in range(1, 26):
            print('%2d ' % r + ''.join(chr(g[r][c][0]) if g[r][c][0] < 128 else '#' for c in range(1, 21)))
