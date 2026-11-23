#!/usr/bin/env python3
"""Vórtice 6 · música POKEY: instrumentos, tablas de afinación medidas y temas.
Genera src/musdata.s.  Canales: 0 synth principal · 1 bajo (distorsión C) · 2 batería · 3 eco/pad
(el 3 lo pisan los efectos y la sirena; el 2 lo pisan explosiones y muerte)."""
import math

CLK = 63921.0                       # reloj base NTSC de 64 kHz
NOMBRE = 'C C# D D# E F F# G G# A A# B'.split()

def midi(t):
    t = t.replace('b', '#') if False else t
    n, o = (t[:-1], int(t[-1]))
    return NOMBRE.index(n) + 12 * (o + 1)

def hz(m): return 440 * 2 ** ((m - 69) / 12)

# --- afinación (comprobada en el emulador midiendo los 256 valores de AUDF)
#   tono puro ($A): f = CLK / (2 (N+1))
#   distorsión C ($C): f = CLK / (15 (N+1)) cuando N no es múltiplo de 3 ni de 5 (si no, otro timbre)
BASE = 24                            # índice 0 de la tabla = C1 (MIDI 24)
NT = 80
def best(fn, ok):
    out = []
    for i in range(NT):
        f = hz(BASE + i)
        c = min(((abs(1200 * math.log2(fn(n) / f)), n) for n in range(256) if ok(n)))
        out.append(c)
    return out
PURA = best(lambda n: CLK / (2 * (n + 1)), lambda n: True)
ZUMB = best(lambda n: CLK / (15 * (n + 1)), lambda n: n % 3 and n % 5)

# --- instrumentos: ctl, tabla (0 puro, 1 zumbido, 2 fijo), N fijo, desliz por cuadro, envolvente, arpegio, vaivén
INS = {}
def ins(nombre, ctl, tab, env, arp=(0,), fix=0, sld=0, wob=0):
    INS[nombre] = dict(ctl=ctl, tab=tab, env=list(env), arp=list(arp), fix=fix, sld=sld & 255, wob=wob)
ins('pulso',   0xA0, 0, [11, 10, 9, 9, 8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 0])
ins('sierra',  0xA0, 0, [7, 9, 10, 10, 9, 9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6], wob=1)
ins('acmen',   0xA0, 0, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], arp=(0, 3, 7))
ins('acmay',   0xA0, 0, [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], arp=(0, 4, 7))
ins('bajo',    0xC0, 1, [14, 13, 11, 10, 9, 8, 7, 6, 5, 4, 0])
ins('bajolar', 0xC0, 1, [13, 13, 12, 12, 11, 11, 11, 10, 10, 10, 10, 9])
ins('bombo',   0xC0, 2, [15, 14, 12, 10, 8, 6, 4, 2, 0], fix=26, sld=9)
ins('caja',    0x80, 2, [14, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], fix=10)
ins('charles', 0x80, 2, [7, 4, 2, 0], fix=1)
ins('abierto', 0x80, 2, [7, 6, 5, 4, 3, 3, 2, 2, 1, 0], fix=1)
ins('ecopul',  0xA0, 0, [5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0])
ins('ecosie',  0xA0, 0, [3, 4, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2], wob=1)
ins('padmen',  0xA0, 0, [2, 3, 4, 5, 5, 5, 5, 5, 4, 4, 4, 4], arp=(0, 3, 7, 12))
ins('padmay',  0xA0, 0, [2, 3, 4, 5, 5, 5, 5, 5, 4, 4, 4, 4], arp=(0, 4, 7, 12))
ins('campana', 0xA0, 0, [13, 10, 8, 7, 6, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0], arp=(0, 19, 12, 24))
ins('coro',    0xA0, 0, [1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 5], arp=(0, 12, 7, 12), wob=1)
ins('piano',   0xA0, 0, [12, 10, 9, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0])
ins('tom',     0xA0, 2, [13, 11, 9, 7, 6, 5, 4, 3, 2, 1, 0], fix=90, sld=6)
INAMES = list(INS)

# --- notación: compases de 16 semicorcheas; ficha = nota[:ranura] · '.' sigue · '-' calla
class Tema:
    def __init__(s, nombre, vel, ranuras):
        s.nombre, s.vel, s.ran = nombre, vel, ranuras     # ranuras: 4 canales x 4 instrumentos
        s.can = [[], [], [], []]
        s.bucle = 0
    def compas(s, c, txt):
        f = txt.split()
        assert len(f) == 16, (s.nombre, c, txt, len(f))
        s.can[c].append(f)
    def marca_bucle(s): s.bucle = len(s.can[0])

def cod(tema, c, tok):
    if tok == '.': return 0
    if tok == '-': return 1
    slot = 0
    if ':' in tok: tok, slot = tok.split(':'); slot = int(slot)
    if c == 2:                       # batería: letra = instrumento
        slot = 'KSHO'.index(tok); val = 2
    else:
        val = midi(tok) - BASE + 2
        assert 2 <= val < 64, tok
    return slot << 6 | val

# ---------------------------------------------------------------- utilidades de composición
def bajo_rueda(r, quinta, final=None):
    """bajo tecno rodando entre bombos: . r r r . r r r . r r r . r q r"""
    q = final or quinta
    return '. %s %s %s . %s %s %s . %s %s %s . %s %s %s' % (r, r, r, r, r, r, r, r, r, r, q, r)

