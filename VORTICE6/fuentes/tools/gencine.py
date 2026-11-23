#!/usr/bin/env python3
"""Datos de los programas de INTRO (V6CINE=1) y FINAL (V6CINE=2): imagen ANTIC E con colores por franja,
frases (modo 7, fuente del juego), créditos (modo 2) y lista de visualización. Escribe build/cine/cinedata.s"""
import sys, os, pickle
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx'), os.path.join(ROOT, 'tools')]
import font, atpic
CINE = int(os.environ.get('V6CINE', '1'))
OUT = os.path.join(ROOT, 'build', 'cine'); os.makedirs(OUT, exist_ok=True)
L = []
def emit(s): L.append(s)
def bl(data, lab=None, per=16):
    if lab: emit('%s:' % lab)
    for i in range(0, len(data), per): emit('    .byte ' + ','.join('$%02X' % b for b in data[i:i + per]))

idx, pals = pickle.load(open(os.path.join(ROOT, 'pic', 'nave.pkl' if CINE == 1 else 'elara.pkl'), 'rb'))
BAND = 4
NB = 192 // BAND
pic = atpic.tobytes(idx)
open(os.path.join(OUT, 'pic.bin'), 'wb').write(pic)
pals = [list(p) + [0] * (4 - len(p)) for p in pals]
emit('NBANDS = %d' % NB)
# por franja: color del fondo (índice 0) y PF0..PF2 (índices 1..3)
bl([p[0] for p in pals], 'PALBK'); bl([p[1] for p in pals], 'PAL0'); bl([p[2] for p in pals], 'PAL1'); bl([p[3] for p in pals], 'PAL2')

def big(t):                     # modo 7: 20 columnas, colores por los 2 bits altos (PF0)
    return font.text(t, 20, center=True, color=0)
FR = {1: ['CUANDO CAYÓ EL CORAZÓN DE ACERO...', 'EL VACÍO TOMÓ SU LUGAR...', 'EL ALMA DEL UNIVERSO PIDE TU AYUDA...'],
      2: ['EL VACÍO DA PASO AL SILENCIO.', 'EL SILENCIO ES LA PAZ.', 'LA GALAXIA RECUPERA LA ESPERANZA.', 'FIN']}[CINE]
emit('NFRASES = %d' % len(FR))
for i, f in enumerate(FR):
    ls = font.split_lines(f, 20)
    assert len(ls) <= 2, f
    ls = ([''] + ls) if len(ls) == 1 else ls
    bl(list(big(ls[0])) + list(big(ls[1])), 'FRASE%d' % i)
emit('FRASES: .word ' + ','.join('FRASE%d' % i for i in range(len(FR))))
# créditos (solo el final)
CRED = [''] * 24 + ['VÓRTICE 6', 'CORAZÓN DEL VACÍO', '', 'UN EUROSHOOTER EN 8 BITS', 'DE', 'TONY C. WARE', '', '',
        'DIRIGIDO Y DISEÑADO POR', 'TONY C. WARE', '', 'GRÁFICOS · FASES · MÚSICA', 'TONY C. WARE', '',
        '',
        'PROTAGONISTA', 'LA COMANDANTE ELARA VOSS', 'A BORDO DEL VÓRTICE 6', '', '',
        'LOS GUARDIANES DEL VACÍO', '', 'FERRUM-9', 'EL COMPACTADOR SOBERANO', '', 'THALASSA',
        'LA MADRE DE LAS MAREAS', '', 'EL TRÍPTICO DE HADES', '', 'SATURNUS', 'EL OFICIANTE VACÍO', '',
        'EL CORAZÓN NULO', 'LEVIATÁN V RESUCITADO', '', '',
        'LA FEDERACIÓN EUROPEA GALÁCTICA', 'TE DA LAS GRACIAS', '', '', 'GRACIAS POR JUGAR', '', '',
        '2026 - TONY C. WARE', '', '', 'ASISTIDO POR GPT Y CLAUDE', '', '', '', '', '', '', '', '', '', '', '']
CRED = [c.replace('·', '-') for c in CRED]
if CINE == 2:
    emit('NCRED = %d' % len(CRED))
    emit('    .align 64')
    emit('CRED:')
    for c in CRED: bl(list(font.text(c, 40, center=True)), per=20)
emit('CH_SPACE = %d' % font.CODE[' '])
emit('DIG0 = %d' % font.CODE['0'])
if CINE == 2:
    bl(list(font.text('PUNTUACIÓN FINAL', 40, center=True)), 'TXSCORE', per=20)
    bl(list(font.text('PULSA FIRE', 40, center=True)), 'TXFIRE', per=20)
