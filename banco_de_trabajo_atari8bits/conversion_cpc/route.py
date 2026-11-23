#!/usr/bin/env python3
"""Busca (BFS) una ruta por cada sala con la misma lógica de pasos que game.s, ignorando
monstruos y gotas, y escribe un guion de run8 para recorrer el juego con la versión CHEAT."""
import sys, os
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rooms import room, tables
T = tables()
SOLID = set(map(ord, '`abcd@'))

def solve(f):
    g = room(f)
    hr, hc = T[f - 1][0][1], T[f - 1][0][2]
    def cell(r, c, door):
        if not (1 <= r <= 24 and 1 <= c <= 20): return 0
        ch, pen = g[r][c]
        if door and ch in (42, 64): return 0
        if ch == 42: return 'K'
        if f == 8 and pen == 2: return 'W'
        if ch == 137: return 'D'
        return 1 if ch in SOLID else 0
    def probe2(cells, door, ev):
        for r, c in cells:
            v = cell(r, c, door)
            if v == 0: continue
            if v == 'K': ev.add('door')
            if v == 'W': ev.add('win')
            if v == 'D': ev.add('dead')
            return True
        return False
    def step(st, a):
        x, y, d, sa, fall, door = st
        ev = set()
        L, R, F = a & 1, a & 2, a & 4
        def down():
            nonlocal x
            if probe2([(x + 2, y), (x + 2, y + 1)], door, ev): return False
            x += 1
            if x > 21: ev.add('next')
            return True
        def up():
            nonlocal x
            if probe2([(x - 1, y), (x - 1, y + 1)], door, ev): return False
            x = max(2, x - 1); return True
        def right():
            nonlocal y
            if probe2([(x, y + 2), (x + 1, y + 2)], door, ev): return False
            y += 1
            if y > 18: ev.add('next')
            return True
        def left():
            nonlocal y
            if probe2([(x, y - 1), (x + 1, y - 1)], door, ev): return False
            y = max(2, y - 1); return True
        if sa:
            (up if sa > 2 else down)()
            if not (ev & {'next', 'win'}):
                sa -= 1
                (right if d == 1 else left)()
        else:
            if not fall:
                if L:
                    if d == 1: d = 2
                    else: left()
                if R and not (ev & {'next', 'win'}):
                    if d == 2: d = 1
                    else: right()
                if F: sa = 6
            fall = 0
            if not (ev & {'next', 'win'}):
                if down(): fall = 1
        if 'door' in ev: door = 1
        return (x, y, d, sa, fall, door), ev
    start = (hr, hc, 1, 0, 0, 0)
    prev = {start: None}
    q = deque([start])
    goal = 'win' if f == 8 else 'next'
    while q:
        st = q.popleft()
        for a in (0, 1, 2, 4, 5, 6):
            ns, ev = step(st, a)
            if 'dead' in ev: continue
            if goal in ev:
                path = [a]; s = st
                while prev[s]: s, b = prev[s]; path.append(b)
                return path[::-1]
            if ns not in prev:
                prev[ns] = (st, a); q.append(ns)
    return None

if __name__ == '__main__':
    TICK = 6
    lines = ['in 160 166 0 1 0']
    t = 330            # primer paso tras la entrada de la sala
    for f in range(1, 9):
        p = solve(f)
        print('sala', f, 'pasos', None if p is None else len(p), p)
        if p is None: sys.exit(1)
        for a in p:
            joy = (4 if a & 1 else 0) | (8 if a & 2 else 0)
            lines.append('in %d %d %d %d 0' % (t, t + TICK - 1, joy, 1 if a & 4 else 0))
            t += TICK
        lines.append('shot %d fin%d.raw' % (t, f))
        t += 70 + (40 if f in (3, 4, 5, 8) else 0)    # entrada de la sala siguiente (+ puertas)
    lines.append('shot %d final.raw' % (t + 120))
    lines.append('end %d' % (t + 130))
    open(sys.argv[1] if len(sys.argv) > 1 else 'ruta.txt', 'w').write('\n'.join(lines) + '\n')