def bateria(t):
    return {'main': 'K H O H S H O H K H O K S H O H',
            'fill': 'K H O H S H O H K S H S S S S S',
            'intro': 'K . H . K . H . K . H . K . H .',
            'hats': '. . H . . . O . . . H . . . O .',
            'medio': 'K . . . . . H . K . . . S . H .',
            'redob': 'S . S . S . S . S S S S S S S S',
            'duro': 'K H K H S H K H K H O K S H S S',
            'nada': '. . . . . . . . . . . . . . . .',
            'lento': 'K . . . . . H . S . . . . . H .',
            'lento2': 'K . . K . . H . S . . . K . H H',
            'rito': 'K . H . S . H . K K H . S . O .',
            'latido': 'K . K . . . H . K . K . . . H .',
            'latido2': 'K . K . S . H . K . K . S . H H',
            'carrera': 'K H K H S H K H K H K H S S S S'}[t]

def acordes(raiz, ran):
    return '%s:%d . %s:%d %s:%d . %s:%d . %s:%d %s:%d . %s:%d . %s:%d %s:%d . %s:%d' % ((raiz, ran) * 10)

def eco(tema, desde, hasta, retardo=3, mapa={0: 0, 1: 1}):
    """el canal 3 repite el canal 0 con 3 semicorcheas de retraso (eco de 'dotted eighth')"""
    plano = [t for comp in tema.can[0] for t in comp]
    for b in range(desde, hasta):
        fila = []
        for k in range(16):
            i = b * 16 + k - retardo
            t = plano[i] if i >= desde * 16 else '.'
            if t not in '.-':
                n, s = (t.split(':') + ['0'])[:2]
                t = '%s:%d' % (n, mapa.get(int(s), 0))
            fila.append(t)
        tema.can[3][b] = fila

# ================================================================ FASE 1 · Re menor · ~138 BPM
def fase1():
    T = Tema('FASE1', (6, 7), [['sierra', 'pulso', 'acmen', 'acmay'],
                               ['bajo', 'bajolar', 'bajo', 'bajo'],
                               ['bombo', 'caja', 'charles', 'abierto'],
                               ['ecosie', 'ecopul', 'padmen', 'padmay']])
    V = '. . . . . . . . . . . . . . . .'
    raices = ['D1', 'D1', 'F1', 'F1', 'A#1', 'A#1', 'A1', 'A1']
    quintas = ['A1', 'A1', 'C2', 'C2', 'F1', 'F1', 'E1', 'E1']
    melA = ['D5 . . . A4 . . . C5 . . D5 . . . .',
            'F5 . . E5 . . D5 . . . C5 . A4 . . .',
            'C5 . . . F5 . . . A5 . . G5 . . F5 .',
            'E5 . . . . . . . C5 . . . A4 . C5 .',
            'D5 . . . A#4 . . . F4 . . . A#4 . D5 .',
            'F5 . . . . . E5 . D5 . . . C5 . . .',
            'C#5 . . . E5 . . . A5 . . . G5 . E5 .',
            'C#5 . . . . . . . - . . . A4 . C#5 .']
    melA2 = melA[:6] + ['E5 . . . C#5 . . . A4 . . . E5 . G5 .',
                        'F5 . E5 . D5 . . . . . . . - . . .']
    def compas(lead, bajo, bat, ecot=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bateria(bat)); T.compas(3, ecot)
    # intro: 4 de batería, 4 con bajo
    for i in range(4): compas(V, V, 'intro' if i < 3 else 'main')
    for i in range(4): compas(V, bajo_rueda(raices[i], quintas[i]), 'main' if i < 3 else 'fill')
    T.marca_bucle()
    # A: melodía con sierra y eco (16)
    a0 = len(T.can[0])
    for v in (melA, melA2):
        for i in range(8):
            compas(v[i], bajo_rueda(raices[i], quintas[i]), 'fill' if i == 7 else 'main')
    eco(T, a0, a0 + 16)
    # B: acordes en arpegio rápido + pad en el canal 3 (16)
    acB = [('D4', 2), ('D4', 2), ('F4', 3), ('F4', 3), ('A#3', 3), ('A#3', 3), ('A3', 3), ('A3', 3)]
    acB2 = [('D4', 2), ('D4', 2), ('C4', 3), ('C4', 3), ('A#3', 3), ('A#3', 3), ('A3', 3), ('A3', 3)]
    baB2 = ['D1', 'D1', 'C2', 'C2', 'A#1', 'A#1', 'A1', 'A1']
    quB2 = ['A1', 'A1', 'G1', 'G1', 'F1', 'F1', 'E1', 'E1']
    for prog, ba, qu in ((acB, raices, quintas), (acB2, baB2, quB2)):
        for i in range(8):
            r, s = prog[i]
            pad = ('%s:%d' % (r.replace('3', '4') if r.endswith('3') else r, s)) + ' . . . . . . . . . . . . . . .' if i % 2 == 0 else V
            compas(acordes(r, s), bajo_rueda(ba[i], qu[i]), 'fill' if i == 7 else 'main', pad)
    # ruptura: sin bombo, bajo largo, sierra lenta (8)
    rup = ['D5 . . . . . . . . . . . . . . .', '. . . . . . . . F5 . . . E5 . . .',
           'D5 . . . . . . . . . . . . . . .', 'C#5 . . . . . . . . . . . A4 . . .',
           'A#4 . . . . . . . . . . . D5 . . .', 'C5 . . . . . . . A4 . . . . . . .',
           'C#5 . . . . . . . E5 . . . G5 . . .', 'A5 . . . . . . . - . . . . . . .']
    braiz = ['D1', 'D1', 'D1', 'A1', 'A#1', 'F1', 'A1', 'A1']
    bat = ['hats', 'hats', 'hats', 'hats', 'medio', 'medio', 'redob', 'redob']
    r0 = len(T.can[0])
    for i in range(8):
        compas(rup[i], '%s:1 . . . . . . . . . . . . . . .' % braiz[i], bat[i])
    eco(T, r0, r0 + 8)
    # A': melodía con pulso (otro color) y eco del pulso (16)
    a0 = len(T.can[0])
    for v in (melA, melA2):
        for i in range(8):
            lead = ' '.join(t if t in '.-' else t + ':1' for t in v[i].split())
            compas(lead, bajo_rueda(raices[i], quintas[i]), 'fill' if i == 7 else 'main')
    eco(T, a0, a0 + 16, mapa={1: 1})
    return T

