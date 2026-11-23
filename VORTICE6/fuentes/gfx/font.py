"""VÓRTICE 6 · fuente propia 8x8 (mayúsculas gruesas con tildes y Ñ).

Fila 0: tilde (o vacía) · filas 1-6: letra · fila 7: vacía.  64 glifos como máximo (ANTIC 6/7 usan 64).
Sirve para ANTIC 2 (marcador, 40 columnas), ANTIC 6 (20 col., 8 líneas) y ANTIC 7 (20 col., 16 líneas).
"""
_G = {}


def _d(ch, rows, accent=None):
    r = [l.ljust(8, '.') for l in rows]
    assert len(r) == 6, ch
    top = '........'
    if accent == 'acute': top = '...XX...'
    if accent == 'tilde': top = '.XX.X...'
    _G[ch] = [top] + r + ['........']


_d(' ', ['', '', '', '', '', ''])
_d('A', ['.XXXX', 'XX..XX', 'XX..XX', 'XXXXXX', 'XX..XX', 'XX..XX'])
_d('B', ['XXXXX', 'XX..XX', 'XXXXX', 'XX..XX', 'XX..XX', 'XXXXX'])
_d('C', ['.XXXX', 'XX..XX', 'XX', 'XX', 'XX..XX', '.XXXX'])
_d('D', ['XXXX', 'XX.XX', 'XX..XX', 'XX..XX', 'XX.XX', 'XXXX'])
_d('E', ['XXXXXX', 'XX', 'XXXXX', 'XX', 'XX', 'XXXXXX'])
_d('F', ['XXXXXX', 'XX', 'XXXXX', 'XX', 'XX', 'XX'])
_d('G', ['.XXXX', 'XX', 'XX.XXX', 'XX..XX', 'XX..XX', '.XXXXX'])
_d('H', ['XX..XX', 'XX..XX', 'XXXXXX', 'XX..XX', 'XX..XX', 'XX..XX'])
_d('I', ['XXXX', '.XX', '.XX', '.XX', '.XX', 'XXXX'])
_d('J', ['...XXX', '....XX', '....XX', '....XX', 'XX..XX', '.XXXX'])
_d('K', ['XX..XX', 'XX.XX', 'XXXX', 'XXXX', 'XX.XX', 'XX..XX'])
_d('L', ['XX', 'XX', 'XX', 'XX', 'XX', 'XXXXXX'])
_d('M', ['XX...XX', 'XXX.XXX', 'XXXXXXX', 'XX.X.XX', 'XX...XX', 'XX...XX'])
_d('N', ['XX..XX', 'XXX.XX', 'XXXXXX', 'XX.XXX', 'XX..XX', 'XX..XX'])
_d('O', ['.XXXX', 'XX..XX', 'XX..XX', 'XX..XX', 'XX..XX', '.XXXX'])
_d('P', ['XXXXX', 'XX..XX', 'XX..XX', 'XXXXX', 'XX', 'XX'])
_d('Q', ['.XXXX', 'XX..XX', 'XX..XX', 'XX.XXX', 'XX..XX', '.XXX.XX'])
_d('R', ['XXXXX', 'XX..XX', 'XX..XX', 'XXXXX', 'XX.XX', 'XX..XX'])
_d('S', ['.XXXXX', 'XX', '.XXXX', '....XX', '....XX', 'XXXXX'])
_d('T', ['XXXXXX', '..XX', '..XX', '..XX', '..XX', '..XX'])
_d('U', ['XX..XX', 'XX..XX', 'XX..XX', 'XX..XX', 'XX..XX', '.XXXX'])
_d('V', ['XX..XX', 'XX..XX', 'XX..XX', 'XX..XX', '.XXXX', '..XX'])
_d('W', ['XX...XX', 'XX...XX', 'XX.X.XX', 'XXXXXXX', 'XXX.XXX', 'XX...XX'])
_d('X', ['XX..XX', '.XXXX', '..XX', '..XX', '.XXXX', 'XX..XX'])
_d('Y', ['XX..XX', 'XX..XX', '.XXXX', '..XX', '..XX', '..XX'])
_d('Z', ['XXXXXX', '...XX', '..XX', '.XX', 'XX', 'XXXXXX'])
_d('0', ['.XXXX', 'XX.XXX', 'XXXXXX', 'XXX.XX', 'XX..XX', '.XXXX'])
_d('1', ['..XX', '.XXX', '..XX', '..XX', '..XX', '.XXXX'])
_d('2', ['.XXXX', 'XX..XX', '...XX', '..XX', '.XX', 'XXXXXX'])
_d('3', ['XXXXX', '....XX', '..XXX', '....XX', '....XX', 'XXXXX'])
_d('4', ['...XX', '..XXX', '.X.XX', 'XXXXXX', '...XX', '...XX'])
_d('5', ['XXXXXX', 'XX', 'XXXXX', '....XX', 'XX..XX', '.XXXX'])
_d('6', ['.XXXX', 'XX', 'XXXXX', 'XX..XX', 'XX..XX', '.XXXX'])
_d('7', ['XXXXXX', '....XX', '...XX', '..XX', '..XX', '..XX'])
_d('8', ['.XXXX', 'XX..XX', '.XXXX', 'XX..XX', 'XX..XX', '.XXXX'])
_d('9', ['.XXXX', 'XX..XX', 'XX..XX', '.XXXXX', '....XX', '.XXXX'])
_d('.', ['', '', '', '', '', '.XX'])
_d(',', ['', '', '', '', '.XX', 'XX'])
_d(':', ['', '.XX', '', '', '.XX', ''])
_d('-', ['', '', 'XXXXX', '', '', ''])
_d('!', ['.XX', '.XX', '.XX', '.XX', '', '.XX'])
_d('?', ['.XXXX', 'XX..XX', '...XX', '..XX', '', '..XX'])
_d('¡', ['.XX', '', '.XX', '.XX', '.XX', '.XX'])
_d('/', ['....XX', '...XX', '..XX', '.XX', 'XX', 'X'])
_d('×', ['', 'XX..XX', '.XXXX', '..XX', '.XXXX', 'XX..XX'])
_d('(', ['..XX', '.XX', '.XX', '.XX', '.XX', '..XX'])
_d(')', ['.XX', '..XX', '..XX', '..XX', '..XX', '.XX'])
_d("'", ['.XX', '.XX', '', '', '', ''])
# vocales con tilde y Ñ: la letra baja una fila y la tilde ocupa la fila 0
for v, base in (('Á', 'A'), ('É', 'E'), ('Í', 'I'), ('Ó', 'O'), ('Ú', 'U')):
    _d(v, _G[base][1:7], 'acute')
