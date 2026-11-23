#!/usr/bin/env python3
"""INTRO: la nave Vórtice 6 de la carátula, redibujada como ilustración propia (polígonos y sombreado por bandas)
para pasarla a ANTIC E. Se dibuja a 640x384 (proporción de pantalla) y se reduce a 160x192 (píxel ancho)."""
import sys, os, math, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'gfx'))
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
W, H = 640, 384
R = random.Random(6)
im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
# ---- fondo: espacio violeta-azul con degradado y nebulosa
for y in range(H):
    t = y / H
    c = (int(18 + 30 * t), int(10 + 8 * t), int(48 + 40 * (1 - abs(t - .4))))
    d.line([(0, y), (W, y)], fill=c)
for k in range(40):                                  # nebulosa
    x, y = R.randrange(W), R.randrange(H // 2)
    r = R.randrange(30, 90)
    d.ellipse((x - r, y - r // 2, x + r, y + r // 2), fill=(60 + R.randrange(40), 30, 110 + R.randrange(60)))
im = im.filter(ImageFilter.GaussianBlur(18)); d = ImageDraw.Draw(im)
for k in range(140):                                 # estrellas
    x, y = R.randrange(W), R.randrange(H)
    b = R.choice((150, 200, 255))
    d.rectangle((x, y, x + 3, y + 1), fill=(b, b, b))
# explosión naranja abajo a la izquierda
for k in range(70):
    x, y = R.gauss(60, 55), R.gauss(345, 35)
    r = R.randrange(14, 40)
    c = R.choice(((255, 140, 30), (240, 90, 20), (255, 190, 80), (200, 50, 10)))
    d.ellipse((x - r, y - r, x + r, y + r), fill=c)
# rayos láser naranjas paralelos a la nave
for (x0, y0, L) in ((640, 210, 300), (620, 300, 260), (520, 372, 200), (640, 130, 130)):
    d.line([(x0, y0), (x0 - L, y0 + L * 0.52)], fill=(255, 150, 60), width=3)
    d.line([(x0, y0), (x0 - L, y0 + L * 0.52)], fill=(255, 230, 180), width=1)
# dos cazas lejanos (siluetas pequeñas)
for (cx, cy, s) in ((520, 270, 1.0), (470, 330, 0.8)):
    pts = [(-18, 0), (10, -4), (16, -14), (14, -3), (22, 0), (14, 3), (16, 12), (10, 4)]
    d.polygon([(cx + s * x, cy + s * y) for x, y in pts], fill=(170, 170, 180))
# ---- la nave: cola arriba a la derecha, punta abajo a la izquierda; v = lado de arriba (luz)
T = np.array([560., 96.]); N = np.array([96., 318.])
u = (N - T) / np.linalg.norm(N - T); v = np.array([u[1], -u[0]])
if v[1] > 0: v = -v
Lh = float(np.linalg.norm(N - T))
def P(s, w): p = T + u * s + v * w; return (float(p[0]), float(p[1]))
def anch(s):
    f = min(max(s / Lh, 0), 1)
    if f < .06: return 30 + 160 * f
    if f < .66: return 40
    return max(5, 40 * (1 - (f - .66) / .34) ** .7)
def tubo(s0, s1, w0, r, luz=(225, 225, 232), som=(110, 110, 122)):
    """cilindro a lo largo del eje: franjas de luz a sombra"""
    n = 6
    for k in range(n):
        t0, t1 = -r + 2 * r * k / n, -r + 2 * r * (k + 1) / n
        f = (k + .5) / n
        c = tuple(int(luz[i] * (1 - f) + som[i] * f) for i in range(3))
        d.polygon([P(s0, w0 + r - (t0 + r)), P(s1, w0 + r - (t0 + r)), P(s1, w0 + r - (t1 + r)), P(s0, w0 + r - (t1 + r))], fill=c)
# alas barridas hacia la cola: arriba y abajo
d.polygon([P(70, 38), P(190, 38), P(30, 150), P(-10, 150)], fill=(185, 185, 195))
d.polygon([P(-10, 150), P(30, 150), P(26, 160), P(-16, 160)], fill=(210, 50, 45))
d.line([P(80, 46), P(10, 140)], fill=(120, 120, 130), width=2)
d.polygon([P(90, -38), P(200, -38), P(70, -128), P(40, -128)], fill=(105, 105, 116))
d.polygon([P(40, -128), P(70, -128), P(68, -136), P(34, -136)], fill=(210, 50, 45))
# deriva (aleta) sobre la cola
d.polygon([P(10, 30), P(60, 30), P(-4, 96), P(-20, 96)], fill=(160, 160, 170))
# cañones largos bajo el casco
for w in (-28, -40):
    d.line([P(150, w), P(Lh * .78, w)], fill=(55, 55, 65), width=5)
    d.line([P(150, w + 2), P(Lh * .78, w + 2)], fill=(160, 160, 170), width=1)
# casco cilíndrico (luz arriba-izquierda, sombra abajo)
steps = 50
for k in range(6):
    f0, f1 = 1 - 2 * k / 6, 1 - 2 * (k + 1) / 6
    sh = (k + .5) / 6
    c = tuple(int(235 * (1 - sh) + 95 * sh) for _ in range(3))
    c = (c[0], c[1], min(255, c[2] + 8))
    poly = [P(Lh * i / steps, anch(Lh * i / steps) * f0) for i in range(steps + 1)] + \
           [P(Lh * i / steps, anch(Lh * i / steps) * f1) for i in range(steps, -1, -1)]
    d.polygon(poly, fill=c)
for s_ in range(30, int(Lh * .9), 30):                # paneles
    a_ = anch(s_)
    d.line([P(s_, -a_), P(s_, a_)], fill=(90, 90, 100), width=2)
# motores gemelos sobre el casco (como en la carátula) y su fuego
for w in (44, -44):
    tubo(-10, 150, w - 14, 14)
    c = P(-14, w)
    d.ellipse((c[0] - 16, c[1] - 14, c[0] + 16, c[1] + 14), fill=(50, 50, 60))
    for k in range(3):
        g = P(-28 - 16 * k, w); rr = 13 - 3 * k
        d.ellipse((g[0] - rr, g[1] - rr, g[0] + rr, g[1] + rr), fill=(150 + 30 * k, 190 + 20 * k, 255))
# franja roja a lo largo y «V6»
d.line([P(Lh * .26, anch(1) * .45), P(Lh * .90, anch(Lh * .9) * .45)], fill=(220, 30, 30), width=9)
d.line([P(Lh * .40, -18), P(Lh * .52, -18)], fill=(215, 40, 40), width=5)
# cabina (cristal oscuro con brillo)
d.polygon([P(Lh * .60, 4), P(Lh * .68, 26), P(Lh * .80, 24), P(Lh * .86, 10), P(Lh * .66, -2)], fill=(28, 36, 70))
d.line([P(Lh * .66, 14), P(Lh * .80, 18)], fill=(170, 200, 240), width=2)
# luces rojas de posición
for s_, w in ((Lh * .45, -38), (Lh * .2, 46), (Lh * .55, -36), (Lh * .3, -40)):
    p = P(s_, w); d.rectangle((p[0] - 3, p[1] - 2, p[0] + 3, p[1] + 2), fill=(255, 40, 40))
im.save(os.path.join(ROOT, 'pic', 'nave_arte.png'))
small = im.resize((160, 192), Image.LANCZOS)
small.save(os.path.join(ROOT, 'pic', 'nave_160.png'))