# ================================================================ JEFE · Mi frigio · 150 BPM
def jefe():
    T = Tema('JEFE', (6, 6), [['sierra', 'pulso', 'acmen', 'acmay'],
                              ['bajo', 'bajolar', 'bajo', 'bajo'],
                              ['bombo', 'caja', 'charles', 'abierto'],
                              ['ecosie', 'ecopul', 'padmen', 'padmay']])
    V = '. . . . . . . . . . . . . . . .'
    def rueda16(r, a):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (r, r, r, r, r, r, a, r, r, r, r, r, r, r, a, r)
    raiz = ['E1', 'E1', 'F1', 'E1', 'E1', 'E1', 'G1', 'F1']
    acen = ['F1', 'F1', 'E1', 'F1', 'B1', 'B1', 'F1', 'E1']
    ac = [('E4', 2), ('E4', 2), ('F4', 3), ('E4', 2), ('C4', 3), ('C4', 3), ('B3', 2), ('F4', 3)]
    mel = ['E5 . . . F5 . . . E5 . . . B4 . . .',
           'C5 . . . B4 . . . G4 . . . F4 . . .',
           'E5 . . . F5 . . . G5 . . . A5 . G5 .',
           'F5 . . . . . . . E5 . . . . . . .',
           'B5 . . . A5 . . . G5 . . . F5 . . .',
           'G5 . . . F5 . . . E5 . . . C5 . . .',
           'D5 . . . E5 . . . F5 . . . G5 . . .',
           'F5 . . . . . . . - . . . E5 . F5 .']
    for i in range(8):
        r, s = ac[i]
        T.compas(0, acordes(r, s)); T.compas(1, rueda16(raiz[i], acen[i]))
        T.compas(2, bateria('fill' if i == 7 else 'duro')); T.compas(3, V)
    a0 = len(T.can[0])
    for i in range(8):
        T.compas(0, mel[i]); T.compas(1, rueda16(raiz[i], acen[i]))
        T.compas(2, bateria('fill' if i == 7 else 'duro')); T.compas(3, V)
    eco(T, a0, a0 + 8)
    return T

