#!/usr/bin/env python3
"""VÓRTICE 6 · FASE 1 jugable · genera src/g1data.s desde gfx/*.py y comprueba los límites."""
import os, sys, json, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'gfx'), os.path.join(ROOT, 'tools')]
import hw, sprites as S, world, nivel1, font, ferrum, mecha, thalassa
FASE = int(os.environ.get('V6FASE', '1'))
if FASE == 5:
    import nivel5, propuestas6 as P6, propuestas5 as P5
    NV = nivel5
    import corazon
    JEFE = corazon
elif FASE == 4:
    import nivel4, propuestas5 as P5
    NV = nivel4
    import saturnus
    JEFE = saturnus
elif FASE == 3:
    import nivel3, propuestas4 as P4
    NV = nivel3
    import triptico
    JEFE = triptico
elif FASE == 2:
    import nivel2, propuestas3 as P3
    NV = nivel2
    JEFE = thalassa
else:
    NV = nivel1
    JEFE = ferrum
from cells import encode

out = []
def emit(s=''): out.append(s)
def bl(b, per=16, lab=None):
    if lab: emit(lab + ':')
    b = list(b)
    for i in range(0, len(b), per):
        emit('    .byte ' + ','.join('$%02X' % x for x in b[i:i + per]))

PH = hw.PHASES[0] if FASE == 1 else dict(hw.PHASES[FASE - 1], **NV.PAL)
BASE = 0x2000

# ======================================================================= juegos de caracteres
class SortedCharset:
    """código 0 = vacío; primero los no sólidos, luego los sólidos (colisión = código >= SOLID0)"""
    def __init__(s, name): s.name = name; s.cells = {}; s.solid = {}
    def add(s, cell, solid):
        e = encode(cell)
        assert e is not None, (s.name, cell)
        s.cells.setdefault(e[0], e[1]); s.solid[e[0]] = s.solid.get(e[0], False) or solid
        return e[0]
    def finish(s):
        blank = bytes(8)
        ns = [b for b in s.cells if not s.solid[b] and b != blank]
        so = [b for b in s.cells if s.solid[b] and b != blank]
        s.glyphs = [blank] + ns + so
        s.solid0 = 1 + len(ns)
        assert len(s.glyphs) <= 128, '%s: %d caracteres' % (s.name, len(s.glyphs))
        s.idx = {g: i for i, g in enumerate(s.glyphs)}
    def code(s, cell):
        b, inv = encode(cell)
        return s.idx[b] | (0x80 if inv else 0)
    def data(s): return b''.join(s.glyphs) + bytes(8 * (128 - len(s.glyphs)))

def cell(p, c, r): return tuple(''.join(p[r * 8 + y][c * 4 + x] for x in range(4)) for y in range(8))

L = NV.build()
CL = SortedCharset('NIVEL1')
for c in range(NV.COLS):
    for r in range(20):
        CL.add(cell(L.p, c, r), any(L.solid[r * 8 + y][c * 4 + x] for y in range(8) for x in range(4)))
CL.finish()

# ---- pantalla del jefe: la ventana final del nivel + FERRUM-9 (versión 2)
BOSS_K = getattr(JEFE, 'BOSS_K', 27)    # byte de la ventana donde empieza el jefe (27 = columna visible 24)
BOSS_R = getattr(JEFE, 'BOSS_R', 3)     # fila de campo donde empieza
bscr = [[L.p[y][NV.ARENA * 4 + x] for x in range(48 * 4)] for y in range(160)]
bsol = [[L.solid[y][NV.ARENA * 4 + x] for x in range(48 * 4)] for y in range(160)]
def put_boss(scr, sol, cv):
    for y in range(JEFE.H):
        for x in range(JEFE.W):
            Y, X = BOSS_R * 8 + y, BOSS_K * 4 + x
            if getattr(JEFE, 'EXENTO', False) and cv.p[y][x] == '.': continue   # jefe exento: deja ver el decorado
            scr[Y][X] = cv.p[y][x]; sol[Y][X] = cv.p[y][x] != '.'
put_boss(bscr, bsol, JEFE.boss(0))
CB = SortedCharset('JEFE1')
for c in range(48):
    for r in range(20):
        CB.add(cell(bscr, c, r), any(bsol[r * 8 + y][c * 4 + x] for y in range(8) for x in range(4)))
# estados del ojo (celdas: filas de canvas 6-7, columnas 6-10)
EYE_ROWS, EYE_C0, EYE_NC = getattr(JEFE, 'EYE_ROWS', (6, 7)), getattr(JEFE, 'EYE_C0', 6), getattr(JEFE, 'EYE_NC', 5)
eye_cells = []
for st in range(3):
    cv = JEFE.boss(st); row = []
    for cr in EYE_ROWS:
        for cc in range(EYE_C0, EYE_C0 + EYE_NC):
            ce = cell(cv.p, cc, cr); CB.add(ce, True); row.append(ce)
    eye_cells.append(row)
plate_cell = tuple(['3333'] + ['2222'] * 6 + ['1111']) if FASE == 1 else tuple(['2222', '1111', '2222', '3333', '3333', '2222', '1111', '2222']) if FASE == 4 else tuple(['3333', '2222', '1212', '1111', '1111', '2121', '2222', '3333']) if FASE == 5 else tuple(['2222', '3322', '2233', '2222', '1122', '2211', '2222', '2222'])   # placa / mechón de pelo
CB.add(plate_cell, True)
# fase 3: roca de la LLUVIA DE ESCORIA (2x2 celdas, 8 píxeles x 16 líneas, sólida)
ROCK = ['..1111..', '.122221.', '12233221', '12322321', '12233221', '.1222321', '12232221', '12222321',
        '.1232221', '12222331', '12332221', '.1222221', '12223221', '.122221.', '..1221..', '...11...']
rock_cells = []
if FASE == 3:
    for r in range(2):
        for k in range(2):
            ce = tuple(ROCK[r * 8 + y][k * 4:k * 4 + 4].replace('.', '.') for y in range(8))
            CB.add(ce, True); rock_cells.append(ce)
