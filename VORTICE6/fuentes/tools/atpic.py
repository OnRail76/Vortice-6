#!/usr/bin/env python3
"""Conversión de imagen a ANTIC E (160x192, 4 colores por franja: negro fijo + 3 que cambia una DLI).
Salida: bitmap (7680 bytes) + tabla de colores por franja (PF0, PF1, PF2) + vista previa."""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'gfx'))
from pal import atari_rgb
from PIL import Image, ImageFilter
import numpy as np
PAL = np.array([atari_rgb(v) for v in range(0, 256, 2)], dtype=float)
VAL = np.arange(0, 256, 2)

def lab(c):            # distancia perceptual sencilla (pesos de luminancia)
    return c * np.array([0.30, 0.59, 0.11]) ** 0.5

def convert(img, band=4, err=0.75, fixed_black=True, prev_weight=0.6, keep=None):
    """img: PIL RGB 160x192 (píxel ancho). Devuelve índices 0-3 por píxel, paletas por franja (valores Atari)"""
    a = np.asarray(img, dtype=float).copy()
    H, W = a.shape[:2]
    idx = np.zeros((H, W), dtype=np.uint8); pals = []
    prev = None
    for y0 in range(0, H, band):
        blk = a[y0:y0 + band].reshape(-1, 3)
        lum = blk.sum(1)
        cand = blk[lum > 40] if (lum > 40).sum() > 12 else blk
        k = 3
        cent = prev.copy() if prev is not None else cand[np.linspace(0, len(cand) - 1, k).astype(int)].copy()
        for it in range(12):
            d = ((cand[:, None] - cent[None]) ** 2).sum(2); l = d.argmin(1)
            for j in range(k):
                if (l == j).any(): cent[j] = cand[l == j].mean(0) * (1 - prev_weight * 0) 
        if prev is not None: cent = cent * (1 - 0.25) + prev * 0.25
        prev = cent.copy()
        cols = []
        for c in cent:
            order = ((PAL - c) ** 2).sum(1).argsort()
            for o in order:
                if VAL[o] not in cols and VAL[o] != 0: cols.append(int(VAL[o])); break
        cols.sort(key=lambda v: v & 15)
        pals.append(cols)
        P = np.array([[0, 0, 0]] + [atari_rgb(v) for v in cols], dtype=float)
        for y in range(y0, min(H, y0 + band)):
            rng = range(W) if y % 2 == 0 else range(W - 1, -1, -1)
            dx = 1 if y % 2 == 0 else -1
            for x in rng:
                old = a[y, x].copy()
                j = ((P - old) ** 2).sum(1).argmin()
                idx[y, x] = j
                e = (old - P[j]) * err
                if keep is not None and keep[y, x]: e = e * 0.4
                if 0 <= x + dx < W: a[y, x + dx] += e * 7 / 16
                if y + 1 < H:
                    if 0 <= x - dx < W: a[y + 1, x - dx] += e * 3 / 16
                    a[y + 1, x] += e * 5 / 16
                    if 0 <= x + dx < W: a[y + 1, x + dx] += e * 1 / 16
    return idx, pals

def clean(idx, protect=None):
    """quita píxeles sueltos (mayoría de los 4 vecinos), salvo en la zona protegida (ojos)"""
    out = idx.copy(); H, W = idx.shape
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if protect is not None and protect[y, x]: continue
            n = [idx[y - 1, x], idx[y + 1, x], idx[y, x - 1], idx[y, x + 1]]
            if idx[y, x] not in n:
                vals, cnt = np.unique(n, return_counts=True)
                if cnt.max() >= 3: out[y, x] = vals[cnt.argmax()]
    return out