# ================================================================ FASE 2 · Fa# dórico · ~113 BPM (8 cuadros por semicorchea)
def fase2():
    """Océanos: arpegios líquidos con eco y notas suspendidas, pero en la misma línea tecno oscura."""
    T = Tema('FASE2', (8, 8), [['sierra', 'pulso', 'acmen', 'acmay'],
                               ['bajo', 'bajolar', 'bajo', 'bajo'],
                               ['bombo', 'caja', 'charles', 'abierto'],
                               ['ecosie', 'ecopul', 'padmen', 'padmay']])
    V = '. . . . . . . . . . . . . . . .'
    # i - IV - i - VII  (F#m - B - F#m - E) y variante  i - III - IV - V(m)  (F#m - A - B - C#m)
    rai = ['F#1', 'F#1', 'B1', 'B1', 'F#1', 'F#1', 'E1', 'E1']
    qui = ['C#2', 'C#2', 'F#1', 'F#1', 'C#2', 'C#2', 'B1', 'B1']
    rai2 = ['F#1', 'F#1', 'A1', 'A1', 'B1', 'B1', 'C#2', 'C#2']
    qui2 = ['C#2', 'C#2', 'E1', 'E1', 'F#1', 'F#1', 'G#1', 'G#1']
    ac = [('F#4', 2), ('F#4', 2), ('B3', 3), ('B3', 3), ('F#4', 2), ('F#4', 2), ('E4', 3), ('E4', 3)]
    ac2 = [('F#4', 2), ('F#4', 2), ('A3', 3), ('A3', 3), ('B3', 3), ('B3', 3), ('C#4', 2), ('C#4', 2)]
    def bajo_ola(r, q):            # bajo que ondula: corcheas con la quinta en medio
        return '%s . %s . . %s %s . %s . %s . . %s %s .' % (r, r, q, r, r, r, q, r)
    mel = ['C#5 . . . . . . . B4 . . . A4 . . .',
           'F#5 . . . . . . . E5 . . . C#5 . . .',
           'D#5 . . . . . . . E5 . . . F#5 . . .',
           'B4 . . . . . . . . . . . - . . .',
           'C#5 . . . . . . . E5 . . . F#5 . . .',
           'A5 . . . . . . . G#5 . . . F#5 . . .',
           'E5 . . . . . . . D#5 . . . B4 . . .',
           'G#4 . . . . . . . . . . . - . . .']
    def compas(lead, bajo, bat, ecot=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bateria(bat)); T.compas(3, ecot)
    # intro: pad suspendido y charles; luego entra el bajo
    for i in range(4):
        r, s = ac[i * 2]
        pad = '%s:%d . . . . . . . . . . . . . . .' % (r if not r.endswith('3') else r[:-1] + '4', s)
        compas(V, V, 'hats', pad)
    for i in range(4):
        compas(V, bajo_ola(rai[i], qui[i]), 'medio' if i < 3 else 'fill')
    T.marca_bucle()
    # A: melodía larga de sierra con eco (16)
    a0 = len(T.can[0])
    for k in range(2):
        for i in range(8):
            compas(mel[i], bajo_ola(rai[i], qui[i]), 'fill' if i == 7 else 'main')
    eco(T, a0, a0 + 16)
    # B: arpegios líquidos + pad (16)
    for prog, ra, qu in ((ac, rai, qui), (ac2, rai2, qui2)):
        for i in range(8):
            r, s = prog[i]
            pad = ('%s:%d' % (r if not r.endswith('3') else r[:-1] + '4', s)) + ' . . . . . . . . . . . . . . .' if i % 2 == 0 else V
            compas(acordes(r, s), bajo_ola(ra[i], qu[i]), 'fill' if i == 7 else 'main', pad)
    # ruptura: sin bombo, bajo largo, notas suspendidas (8)
    rup = ['C#5 . . . . . . . . . . . . . . .', 'B4 . . . . . . . . . . . . . . .',
           'D#5 . . . . . . . . . . . . . . .', 'C#5 . . . . . . . . . . . - . . .',
           'F#5 . . . . . . . E5 . . . . . . .', 'D#5 . . . . . . . B4 . . . . . . .',
           'C#5 . . . . . . . E5 . . . G#5 . . .', 'F#5 . . . . . . . - . . . . . . .']
    braiz = ['F#1', 'B1', 'B1', 'F#1', 'A1', 'B1', 'C#2', 'C#2']
    bat = ['hats', 'hats', 'hats', 'hats', 'medio', 'medio', 'redob', 'redob']
    r0 = len(T.can[0])
    for i in range(8):
        compas(rup[i], '%s:1 . . . . . . . . . . . . . . .' % braiz[i], bat[i])
    eco(T, r0, r0 + 8)
    # A': melodía con pulso y eco (16)
    a0 = len(T.can[0])
    for k in range(2):
        for i in range(8):
            lead = ' '.join(t if t in '.-' else t + ':1' for t in mel[i].split())
            compas(lead, bajo_ola(rai[i], qui[i]), 'fill' if i == 7 else 'main')
    eco(T, a0, a0 + 16, mapa={1: 1})
    return T

# ================================================================ FASE 3 · La frigio · 150 BPM: percusión agresiva, pulsos graves
def fase3():
    T = Tema('FASE3', (6, 6), [['sierra', 'pulso', 'acmen', 'acmay'],
                               ['bajo', 'bajolar', 'bajo', 'bajo'],
                               ['bombo', 'caja', 'charles', 'abierto'],
                               ['ecosie', 'ecopul', 'padmen', 'padmay']])
    V = '. . . . . . . . . . . . . . . .'
    def martillo(r, b2):           # bajo martilleante con la segunda menor (frigio)
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (r, r, b2, r, r, r, r, b2, r, r, b2, r, r, r, b2, r)
    rai = ['A1', 'A1', 'A#1', 'A1', 'F1', 'F1', 'G1', 'A#1']
    seg = ['A#1', 'A#1', 'C2', 'A#1', 'G1', 'G1', 'A1', 'C2']
    ac = [('A3', 2), ('A3', 2), ('A#3', 3), ('A3', 2), ('F3', 3), ('F3', 3), ('G3', 2), ('A#3', 3)]
    riff = ['A4 . . A4 . . A#4 . A4 . . . E5 . D5 .',
            'C5 . . A#4 . . A4 . . . . . - . . .',
            'A4 . . A4 . . A#4 . C5 . . . D5 . E5 .',
            'F5 . . E5 . . D5 . A#4 . . . A4 . . .',
            'A5 . . . G5 . . . F5 . . . E5 . . .',
            'F5 . . . E5 . . . D5 . . . C5 . A#4 .',
            'A4 . . . C5 . . . E5 . . . G5 . F5 .',
            'E5 . . . . . . . - . . . A4 . A#4 .']
    def compas(lead, bajo, bat, ecot=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bateria(bat)); T.compas(3, ecot)
    for i in range(4): compas(V, martillo(rai[i], seg[i]) if i >= 2 else V, 'duro' if i % 2 else 'main')
    T.marca_bucle()
    a0 = len(T.can[0])
    for k in range(2):
        for i in range(8):
            compas(riff[i], martillo(rai[i], seg[i]), 'fill' if i == 7 else 'duro')
    eco(T, a0, a0 + 16)
    for k in range(2):
        for i in range(8):
            r, s_ = ac[i]
            pad = ('%s:%d' % (r[:-1] + '4', s_)) + ' . . . . . . . . . . . . . . .' if i % 2 == 0 else V
            compas(acordes(r, s_), martillo(rai[i], seg[i]), 'fill' if i == 7 else 'main', pad)
    rup = ['A4 . . . . . . . . . . . . . . .', 'A#4 . . . . . . . . . . . . . . .',
           'C5 . . . . . . . A#4 . . . . . . .', 'A4 . . . . . . . - . . . . . . .']
    for i in range(4):
        compas(rup[i], '%s:1 . . . . . . . %s:1 . . . . . . .' % (rai[i], seg[i]), 'medio' if i < 2 else 'redob')
    a0 = len(T.can[0])
    for i in range(8):
        lead = ' '.join(t if t in '.-' else t + ':1' for t in riff[i].split())
        compas(lead, martillo(rai[i], seg[i]), 'fill' if i == 7 else 'duro')
    eco(T, a0, a0 + 8, mapa={1: 1})
    return T

