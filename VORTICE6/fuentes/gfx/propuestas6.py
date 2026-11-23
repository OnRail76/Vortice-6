"""FASE 5 · LA NAVE VIVIENTE · propuestas de enemigos (los 4 del GDD).
Paleta: verde enfermizo, rojo sangre, hueso pálido y negro. Colores claros (las balas usan los de su franja)."""


def g(t):
    return [l.strip() for l in t.strip('\n').split('\n')]


GLOBULO = {
 'A · célula facetada con núcleo (8x8)': ('M8', (0x3A, 0x0E), g("""
..aaaa..
.abbbba.
abbccbba
abccccba
abccccba
abbccbba
.abbbba.
..aaaa.."""), g("""
..aaaa..
.abbbba.
abccbbba
abcccbba
abbcccba
abbbccba
.abbbba.
..aaaa..""")),
 'B · glóbulo de membrana dentada (12x11)': ('M12', (0x3A, 0x0E), g("""
....XXXX....
..XX.XX.XX..
.X.XXXXXX.X.
.XXXccccXXX.
XXXccXXccXXX
XXXcXXXXcXXX
XXXccXXccXXX
.XXXccccXXX.
.X.XXXXXX.X.
..XX.XX.XX..
....XXXX...."""), g("""
....XXXX....
..XXXXXXXX..
.XX.XXXX.XX.
.XXXccccXXX.
XXXcXXXXcXXX
XXXcXccXcXXX
XXXcXXXXcXXX
.XXXccccXXX.
.XX.XXXX.XX.
..XXXXXXXX..
....XXXX....""")),
}
ESPINA = {
 'A · aguja de hueso con vértebras (8x20)': ('M8', (0x0C, 0xDA), g("""
...cc...
...cc...
...cc...
..acca..
..acca..
..aaaa..
..acca..
.aacbaa.
.aacbaa.
.aaaaaa.
.aacbaa.
aaacbbaa
aaacbbaa
aaaaaaaa
aaacbbaa
aacccbba
aacccbba
aaaaaaaa
.a.aa.a.
a..aa..a"""), g("""
........
........
...cc...
...cc...
..acca..
..acca..
..aaaa..
..acca..
.aacbaa.
.aacbaa.
.aaaaaa.
.aacbaa.
aaacbbaa
aaacbbaa
aaaaaaaa
aaacbbaa
aacccbba
aaaaaaaa
.a.aa.a.
a..aa..a""")),
 'B · púa con burbuja de aviso (8x18)': ('M8', (0x0C, 0xDA), g("""
..bbbb..
.b....b.
.b.bb.b.
.b....b.
..bbbb..
...cc...
...cc...
..acca..
..acca..
.aacbaa.
.aacbaa.
.aacbaa.
aaacbbaa
aaacbbaa
aacccbba
aacccbba
aaaaaaaa
a.a..a.a"""), g("""
........
..bbbb..
.b.bb.b.
..bbbb..
........
...cc...
...cc...
..acca..
..acca..
.aacbaa.
.aacbaa.
.aacbaa.
aaacbbaa
aaacbbaa
aacccbba
aacccbba
aaaaaaaa
a.a..a.a""")),
}
LARVA = {
 'A · dron segmentado con mandíbulas (12x8)': ('M12', (0xCA, 0x0E), g("""
X...........
.XX.XXXXXXX.
X.XXcXXcXXcX
.XXXXXXXXXXX
X.XXcXXcXXcX
.XX.XXXXXXX.
X...X..X..X.
...X..X..X.."""), g("""
.X..........
X.X.XXXXXXX.
..XXcXXcXXcX
.XXXXXXXXXXX
..XXcXXcXXcX
X.X.XXXXXXX.
.X...X..X..X
....X..X..X.""")),
 'B · larva acorazada, doble ancho (16x8)': ('M8x2', (0xCA, 0x0E), g("""
a..aaaaa
.aabcbcb
aabbbbbb
.acbcbcb
aabbbbbb
.aabcbcb
a..aaaaa
..a.a.a."""), g("""
.a.aaaaa
a.abcbcb
.abbbbbb
aacbcbcb
.abbbbbb
a.abcbcb
.a.aaaaa
.a.a.a.a""")),
}
PARASITO = {
 'A · pústula sobre tendón (8x12)': ('M8', (0x4A, 0xDC), g("""
..aaaa..
.abbbba.
abbccbba
abccccba
abbccbba
.abbbba.
..aaaa..
...cc...
..c..c..
.c....c.
c......c
........"""), g("""
..aaaa..
.abbbba.
abcbbcba
abbccbba
abcbbcba
.abbbba.
..aaaa..
...cc...
...cc...
..c..c..
.c....c.
c......c""")),
 'B · racimo de pústulas (12x12)': ('M12', (0x4A, 0xDC), g("""
..XX....XX..
.XccX..XccX.
.XccXXXXccX.
..XXXccXXX..
...XcXXcX...
..XcccccccX.
..XcXXXXXcX.
...XXXXXXX..
.....XX.....
....X..X....
...X....X...
..X......X.."""), g("""
..XX....XX..
.XXXX..XXXX.
.XccXXXXccX.
..XXXccXXX..
...XcccccX..
..XcXXXXXcX.
..XcccccccX.
...XXXXXXX..
.....XX.....
.....XX.....
....X..X....
...X....X...""")),
}
BKGRAD_F5 = [0x00, 0x00, 0x20, 0x30, 0x30, 0x40, 0x40, 0x40, 0x30, 0x30, 0x40, 0x40, 0x40, 0x30, 0x30, 0x20, 0x20, 0x00, 0x00, 0x00]