def preview(idx, pals, band, scale=3):
    H, W = idx.shape
    im = Image.new('RGB', (W * 2 * scale, H * scale)); px = im.load()
    for y in range(H):
        P = [(0, 0, 0)] + [atari_rgb(v) for v in pals[y // band]]
        for x in range(W):
            c = P[idx[y, x]]
            for dy in range(scale):
                for dx in range(2 * scale): px[x * 2 * scale + dx, y * scale + dy] = c
    return im

def tobytes(idx):
    H, W = idx.shape
    out = bytearray()
    for y in range(H):
        for x in range(0, W, 4):
            out.append((idx[y, x] << 6) | (idx[y, x + 1] << 4) | (idx[y, x + 2] << 2) | idx[y, x + 3])
    return bytes(out)

def convert2(img, cand, band=4, err=0.7, lam=None):
    """paleta por franja elegida de un juego corto de colores (cand), con coste por cambiar de franja a franja:
    menos rayas horizontales. Negro fijo como fondo."""
    import itertools
    a = np.asarray(img, dtype=float).copy()
    H, W = a.shape[:2]
    C = np.array([atari_rgb(v) for v in cand], dtype=float)
    combos = list(itertools.combinations(range(len(cand)), 3))
    if lam is None: lam = 2500.0 * band * W / 160
    pals = []; prev = None
    for y0 in range(0, H, band):
        blk = a[y0:y0 + band].reshape(-1, 3)
        dk = (blk ** 2).sum(1)                                   # al negro
        dc = ((blk[:, None] - C[None]) ** 2).sum(2)              # a cada candidato
        best = None
        for cb in combos:
            e = np.minimum(dk, dc[:, list(cb)].min(1)).sum()
            if prev is not None: e += lam * len(set(cb) - set(prev))
            if best is None or e < best[0]: best = (e, cb)
        prev = best[1]
        pals.append(sorted([cand[i] for i in best[1]], key=lambda v: v & 15))
    idx = np.zeros((H, W), dtype=np.uint8)
    for y in range(H):
        P = np.array([[0, 0, 0]] + [atari_rgb(v) for v in pals[y // band]], dtype=float)
        rng = range(W) if y % 2 == 0 else range(W - 1, -1, -1); dx = 1 if y % 2 == 0 else -1
        for x in rng:
            old = a[y, x].copy(); j = ((P - old) ** 2).sum(1).argmin(); idx[y, x] = j
            e = (old - P[j]) * err
            if 0 <= x + dx < W: a[y, x + dx] += e * 7 / 16
            if y + 1 < H:
                if 0 <= x - dx < W: a[y + 1, x - dx] += e * 3 / 16
                a[y + 1, x] += e * 5 / 16
                if 0 <= x + dx < W: a[y + 1, x + dx] += e * 1 / 16
    return idx, pals

def convert4(img, cand, band=4, err=0.8, lam=40000.0):
    """como convert2 pero con 4 colores libres por franja (el fondo también cambia por DLI)"""
    import itertools
    a = np.asarray(img, dtype=float).copy()
    H, W = a.shape[:2]
    C = np.array([atari_rgb(v) for v in cand], dtype=float)
    combos = np.array(list(itertools.combinations(range(len(cand)), 4)))
    pals = []; prev = None
    for y0 in range(0, H, band):
        blk = a[y0:y0 + band].reshape(-1, 3)
        dc = ((blk[:, None] - C[None]) ** 2).sum(2)               # píxeles x candidatos
        e = dc[:, combos].min(2).sum(0)                           # por combinación
        if prev is not None:
            ch = np.array([len(set(cb) - set(prev)) for cb in combos])
            e = e + lam * ch
        cb = combos[e.argmin()]; prev = list(cb)
        pals.append(sorted([cand[i] for i in cb], key=lambda v: v & 15))
    idx = np.zeros((H, W), dtype=np.uint8)
    for y in range(H):
        P = np.array([atari_rgb(v) for v in pals[y // band]], dtype=float)
        rng = range(W) if y % 2 == 0 else range(W - 1, -1, -1); dx = 1 if y % 2 == 0 else -1
        for x in rng:
            old = a[y, x].copy(); j = ((P - old) ** 2).sum(1).argmin(); idx[y, x] = j
            e = (old - P[j]) * err
            if 0 <= x + dx < W: a[y, x + dx] += e * 7 / 16
            if y + 1 < H:
                if 0 <= x - dx < W: a[y + 1, x - dx] += e * 3 / 16
                a[y + 1, x] += e * 5 / 16
                if 0 <= x + dx < W: a[y + 1, x + dx] += e * 1 / 16
    return idx, pals

def preview4(idx, pals, band, scale=3):
    H, W = idx.shape
    im = Image.new('RGB', (W * 2 * scale, H * scale)); px = im.load()
    for y in range(H):
        P = [atari_rgb(v) for v in pals[y // band]]
        for x in range(W):
            c = P[idx[y, x]]
            for dy in range(scale):
                for dx in range(2 * scale): px[x * 2 * scale + dx, y * scale + dy] = c
    return im