# ================================================================ FASE 4 · Do menor · ~100 BPM: coro sintético, campanas metálicas, paso lento
def fase4():
    """El Sarcófago de Saturno: ritual lento y pesado; coro que se hincha, campanas de metal, bombo a medio tiempo."""
    T = Tema('FASE4', (9, 9), [['coro', 'campana', 'acmen', 'acmay'],
                               ['bajolar', 'bajo', 'bajo', 'bajo'],
                               ['bombo', 'caja', 'charles', 'abierto'],
                               ['campana', 'coro', 'padmen', 'padmay']])
    V = '. . . . . . . . . . . . . . . .'
    # i - VI - iv - V (Cm - Ab - Fm - G) y i - VII - VI - V (Cm - Bb - Ab - G)
    rai = ['C2', 'C2', 'G#1', 'G#1', 'F1', 'F1', 'G1', 'G1']
    rai2 = ['C2', 'C2', 'A#1', 'A#1', 'G#1', 'G#1', 'G1', 'G1']
    ac = [('C4', 2), ('C4', 2), ('G#3', 3), ('G#3', 3), ('F3', 2), ('F3', 2), ('G3', 3), ('G3', 3)]
    def bajo_rito(r):               # medio tiempo: golpe largo y réplica antes del 3
        return '%s . . . . . %s . %s:1 . . . . . %s:1 .' % (r, r, r, r)
    coro = ['G4 . . . . . . . . . . . D#4 . . .',
            'C4 . . . . . . . . . . . - . . .',
            'G#4 . . . . . . . G4 . . . D#4 . . .',
            'C4 . . . . . . . . . . . - . . .',
            'F4 . . . . . . . G#4 . . . C5 . . .',
            'A#4 . . . . . . . G#4 . . . G4 . . .',
            'D4 . . . . . . . F4 . . . B4 . . .',
            'G4 . . . . . . . . . . . - . . .']
    camp = ['C5:1 . . G4:1 . . D#5:1 . . . C5:1 . . G4:1 . .',
            '- . . . . . . . . . . . . . . .',
            'G#4:1 . . D#4:1 . . C5:1 . . . G#4:1 . . D#4:1 . .',
            '- . . . . . . . . . . . . . . .',
            'F4:1 . . C4:1 . . G#4:1 . . . F4:1 . . C4:1 . .',
            'A#4:1 . . F4:1 . . D5:1 . . . A#4:1 . . F4:1 . .',
            'G4:1 . . D4:1 . . B4:1 . . . G4:1 . . D4:1 . .',
            'B4:1 . . . G4:1 . . . D4:1 . . . B3:1 . . .']
    tolle = 'C5:0 . . . . . . . . . . . . . . .'     # campana sola en el canal 3
    def compas(lead, bajo, bat, ecot=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bateria(bat)); T.compas(3, ecot)
    # intro: campanas que tañen en el vacío
    for i in range(4):
        compas(V, V, 'hats' if i >= 2 else 'nada', tolle if i % 2 == 0 else 'G4:0 . . . . . . . . . . . . . . .')
    for i in range(4):
        compas(camp[i * 2], bajo_rito(rai[i * 2]), 'lento' if i < 3 else 'lento2')
    T.marca_bucle()
    # A: el coro (16) con campanas en eco
    for k in range(2):
        for i in range(8):
            compas(coro[i], bajo_rito((rai, rai2)[k][i]), 'lento2' if i == 7 else 'lento',
                   ('%s:0' % ('C5', 'G4', 'G#4', 'D#4', 'F4', 'A#4', 'G4', 'D4')[i]) + ' . . . . . . . . . . . . . . .' if i % 2 == 0 else V)
    # B: campanas al frente, coro de fondo (16)
    for k in range(2):
        for i in range(8):
            r, s_ = ac[i]
            pad = ('%s:%d' % (r[:-1] + '4', s_)) + ' . . . . . . . . . . . . . . .' if i % 2 == 0 else V
            compas(camp[i], bajo_rito((rai, rai2)[k][i]), 'rito' if i % 4 == 3 else 'lento', pad)
    # ruptura: solo coro y bajo largo (4)
    rup = ['C5 . . . . . . . . . . . . . . .', 'B4 . . . . . . . . . . . . . . .',
           'G#4 . . . . . . . . . . . . . . .', 'G4 . . . . . . . - . . . . . . .']
    for i, r in enumerate(('C2', 'G1', 'G#1', 'G1')):
        compas(rup[i], '%s . . . . . . . . . . . . . . .' % r, 'nada' if i < 2 else 'medio')
    # A': coro con campanas en el canal 3 (8)
    a0 = len(T.can[0])
    for i in range(8):
        compas(coro[i], bajo_rito(rai[i]), 'fill' if i == 7 else 'rito')
    eco(T, a0, a0 + 8, retardo=6, mapa={0: 1})
    return T

