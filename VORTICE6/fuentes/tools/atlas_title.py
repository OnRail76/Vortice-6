"""Rótulos con la fuente del juego (8x8), en degradado, para el Atlas."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gfx'))
import font
from PIL import Image
GRADS = {'fuego': [(255, 236, 140), (255, 196, 60), (255, 140, 30), (240, 80, 20), (200, 40, 20), (150, 20, 20), (120, 10, 30), (90, 10, 40)],
         'acero': [(255, 255, 255), (230, 236, 245), (200, 210, 225), (175, 185, 205), (150, 160, 185), (130, 140, 170), (110, 120, 150), (90, 95, 130)],
         'cian':  [(220, 250, 255), (160, 235, 255), (100, 215, 255), (70, 190, 245), (50, 160, 230), (40, 130, 210), (30, 100, 190), (20, 80, 170)]}
def atari(text, out, scale=4, grad='fuego', shadow=True):
    t = text.upper()
    w, h = len(t) * 8, 8
    im = Image.new('RGBA', ((w + 1) * scale, (h + 1) * scale), (0, 0, 0, 0))
    px = im.load()
    G = GRADS[grad]
    for i, ch in enumerate(t):
        rows = font._G.get(ch, font._G['?'])
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c != 'X': continue
                for yy in range(scale):
                    for xx in range(scale):
                        X, Y = (i * 8 + x) * scale + xx, y * scale + yy
                        if shadow:
                            px[X + scale // 2, Y + scale // 2] = (0, 0, 0, 200) if px[X + scale // 2, Y + scale // 2][3] == 0 else px[X + scale // 2, Y + scale // 2]
    for i, ch in enumerate(t):
        rows = font._G.get(ch, font._G['?'])
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c != 'X': continue
                for yy in range(scale):
                    for xx in range(scale):
                        px[(i * 8 + x) * scale + xx, y * scale + yy] = G[y] + (255,)
    im.save(out)
