"""Escena de texto -> juego de caracteres ANTIC 4 + mapa de códigos."""
VAL = {'.': 0, '1': 1, '2': 2, '3': 3, '4': 3}


def cell_of(p, col, row):
    return tuple(''.join(p[row * 8 + y][col * 4 + x] for x in range(4)) for y in range(8))


def encode(cell):
    """-> (8 bytes, invertido) ; error si mezcla '3' y '4'"""
    flat = ''.join(cell)
    if '3' in flat and '4' in flat:
        return None
    inv = '4' in flat
    b = []
    for l in cell:
        v = 0
        for ch in l:
            v = (v << 2) | VAL[ch]
        b.append(v)
    return bytes(b), inv


class Charset:
    def __init__(s, name):
        s.name = name
        s.glyphs = [bytes(8)]          # código 0 = vacío
        s.index = {bytes(8): 0}
        s.conflicts = []

    def code(s, cell, where=''):
        e = encode(cell)
        if e is None:
            # arreglo: el '4' manda en la celda (se pierde el '3'); se informa
            s.conflicts.append(where)
            cell = tuple(l.replace('3', '4') for l in cell)
            e = encode(cell)
        b, inv = e
        if b not in s.index:
            s.index[b] = len(s.glyphs)
            s.glyphs.append(b)
        c = s.index[b]
        return c | (0x80 if inv else 0)

    def data(s):
        assert len(s.glyphs) <= 128, '%s: %d caracteres (>128)' % (s.name, len(s.glyphs))
        return b''.join(s.glyphs) + bytes(8 * (128 - len(s.glyphs)))


def scene_map(sc, cs, rows=20):
    m = []
    for r in range(rows):
        m.append([cs.code(cell_of(sc.p, c, r), '%s r%d c%d' % (cs.name, r, c)) for c in range(sc.cols)])
    return m
