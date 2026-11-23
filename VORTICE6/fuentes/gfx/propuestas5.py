"""FASE 4 · EL SARCÓFAGO DE SACRIFICIOS DE SATURNO · propuestas de enemigos.
Paleta: violeta profundo, oro envejecido, jade pálido y negro. Colores claros (las balas usan los de su franja)."""


def g(t):
    return [l.strip() for l in t.strip('\n').split('\n')]


ACOLITO = {
 'A · rombo dorado con iris (8x11)': ('M8', (0x2A, 0x0C), g("""
...aa...
..aaaa..
.aabbaa.
aabccbaa
aabcbcaa
aabccbaa
.aabbaa.
..aaaa..
...aa...
....a...
...a.a.."""), g("""
...aa...
..aaaa..
.aabbaa.
aabbbbaa
aabccbaa
aabbbbaa
.aabbaa.
..aaaa..
...aa...
...a.a..
....a...""")),
 'B · rombo con anillo orbital (16x9, doble ancho)': ('M8x2', (0x2A, 0x0C), g("""
...aa...
..aaaa..
bbabcabb
b.acca.b
bbabcabb
..aaaa..
...aa...
........
........"""), g("""
...aa...
.baaaab.
b.abca.b
..acca..
b.abca.b
.baaaab.
...aa...
........
........""")),
}
GUARDIAN = {
 'A · segmento curvo de armadura (12x14)': ('M12', (0x6A, 0x0C), g("""
......XXXX..
....XXXXX...
...XXXcX....
..XXXcX.....
.XXXXX......
.XXXcX......
XXXXX.......
XXXXX.......
.XXXcX......
.XXXXX......
..XXXcX.....
...XXXcX....
....XXXXX...
......XXXX.."""), g("""
.......XXX..
....XXXXX...
...XXXcX....
..XXXcX.....
.XXXXX......
.XXXcX......
XXXXX.......
XXXXX.......
.XXXcX......
.XXXXX......
..XXXcX.....
...XXXcX....
....XXXXX...
.......XXX..""")),
 'B · anillo partido con remaches (16x10, doble ancho)': ('M8x2', (0x6A, 0x0C), g("""
...aaaa.
.aacbbaa
aac....b
ac......
ac......
ac......
aac....b
.aacbbaa
...aaaa.
........"""), g("""
...aaaa.
.aabcbaa
aab....b
ab......
ac......
ab......
aab....b
.aabcbaa
...aaaa.
........""")),
}
VASO = {
 'A · urna negra con luz púrpura (8x12)': ('M8', (0x5C, 0x0A), g("""
..bbbb..
...bb...
.bbbbbb.
bbbaabbb
bbaccabb
bbaccabb
bbbaabbb
bbbbbbbb
.bbbbbb.
..bbbb..
.bb..bb.
........"""), g("""
..bbbb..
...bb...
.bbbbbb.
bbbccbbb
bbcaacbb
bbcaacbb
bbbccbbb
bbbbbbbb
.bbbbbb.
..bbbb..
.bb..bb.
........""")),
 'B · cápsula votiva, 1 color (8x10, 2 por franja)': ('N', 0x5C, g("""
..XXXX..
.XX..XX.
XX.XX.XX
X.XXXX.X
X.XXXX.X
XX.XX.XX
.XX..XX.
..XXXX..
...XX...
........"""), g("""
..XXXX..
.XXXXXX.
XXX..XXX
XX.XX.XX
XX.XX.XX
XXX..XXX
.XXXXXX.
..XXXX..
...XX...
........""")),
}
ESCRIBA = {
 'A · máscara alargada flotante (8x16)': ('M8', (0xBA, 0x0E), g("""
..aaaa..
.aaaaaa.
aaccccaa
aac..caa
aaccccaa
aaaaaaaa
ab.aa.ba
abbaabba
aaaaaaaa
aaacc.aa
aaaaaaaa
.aabbaa.
.aaaaaa.
..aaaa..
...aa...
...a...."""), g("""
..aaaa..
.aaaaaa.
aaccccaa
aac..caa
aaccccaa
aaaaaaaa
ab.aa.ba
abbaabba
aaaaaaaa
aaaccaaa
aaaaaaaa
.aabbaa.
.aaaaaa.
..aaaa..
...aa...
....a...""")),
 'B · escriba con tablilla (12x14)': ('M12', (0xBA, 0x0E), g("""
...XXXX.....
..XXXXXX....
..XcXXcX....
..XXXXXX....
...XccX.....
....XX......
..XXXXXXXXX.
.XXXXXXX..X.
XX.XXXXX.XX.
...XXXXX..X.
...XXXXXXXX.
...XX..XX...
...XX..XX...
..XXX..XXX.."""), g("""
...XXXX.....
..XXXXXX....
..XcXXcX....
..XXXXXX....
...XccX.....
....XX......
..XXXXXXXXX.
.XXXXXXX.X..
XX.XXXXX.X..
...XXXXX.X..
...XXXXXXXX.
...XX..XX...
..XX....XX..
.XXX....XXX.""")),
}
BKGRAD_F4 = [0x00, 0x00, 0x00, 0x50, 0x50, 0x60, 0x60, 0x60, 0x62, 0x62, 0x70, 0x70, 0x72, 0x72, 0x60, 0x60, 0x50, 0x50, 0x00, 0x00]