_d('Ñ', _G['N'][1:7], 'tilde')
# iconos del marcador
_d('■', ['XXXXX', 'XXXXX', 'XXXXX', 'XXXXX', 'XXXXX', ''])
_d('▸', ['XX', 'XXXX', 'XXXXXX', 'XXXX', 'XX', ''])
_d('◂', ['....XX', '..XXXX', 'XXXXXX', '..XXXX', '....XX', ''])

ORDER = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
         'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', ':', '-', '!', '?', '¡',
         '/', '×', '(', ')', "'", 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ñ', '■', '▸', '◂']
assert len(ORDER) <= 64, len(ORDER)
CODE = {ch: i for i, ch in enumerate(ORDER)}


def font_bytes():
    out = bytearray(1024)
    for i, ch in enumerate(ORDER):
        for y, row in enumerate(_G[ch]):
            out[i * 8 + y] = int(row.replace('.', '0').replace('X', '1'), 2)
    return bytes(out)


def text(t, w=None, center=False, color=0):
    """códigos de pantalla; color 0-3 = bits 6-7 en ANTIC 6/7"""
    t = t.upper()
    if w:
        t = t.center(w) if center else t.ljust(w)
        t = t[:w]
    return [CODE.get(ch, CODE['?']) | (color << 6) for ch in t]


def split_lines(t, w):
    """parte por palabras en líneas de w caracteres como máximo, sin cortar palabras"""
    out, line = [], ''
    for word in t.split():
        if len(word) > w: raise ValueError('palabra demasiado larga: ' + word)
        if line and len(line) + 1 + len(word) > w:
            out.append(line); line = word
        else:
            line = (line + ' ' + word).strip()
    out.append(line)
    return out
