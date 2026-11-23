#!/usr/bin/env python3
"""¿Se puede pasar cada sala con monstruos y gotas? BFS sobre (héroe, tiempo) simulando el mundo
paso a paso como game.s. Dos reglas: 'port' (todo mata, también encima) y 'orig' (BASIC original:
códigos 121-130 hacen de pared; muerte por solape solo con monstruos; las gotas solo al chocarlas)."""
import sys, os
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rooms import room, tables
T = tables()
DROPS = {1: ([(14, 0)], 16, 19, 1, 0), 4: ([(13, 0)], 5, 13, 0, 0),
         6: ([(5, 0), (15, 0)], 5, 19, 0, 0), 7: ([(5, 0), (15, 6)], 5, 13, 0, 5)}

def world(f):
    """Capas dinámicas D[k] (celda -> etiqueta) tras k pasos, y el periodo."""
    ms = [list(m[1:9]) + [m[10], m[11]] for m in T[f - 1][1:]]
    d = DROPS.get(f)
    gy, gyb, dst, dwait, slow = (d[1] if d else 0), 0, 0, 0, 0
    lay = {}
    D, seen = [dict()], {}
    def put(r, c, v):
        if v is None: lay.pop((r, c), None)
        else: lay[(r, c)] = v
    for k in range(1, 5000):
        for m in ms:
            r, c = m[0], m[1]
            for dr in (0, 1):
                for dc in (0, 1): put(r + dr, c + dc, None)
            if m[2] == 0:
                m[0] -= 1
                if m[0] == m[3]: m[2] = 2
            elif m[2] == 2:
                m[0] += 1
                if m[0] == m[4]: m[2] = 0
            if m[5] == 0:
                m[1] -= 1
                if m[1] == m[6]: m[5] = 2
            elif m[5] == 2:
                m[1] += 1
                if m[1] == m[7]: m[5] = 0
            m[8], m[9] = m[9], m[8]
            for i, (dr, dc) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
                put(m[0] + dr, m[1] + dc, ('M', m[8] + i))
        if d:
            cols, st, lim, sl, wt = d
            def row(rr, v):
                for c, off in cols:
                    put(rr + off, c, v); put(rr + off, c + 1, v)
            go = True
            if dwait: dwait -= 1; go = False
            elif sl:
                slow ^= 1
                if slow: go = False
            if go:
                if dst == 0:
                    if gyb: row(gyb, None)
                    row(gy, 'G'); row(gy + 1, 'G'); gyb = gy; gy += 1
                    if gy > lim:
                        row(gy - 1, None); row(gy, 'G'); dst = 1
                elif dst == 1: dst = 2
                else:
                    row(gy, None); gy = st; dst = 0; gyb = 0; dwait = wt
        key = (tuple(tuple(m) for m in ms), gy, gyb, dst, dwait, slow)
        D.append(dict(lay))
        if key in seen: return D, seen[key], k - seen[key]
        seen[key] = k
    raise RuntimeError

def solve(f, rules):
    g = room(f)
    D, j, P = world(f)
    def dyn(k): return D[k] if k < len(D) - 1 else D[j + (k - j) % P]
    def tnorm(k): return k if k < j else j + (k - j) % P
    hr, hc = T[f - 1][0][1], T[f - 1][0][2]
    def cls(r, c, door, lay):
        v = lay.get((r, c))
        if v == 'G': return 'D'
        if v:
            code = v[1]
            return 1 if (rules == 'orig' and 121 <= code <= 130) else 'D'
        if not (1 <= r <= 24 and 1 <= c <= 20): return 0
        ch, pen = g[r][c]
        if door and ch in (42, 64): return 0
        if ch == 42: return 'K'
        if f == 8 and pen == 2: return 'W'
        if ch == 137: return 'D'
        return 1 if ch in map(ord, '`abcd@') else 0
    def step(st, a, k):
        x, y, d, sa, fall, door = st
        lay = dyn(k - 1)
        ev = set()
        def p2(cells):
            for r, c in cells:
                v = cls(r, c, door, lay)
                if v == 0: continue
                ev.add({'K': 'door', 'W': 'win', 'D': 'dead'}.get(v, 'blk'))
                return True
            return False
        def down():
            nonlocal x
            if p2([(x + 2, y), (x + 2, y + 1)]): return False
            x += 1
            if x > 21: ev.add('next')
            return True
        def up():
            nonlocal x
            if p2([(x - 1, y), (x - 1, y + 1)]): return False
            x = max(2, x - 1); return True
        def right():
            nonlocal y
            if p2([(x, y + 2), (x + 1, y + 2)]): return False
            y += 1
            if y > 18: ev.add('next')
            return True
        def left():
            nonlocal y
            if p2([(x, y - 1), (x + 1, y - 1)]): return False
            y = max(2, y - 1); return True
        stop = lambda: ev & {'next', 'win', 'dead'}
        if sa:
            (up if sa > 2 else down)()
            if not stop():
                sa -= 1
                (right if d == 1 else left)()
        else:
            if not fall:
                if a & 1:
                    if d == 1: d = 2
                    else: left()
                if a & 2 and not stop():
                    if d == 2: d = 1
                    else: right()
                if a & 4: sa = 6
            fall = 0
            if not stop():
                if down(): fall = 1
        if not stop():      # tras mover monstruos y gotas: ¿algo mortal encima?
            after = dyn(k)
            for r in (x, x + 1):
                for c in (y, y + 1):
                    v = after.get((r, c))
                    if v and (rules == 'port' or v != 'G'): ev.add('dead')
        if 'door' in ev: door = 1
        return (x, y, d, sa, fall, door), ev
    start = (hr, hc, 1, 0, 0, 0, 0)
    prev = {start: None}
    q = deque([start])
    goal = 'win' if f == 8 else 'next'
    while q:
        s = q.popleft()
        k = s[6] + 1
        for a in (0, 1, 2, 4, 5, 6):
            ns, ev = step(s[:6], a, k)
            if 'dead' in ev: continue
            if goal in ev:
                n = 1; t = s
                while prev[t]: t = prev[t]; n += 1
                return n
            ns = ns + (tnorm(k),)
            if ns not in prev:
                prev[ns] = s; q.append(ns)
    return None

if __name__ == '__main__':
    for rules in ('orig', 'port'):
        print(rules, ' '.join('s%d:%s' % (f, solve(f, rules)) for f in range(1, 9)))