# ================================================================ FASE 5 · Si menor · ~128 BPM: latido, percusión orgánica, melodía final oscura
def fase5():
    """La Nave Viviente: el bombo doble es el corazón; bajo que respira, sierra que llora y pad de coro al final."""
    T = Tema('FASE5', (7, 7), [['sierra', 'pulso', 'acmen', 'acmay'],
                               ['bajo', 'bajolar', 'bajo', 'bajo'],
                               ['bombo', 'caja', 'charles', 'abierto'],
                               ['ecosie', 'coro', 'padmen', 'padmay']])
    V = '. . . . . . . . . . . . . . . .'
    # i - VI - VII - v  (Bm - G - A - F#m) y  i - iv - VI - V  (Bm - Em - G - F#)
    rai = ['B1', 'B1', 'G1', 'G1', 'A1', 'A1', 'F#1', 'F#1']
    rai2 = ['B1', 'B1', 'E1', 'E1', 'G1', 'G1', 'F#1', 'F#1']
    ac = [('B3', 2), ('B3', 2), ('G3', 3), ('G3', 3), ('A3', 3), ('A3', 3), ('F#3', 2), ('F#3', 2)]
    def respira(r):                  # bajo que respira: dos golpes con el latido y una subida
        return '%s . %s . . . . %s:1 %s . %s . . . %s .' % (r, r, r, r, r, r)
    mel = ['F#4 . . . . . . . D5 . . . C#5 . . .',
           'B4 . . . . . . . - . . . A4 . B4 .',
           'D5 . . . . . . . E5 . . . F#5 . . .',
           'E5 . . . . . . . - . . . D5 . C#5 .',
           'C#5 . . . . . . . E5 . . . A5 . . .',
           'G5 . . . . . . . F#5 . . . E5 . . .',
           'F#5 . . . . . . . C#5 . . . A#4 . . .',
           'B4 . . . . . . . - . . . . . . .']
    def compas(lead, bajo, bat, ecot=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bateria(bat)); T.compas(3, ecot)
    for i in range(4):                       # solo el latido, y entra el bajo
        compas(V, respira(rai[i * 2]) if i >= 2 else V, 'latido')
    T.marca_bucle()
    a0 = len(T.can[0])
    for k in range(2):
        for i in range(8):
            compas(mel[i], respira((rai, rai2)[k][i]), 'latido2' if i == 7 else 'latido')
    eco(T, a0, a0 + 16)
    for k in range(2):                       # arpegios + coro
        for i in range(8):
            r, s_ = ac[i]
            pad = ('%s:1' % (r[:-1] + '4')) + ' . . . . . . . . . . . . . . .' if i % 2 == 0 else V
            compas(acordes(r, s_), respira((rai, rai2)[k][i]), 'carrera' if i % 4 == 3 else 'latido', pad)
    for i, r in enumerate(('B1', 'G1', 'A1', 'F#1')):      # ventrículo: casi silencio, solo el corazón
        compas(V if i < 2 else 'B4:1 . . . . . . . . . . . . . . .', '%s:1 . . . . . . . . . . . . . . .' % r, 'latido')
    a0 = len(T.can[0])
    for i in range(8):
        lead = ' '.join(t if t in '.-' else t + ':1' for t in mel[i].split())
        compas(lead, respira(rai[i]), 'carrera' if i == 7 else 'latido2')
    eco(T, a0, a0 + 8, mapa={1: 1})
    return T