CB.finish()
# hasta dónde llegan las placas en cada fila (byte de la ventana, exclusivo)
bc = JEFE.boss(0)
FILLEND = []
for r in range(20):
    if r < 2 or r > 17: FILLEND.append(3); continue
    cr = r - BOSS_R
    if cr < 0 or cr >= JEFE.H // 8:
        FILLEND.append(43); continue
    rows = bc.p[cr * 8:cr * 8 + 8]
    left = [x for x in range(JEFE.FACE - 4) if any(rw[x] != '.' for rw in rows)]
    if FASE in (2, 4, 5):
        xs = [x for x in range(JEFE.W) if any(rw[x] != '.' for rw in rows)]
        FILLEND.append(BOSS_K + (min(xs) // 4 if xs else 16)); continue
    FILLEND.append(BOSS_K if not left and JEFE.POCKET_Y0 <= cr * 8 and cr * 8 + 7 <= JEFE.POCKET_Y1 + 6 else BOSS_K + JEFE.FACE // 4)
print('placas hasta (byte por fila):', FILLEND)
EYEROW0 = BOSS_R + EYE_ROWS[0]
EYEK0 = BOSS_K + EYE_C0
lg = world.logo()
CLG = SortedCharset('LOGO')
for c in range(40):
    for r in range(world.LOGO_ROWS): CLG.add(cell(lg.p, c, r), True)
CLG.finish()

emit('; ===== generado por tools/gen1.py: no editar =====')
emit('; ---- juegos de caracteres (1 KB, alineados en $2000)')
CH = {}
for cs in (CL, CB, CLG):
    CH[cs.name] = BASE + 1024 * len(CH)
    emit('CH_%s:  ; %d caracteres, sólidos desde %d' % (cs.name, len(cs.glyphs), cs.solid0))
    bl(cs.data())
CH['FONT'] = BASE + 1024 * len(CH)
emit('CH_FONT:'); bl(font.font_bytes())
emit('SOLID0_N = %d' % CL.solid0)
emit('SOLID0_B = %d' % CB.solid0)
emit('PLATECH = $%02X' % CB.code(plate_cell))
if rock_cells: emit('ROCKCH: .byte ' + ','.join('$%02X' % CB.code(c) for c in rock_cells))
emit('FILLEND: .byte ' + ','.join('%d' % v for v in FILLEND))
emit('BOSSHP = %d' % {1: 40, 2: 60, 3: 110, 4: 140, 5: 180}.get(FASE, 40))
emit('BOSSK0 = %d' % BOSS_K)
emit('BOSSK1 = %d' % min(43, BOSS_K + JEFE.W // 4))
emit('BOSSR0 = %d' % BOSS_R)
emit('BOSSR1 = %d' % (BOSS_R + getattr(JEFE, 'FILAS', JEFE.H // 8)))
emit('BOSSX0 = %d' % (4 * BOSS_K + 35))
emit('BOSSY0 = %d' % (42 + 8 * BOSS_R))
emit('BOSSYM = %d' % (127 if JEFE.H >= 128 else 63))
emit('BKWARN = $%02X        ; destello de aviso del fondo' % (0x42 if FASE == 1 else 0x46 if FASE == 5 else 0xA6))
G = getattr(NV, 'GEYSERS', [])
emit('NGEY = %d' % len(G))
if G:
    emit('GEYCL: .byte ' + ','.join('<%d' % c for c, a, b in G))
    emit('GEYCH: .byte ' + ','.join('>%d' % c for c, a, b in G))
    emit('GEYY0: .byte ' + ','.join('%d' % (42 + 8 * a) for c, a, b in G))
    emit('GEYY1: .byte ' + ','.join('%d' % (42 + 8 * b + 7) for c, a, b in G))
# fase 2: carriles de la corriente. Tres carriles (filas 2-6, 7-12, 13-17); en cada ciclo uno queda libre
# y los chorros llenan las otras filas, de lejos hacia el carril libre, de dos en dos (6 pasos)
LANES = [range(2, 7), range(7, 13), range(13, 18)]
lt = []
for libre in range(3):
    filas = [r for r in range(2, 18) if r not in LANES[libre]]
    centro = (LANES[libre][0] + LANES[libre][-1]) / 2
    filas.sort(key=lambda r: -abs(r - centro))
    filas += [0] * (12 - len(filas))
    lt += filas
emit('LANEROWS: .byte ' + ','.join('%d' % v for v in lt))
for st in range(3):
    emit('EYE%d: .byte ' % st + ','.join('$%02X' % CB.code(c) for c in eye_cells[st]))
emit('EYEROW0 = %d' % EYEROW0)
emit('EYEK0 = %d' % EYEK0)
emit('EYENC = %d' % EYE_NC)
_facek = BOSS_K + JEFE.FACE // 4
emit('EYEX0 = %d          ; HPOS desde donde un disparo da en el ojo: 24 antes de la cara (la punta del láser va 14 por delante y avanza 8)' % (4 * _facek + 35 - 24))
emit('EYEY0 = %d' % (42 + 8 * EYEROW0 - 2))
emit('EYEY1 = %d' % (42 + 8 * EYEROW0 + 18))
emit('JAWX = %d' % ((4 * _facek + 35 - 10) if hasattr(JEFE, 'MOUTH_Y0') else (4 * BOSS_K + 35 - 6)))
emit('JAWY0 = %d' % (42 + 8 * BOSS_R + getattr(JEFE, 'MOUTH_Y0', 30)))
emit('JAWY1 = %d' % (42 + 8 * BOSS_R + getattr(JEFE, 'MOUTH_Y1', 76)))
emit('EYEPX = %d' % (4 * _facek + 35 - 4))
emit('EYEPY = %d' % (42 + 8 * BOSS_R + JEFE.EYE_CY - 3))

# ======================================================================= nivel: 4 diccionarios de trozos de 5 filas
codes = [[CL.code(cell(L.p, c, r)) for r in range(20)] for c in range(NV.COLS)]
for q in range(4):
    d = {}; seq = []
    for c in range(NV.COLS):
        t = tuple(codes[c][q * 5:q * 5 + 5])
        if t not in d: d[t] = len(d)
        seq.append(d[t])
    assert len(d) <= 256, 'cuarto %d: %d trozos' % (q, len(d))
    emit('; ---- cuarto %d: %d trozos' % (q, len(d)))
    emit('QD%d:' % q)
    for t, i in sorted(d.items(), key=lambda kv: kv[1]):
        emit('    .byte ' + ','.join('$%02X' % v for v in t))
    emit('QL%d: .byte ' % q + ','.join('<(QD%d+%d)' % (q, 5 * i) for i in range(len(d))))
    emit('QH%d: .byte ' % q + ','.join('>(QD%d+%d)' % (q, 5 * i) for i in range(len(d))))
    emit('MAPQ%d:' % q)
    for i in range(0, len(seq), 32): emit('    .byte ' + ','.join('%d' % v for v in seq[i:i + 32]))
    print('cuarto', q, len(d), 'trozos')
emit('LEVCOLS = %d' % NV.COLS)
emit('ARENA = %d' % NV.ARENA)
emit('BKG: .byte ' + ','.join('$%02X' % v for v in NV.BKGRAD))

# ---- pantalla del jefe (se copia a RAM)
emit('BOSSROM:')
for r in range(20):
    emit('    .byte ' + ','.join('$%02X' % CB.code(cell(bscr, c, r)) for c in range(48)))

# ---- oleadas (por franja)
W = NV.WAVES
TYP = {1: {'R': 1, 'C': 2, 'M': 8}, 2: {'J': 1, 'R': 2, 'M': 8, 'A': 9}, 3: {'A': 1, 'S': 2, 'M': 8, 'P': 9}, 4: {'A': 1, 'G': 2, 'M': 8, 'V': 9, 'E': 10}, 5: {'G': 1, 'L': 2, 'M': 8, 'S': 10}}[FASE]
emit('FASE = %d' % FASE)
# ---- curva de dificultad (Euroshooter: dura pero justa, sube fase a fase)
#   BULXTRA: velocidad extra de las balas enemigas · FAIRD: distancia mínima de nacimiento por delante de la nave
#   UZWAIT: cuadros entre disparos de la UNIDAD CERO · HPX: vida extra de los enemigos comunes · GAPF: densidad de oleadas
DIF = {1: (0, 0, 70, 1.00), 2: (0, 0, 62, 0.92), 3: (1, 1, 54, 0.85), 4: (1, 1, 46, 0.80), 5: (2, 2, 40, 0.75)}[FASE]
BULXTRA, HPX, UZWAIT, GAPF = DIF
emit('BULXTRA = %d' % BULXTRA)
emit('FAIRD = %d' % (32 + 6 * BULXTRA))
emit('UZWAIT = %d' % UZWAIT)
# jefes: aviso, paso de cierre y duración de la 1.ª fase, más cortos fase a fase (más tensos, siempre con tiempo)
BWARN, BSTEP, BREC = {1: (36, 14, 260), 2: (34, 13, 250), 3: (30, 12, 240), 4: (28, 11, 220), 5: (26, 10, 200)}[FASE]
emit('BWARN = %d' % BWARN)
emit('BSTEP = %d' % BSTEP)
emit('BREC = %d' % BREC)
emit('UNPLT = %d' % (BWARN + 8 * BSTEP + 48))
# ---- dificultades: FÁCIL · NORMAL · HARDCORE (el motor copia la columna elegida al empezar)
def _b(v): return '$%02X' % (v & 0xFF)
emit('DBULX: .byte %s, %s, %s   ; velocidad extra de las balas' % (_b(BULXTRA - 1), _b(BULXTRA), _b(BULXTRA + 1)))
emit('DFAIR: .byte %d, %d, %d   ; distancia mínima de nacimiento' % (32 + 6 * BULXTRA + 12, 32 + 6 * BULXTRA, 32 + 6 * BULXTRA - 4))
emit('DHPADJ: .byte $FF, 0, 1   ; golpes de más o de menos de los enemigos')
emit('DUZW: .byte %d, %d, %d   ; cuadros entre disparos de la UNIDAD CERO' % (round(UZWAIT * 1.3), UZWAIT, round(UZWAIT * 0.75)))
_ew = 30 if FASE == 4 else 24
emit('DESCW: .byte %d, %d, %d   ; aviso de la raya del ESCRIBA' % (_ew + 12, _ew, _ew - 6))
emit('DBWARN: .byte %d, %d, %d   ; aviso de los ataques del jefe' % (BWARN + 12, BWARN, BWARN - 6))
emit('DBSTEP: .byte %d, %d, %d   ; paso de cierre de los ataques del jefe' % (BSTEP + 4, BSTEP, BSTEP - 2))
_bh = {1: 40, 2: 60, 3: 110, 4: 140, 5: 180}.get(FASE, 40)
emit('DBHP: .byte %d, %d, %d   ; vida del jefe' % (round(_bh * 0.75), _bh, min(250, round(_bh * 1.25))))
assert (BWARN + 12) + 8 * (BSTEP + 4) + 56 < 256
emit('NWAVES = %d' % len(W))
emit('WVCL: .byte ' + ','.join('<%d' % w[0] for w in W))
emit('WVCH: .byte ' + ','.join('>%d' % w[0] for w in W))
emit('WVTYP: .byte ' + ','.join('%d' % TYP[w[1]] for w in W))
emit('WVN: .byte ' + ','.join('%d' % w[2] for w in W))
emit('WVB: .byte ' + ','.join('%d' % w[3] for w in W))
emit('WVB2: .byte ' + ','.join('%d' % (w[3] + 1 if w[3] < 3 else 2) for w in W))
emit('WVGAP: .byte ' + ','.join('%d' % (w[4] if w[4] <= 1 else max(16, round(w[4] * GAPF))) for w in W))
emit('WVDROP: .byte ' + ','.join('%d' % {'': 0, 'P': 3, 'S': 4}[w[5]] for w in W))
# patrones de oleada (7.º campo, opcional): D por detrás · B bucle · Q patrulla · C carga · E escalera
PAT = {'': 0, 'D': 1, 'B': 2, 'Q': 3, 'C': 4, 'E': 5}
for w in W:
    if len(w) > 6 and w[6]:
        assert TYP[w[1]] in (1, 2, 9) and not (FASE == 4 and w[1] == 'E'), ('patrón solo para enemigos comunes', w)
emit('WVPAT: .byte ' + ','.join('%d' % PAT[w[6] if len(w) > 6 else ''] for w in W))
emit('CIRX: .byte ' + ','.join('%d' % (round(20 * math.cos(2 * math.pi * i / 64)) & 255) for i in range(64)))
emit('CIRY: .byte ' + ','.join('%d' % round(10 - 10 * math.sin(2 * math.pi * i / 64)) for i in range(64)))
# franjas: filas 2-5, 6-9, 10-13, 14-17 -> primera línea donde puede empezar un sprite (y la última = +20)
emit('BTOP: .byte ' + ','.join('%d' % (42 + 8 * (2 + 4 * b) + 1) for b in range(4)))
emit('ZIG: .byte ' + ','.join('%d' % (round(20 * (i / 32 if i < 32 else (64 - i) / 32))) for i in range(64)))

# ======================================================================= sprites
def pl(rows, on, shift=0, n=11):
    o = []
    for l in rows:
        v = 0
        for x in range(8):
            c = l[x + shift] if x + shift < len(l) else '.'
            v = (v << 1) | (1 if c in on else 0)
        o.append(v)
    return (o + [0] * n)[:n]
emit('; ---- sprites (11 bytes)')
for k in ('A', 'B'):
    bl(pl(S.SHIP[k], 'ac', 0), lab='SHIP_%s_P0' % k)
    bl(pl(S.SHIP[k], 'bc', 4), lab='SHIP_%s_P1' % k)
bl(pl(S.SHIP_BOOM[0], 'a'), lab='SBOOM0'); bl(pl(S.SHIP_BOOM[1], 'a'), lab='SBOOM1')
DEBRIS = ['........', '..XXX...', '.XX.XX..', 'XXXXX...', '.XX.XXX.', '..XXX...', '........', '........']
if FASE == 2:
    DEBRIS = ['..XXXX..', '.X....X.', 'X..XX..X', 'X.X....X', 'X......X', 'X......X', '.X....X.', '..XXXX..']   # burbuja grande
    S.ORB = ['........', '..XXX...', '.XXXXX..', '.X.X.X..', '.XXXXX..', '.X.X.X..', 'X.X.X...', '.X...X..']    # cría
shapes = [('REC_A', S.FLY['CARROÑERO'][0], 'X'), ('REC_B', S.FLY['CARROÑERO'][1], 'X'),
          ('CPP_A', S.PAIR['CAPSULA P'][0], 'ac'), ('CPP_B', S.PAIR['CAPSULA P'][0], 'bc'),
          ('CPS_A', S.PAIR['CAPSULA S'][0], 'ac'), ('CPS_B', S.PAIR['CAPSULA S'][0], 'bc'),
          ('BOOM0', S.BOOM[0], 'X'), ('BOOM1', S.BOOM[1], 'X'), ('BOOM2', S.BOOM[2], 'X'),
          ('ORB', S.ORB, 'X'), ('DEBR', DEBRIS, 'X'),
          ]
for lab, rows, on in shapes: bl(pl(rows, on), lab='SH_' + lab)
# CHATARRÍN (pareja a +4): A/B = cuadro 1 en P2/P3, C/D = cuadro 2
ca, cb = S.CHATARRIN
bl(pl(ca, 'ac', 0), lab='SH_CHA_A'); bl(pl(ca, 'bc', 4), lab='SH_CHA_B')
bl(pl(cb, 'ac', 0), lab='SH_CHA_C'); bl(pl(cb, 'bc', 4), lab='SH_CHA_D')
# UNIDAD CERO mecha (24 líneas, pareja a +4)
bl(pl(mecha.MECHA_A, 'ac', 0, 24), lab='SH_MEC_A'); bl(pl(mecha.MECHA_A, 'bc', 4, 24), lab='SH_MEC_B')
bl(pl(mecha.MECHA_B, 'ac', 0, 24), lab='SH_MEC_C'); bl(pl(mecha.MECHA_B, 'bc', 4, 24), lab='SH_MEC_D')
# ---- tablas por tipo (0..9): 1/2/9 cambian con la fase; 3 cápsula P, 4 cápsula S, 5 explosión, 6 orbe, 7 chatarra, 8 UNIDAD CERO
#   OPAIR: usa P2 y P3 · OPOFS: x de P3 respecto a P2 (color clocks) · OSIZE: 1 = doble ancho (SIZEP por franja en la DLI)
#   OFRM: máscara de frame para el 2.º cuadro · SHL/SHH: 4 formas por tipo (cuadro 1 P2, cuadro 1 P3, cuadro 2 P2, cuadro 2 P3)
def norm12(rows):
    out = []
    for r in rows:
        q = ''
        for x, ch in enumerate(r.ljust(12, '.')):
            q += '.' if ch == '.' else ('a' if x < 4 else 'b' if x > 7 else ('c' if ch == 'X' else ch))
        out.append(q)
    return out
T10 = T11 = ['SH_ORB'] * 4
C10 = C11 = (0x0E, 0x0E)
PROP10 = PROP11 = (11, 7, 6, 0, 0, 0, 8, 1)
NODO_A = ['...XX...', '..X..X..', '.X.XX.X.', 'X.XXXX.X', 'X.X..X.X', 'X.XXXX.X', '.X.XX.X.', '..X..X..', '...XX...', '........', '........']
NODO_B = ['...XX...', '..XXXX..', '.XX..XX.', 'XX.XX.XX', 'X.XXXX.X', 'XX.XX.XX', '.XX..XX.', '..XXXX..', '...XX...', '........', '........']
if FASE == 5:
    glo = P6.GLOBULO['B · glóbulo de membrana dentada (12x11)']
    lar = P6.LARVA['A · dron segmentado con mandíbulas (12x8)']
    esc = P5.ESCRIBA['B · escriba con tablilla (12x14)']
    a1, a2 = norm12(glo[2]), norm12(glo[3])
    bl(pl(a1, 'ac', 0, 11), lab='SH_T1A'); bl(pl(a1, 'bc', 4, 11), lab='SH_T1B')
    bl(pl(a2, 'ac', 0, 11), lab='SH_T1C'); bl(pl(a2, 'bc', 4, 11), lab='SH_T1D')
    b1, b2 = norm12(lar[2]), norm12(lar[3])
    bl(pl(b1, 'ac', 0, 8), lab='SH_T2A'); bl(pl(b1, 'bc', 4, 8), lab='SH_T2B')
    bl(pl(b2, 'ac', 0, 8), lab='SH_T2C'); bl(pl(b2, 'bc', 4, 8), lab='SH_T2D')
    e1_, e2_ = norm12(esc[2]), norm12(esc[3])
    bl(pl(e1_, 'ac', 0, 14), lab='SH_TAA'); bl(pl(e1_, 'bc', 4, 14), lab='SH_TAB')
    bl(pl(e2_, 'ac', 0, 14), lab='SH_TAC'); bl(pl(e2_, 'bc', 4, 14), lab='SH_TAD')
    bl(pl(NODO_A, 'X'), lab='SH_NODA'); bl(pl(NODO_B, 'X'), lab='SH_NODB')
    T1 = ['SH_T1A', 'SH_T1B', 'SH_T1C', 'SH_T1D']; T2 = ['SH_T2A', 'SH_T2B', 'SH_T2C', 'SH_T2D']; T9 = T1
    T10 = ['SH_TAA', 'SH_TAB', 'SH_TAC', 'SH_TAD']; T11 = ['SH_NODA', 'SH_NODA', 'SH_NODB', 'SH_NODB']
    # sin verdes: glóbulo rojo sangre, larva hueso salmón, escribas hueso y magenta (fantasmas de Saturno)
    C1, C2, C10, C11 = (0x4A, 0x0E), (0x3C, 0x0E), (0x0C, 0x5C), (0x0E, 0x0E)
    C9 = C1
    PROP = {1: (11, 12, 9, 1, 4, 0, 8, 1), 2: (8, 12, 6, 1, 4, 0, 8, 1), 9: (11, 12, 9, 1, 4, 0, 8, 1)}
    PROP10 = (14, 12, 12, 1, 4, 0, 8, 2 + HPX)
    PROP11 = (11, 8, 9, 0, 0, 0, 16, 6)
elif FASE == 4:
    aco = P5.ACOLITO['B · rombo con anillo orbital (16x9, doble ancho)']
    gua = P5.GUARDIAN['A · segmento curvo de armadura (12x14)']
    vas = P5.VASO['A · urna negra con luz púrpura (8x12)']
    esc = P5.ESCRIBA['B · escriba con tablilla (12x14)']
    bl(pl(aco[2], 'ac', 0, 9), lab='SH_T1A'); bl(pl(aco[2], 'bc', 0, 9), lab='SH_T1B')
    bl(pl(aco[3], 'ac', 0, 9), lab='SH_T1C'); bl(pl(aco[3], 'bc', 0, 9), lab='SH_T1D')
    g1_, g2_ = norm12(gua[2]), norm12(gua[3])
    bl(pl(g1_, 'ac', 0, 14), lab='SH_T2A'); bl(pl(g1_, 'bc', 4, 14), lab='SH_T2B')
    bl(pl(g2_, 'ac', 0, 14), lab='SH_T2C'); bl(pl(g2_, 'bc', 4, 14), lab='SH_T2D')
    bl(pl(vas[2], 'ac', 0, 12), lab='SH_T9A'); bl(pl(vas[2], 'bc', 0, 12), lab='SH_T9B')
    bl(pl(vas[3], 'ac', 0, 12), lab='SH_T9C'); bl(pl(vas[3], 'bc', 0, 12), lab='SH_T9D')
    e1_, e2_ = norm12(esc[2]), norm12(esc[3])
    bl(pl(e1_, 'ac', 0, 14), lab='SH_TAA'); bl(pl(e1_, 'bc', 4, 14), lab='SH_TAB')
    bl(pl(e2_, 'ac', 0, 14), lab='SH_TAC'); bl(pl(e2_, 'bc', 4, 14), lab='SH_TAD')
    bl(pl(NODO_A, 'X'), lab='SH_NODA'); bl(pl(NODO_B, 'X'), lab='SH_NODB')
    T1 = ['SH_T1A', 'SH_T1B', 'SH_T1C', 'SH_T1D']; T2 = ['SH_T2A', 'SH_T2B', 'SH_T2C', 'SH_T2D']; T9 = ['SH_T9A', 'SH_T9B', 'SH_T9C', 'SH_T9D']
    T10 = ['SH_TAA', 'SH_TAB', 'SH_TAC', 'SH_TAD']; T11 = ['SH_NODA', 'SH_NODA', 'SH_NODB', 'SH_NODB']
    C1, C2, C9, C10, C11 = aco[1], gua[1], vas[1], esc[1], (0xCE, 0xCE)
    #       alto, ancho, alto de choque, pareja, x de P3, doble ancho, máscara de cuadro, vida
    PROP = {1: (9, 16, 7, 1, 0, 1, 8, 1), 2: (14, 12, 12, 1, 4, 0, 8, 3), 9: (12, 8, 10, 1, 0, 0, 8, 1)}
    PROP10 = (14, 12, 12, 1, 4, 0, 8, 2 + HPX)
    PROP11 = (11, 8, 9, 0, 0, 0, 16, 4)
elif FASE == 3:
    asc = P4.ASCORIA['A · roca facetada, 3 colores (8x8)']
    ser = P4.SERAFIN['A · caza de alas en flecha (12x11)']
    mar = P4.MARTIR['A · espectro encapuchado, 3 colores (8x16)']
    def norm12(rows):
        out = []
        for r in rows:
            q = ''
            for x, ch in enumerate(r.ljust(12, '.')):
                q += '.' if ch == '.' else ('a' if x < 4 else 'b' if x > 7 else ('c' if ch == 'X' else ch))
            out.append(q)
        return out
    bl(pl(asc[2], 'ac', 0, 8), lab='SH_T1A'); bl(pl(asc[2], 'bc', 0, 8), lab='SH_T1B')
    bl(pl(asc[3], 'ac', 0, 8), lab='SH_T1C'); bl(pl(asc[3], 'bc', 0, 8), lab='SH_T1D')
    s1, s2 = norm12(ser[2]), norm12(ser[3])
    bl(pl(s1, 'ac', 0, 11), lab='SH_T2A'); bl(pl(s1, 'bc', 4, 11), lab='SH_T2B')
    bl(pl(s2, 'ac', 0, 11), lab='SH_T2C'); bl(pl(s2, 'bc', 4, 11), lab='SH_T2D')
    bl(pl(mar[2], 'ac', 0, 16), lab='SH_T9A'); bl(pl(mar[2], 'bc', 0, 16), lab='SH_T9B')
    bl(pl(mar[3], 'ac', 0, 16), lab='SH_T9C'); bl(pl(mar[3], 'bc', 0, 16), lab='SH_T9D')
    T1 = ['SH_T1A', 'SH_T1B', 'SH_T1C', 'SH_T1D']; T2 = ['SH_T2A', 'SH_T2B', 'SH_T2C', 'SH_T2D']; T9 = ['SH_T9A', 'SH_T9B', 'SH_T9C', 'SH_T9D']
    C1, C2, C9 = asc[1], ser[1], mar[1]
    PROP = {1: (8, 8, 7, 1, 0, 0, 8, 2), 2: (11, 12, 9, 1, 4, 0, 8, 1), 9: (16, 8, 14, 1, 0, 0, 8, 2)}
elif FASE == 2:
    med = P3.MEDUSA['B · campana, 3 colores (8x14)']
    man = P3.MANTA = P3.RAYA['B · manta, 3 colores, doble ancho (16x9)']
    ang = P3.ANGUILA['C · anguila larga, doble ancho (24x8)']
    def norm12(rows):
        out = []
        for r in rows:
            q = ''
            for x, ch in enumerate(r.ljust(12, '.')):
                q += '.' if ch == '.' else ('a' if x < 4 else 'b' if x > 7 else ('c' if ch == 'X' else ch))
            out.append(q)
        return out
    bl(pl(med[2], 'ac', 0, 14), lab='SH_T1A'); bl(pl(med[2], 'bc', 0, 14), lab='SH_T1B')
    bl(pl(med[3], 'ac', 0, 14), lab='SH_T1C'); bl(pl(med[3], 'bc', 0, 14), lab='SH_T1D')
    bl(pl(man[2], 'ac', 0, 9), lab='SH_T2A'); bl(pl(man[2], 'bc', 0, 9), lab='SH_T2B')
    bl(pl(man[3], 'ac', 0, 9), lab='SH_T2C'); bl(pl(man[3], 'bc', 0, 9), lab='SH_T2D')
    a1, a2 = norm12(ang[2]), norm12(ang[3])
    bl(pl(a1, 'ac', 0, 8), lab='SH_T9A'); bl(pl(a1, 'bc', 4, 8), lab='SH_T9B')
    bl(pl(a2, 'ac', 0, 8), lab='SH_T9C'); bl(pl(a2, 'bc', 4, 8), lab='SH_T9D')
    T1 = ['SH_T1A', 'SH_T1B', 'SH_T1C', 'SH_T1D']; T2 = ['SH_T2A', 'SH_T2B', 'SH_T2C', 'SH_T2D']; T9 = ['SH_T9A', 'SH_T9B', 'SH_T9C', 'SH_T9D']
    C1, C2, C9 = med[1], man[1], ang[1]
    PROP = {1: (14, 8, 12, 1, 0, 0, 8, 1), 2: (9, 16, 7, 1, 0, 1, 8, 1), 9: (8, 24, 6, 1, 8, 1, 8, 2)}
else:
    T1 = ['SH_REC_A', 'SH_REC_A', 'SH_REC_B', 'SH_REC_B']; T2 = ['SH_CHA_A', 'SH_CHA_B', 'SH_CHA_C', 'SH_CHA_D']; T9 = T1
    C1, C2, C9 = (0xAC, 0xAC), S.CHATARRIN_COL, (0xAC, 0xAC)
    PROP = {1: (11, 8, 9, 0, 0, 0, 8, 1), 2: (11, 12, 7, 1, 4, 0, 8, 1), 9: (11, 8, 9, 0, 0, 0, 8, 1)}
#        alto, ancho, alto de choque, pareja, x de P3, doble ancho, máscara de cuadro, vida
PROP = {t: v[:7] + (v[7] + HPX,) for t, v in PROP.items()}
TAB = {0: ((0, 0, 0, 0, 0, 0, 0, 0), ['SH_ORB'] * 4, (0, 0)),
       1: (PROP[1], T1, C1), 2: (PROP[2], T2, C2),
       3: ((11, 8, 7, 1, 0, 0, 0, 1), ['SH_CPP_A', 'SH_CPP_B'] * 2, (0x38, 0x0E)),
       4: ((11, 8, 7, 1, 0, 0, 0, 1), ['SH_CPS_A', 'SH_CPS_B'] * 2, (0x88, 0x0E)),
       5: ((11, 8, 8, 0, 0, 0, 0, 1), ['SH_BOOM0'] * 4, (0x3E, 0x3E)),
       6: ((11, 7, 6, 0, 0, 0, 8, 1), ['SH_ORB'] * 4, (0x0E, 0x0E) if FASE == 1 else (0xAC, 0xAC)),
       7: ((11, 7, 6, 0, 0, 0, 8, 1), ['SH_DEBR'] * 4, (0x2A, 0x2A) if FASE == 1 else (0x0E, 0x0E)),
       8: ((24, 12, 22, 1, 4, 0, 4, 8 + 2 * (FASE - 1)), ['SH_MEC_A', 'SH_MEC_B', 'SH_MEC_C', 'SH_MEC_D'], (0x4A, 0x0C) if FASE == 5 else mecha.MECHA_COL),   # fase 5: carne roja y acero
       9: (PROP[9], T9, C9),
       10: (PROP10, T10, C10),             # ESCRIBA (fase 4)
       11: (PROP11, T11, C11)}             # NODO de jade de la puerta ceremonial (fase 4)
NT = 12
for k, nm in enumerate(('OHGT', 'OWID', 'OHIT', 'OPAIR', 'OPOFS', 'OSIZE', 'OFRM', 'OHP')):
    emit('%s: .byte %s' % (nm, ','.join('%d' % TAB[t][0][k] for t in range(NT))))
emit('SHL: .byte ' + ','.join('<' + TAB[t][1][i] for t in range(NT) for i in range(4)))
emit('SHH: .byte ' + ','.join('>' + TAB[t][1][i] for t in range(NT) for i in range(4)))
# todos los colores de enemigo con luminancia alta: las balas que cruzan su franja toman su color
emit('OCOL2: .byte ' + ','.join('$%02X' % TAB[t][2][0] for t in range(NT)))
emit('OCOL3: .byte ' + ','.join('$%02X' % TAB[t][2][1] for t in range(NT)))
for t in (1, 2, 8, 9, 10, 11): assert TAB[t][2][0] & 15 >= 10 and TAB[t][2][1] & 15 >= 10, ('color oscuro: las balas no se verían', t)
emit('BULCOL = $2E          ; color fijo de las balas fuera de las franjas ocupadas')
emit('BOOMTAB_L: .byte <SH_BOOM0,<SH_BOOM1,<SH_BOOM2')
emit('BOOMTAB_H: .byte >SH_BOOM0,>SH_BOOM1,>SH_BOOM2')
emit('SHIPCOL: .byte $%02X,$%02X,$%02X,$%02X,$0E,$0E' % (hw.SHIP['p0'], hw.SHIP['p1'], hw.SHIELD['p0'], hw.SHIELD['p1']))
emit('PHCOL: .byte $%02X,$%02X,$%02X,$%02X,$%02X   ; PF3 late (luces rojas / corrientes)' % ((PH['pf0'], PH['pf1'], PH['pf2']) + ((0x46, 0x4C) if FASE == 1 else (0xBA, 0xCE) if FASE == 4 else (0x42, 0x4E) if FASE == 5 else (0x96, 0x9E))))
emit('MSIN: .byte ' + ','.join('%d' % round(6 + 6 * math.sin(2 * math.pi * i / 32)) for i in range(32)))
emit('WAVE: .byte ' + ','.join('%d' % round(10 + 10 * math.sin(2 * math.pi * i / 64)) for i in range(64)))
import math

# arco del RECORTADOR (64 pasos, ±18 líneas) y tabla de seno corta
import math
emit('ARC: .byte ' + ','.join('%d' % (int(round(18 * math.sin(math.pi * i / 63))) & 255) for i in range(64)))

# ======================================================================= textos y pantallas fijas
FT = font.text
def T(t, w, center=True, color=0):
    assert len(t) <= w, 'TEXTO CORTADO (%d > %d): %s' % (len(t), w, t)
    return FT(t, w, center, color)

texts = {}
def textline(key, codes): texts[key] = codes; return key

FIELDS = ['MODE', 'BK', 'CH', 'PF0', 'PF1', 'PF2', 'PF3', 'X0', 'X1', 'X2', 'X3', 'C0', 'C1', 'C2', 'C3']
FONTHI = CH['FONT'] >> 8
def entry(**k):
    e = dict(MODE=1, BK=0, CH=FONTHI, PF0=0x2C, PF1=0x0E, PF2=0x00, PF3=0x46, X0=0, X1=0, X2=0, X3=0,
             C0=hw.SHIP['p0'], C1=hw.SHIP['p1'], C2=0, C3=0)
    e.update(k); return e

SCREENS = {}
def screen(name, dl, entries):
    SCREENS[name] = (dl, entries)

# ---- título
dl = [0x70, 0x70]
e = []
dl += [0xF0]                # (sin 'TONY C. WARE PRESENTA': línea en blanco con su DLI)
textline('T_BRAND', T('', 40))
e.append(entry(CH=CH['LOGO'] >> 8, PF0=0x22, PF1=0x26, PF2=0x0E, PF3=0x46))
dl += [0x70 | 0x80 - 0x80, 0x70]
dl[-1] = 0xF0   # DLI en la última línea en blanco -> primera fila del logotipo
e.append(entry(CH=CH['LOGO'] >> 8, PF0=0x22, PF1=0x26, PF2=0x0E, PF3=0x46))
e.pop(0)
e.insert(0, entry(CH=FONTHI, PF0=0x2C, PF1=0x0C, PF2=0x00))   # (sin uso: la marca usa sombras)
lr = 'LOGOROWS'
grad = [(0x22, 0x26, 0x0E), (0x24, 0x28, 0x0C), (0x34, 0x2A, 0x0E), (0x36, 0x2C, 0x0E), (0x44, 0x3A, 0x0C), (0x46, 0x3C, 0x0E)]
e = []
# entrada 0: DLI de la línea de marca (prepara el blanco), 1: DLI del blanco (prepara logo fila 0)
e.append(entry(CH=FONTHI))
e.append(entry(CH=CH['LOGO'] >> 8, PF0=grad[0][0], PF1=grad[0][1], PF2=grad[0][2], PF3=0x46))
for r in range(world.LOGO_ROWS):
    dl += [0xC4 if r < world.LOGO_ROWS else 0x44, 'LOGO%d' % r]
    if r + 1 < world.LOGO_ROWS:
        a, b, c = grad[r + 1]
        e.append(entry(CH=CH['LOGO'] >> 8, PF0=a, PF1=b, PF2=c, PF3=0x46 if r < 2 else 0x44))
e.append(entry(CH=FONTHI, PF0=0x48, PF1=0x2C, PF2=0x00, PF3=0x9A))      # textos de abajo
dl += [0x70]
dl += [0x46, 'T_SUB']; textline('T_SUB', T('CORAZÓN DEL VACÍO', 20, color=1))
dl += [0xB0]                # DLI: prepara la franja de EUROSHOOTER (entrada 8, la anima el título)
e.append(entry(CH=FONTHI, PF0=0x48, PF1=0x0E, PF2=0x32, PF3=0x9A))
# centrada con el logotipo y el subtítulo (que caen medio carácter grande a la izquierda)
dl += [0xC2, 'T_EURO']; textline('T_EURO', T(('   ' + 'EUROSHOOTER EN 8 BITS REDEFINIDO').ljust(40), 40, center=False))
e.append(entry(CH=FONTHI, PF0=0x48, PF1=0x2C, PF2=0x00, PF3=0x9A))      # resto de textos (entrada 9)
import math as _mt
_eh = [2, 2, 3, 3, 4, 4, 4, 4, 3, 3, 2, 2, 3, 3, 4, 4]
emit('EUROBG: .byte ' + ','.join('$%02X' % (_eh[i] * 16 + (0, 0, 2, 2, 4, 4, 4, 2, 2, 0, 0, 0, 2, 4, 2, 0)[i]) for i in range(16)) + '   ; franja: tono y brillo del fondo')
emit('EUROTX: .byte ' + ','.join('$%02X' % v for v in (0x0A, 0x0C, 0x0C, 0x0E, 0x0E, 0x0E, 0x0E, 0x0C, 0x0C, 0x0A, 0x0A, 0x0A, 0x0C, 0x0E, 0x0C, 0x0A)) + '   ; brillo del texto')
dl += [0x70] * 3            # aquí vuela la nave, por debajo del subtítulo
dl += [0x42, 'T_CR1']; textline('T_CR1', T('2026 - TONY C. WARE', 40))
dl += [0x70]
dl += [0x42, 'T_CR2']; textline('T_CR2', T(('5 FASES · 5 JEFES · ATARI 8 BITS' if FASE == 1 else 'FASE %d DE 5 · ATARI 8 BITS' % FASE).replace('·', '-'), 40))
dl += [0x70]
dl += [0x42, 'DIFSCR']   # línea en RAM con la dificultad (izquierda / derecha)
textline('T_DIF0', T('◂  DIFICULTAD:  FÁCIL     ▸', 40))
textline('T_DIF1', T('◂  DIFICULTAD:  NORMAL    ▸', 40))
textline('T_DIF2', T('◂  DIFICULTAD:  HARDCORE  ▸', 40))
dl += [0x70]
dl += [0x42, 'HISCR']   # línea en RAM con el récord
_hi = 'RÉCORD  000000'.center(40)
textline('T_HI', FT(_hi, 40))
textline('T_INV', T('MODO INVENCIBLE ACTIVADO', 40))
emit('HI_OFS = %d' % _hi.index('000000'))
dl += [0x70, 0x70]
dl += [0x46, 'T_FIRE']; textline('T_FIRE', T('PULSA FIRE', 20, color=3))
screen('TITLE', dl, e)


# ---- rótulo de fase: nombre íntegro, partido por palabras
def card(name, kicker, lines7, foot, colors):
    dl = [0x70, 0x70, 0x70, 0x70, 0x70, 0x70]
    dl += [0x46, name + '_K']; textline(name + '_K', T(kicker, 20, color=1))
    dl += [0x70, 0x70]
    for i, l in enumerate(lines7):
        dl += [0x47, '%s_%d' % (name, i)]; textline('%s_%d' % (name, i), T(l, 20, color=0))
        dl += [0x70]
    dl += [0x70, 0x70]
    for i, f in enumerate(foot):
        if f == 'SCORE_SLOT':
            dl += [0x42, 'SCORE_SLOT']
        else:
            dl += [0x42, '%s_F%d' % (name, i)]; textline('%s_F%d' % (name, i), T(f, 40))
        dl += [0x70]
    e = [entry(CH=FONTHI, PF0=colors[0], PF1=colors[1], PF2=0, PF3=0)]
    return dl, e

nm = font.split_lines(hw.NOMBRES_DOC[FASE - 1], 20)
dl, e = card('CARD', 'FASE %d' % FASE, nm, [{1: 'ÓXIDO - CHATARRA - INERCIA', 2: 'BIOLUMINISCENCIA - PRESIÓN - CORRIENTES', 3: 'CENIZA - FUEGO - ERUPCIÓN', 4: 'ORO - JADE - SACRIFICIO', 5: 'CARNE - HUESO - LATIDO'}[FASE], '', 'PREPÁRATE, VÓRTICE 6'], {1: (0x0E, 0x3C), 2: (0x0E, 0xAC), 3: (0x0E, 0x2C), 4: (0x0E, 0x6C), 5: (0x0E, 0x3C)}[FASE])
screen('CARD', dl, e)
# GAME OVER: centrado en vertical, con peso
dl = [0x70] * 7
dl += [0x46, 'OVER_K']; textline('OVER_K', T('VÓRTICE 6', 20, color=1))
dl += [0x70, 0x70]
dl += [0x47, 'OVER_0']; textline('OVER_0', T('GAME OVER', 20, color=0))
dl += [0x70, 0x30]
dl += [0x42, 'OVER_F0']; textline('OVER_F0', T('EL VACÍO HA RECLAMADO TU ALMA', 40))
dl += [0x70]
dl += [0x42, 'OVER_F1']; textline('OVER_F1', T(('FASE %d · ' % FASE).replace('·', '-') + hw.NOMBRES_DOC[FASE - 1] if len(hw.NOMBRES_DOC[FASE - 1]) <= 32 else hw.NOMBRES_DOC[FASE - 1], 40))
dl += [0x70, 0x70]
dl += [0x42, 'OVER_F2']; textline('OVER_F2', T('PUNTUACIÓN', 40))
dl += [0x42, 'SCORE_SLOT']
e = [entry(CH=FONTHI, PF0=0x46, PF1=0x2C, PF2=0, PF3=0)]
screen('OVER', dl, e)
dl, e = card('CLEAR', 'FASE %d' % FASE, ['SUPERADA'], ['FERRUM-9, EL COMPACTADOR SOBERANO,', 'HA CAÍDO', 'SCORE_SLOT', ''] if FASE == 1 else
             ['THALASSA, LA MADRE DE LAS MAREAS,', 'HA CAÍDO', 'SCORE_SLOT', ''] if FASE == 2 else
             ['EL TRÍPTICO DE HADES', 'SE HA APAGADO', 'SCORE_SLOT', ''] if FASE == 3 else
             ['SATURNUS, EL OFICIANTE VACÍO,', 'HA CAÍDO', 'SCORE_SLOT', ''] if FASE == 4 else
             ['EL CORAZÓN NULO', 'HA DEJADO DE LATIR', 'SCORE_SLOT', 'LA GALAXIA RESPIRA'], (0xAC, 0x2E))
screen('CLEAR', dl, e)

# marcador y avisos
_top = ' SCORE 000000      HI 000000     V6 ×3'
_bot = ' FASE %d    DISPARO ▸     ESCUDO -' % FASE
emit('HUD_SC = %d' % (_top.index('SCORE') + 6))
emit('HUD_HI = %d' % (_top.index('HI ') + 3))
emit('HUD_LV = %d' % (len(_top) - 1))
emit('HUD_PW = %d' % _bot.index('▸'))
emit('HUD_SH = %d' % (len(_bot) - 1))
textline('HUD_TOP', FT(' SCORE 000000      HI 000000     V6 ×3', 40))
textline('HUD_BOT', FT(_bot, 40))
textline('WARN_TOP', FT({1: '¡ATENCIÓN!  SE ACERCA FERRUM-9', 2: '¡ATENCIÓN!  SE ACERCA THALASSA', 3: '¡ATENCIÓN!  DESPIERTA EL TRÍPTICO', 4: '¡ATENCIÓN!  SATURNUS OFICIA', 5: '¡ALARMA!  EL CORAZÓN NULO DESPIERTA'}[FASE], 40, True))
textline('WARN_BOT', FT({1: 'EL COMPACTADOR SOBERANO', 2: 'LA MADRE DE LAS MAREAS', 3: 'FURIA - HAMBRE - CENIZA', 4: 'EL OFICIANTE VACÍO', 5: 'NÚCLEO DE LA NAVE VIVIENTE'}[FASE], 40, True))
textline('COMP_BOT', T({1: '¡COMPACTACIÓN! ENTRA ENTRE SUS PINZAS', 2: '¡LAS CRÍAS DE LA MAREA! ACABA CON ELLAS', 3: '¡LLUVIA DE ESCORIA! ESQUIVA LAS ROCAS', 4: '¡EL RITO! BUSCA LA FILA LIBRE', 5: '¡EL CORAZÓN TE ASPIRA! TIRA HACIA ATRÁS'}[FASE], 40))
textline('COMP2_BOT', T('¡SANGRE NUEVA! LLAMA A SUS CRÍAS' if FASE == 5 else '', 40))
textline('EXPO_BOT', FT({1: '¡EL OJO ESTÁ ABIERTO!  DISPARA AL OJO', 2: '¡LA DIOSA ABRE EL OJO! DISPARA AL OJO', 3: '¡CENIZA! EL REACTOR ESTÁ EXPUESTO', 4: '¡EL CÁLIZ SE ABRE! DISPARA AL VACÍO', 5: '¡NÚCLEO EXPUESTO! DISPARA AL REACTOR'}[FASE], 40, True))
emit('DIG0 = %d' % font.CODE['0'])
emit('CH_ARROW = %d' % font.CODE['▸'])
emit('CH_BLOCK = %d' % font.CODE['■'])
emit('CH_MINUS = %d' % font.CODE['-'])
emit('CH_SPACE = %d' % font.CODE[' '])

emit('; ---- textos (ninguna ventana de 40 bytes cruza 4 KB: se alinean a 64)')
for k, codes in texts.items():
    if k.endswith('SCORE_SLOT') or 'SCORE_SLOT' in [None]: pass
    emit('    .align 64')
    bl(codes, 20, lab='TX_' + k)

# ---- display lists y tablas de las pantallas fijas
def resolve(x):
    if isinstance(x, int): return ['$%02X' % x]
    if x in ('HISCR', 'DIFSCR'): return ['<' + x, '>' + x]
    if x.startswith('LOGO'): r = int(x[4:]); return ['<LOGOROW%d' % r, '>LOGOROW%d' % r]
    if x.endswith('SCORE_SLOT'): return ['<SCRLINE', '>SCRLINE']
    return ['<TX_' + x, '>TX_' + x]
for name, (dl, e) in SCREENS.items():
    items = []
    i = 0
    while i < len(dl):
        x = dl[i]
        if isinstance(x, int) and (x & 0x0F) not in (0, 1) and i + 1 < len(dl) and isinstance(dl[i + 1], str):
            items += ['$%02X' % (x | 0x40)] + resolve(dl[i + 1]); i += 2
        else:
            items += resolve(x); i += 1
    # DLI: en las pantallas de rótulo, solo una (la primera línea en blanco)
    if name != 'TITLE':
        items[0] = '$F0'
    items += ['$41', '<DLBUF', '>DLBUF']
    emit('SCR_%s_DL:' % name)
    for k in range(0, len(items), 12): emit('    .byte ' + ','.join(items[k:k + 12]))
    emit('SCR_%s_DLEND:' % name)
    emit('SCR_%s_TAB:' % name)
    for f in FIELDS: bl([en[f] for en in e], 24)
    emit('SCR_%s: .word SCR_%s_DL, SCR_%s_TAB\n    .byte SCR_%s_DLEND-SCR_%s_DL, %d' % (name, name, name, name, name, len(e)))

# filas del logotipo
emit('    .align 64')
for r in range(world.LOGO_ROWS):
    bl([CLG.code(cell(lg.p, c, r)) for c in range(40)], 20, lab='LOGOROW%d' % r)

emit('CHHI_NIVEL = $%02X' % (CH['NIVEL1'] >> 8))
emit('CHHI_JEFE = $%02X' % (CH['JEFE1'] >> 8))
emit('CHHI_FONT = $%02X' % FONTHI)

open(os.path.join(ROOT, 'src', 'g1data.s'), 'w').write('\n'.join(out) + '\n')
print('NIVEL1 %d car. (sólidos desde %d) · JEFE1 %d (desde %d) · LOGO %d · columnas %d · torretas %d · oleadas %d'
      % (len(CL.glyphs), CL.solid0, len(CB.glyphs), CB.solid0, len(CLG.glyphs), 0, 0, len(W)))
