#!/usr/bin/env python3
"""Convierte saltos condicionales fuera de alcance (errores de ca65) en salto invertido + jmp."""
import re, subprocess, sys
INV = {'beq': 'bne', 'bne': 'beq', 'bcc': 'bcs', 'bcs': 'bcc', 'bpl': 'bmi', 'bmi': 'bpl', 'bvc': 'bvs', 'bvs': 'bvc'}
src, cc = sys.argv[1], sys.argv[2]
for it in range(20):
    r = subprocess.run([cc + '/ca65', '-I', 'src', '-o', '/tmp/x.o', src], capture_output=True, text=True)
    lines = sorted({int(m) for m in re.findall(r'g1\.s:(\d+): Error: Range error', r.stderr)}, reverse=True)
    if not lines:
        print('ok tras', it, 'pasadas'); print(r.stderr[:2000]); break
    L = open(src).read().split('\n')
    for n in lines:
        l = L[n - 1]
        m = re.match(r'^(\S*:)?(\s+)(b(?:eq|ne|cc|cs|pl|mi|vc|vs))\s+(\S+)(.*)$', l)
        if not m: print('no sé arreglar', n, l); sys.exit(1)
        lab, sp, op, tgt, rest = m.groups()
        L[n - 1] = (lab or '') + sp + INV[op] + ' *+5' + rest
        L.insert(n, '        jmp ' + tgt)
    open(src, 'w').write('\n'.join(L))