# ---- INTRO: las dos páginas de la historia (se escriben letra a letra) y los datos del panel de mando
if CINE == 1:
    HIST = [
        ('LA HISTORIA - I',
         'TRAS LA CAÍDA DEL CORAZÓN DE ACERO, LEVIATÁN V, A MANOS DEL MISTERIOSO PILOTO DE LA VÓRTICE 5, '
         'VIVIMOS 2000 AÑOS DE PAZ.|'
         'HASTA AHORA. EL EMPERADOR XOR VII, DE LA FEDERACIÓN EUROPEA GALÁCTICA, REINABA EN PAZ... '
         'UNA PAZ ROTA POR SU MUERTE A MANOS DE SERES DE LOS ABISMOS DE SATURNO.'),
        ('LA HISTORIA - II',
         'EL SARCÓFAGO DE SACRIFICIOS DE SATURNO VUELVE A PALPITAR CON RITUALES PROHIBIDOS. EL OFICIANTE VACÍO, '
         'NIGROMANTE CÓSMICO, ESTÁ DECIDIDO A RESUCITAR AL ORDENADOR LOCO QUE QUISO DESTRUIR LA GALAXIA... LEVIATÁN V.|'
         'POR ESA RAZÓN, LA FEDERACIÓN ENVÍA A LA DESCENDIENTE DIRECTA DEL MISTERIOSO PILOTO QUE NOS SALVÓ UNA VEZ, '
         'LA COMANDANTE ELARA VOSS, A BORDO DEL NUEVO CAZA ESTELAR VÓRTICE 6.|'
         'SU MISIÓN: DESTRUIR AL CORAZÓN DEL VACÍO.')]
    for n, (tit, txt) in enumerate(HIST):
        lines = []
        for k, par in enumerate(txt.split('|')):
            if k: lines.append('')
            lines += font.split_lines(par, 38)
        assert len(lines) <= 17, len(lines)
        bl(list(font.text(tit, 20, center=True, color=0)), 'HIST%d_T' % n)
        emit('HIST%d_N = %d' % (n, len(lines)))
        emit('HIST%d:' % n)
        for l in lines: bl(list(font.text((' ' + l).ljust(40), 40)), per=20)
    import menu_art as M
    M.check()
    ML = []
    def memit(x): ML.append(x)
    def mbl(data, lab=None, per=16):
        if lab: memit('%s:' % lab)
        for i in range(0, len(data), per): memit('    .byte ' + ','.join('$%02X' % b for b in data[i:i + per]))
    raw = M.tobytes_rows(0, 192)
    def rle(d):
        out = bytearray(); i = 0; n = len(d)
        while i < n:
            j = i
            while j < n and j - i < 128 and d[j] == d[i]: j += 1
            if j - i >= 3:
                out += bytes([(257 - (j - i)) & 255, d[i]]); i = j; continue
            lit = bytearray(); j = i
            while j < n and len(lit) < 128:
                k = j
                while k < n and k - j < 3 and d[k] == d[j]: k += 1
                if k - j >= 3: break
                lit.append(d[j]); j += 1
            out += bytes([len(lit) - 1]) + lit; i = j
        out.append(0x80)                  # fin
        return bytes(out)
    def unrle(r):
        o = bytearray(); i = 0
        while r[i] != 0x80:
            c = r[i]
            if c < 128: o += r[i + 1:i + 2 + c]; i += 2 + c
            else: o += bytes([r[i + 1]]) * (257 - c); i += 2
        return bytes(o)
    R = rle(raw); assert unrle(R) == raw
    mbl(R, 'MENURLE')
    for k, nm in enumerate(('MPALBK', 'MPAL0', 'MPAL1', 'MPAL2')): bl([p[k] for p in M.pal], nm)
    MENA = 0x8010
    def rowaddr(y): return MENA + 40 * y if y < 102 else 0x9000 + 40 * (y - 102)
    def crop(rows_list, n):
        x0 = min(min(i for i in range(40) if any(r[y * 40 + i] for y in range(n))) for r in rows_list)
        x1 = max(max(i for i in range(40) if any(r[y * 40 + i] for y in range(n))) for r in rows_list) + 1
        return x0, x1 - x0, [[bytes(r[y * 40 + x0:y * 40 + x1]) for y in range(n)] for r in rows_list]
    dx, dw, dr = crop(M.DIFROWS, 8)
    emit('DIFADR = $%04X' % (rowaddr(M.DIF_Y) + dx)); emit('DIFW = %d' % dw)
    for i, r in enumerate(dr): bl(b''.join(r), 'DIFR%d' % i)
    lx, lw, lr = crop(M.LBLROWS, 6)
    emit('LBLADR = $%04X' % (rowaddr(M.LBL_Y - 1) + lx)); emit('LBLW = %d' % lw)
    for i, r in enumerate(lr): bl(b''.join(r), 'LBLR%d' % i)
    bl(M.DIGB, 'DIGB')
    emit('RECADR = $%04X' % (rowaddr(M.REC_Y) + M.REC_DX))
    emit('MENA = $%04X' % MENA)
    emit('MON_B0 = %d' % M.MON_B0); emit('MON_B1 = %d' % M.MON_B1)
    bl([b0 for b0, b1 in M.ENT_B], 'ENTB0'); bl([b1 for b0, b1 in M.ENT_B], 'ENTB1')
    bl([x for x, y in M.SHIP_PATH], 'PATHX'); bl([y for x, y in M.SHIP_PATH], 'PATHY')
    _eh = [2, 2, 3, 3, 4, 4, 4, 4, 3, 3, 2, 2, 3, 3, 4, 4]
    bl([_eh[i] * 16 + (0, 0, 2, 2, 4, 4, 4, 2, 2, 0, 0, 0, 2, 4, 2, 0)[i] for i in range(16)], 'EUROBG')
    bl([0x0A, 0x0C, 0x0C, 0x0E, 0x0E, 0x0E, 0x0E, 0x0C, 0x0C, 0x0A, 0x0A, 0x0A, 0x0C, 0x0E, 0x0C, 0x0A], 'EUROTX')
    bl([0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E, 0x0E, 0x0E, 0x0E, 0x0E, 0x0C, 0x0A, 0x08, 0x06, 0x04, 0x04], 'FIRETAB')
    emit('CH_CUR = %d' % font.CODE['■'])
    open(os.path.join(OUT, 'menudata.s'), 'w').write('\n'.join(ML) + '\n')
    print('panel: imagen %d bytes comprimida en %d' % (len(raw), len(R)))
# fuente del juego (1 KB, alineada)
emit('    .align 1024')
bl(list(font.font_bytes()), 'FONT')
open(os.path.join(OUT, 'cinedata.s'), 'w').write('\n'.join(L) + '\n')
print('cine %d: %d franjas, %d frases, %d líneas de créditos' % (CINE, NB, len(FR), len(CRED)))
