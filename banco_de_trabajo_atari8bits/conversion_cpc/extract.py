import sys,struct
d=open(sys.argv[1],'rb').read(); out=sys.argv[2]
rom=b''.join(d[12+i*16392+8:12+i*16392+8+16384] for i in range(32))
base=0xc000
files={}
for e in range(64):
    ent=rom[base+e*32:base+e*32+32]
    if ent[0]==0xe5: continue
    name=(bytes(c&0x7f for c in ent[1:9]).decode().strip()+'.'+bytes(c&0x7f for c in ent[9:12]).decode())
    ex=ent[12]; rc=ent[15]; blocks=[b for b in ent[16:32] if b]
    files.setdefault(name,[]).append((ex,rc,blocks))
for n,exts in files.items():
    data=b''
    for ex,rc,bl in sorted(exts):
        chunk=b''.join(rom[base+b*1024:base+b*1024+1024] for b in bl)
        data+=chunk[:rc*128]
    open(out+'/'+n,'wb').write(data)
    h=data[:128]
    print(n,len(data),'type',h[0x12],'load',hex(struct.unpack('<H',h[0x15:0x17])[0]),'len',struct.unpack('<H',h[0x18:0x1a])[0],'exec',hex(struct.unpack('<H',h[0x1a:0x1c])[0]))