# ================================================================ INTRO · Re menor -> Re mayor · ~90 BPM
def intro():
    """Más allá del horizonte: empieza oscuro (las frases de la historia), sube con un redoble y estalla en un
    tema heroico en Re mayor; melodía propia, larga y con saltos, sobre bajo que empuja y arpegios."""
    T = Tema('INTRO', (10, 10), [['sierra', 'campana', 'acmen', 'acmay'],
                                 ['bajolar', 'bajo', 'bajo', 'bajo'],
                                 ['bombo', 'caja', 'charles', 'abierto'],
                                 ['padmen', 'padmay', 'ecosie', 'campana']])
    V = '. . . . . . . . . . . . . . . .'
    def compas(lead, bajo, bat, ecot=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bateria(bat)); T.compas(3, ecot)
    # 1 · las frases (8): Rem - Sib - Fa - Do, colchón y campana lejana
    for i, (r, pad) in enumerate((('D1', 'D4:0'), ('A#1', 'A#3:1'), ('F1', 'F4:1'), ('C2', 'C4:1'),
                                  ('D1', 'D4:0'), ('A#1', 'A#3:1'), ('G1', 'G3:0'), ('A1', 'A3:1'))):
        camp = 'A4:1 . . . . . . . . . . . . . . .' if i % 2 == 0 else ('F4:1 . . . . . . . E4:1 . . . . . . .' if i == 7 else V)
        compas(camp, '%s . . . . . . . . . . . . . . .' % r, 'nada', pad + ' . . . . . . . . . . . . . . .')
    # 2 · subida (4): pedal de La, bajo en corcheas y redoble
    for i in range(4):
        compas(V if i < 2 else 'A4:3 . . . . . . . . . . . . . . .', 'A1 . A1 . A1 . A1 . A1 . A1 . A1 . A1 .',
               ('hats', 'intro', 'medio', 'redob')[i], 'A3:1 . . . . . . . . . . . . . . .' if i % 2 == 0 else V)
    T.marca_bucle()
    # 3 · tema heroico (16): Re - Sim - Sol - La
    mel = ['A4 . . . . . D5 . . . E5 . F#5 . . .', 'F#5 . . . E5 . D5 . . . E5 . B4 . . .',
           'D5 . . . . . . . B4 . . . G4 . A4 .', 'A4 . . . . . . . . . . . - . . .',
           'A4 . . . . . D5 . . . E5 . F#5 . A5 .', 'B5 . . . A5 . F#5 . . . D5 . E5 . F#5 .',
           'G5 . . . F#5 . E5 . D5 . . . E5 . . .', 'E5 . . . . . . . - . . . . . . .',
           # puente: Sol - La - Fa#m - Sim · Sol - La - Re
           'D5 . . . . . . . G5 . . . F#5 . E5 .', 'E5 . . . . . . . A5 . . . G5 . F#5 .',
           'F#5 . . . . . . . C#5 . . . A4 . . .', 'B4 . . . . . . . D5 . . . F#5 . . .',
           'G5 . . . F#5 . . . E5 . . . D5 . . .', 'E5 . . . . . . . C#5 . . . A4 . . .',
           'D5 . . . . . . . . . . . . . . .', 'A4 . . . B4 . . . C#5 . . . E5 . . .']
    rai = ['D1', 'B1', 'G1', 'A1', 'D1', 'B1', 'G1', 'A1', 'G1', 'A1', 'F#1', 'B1', 'G1', 'A1', 'D1', 'A1']
    ac = [('D4', 3), ('B3', 2), ('G3', 3), ('A3', 3), ('D4', 3), ('B3', 2), ('G3', 3), ('A3', 3),
          ('G3', 3), ('A3', 3), ('F#3', 2), ('B3', 2), ('G3', 3), ('A3', 3), ('D4', 3), ('A3', 3)]
    a0 = len(T.can[0])
    for i in range(16):
        r = rai[i]
        bajo = '%s . %s . . %s . %s %s . %s . . %s . %s' % (r, r, r, r, r, r, r, r)
        r_, s_ = ac[i]
        compas(mel[i], bajo, 'fill' if i in (7, 15) else ('medio' if i < 4 else 'main'), V)
        T.can[3][-1] = acordes(r_, s_).split()
    eco(T, a0 + 4, a0 + 8, retardo=3, mapa={0: 2})
    return T


# ================================================================ FINAL · La mayor · ~64 BPM
def final():
    """Un sueño de paz: piano en arpegios, coro que canta despacio, bajo largo y una batería suave que entra al
    final; agridulce y luminoso. Suena con la imagen de Elara Voss y los créditos."""
    T = Tema('FINAL', (14, 14), [['coro', 'piano', 'sierra', 'acmay'],
                                 ['bajolar', 'bajo', 'bajo', 'bajo'],
                                 ['bombo', 'caja', 'charles', 'abierto'],
                                 ['piano', 'padmay', 'padmen', 'campana']])
    V = '. . . . . . . . . . . . . . . .'
    def compas(lead, bajo, bat, ecot=V):
        T.compas(0, lead); T.compas(1, bajo); T.compas(2, bateria(bat)); T.compas(3, ecot)
    def arp(n1, n2, n3, n4):        # piano en arpegio (corcheas)
        return '%s . %s . %s . %s . %s . %s . %s . %s .' % (n1, n2, n3, n4, n3, n2, n3, n4)
    # La - Mi/Sol# - Fa#m - Re · Re - Mi - Do#m - Fa#m
    prog = [('A1', ('A3', 'E4', 'A4', 'C#5')), ('E1', ('G#3', 'E4', 'B4', 'E5')), ('F#1', ('F#3', 'C#4', 'A4', 'C#5')),
            ('D1', ('D4', 'A4', 'D5', 'F#5')), ('D1', ('D4', 'A4', 'F#4', 'A4')), ('E1', ('E4', 'B4', 'G#4', 'B4')),
            ('C#2', ('C#4', 'G#4', 'E4', 'G#4')), ('F#1', ('F#3', 'C#4', 'A4', 'C#5'))]
    for i in range(4):                                   # entrada: solo piano
        r, n = prog[i]
        compas(V, '%s . . . . . . . . . . . . . . .' % r if i >= 2 else V, 'nada', arp(*n))
    T.marca_bucle()
    mel = ['E5 . . . . . . . C#5 . . . B4 . A4 .', 'B4 . . . . . . . . . . . E4 . . .',
           'A4 . . . C#5 . . . E5 . . . F#5 . . .', 'F#5 . . . . . . . E5 . . . . . . .',
           'F#5 . . . . . . . E5 . . . D5 . . .', 'E5 . . . . . . . B4 . . . . . . .',
           'C#5 . . . E5 . . . G#5 . . . F#5 . . .', 'F#5 . . . . . . . . . . . - . . .']
    for k in range(2):
        for i in range(8):
            r, n = prog[i]
            bat = 'nada' if k == 0 else ('lento2' if i == 7 else 'lento')
            lead = mel[i] if k == 0 else ' '.join(t if t in '.-' else t + ':0' for t in mel[i].split())
            compas(lead, '%s . . . . . . . %s . . . . . . .' % (r, r), bat, arp(*n))
    # cierre: el piano solo, resolviendo en La
    for i, (r, n) in enumerate((prog[3], prog[5], prog[0], prog[0])):
        compas('A4:1 . . . . . . . . . . . . . . .' if i == 3 else V, '%s . . . . . . . . . . . . . . .' % r, 'nada', arp(*n))
    return T

import os
FASE = int(os.environ.get('V6FASE', '1'))
# cada fase lleva solo su tema (0) y el del jefe (1): así cabe todo en memoria
TODOS = {1: fase1, 2: fase2, 3: fase3, 4: fase4, 5: fase5}
TEMAS = [TODOS[FASE](), jefe()]
if os.environ.get('V6TEMAS'):          # grabaciones: otros temas en las ranuras 0 y 1 (intro, final...)
    EXTRA = {'intro': intro, 'final': final, 'jefe': jefe}
    TEMAS = [EXTRA[n]() for n in os.environ['V6TEMAS'].split(',')]

# ---------------------------------------------------------------- salida
def main():
    L = ['; generado por tools/musica.py · no editar', '']
    pats, pid = [], {}
    temas = []
    for T in TEMAS:
        n = len(T.can[0])
        assert all(len(c) == n for c in T.can), T.nombre
        compases = []
        for b in range(n):
            fila = []
            for c in range(4):
                p = tuple(cod(T, c, t) for t in T.can[c][b])
                if p not in pid: pid[p] = len(pats); pats.append(p)
                fila.append(pid[p])
            compases.append(fila)
        temas.append((T, compases))
    assert len(pats) < 256
    # tablas de afinación (con hueco para arpegios)
    L.append('MUS_PURA: .byte ' + ','.join('$%02X' % n for c, n in PURA))
    L.append('MUS_ZUMB: .byte ' + ','.join('$%02X' % n for c, n in ZUMB))
    # instrumentos
    env, arp, eo, ao = [], [], [], []
    for k in INAMES:
        i = INS[k]; eo.append(len(env)); env += i['env']; ao.append(len(arp)); arp += i['arp']
    assert len(env) < 256 and len(arp) < 256
    def row(nm, vals): L.append('%s: .byte %s' % (nm, ','.join('$%02X' % v for v in vals)))
    row('MI_CTL', [INS[k]['ctl'] for k in INAMES])
    row('MI_TAB', [INS[k]['tab'] for k in INAMES])
    row('MI_FIX', [INS[k]['fix'] for k in INAMES])
    row('MI_SLD', [INS[k]['sld'] for k in INAMES])
    row('MI_ENV', eo)
    row('MI_ENVL', [len(INS[k]['env']) - 1 for k in INAMES])
    row('MI_ARP', ao)
    row('MI_ARPL', [len(INS[k]['arp']) for k in INAMES])
    row('MI_WOB', [INS[k]['wob'] for k in INAMES])
    row('MUS_ENVT', env)
    row('MUS_ARPT', arp)
    # patrones
    L.append('MUS_PATLO: .byte ' + ','.join('<MP%d' % i for i in range(len(pats))))
    L.append('MUS_PATHI: .byte ' + ','.join('>MP%d' % i for i in range(len(pats))))
    for i, p in enumerate(pats): L.append('MP%d: .byte %s' % (i, ','.join('$%02X' % v for v in p)))
    # temas
    for k, (T, comp) in enumerate(temas):
        L.append('MUS_T%d: .byte %s' % (k, ','.join('%d' % v for f in comp for v in f)))
        L.append('MUS_T%d_INS: .byte %s' % (k, ','.join('%d' % INAMES.index(x) for c in T.ran for x in c)))
    row('MUS_LEN', [len(c) for T, c in temas])
    row('MUS_LOOP', [T.bucle for T, c in temas])
    row('MUS_SPD0', [T.vel[0] - 1 for T, c in temas])
    row('MUS_SPD1', [T.vel[1] - 1 for T, c in temas])
    L.append('MUS_TLO: .byte ' + ','.join('<MUS_T%d' % k for k in range(len(temas))))
    L.append('MUS_THI: .byte ' + ','.join('>MUS_T%d' % k for k in range(len(temas))))
    L.append('MUS_ILO: .byte ' + ','.join('<MUS_T%d_INS' % k for k in range(len(temas))))
    L.append('MUS_IHI: .byte ' + ','.join('>MUS_T%d_INS' % k for k in range(len(temas))))
    L.append('MUS_BASE = %d' % BASE)
    open('src/musdata.s', 'w').write('\n'.join(L) + '\n')
    tam = len(pats) * 16 + sum(len(c) * 4 for T, c in temas) + 2 * NT + len(env) + len(arp)
    for T, c in temas:
        bpm = 3600 / (sum(T.vel) / 2 * 4) * 59.94 / 60
        print('%s: %d compases (bucle desde %d) · %.0f BPM · %.0f s' % (T.nombre, len(c), T.bucle, bpm, len(c) * 16 * sum(T.vel) / 2 / 59.94))
    print('patrones %d · datos de música ~%d bytes' % (len(pats), tam))
    # notas usadas y su desafinación
    usadas = {}
    for T in TEMAS:
        for c in (0, 1, 3):
            for comp in T.can[c]:
                for t in comp:
                    if t in '.-': continue
                    n = t.split(':')[0]; m = midi(n)
                    tab = ZUMB if c == 1 else PURA
                    usadas[(c == 1, n)] = round(tab[m - BASE][0])
    peor = sorted(((v, k) for k, v in usadas.items()), reverse=True)[:6]
    print('mayor desafinación (cents):', ', '.join('%s %s %d' % ('bajo' if b else 'synth', n, v) for v, (b, n) in peor))

if __name__ == '__main__':
    main()
