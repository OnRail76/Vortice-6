; ---------------------------------------------------------------
; VÓRTICE 6 · CORAZÓN DEL VACÍO · FASE 1: EL DESGUACE ESPACIAL
; Atari 8 bits · 2026 - Tony C. Ware · programa y asistencia: GPT y Claude
;
; Pantalla como en Vórtice 5 y Zak Attack:
;  - 4 franjas fijas (filas 2-5, 6-9, 10-13, 14-17) con 2 huecos cada una (P2, P3).
;    Cada objeto tiene su hueco de por vida: nunca hay más sprites que huecos (sin parpadeo).
;  - Doble búfer completo: PMG (2 zonas), tablas DLI (2 bancos) y HPOS congelados por búfer.
;    El programa dibuja en el búfer oculto; la VBI solo cambia punteros (nada se corta).
;  - Los misiles se repintan enteros en cada cuadro (no quedan balas fantasma).
; ---------------------------------------------------------------
        .include "hw.inc"
HSCROL  = $D404

RING    = $A000             ; 20 filas x 128 (64 columnas escritas dos veces)
BOSSCR  = $AA00             ; pantalla de FERRUM-9 (20 x 48)
DLBUF   = $AE00
TB      = $9400             ; 15 tablas DLI x 64 (dos bancos de 32: entrada = fila)
TMODE   = TB
TBK     = TB+$40
TCH     = TB+$80
TPF0    = TB+$C0
TPF1    = TB+$100
TPF2    = TB+$140
TPF3    = TB+$180
TX0     = TB+$1C0
TX1     = TB+$200
TX2     = TB+$240
TX3     = TB+$280
TC0     = TB+$2C0
TC1     = TB+$300
TC2     = TB+$340
TC3     = TB+$380
TS2     = TB+$3C0             ; SIZEP2 por fila (doble ancho)
TS3     = TB+$400             ; SIZEP3 por fila
PMA     = $B000             ; búfer de sprites A
PMB     = $B800             ; búfer de sprites B

MAXO    = 10
ST_PLAY = 1
ST_BOSS = 2

; ---------------------------------------------------------------
        .segment "ZEROPAGE"
ptr:    .res 2
src:    .res 2
dst:    .res 2
colp:   .res 2
mq0:    .res 2              ; punteros del mapa (4 trozos de 5 filas)
mq1:    .res 2
mq2:    .res 2
mq3:    .res 2
tmp:    .res 8
frame:  .res 1
dlin:   .res 1
shown:  .res 1              ; búfer en pantalla (0/1)
rb:     .res 1              ; búfer en preparación
rbk:    .res 1              ; banco de tablas en preparación (0/8)
pmhi:   .res 1              ; página base del búfer de sprites en preparación
ready:  .res 1
gmode:  .res 1
scroll: .res 1
mbar:   .res 2              ; música: compás actual
mpp:    .res 2              ; música: patrón
mins:   .res 2              ; música: ranuras de instrumento del tema
mt:     .res 1
mt1:    .res 1
mt2:    .res 1
mt3:    .res 1
arena:  .res 1
camx:   .res 2
coarse: .res 2
colidx: .res 2
fine:   .res 1
solid0: .res 1
state:  .res 1
trig:   .res 1
shipx:  .res 1
shipy:  .res 1
shipst: .res 1              ; 0 viva, 1 explotando, 2 invulnerable
shiptm: .res 1
lives:  .res 1
power:  .res 1
shield: .res 1
score:  .res 3
hisc:   .res 3
hudd:   .res 1
hudmsg: .res 1
s0x:    .res 1
s0y:    .res 1
s1x:    .res 1              ; (libre)
s1y:    .res 1
s2y:    .res 1
sal:    .res 1              ; láseres vivos de la ráfaga: bits 0,1,2 = arriba, centro, abajo
sfan:   .res 1              ; 1 = abanico (P nivel 3)
ktyp:   .res 1              ; tipo del objeto destruido
mdrop:  .res 1
lane:   .res 1
gtm:    .res 1              ; fase 3: reloj de las erupciones              ; THALASSA: carril libre de la corriente (0-2)              ; UNIDAD CERO destruidos (sueltan P, S, P, S...)
cool:   .res 1
e0x:    .res 1
e0y:    .res 1
e0dy:   .res 1
e0dx:   .res 1
e1x:    .res 1
e1y:    .res 1
e1dy:   .res 1
e1dx:   .res 1
wv:     .res 1
spn:    .res 1
spt:    .res 1
sptyp:  .res 1
spb:    .res 1
spb2:   .res 1
spgap:  .res 1
spw:    .res 1
spk:    .res 1
pcap:   .res 1              ; cápsula pendiente (tipo), su x y su franja
pcx:    .res 1
pcb:    .res 1
nvt:    .res 1
bst:    .res 1
btm:    .res 2
bhp:    .res 1
eyefl:  .res 1
plate:  .res 1
siren:  .res 1
bassi:  .res 1
basst:  .res 1
bnote:  .res 1
lag:    .res 1
lastf:  .res 1
cheat:  .res 1              ; truco: abajo, abajo, FIRE en el título
chk:    .res 1
chkt:   .res 1
stkp:   .res 1
ctm:    .res 2              ; reloj de los estados del jefe
eyeopen:.res 1
wallk:  .res 1
vt:     .res 2              ; temporales SOLO de la VBI

; ---------------------------------------------------------------
        .segment "HIBSS"
HUDTOP: .res 64
HUDBOT: .res 64
HISCR:  .res 64
DIFSCR: .res 64             ; línea del título con la dificultad
; dificultad en uso (se copian de las tablas al empezar: setdif)
dbulx:  .res 1
dfair:  .res 1
dhp:    .res 1
duzw:   .res 1
duzw20: .res 1
descw:  .res 1
descw1: .res 1
descw14:.res 1
dbwarn: .res 1
dbwarn8:.res 1
dbstep: .res 1
dbstep8:.res 1
dunpl:  .res 1
dunpl8: .res 1
dbhp:   .res 1
idlec:  .res 2              ; título: cuadros sin tocar el mando (sale la historia)
stkh:   .res 1              ; título: izquierda/derecha ya pulsado
dcap:   .res 1              ; fácil: alterna cápsula extra en las oleadas sin cápsula
SCRLINE:.res 64
ROWLL:  .res 20
ROWLH:  .res 20
OT:     .res MAXO           ; objetos
OX:     .res MAXO
OY:     .res MAXO
OS:     .res MAXO
OTM:    .res MAXO
OH:     .res MAXO
pcrow:  .res 1              ; cápsula: fila de la comprobación en curso (0 = empezar)
pcbt:   .res 1              ; cápsula: franja que se comprueba
npar:   .res 1              ; fase 5: algún NODO PARÁSITO vivo (los glóbulos disparan el doble)
bdk:    .res 1              ; fase 5: nodos del CORAZÓN NULO destruidos (2 = sin blindaje)
bcyc:   .res 1              ; fase 5: ciclo de la Mutación (alterna carriles y aspiración)
OW:     .res MAXO
ODX:    .res MAXO
ODY:    .res MAXO
OBT:    .res MAXO           ; primera línea de su franja
OB:     .res MAXO           ; franja
OP:     .res MAXO           ; 0 = P2, 1 = P3, 2 = pareja
SLOT:   .res 8              ; franja*2 + player -> objeto+1
SDY:    .res 16             ; y dibujada por búfer y hueco
SDH:    .res 16             ; altura dibujada
SHY:    .res 2              ; y de la nave dibujada por búfer
LHP0:   .res 2              ; HPOS congelados por búfer
LHM0:   .res 2
LHM1:   .res 2
LHM2:   .res 2
LHM3:   .res 2
WREM:   .res 48
RKC:    .res 4              ; fase 3: rocas de la lluvia de escoria (columna, fila, tiempo)
RKR:    .res 4
RKT:    .res 4
OPAT:   .res MAXO           ; patrón de movimiento de la oleada (0 = el propio del enemigo)
sppat:  .res 1              ; patrón de la oleada en curso
sbt:    .res 2              ; temporal del spawner · esperas de la UNIDAD CERO
SDUR:   .res 4              ; efectos: solo se usan los canales 3 y 4
SFRQ:   .res 4
SFST:   .res 4
SVOL:   .res 4
SCTL:   .res 4
SPRI:   .res 4
mplay:  .res 1
msong:  .res 1
mrow:   .res 1
mbarn:  .res 1
malt:   .res 1
mtick:  .res 1
MCI:    .res 4              ; instrumento por canal ($FF = calla)
MCN:    .res 4              ; nota
MCE:    .res 4              ; posición de la envolvente
MCA:    .res 4              ; posición del arpegio
MCF:    .res 4              ; frecuencia del sonido fijo

; ---------------------------------------------------------------
        .segment "INITSEG"
init:   lda PORTB
        ora #$02
        sta PORTB
        rts

; ---------------------------------------------------------------
        .segment "CODE"
        .include "g1data.s"
PMPAGE: .byte >PMA, >PMB
BANK:   .byte 0, 32
; filas de campo cuya DLI prepara una franja (o la vuelta al marcador)

; bloque que sobrevive entre programas del disco (página 5)
PERS    = $0580
P_MAGIC = PERS              ; $56 si el bloque es válido
P_DIF   = PERS+1            ; 0 FÁCIL · 1 NORMAL · 2 HARDCORE
P_CHAIN = PERS+2            ; 1: empezar la fase directamente (viene de la anterior)
P_SCORE = PERS+3            ; 3 bytes
P_LIVES = PERS+6
P_POWER = PERS+7
P_SHLD  = PERS+8
P_HISC  = PERS+9            ; 3 bytes
P_CHEAT = PERS+12
P_DISK  = PERS+13            ; 1 = arrancado del disco (cargador residente en LOADER)
LOADER  = $0710             ; cargador del disco: A = programa (0 intro, 1-5 fases, 6 final)
dif     = P_DIF

; ===============================================================
start:  cld
        lda PORTB           ; XL/XE: BASIC fuera, $A000-$BFFF = RAM
        ora #$02
        sta PORTB
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta AUDCTL
        sta hisc
        sta hisc+1
        sta hisc+2
        sta shown
        sta ready
        sta cheat
        lda P_MAGIC         ; primera carga: dificultad NORMAL
        cmp #$56
        beq @pm
        lda #$56
        sta P_MAGIC
        lda #1
        sta P_DIF
        lda #0
        sta P_CHAIN
        sta P_HISC
        sta P_HISC+1
        sta P_HISC+2
        sta P_CHEAT
        sta P_DISK
@pm:    lda P_HISC
        sta hisc
        lda P_HISC+1
        sta hisc+1
        lda P_HISC+2
        sta hisc+2
        lda P_CHEAT
        sta cheat
        lda #3
        sta SKCTL
        lda #>PMA
        sta PMBASE
        lda #$21            ; players sobre el campo + OR en parejas
        sta GPRIOR
        lda #$5F            ; M0/M1 x4 (disparos), M2/M3 x2 (balas)
        sta SIZEM
        lda #<dli
        sta VDSLST
        lda #>dli
        sta VDSLST+1
        lda #7
        ldy #<vbi
        ldx #>vbi
        jsr SETVBV
        lda #1
        sta trig
        lda P_CHAIN         ; disco: viene de la fase anterior -> directo a la partida
        beq title
        lda #0
        sta P_CHAIN
        lda P_SCORE
        sta score
        lda P_SCORE+1
        sta score+1
        lda P_SCORE+2
        sta score+2
        lda P_LIVES
        sta lives
        lda P_POWER
        sta power
        lda P_SHLD
        sta shield
        lda #0
        sta mdrop
        jsr setdif
        jmp phasego

; ---------------------------------------------------------------
TSHIPY  = 134               ; altura de la nave del título (por debajo de EUROSHOOTER)
title:  jsr sndoff
        lda #0
        sta chk
        sta idlec
        sta idlec+1
        jsr titleline
        jsr difline
        lda #<SCR_TITLE
        ldx #>SCR_TITLE
        jsr showscr
        ; la nave cruza el título (búfer A)
        ldx #10
@sh:    lda SHIP_A_P0,x
        sta PMA+$400+TSHIPY,x
        lda SHIP_A_P1,x
        sta PMA+$500+TSHIPY,x
        dex
        bpl @sh
        lda #0
        sta shipx
@lp:    jsr waitfr
        inc shipx
        lda shipx
        sta LHP0
        ldx #0
@px:    lda shipx
        sta TX0,x
        clc
        adc #4
        sta TX1,x
        inx
        cpx #10
        bne @px
        lda frame
        and #16
        beq @b1
        lda #$0E
        bne @b2
@b1:    lda #$04
@b2:    sta TPF3+7
        lda frame           ; EUROSHOOTER late: la franja cambia de tono (rojo-naranja) y el texto brilla
        lsr a
        lsr a
        and #15
        tay
        lda EUROBG,y
        sta TPF2+8
        lda EUROTX,y
        sta TPF1+8
        ; truco: abajo, abajo (4 s como máximo entre pulsaciones) y FIRE
        lda chkt
        beq @k
        dec chkt
        bne @k
        lda #0
        sta chk
@k:     lda STICK0
        and #2
        bne @up
        lda stkp
        bne @j
        lda #1
        sta stkp
        lda chk
        cmp #2
        bcs @j
        inc chk
        lda #240
        sta chkt
        jmp @j
@up:    lda #0
        sta stkp
@j:     lda STICK0          ; izquierda / derecha: dificultad
        and #12
        cmp #12
        beq @nlr
        ldx stkh
        bne @lr
        inc stkh
        and #4
        bne @rt
        lda dif             ; izquierda
        beq @lr
        dec dif
        jmp @chg
@rt:    lda dif             ; derecha
        cmp #2
        bcs @lr
        inc dif
@chg:   jsr difline
        jsr sfxpick
        jmp @lr
@nlr:   lda #0
        sta stkh
@lr:
        jsr fireedge
        bcs @f
        jmp @lp
@f:     lda chk
        cmp #2
        bne @go
        lda #0
        sta chk
        lda cheat
        eor #1
        sta cheat
        sta P_CHEAT
        jsr titleline
        jsr sfxpick
        jmp @lp
@go:    jmp newgame


; línea del título con la dificultad elegida
difline:
        lda dif
        asl a
        tax
        lda DIFTX,x
        sta src
        lda DIFTX+1,x
        sta src+1
        ldy #39
@c:     lda (src),y
        sta DIFSCR,y
        dey
        bpl @c
        rts
DIFTX:  .word TX_T_DIF0, TX_T_DIF1, TX_T_DIF2

; línea del título: récord o aviso del modo invencible
titleline:
        ldx #39
        lda cheat
        bne @inv
@c:     lda TX_T_HI,x
        sta HISCR,x
        dex
        bpl @c
        lda #<(HISCR+HI_OFS)
        sta dst
        lda #>HISCR
        sta dst+1
        jmp puthi
@inv:   lda TX_T_INV,x
        sta HISCR,x
        dex
        bpl @inv
        rts

; ---------------------------------------------------------------
newgame:
        lda #0
        sta score
        sta score+1
        sta score+2
        sta shield
        sta mdrop
        ldx dif
        lda DLIVES,x
        sta lives
        jsr setdif
        lda #1
.ifdef POTENCIA
        lda #POTENCIA
.endif
        sta power
phasego:
        lda #<SCR_CARD
        ldx #>SCR_CARD
        jsr showscr
        lda #240
        sta tmp+4
@w:     jsr waitfr
        jsr fireedge
        bcs @go
        dec tmp+4
        bne @w
@go:    jsr setgame

; ---------------------------------------------------------------
gloop:  jsr waitfr
        lda frame           ; medida: ¿se pasó del cuadro?
        sec
        sbc lastf
        cmp #2
        bcc @t
        inc lag
@t:     lda frame
        sta lastf
        jsr ship
.if FASE = 2
        jsr corriente
.endif
        jsr shots
        lda state
        cmp #ST_BOSS
        beq @b
        jsr spawner
        lda arena
        beq @n
        jsr bossstart
        jmp @n
@b:     jsr boss
@n:
.if FASE = 3
        jsr geyser
.elseif FASE = 5
        lda state           ; paredes respirantes en el nivel; con el CORAZÓN NULO, el latido de la válvula
        cmp #ST_BOSS
        beq @p5
        jsr geyser
        lda frame
        jsr bkfix
        lda frame
        eor #16
        jsr bkfix
        jmp @d5
@p5:    jsr pulse
@d5:
.elseif FASE = 4
        lda state           ; puertas en el nivel; con SATURNUS, el latido del vacío
        cmp #ST_BOSS
        beq @pu
        jsr door
        jmp @dd
@pu:    jsr pulse
@dd:
.else
        jsr pulse
.endif
        jsr capsule
        jsr objects
        jsr ebull
        jsr collide
        jsr render
        jsr hud
        lda shipst
        cmp #1
        bne @ok
        lda shiptm
        bne @ok
        lda lives
        bne @resp
        jmp gameover
@resp:  lda bst             ; no reaparece entre las placas cerradas
        cmp #4
        beq @ok
        jsr respawn
@ok:    lda bst
        cmp #9
        bne gloop
        jmp cleared

; ===============================================================
waitfr: lda frame
@w:     cmp frame
        beq @w
        rts

fireedge:
        lda STRIG0
        bne @up
        lda trig
        bne @no
        lda #1
        sta trig
        sec
        rts
@up:    lda #0
        sta trig
@no:    clc
        rts

; pantalla fija: A/X = descriptor (DL, tablas, largo DL, entradas)
showscr:
        sta ptr
        stx ptr+1
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        sta gmode
        sta scroll
        jsr waitfr
        jsr clrpm
        jsr clrtab
        lda #0
        sta shown
        sta ready
        sta shipx
        ldx #1
@lh:    sta LHP0,x
        sta LHM0,x
        sta LHM1,x
        sta LHM2,x
        sta LHM3,x
        dex
        bpl @lh
        ldy #0
        lda (ptr),y
        sta src
        iny
        lda (ptr),y
        sta src+1
        iny
        lda (ptr),y
        sta dst
        iny
        lda (ptr),y
        sta dst+1
        iny
        lda (ptr),y
        tax
        iny
        lda (ptr),y
        sta tmp+2
        ldy #0
@dl:    lda (src),y
        sta DLBUF,y
        iny
        dex
        bne @dl
        lda dst
        sta src
        lda dst+1
        sta src+1
        lda #<TB
        sta dst
        lda #>TB
        sta dst+1
        ldx #15
@f:     ldy #0
@fe:    lda (src),y
        sta (dst),y
        iny
        cpy tmp+2
        bne @fe
        lda src
        clc
        adc tmp+2
        sta src
        bcc @f1
        inc src+1
@f1:    lda dst
        clc
        adc #64
        sta dst
        bcc @f2
        inc dst+1
@f2:    dex
        bne @f
        lda #CHHI_FONT
        sta CHBAS
        lda #$2C
        sta COLOR0
        lda #$0C
        sta COLOR1
        lda #0
        sta COLOR2
        sta COLOR4
        lda #$46
        sta COLOR3
        jmp dison

dison:  lda #<DLBUF
        sta SDLSTL
        lda #>DLBUF
        sta SDLSTL+1
        lda #3
        sta GRACTL
        lda #$3E
        sta SDMCTL
        jsr waitfr
        jsr waitfr
        lda #$C0
        sta NMIEN
        rts

clrpm:  lda #0
        tax
@c:     .repeat 16, K
        sta PMA+K*256,x
        .endrepeat
        inx
        bne @c
        rts

clrtab: lda #0
        tax
@c:     sta TB,x
        sta TB+$100,x
        sta TB+$200,x
        sta TB+$2C0,x
        sta TB+$3C0,x
        inx
        bne @c
        rts

; ===============================================================
; DLI: entrada dlin (banco 0 = 0..20, banco 1 = 32..52); una por fila
dli:    pha
        txa
        pha
        ldx dlin
        lda TMODE,x
        bne @full
        lda TBK,x
        sta WSYNC
        sta COLBK
        lda TX2,x
        sta HPOSP2
        lda TX3,x
        sta HPOSP3
        lda TC2,x
        sta COLPM2
        lda TC3,x
        sta COLPM3
        lda TS2,x
        sta SIZEP2
        lda TS3,x
        sta SIZEP3
        inc dlin
        pla
        tax
        pla
        rti
@full:  lda TBK,x
        sta WSYNC
        sta COLBK
        lda TCH,x
        sta CHBASE
        lda TPF0,x
        sta COLPF0
        lda TPF1,x
        sta COLPF1
        lda TPF2,x
        sta COLPF2
        lda TPF3,x
        sta COLPF3
        lda TX0,x
        sta HPOSP0
        lda TX1,x
        sta HPOSP1
        lda TX2,x
        sta HPOSP2
        lda TX3,x
        sta HPOSP3
        lda TC0,x
        sta COLPM0
        lda TC1,x
        sta COLPM1
        lda TC2,x
        sta COLPM2
        lda TC3,x
        sta COLPM3
        lda TS2,x
        sta SIZEP2
        lda TS3,x
        sta SIZEP3
        inc dlin
        pla
        tax
        pla
        rti

; ===============================================================
; VBI diferida: cambia de búfer si hay uno listo; scroll; sonido
vbi:    cld
        lda #0
        sta ATRACT          ; nunca entra el modo atracción
        inc frame
        lda ready
        beq @nr
        lda rb
        sta shown
        lda #0
        sta ready
@nr:    ldx shown
        lda PMPAGE,x
        sta PMBASE
        lda BANK,x
        sta dlin
        lda LHP0,x
        sta HPOSP0
        clc
        adc #4
        sta HPOSP1
        lda #0
        sta HPOSP2
        sta HPOSP3
        lda LHM0,x
        sta HPOSM0
        lda LHM1,x
        sta HPOSM1
        lda LHM2,x
        sta HPOSM2
        lda LHM3,x
        sta HPOSM3
        lda gmode
        beq @snd
        lda scroll
        beq @hs
        lda frame
        and #1
        bne @hs
        inc camx
        bne @c1
        inc camx+1
@c1:    lda camx
        and #3
        bne @hs
        inc coarse
        bne @c2
        inc coarse+1
@c2:    jsr newcol
@hs:    lda camx
        and #3
        sta fine
        eor #3
        sta HSCROL
@snd:   jsr mus
        jsr sound
        jmp XITVBV

; escribe la columna coarse+47 en el anillo y desplaza los 20 LMS
newcol: inc colidx
        bne @i
        inc colidx+1
@i:     lda colidx+1
        cmp #>LEVCOLS
        bcc @w
        beq @lo
        jmp @lms
@lo:    lda colidx
        cmp #<LEVCOLS
        bcc @w
        jmp @lms
@w:     lda colidx
        and #63
        sta vt+1
        .repeat 4, Q
        ldy #0
        lda (mq0+Q*2),y
        tax
        .if Q = 0
        lda QL0,x
        sta colp
        lda QH0,x
        .elseif Q = 1
        lda QL1,x
        sta colp
        lda QH1,x
        .elseif Q = 2
        lda QL2,x
        sta colp
        lda QH2,x
        .else
        lda QL3,x
        sta colp
        lda QH3,x
        .endif
        sta colp+1
        ldx vt+1
        .repeat 5, R
        ldy #R
        lda (colp),y
        sta RING+(Q*5+R)*128,x
        sta RING+(Q*5+R)*128+64,x
        .endrepeat
        inc mq0+Q*2
        bne :+
        inc mq0+Q*2+1
:
        .endrepeat
@lms:   lda coarse
        and #63
        sta vt
        ldx #0
        ldy #8
@l:     txa
        and #1
        beq @e
        lda #128
@e:     clc
        adc vt
        sta DLBUF,y
        sta ROWLL,x
        iny
        iny
        iny
        inx
        cpx #20
        bne @l
        ; ¿llegamos a la arena?
        lda coarse+1
        cmp #>ARENA
        bne @x
        lda coarse
        cmp #<ARENA
        bne @x
        lda #0
        sta scroll
        lda #1
        sta arena
@x:     rts

; ===============================================================
; preparación de la fase
setgame:
        lda #$40
        sta NMIEN
        lda #0
        sta SDMCTL
        jsr waitfr
        jsr clrpm
        jsr clrtab
        lda #0
        ldx #MAXO-1
@o:     sta OT,x
        dex
        bpl @o
        ldx #15
@s:     sta SDY,x
        dex
        bpl @s
        ldx #7
@sl:    sta SLOT,x
        dex
        bpl @sl
        ldx #1
@lh:    sta SHY,x
        sta LHP0,x
        sta LHM0,x
        sta LHM1,x
        sta LHM2,x
        sta LHM3,x
        dex
        bpl @lh
        sta camx
        sta camx+1
        sta coarse
        sta coarse+1
        sta fine
        sta arena
        sta wv
        sta spn
        sta spk
        sta pcap
        sta pcrow
        sta nvt
        sta bst
        sta s0x
        sta sal
        sta e0x
        sta e1x
        sta ready
        sta shown
        sta siren
        sta bassi
        sta lag
        lda #SOLID0_N
        sta solid0
        ; 48 columnas iniciales
        lda #<MAPQ0
        sta mq0
        lda #>MAPQ0
        sta mq0+1
        lda #<MAPQ1
        sta mq1
        lda #>MAPQ1
        sta mq1+1
        lda #<MAPQ2
        sta mq2
        lda #>MAPQ2
        sta mq2+1
        lda #<MAPQ3
        sta mq3
        lda #>MAPQ3
        sta mq3+1
        lda #$FF
        sta colidx
        sta colidx+1
@ic:    jsr newcol
        lda colidx
        cmp #47
        bne @ic
        ; display list: DLI solo donde empieza una franja y en la vuelta al marcador
        ldx #0
        lda #$70
        sta DLBUF,x
        inx
        sta DLBUF,x
        inx
        sta DLBUF,x
        inx
        lda #$C2
        sta DLBUF,x
        inx
        lda #<HUDTOP
        sta DLBUF,x
        inx
        lda #>HUDTOP
        sta DLBUF,x
        inx
        lda #$10
        sta DLBUF,x
        inx
        ldy #0
@dl:    lda #$D4            ; ANTIC 4 + LMS + HSCROL + DLI (degradado fila a fila)
        sta DLBUF,x
        inx
        tya
        and #1
        beq @lo
        lda #128
@lo:    sta DLBUF,x
        sta ROWLL,y
        inx
        tya
        lsr a
        clc
        adc #>RING
        sta DLBUF,x
        sta ROWLH,y
        inx
        iny
        cpy #20
        bne @dl
        lda #$10
        sta DLBUF,x
        inx
        lda #$42
        sta DLBUF,x
        inx
        lda #<HUDBOT
        sta DLBUF,x
        inx
        lda #>HUDBOT
        sta DLBUF,x
        inx
        lda #$41
        sta DLBUF,x
        inx
        lda #<DLBUF
        sta DLBUF,x
        inx
        lda #>DLBUF
        sta DLBUF,x
        ldx #0
        jsr gtab
        ldx #32
        jsr gtab
        jsr hudinit
        lda #CHHI_FONT
        sta CHBAS
        lda #$0E
        sta COLOR1
        lda #$02
        sta COLOR2
        lda #0
        sta COLOR4
        lda #64
        sta shipx
        lda #110
        sta shipy
        lda #2
        sta shipst
        lda #90
        sta shiptm
        lda #ST_PLAY
        sta state
        lda #1
        sta gmode
        sta scroll
        lda #0              ; tema de la fase (musica.py solo monta el de esta fase y el del jefe)
.ifdef TEMA
        lda #TEMA
.endif
        jsr musstart
.ifdef PRUEBACAP
        lda #3
        sta pcap
        lda #170
        sta pcx
        lda #1
        sta pcb
.endif
        jsr render          ; primer cuadro preparado antes de encender
        jmp dison

; tablas de un banco (X = 0 o 32): entrada r = fila r (0 completa), 20 = marcador inferior
gtab:   stx tmp
        ldy #0
@r:     lda BKG,y
        sta TBK,x
        lda #BULCOL
        sta TC2,x
        sta TC3,x
        lda #0
        sta TMODE,x
        inx
        iny
        cpy #20
        bne @r
        lda #BULCOL
        sta TC2,x
        sta TC3,x
        lda #0
        sta TBK,x
        ldx tmp
        lda #1
        sta TMODE,x
        sta TMODE+20,x
        lda #CHHI_NIVEL
        sta TCH,x
        lda #CHHI_FONT
        sta TCH+20,x
        lda PHCOL
        sta TPF0,x
        lda PHCOL+1
        sta TPF1,x
        lda PHCOL+2
        sta TPF2,x
        lda PHCOL+3
        sta TPF3,x
        lda #$0E
        sta TPF1+20,x
        lda #$02
        sta TPF2+20,x
        rts

; luces rojas (PF3): laten cada 16 cuadros; el ojo del jefe manda cuando destella
pulse:  lda eyefl
        beq @p
        lda #$0E
        bne @s
@p:     lda frame
        and #16
        beq @a
        lda PHCOL+4
        bne @s
@a:     lda PHCOL+3
@s:     sta TPF3
        sta TPF3+32
        rts

; ===============================================================
; nave (lógica; se dibuja en render)
ship:   lda shipst
        cmp #1
        bne @alive
        dec shiptm
        rts
@alive: lda STICK0
        lsr a
        bcs @nu
        ldx shipy
        cpx #47
        bcc @nu
        dec shipy
        dec shipy
@nu:    lsr a
        bcs @nd
        ldx shipy
        cpx #189
        bcs @nd
        inc shipy
        inc shipy
@nd:    lsr a
        bcs @nl
        ldx shipx
        cpx #51
        bcc @nl
        dec shipx
        dec shipx
@nl:    lsr a
        bcs @nr
        ldx shipx
        cpx #178
        bcs @nr
        inc shipx
        inc shipx
@nr:    lda shipst
        cmp #2
        bne @r
        dec shiptm
        bne @r
        jsr shipsolid       ; no se vuelve vulnerable dentro de un obstáculo
        bcc @v
        inc shiptm
        rts
@v:     lda #0
        sta shipst
@r:     rts

respawn:
        lda #64
        sta shipx
        ldx #0
@try:   lda RESPY,x
        sta shipy
        jsr shipsolid
        bcc @ok
        inx
        cpx #7
        bne @try
@ok:    lda #2
        sta shipst
        lda #180            ; 3 segundos invulnerable (parpadeando)
        sta shiptm
        lda #0
        sta shield
        lda #1
        sta hudd
        rts
RESPY:  .byte 110,94,126,78,142,62,158

; ===============================================================
; disparos de la nave: LÁSER CÁPSULA de 16 cc x 7 líneas (M0 cola azul + M1 punta blanca)
;   una ráfaga a la vez; los láseres de una ráfaga comparten x (avanzan igual), cada uno con su y
;   P1: un láser · P2: dos en paralelo · P3: tres en abanico
shots:  lda cool
        beq @c0
        dec cool
@c0:    lda s0x
        bne @mv
        jmp @fire
@mv:    clc
        adc #8
        cmp #212
        bcc @in
        jmp @kill
@in:    sta s0x
        lda sfan
        beq @w
        lda s0y             ; abanico: el de arriba sube y el de abajo baja
        sec
        sbc #2
        sta s0y
        cmp #42
        bcs @f1
        lda sal
        and #$FE
        sta sal
@f1:    lda s2y
        clc
        adc #2
        sta s2y
        cmp #202
        bcc @w
        lda sal
        and #$FB
        sta sal
@w:     lda s0x             ; choque con el decorado por la punta
        clc
        adc #14
        sta tmp+2
        lda sal
        and #1
        beq @w1
        lda s0y
        clc
        adc #3
        tay
        lda tmp+2
        jsr solidat
        bcc @w1
        lda sal
        and #$FE
        sta sal
@w1:    lda sal
        and #2
        beq @w2
        lda s1y
        clc
        adc #3
        tay
        lda tmp+2
        jsr solidat
        bcc @w2
        lda sal
        and #$FD
        sta sal
@w2:    lda sal
        and #4
        beq @w3
        lda s2y
        clc
        adc #3
        tay
        lda tmp+2
        jsr solidat
        bcc @w3
        lda sal
        and #$FB
        sta sal
@w3:    lda sal
        bne @x
@kill:  lda #0
        sta s0x
        sta sal
@x:     rts
@fire:  lda shipst
        cmp #1
        beq @x
        lda STRIG0
        bne @x
        lda cool
        bne @x
        lda shipx
        clc
        adc #10
        sta s0x
        lda #5
        sta cool
        lda #0
        sta sfan
        lda shipy
        clc
        adc #2
        sta s1y
        ldx power
        cpx #2
        beq @p2
        bcs @p3
        lda #2              ; P1: el central
        sta sal
        jmp sfxshot
@p2:    lda shipy           ; P2: dos en paralelo
        sec
        sbc #3
        sta s0y
        clc
        adc #10
        sta s2y
        lda #5
        sta sal
        jmp sfxshot
@p3:    lda s1y             ; P3: tres en abanico
        sta s0y
        sta s2y
        lda #1
        sta sfan
        lda #7
        sta sal
        jmp sfxshot

; ===============================================================
; balas enemigas M2 (e0) y M3 (e1): solo lógica
ebull:  lda e0x
        beq @b
        clc
        adc e0dx
        sta e0x
        cmp #40
        bcc @k0
        cmp #216
        bcs @k0
        lda frame
        and #1
        beq @b
        lda e0y
        clc
        adc e0dy
        sta e0y
        cmp #46
        bcc @k0
        cmp #196
        bcc @b
@k0:    lda #0
        sta e0x
@b:     lda e1x
        beq @x
        clc
        adc e1dx
        sta e1x
        cmp #40
        bcc @k1
        cmp #216
        bcs @k1
        lda frame
        and #1
        beq @x
        lda e1y
        clc
        adc e1dy
        sta e1y
        cmp #46
        bcc @k1
        cmp #196
        bcc @x
@k1:    lda #0
        sta e1x
@x:     rts

; dispara bala: A = x, Y = y, X = dy, tmp+3 = dx ; C=1 si no se dispara
; juego justo: no nace a menos de 32 color clocks por delante de la nave
fireb:  sta tmp+2
        sec
        sbc shipx
        bcc @no
        cmp dfair
        bcc @no
        lda tmp+3           ; curva de dificultad (fase y dificultad): balas más o menos rápidas
        sec
        sbc dbulx
        sta tmp+3
        lda e0x
        bne @t1
        lda tmp+2
        sta e0x
        sty e0y
        stx e0dy
        lda tmp+3
        sta e0dx
        clc
        rts
@t1:    lda e1x
        bne @no
        lda tmp+2
        sta e1x
        sty e1y
        stx e1dy
        lda tmp+3
        sta e1dx
        clc
        rts
@no:    sec
        rts

; ===============================================================
; objetos: hueco fijo en una franja
; newobj: A = tipo, X = x, Y = franja -> X = objeto (C=0) o C=1 si no cabe
newobj: sta tmp+5
        stx tmp+6
        sty tmp+4
        ldx #MAXO-1
@f:     lda OT,x
        beq @ok
        dex
        bpl @f
@fail:  sec
        rts
@ok:    ldy tmp+5
        lda OPAIR,y
        php
        lda tmp+4
        asl a
        tay
        plp
        bne @pair
        lda SLOT,y
        beq @g
        iny
        lda SLOT,y
        bne @fail
@g:     txa
        clc
        adc #1
        sta SLOT,y
        tya
        and #1
        sta OP,x
        jmp @init
@pair:  lda SLOT,y
        ora SLOT+1,y
        bne @fail
        txa
        clc
        adc #1
        sta SLOT,y
        sta SLOT+1,y
        lda #2
        sta OP,x
@init:  lda #0
        sta OPAT,x
        lda tmp+5
        sta OT,x
        tay
        lda OHP,y
        beq @hp
        clc                 ; dificultad: -1 / 0 / +1 golpe (mínimo 1)
        adc dhp
        bne @hp
        lda #1
@hp:    sta OH,x
        lda tmp+6
        sta OX,x
        ldy tmp+4
        tya
        sta OB,x
        lda BTOP,y
        sta OBT,x
        sta OY,x
        lda #0
        sta OS,x
        sta OTM,x
        lda #$FF
        sta OW,x
        lda #1
        sta ODY,x
        lda #$FE
        sta ODX,x
        clc
        rts

; newobjy: igual pero con Y = línea; elige la franja y coloca dentro de ella
newobjy:
        sty tmp+1
        pha
        tya
        sec
        sbc #59
        bcs @p
        lda #0
@p:     lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        cmp #4
        bcc @b
        lda #3
@b:     tay
        pla
        jsr newobj
        bcs @r
        lda tmp+1
        sec
        sbc OBT,x
        bcc @top
        cmp #21
        bcc @in
        lda #20
        bne @in
@top:   lda #0
@in:    clc
        adc OBT,x
        sta OY,x
        clc
@r:     rts

; libera el objeto X y su hueco
freeobj:
        lda #0
        sta OT,x
        txa
        clc
        adc #1
        ldy #7
@l:     cmp SLOT,y
        bne @n
        pha
        lda #0
        sta SLOT,y
        pla
@n:     dey
        bpl @l
        rts

; oleadas: alterna entre su franja y la vecina; si no hay hueco, espera
spawner:
        lda spn
        bne *+5
        jmp @nw
        dec spt
        bne @x
        lda spk
        and #1
        bne @alt
        ldy spb
        jsr @try
        bcs *+5
        jmp @ok
        ldy spb2
        jsr @try
        bcs *+5
        jmp @ok
        jmp @wait
@alt:   ldy spb2
        jsr @try
        bcs *+5
        jmp @ok
        ldy spb
        jsr @try
        bcs *+5
        jmp @ok
@wait:  lda #1
        sta spt
        lda sptyp           ; UNIDAD CERO sin sitio: lo vuelve a mirar cada 8 cuadros y,
        cmp #8              ; si en unos 5 s no lo encuentra, esa oleada se pierde
        bne @x
        lda #8
        sta spt
        inc sbt+1
        lda sbt+1
        cmp #40
        bcc @x
        lda #0
        sta spn
        sta sbt+1
@x:     rts
@try:   lda sptyp
        cmp #8              ; UNIDAD CERO: de uno en uno
        bne @t
        ldx #MAXO-1
@m:     lda OT,x
        cmp #8
        beq @busy
        dex
        bpl @m
        sty sbt             ; y solo donde haya sitio libre de decorado y se le pueda disparar
        jsr ucfree
        bcc @uok
        ldy #3
@ub:    sty sbt
        jsr ucfree
        bcc @uok
        ldy sbt
        dey
        bpl @ub
        bmi @busy
@uok:   ldy sbt
        lda #8
        ldx #212
        jmp newobj
@t:     lda sppat
        cmp #1
        bne @t3
        sty sbt             ; POR DETRÁS: nunca en la franja de la nave
        jsr shipband
        cmp sbt
        beq @busy
        cpx sbt
        beq @busy
        ldy sbt
        lda sptyp
        ldx #38
        jmp newobj
@t3:    lda sptyp
        ldx #212
        jmp newobj
@busy:  sec
        rts
@ok:    lda spw
        sta OW,x
        lda sppat
        beq @k0
        sta OPAT,x
        lda OBT,x           ; los patrones empiezan a media franja
        clc
        adc #10
        sta OY,x
        lda #0
        sta OS,x
        sta OTM,x
        lda spk             ; PATRULLA: se plantan escalonados
        and #3
        sta sbt
        asl a
        asl a
        asl a
        asl a
        sec
        sbc sbt
        sbc sbt
        eor #$FF
        clc
        adc #193            ; 192 - 14*k
        sta ODX,x
@k0:    lda OT,x
        cmp #8
        bne @k
        lda #168
        sta ODX,x           ; UNIDAD CERO: x donde se para
        lda #0
        sta ODY,x           ; disparos hechos
@k:     inc spk
        dec spn
        lda spgap
        sta spt
        rts
@nw:    ldx wv
        cpx #NWAVES
        bcc *+5
        jmp @x
        lda coarse+1
        cmp WVCH,x
        bcs *+5
        jmp @x
        bne @go
        lda coarse
        cmp WVCL,x
        bcs *+5
        jmp @x
@go:    lda #0
        sta sbt+1
        lda WVPAT,x
        sta sppat
        lda WVTYP,x
        sta sptyp
        lda WVN,x
        sta spn
        sta WREM,x
        lda WVB,x
        sta spb
        lda WVB2,x
        sta spb2
        lda WVGAP,x
        cmp #2
        bcc @g
        ldy dif
        beq @ez
        cpy #2
        bne @g
        sta tmp             ; HARDCORE: un octavo menos
        lsr a
        lsr a
        lsr a
        eor #$FF
        sec
        adc tmp
        jmp @g
@ez:    sta tmp             ; FÁCIL: un cuarto más
        lsr a
        lsr a
        clc
        adc tmp
@g:     sta spgap
        stx spw
        lda #1
        sta spt
        lda #0
        sta spk
        inc wv
        rts

; cápsula pendiente: espera a una franja entera libre
capsule:
.ifdef PRUEBACAP2
        lda pcap
        bne @d0
        lda frame
        and #127
        bne @d0
        lda #3
        sta pcap
        lda $D20A
        and #127
        adc #60
        sta pcx
        lda $D20A
        and #3
        sta pcb
@d0:
.endif
        lda pcap
        beq @r
        lda shipx           ; siempre por delante de la nave (40 color clocks como mínimo)
        clc
        adc #40
        cmp pcx
        bcc @t0
        sta pcx
@t0:    lda pcx             ; y nunca más allá del borde derecho; si no hay sitio libre
        cmp #200            ; (nunca nace dentro ni cerca de un obstáculo) espera quieta en pantalla
        bcc @t
        lda #196
        sta pcx
@t:     lda pcx
        cmp #48
        bcs @t2
        lda #48
        sta pcx
@t2:    lda shipy           ; primero la franja donde está la nave
        clc
        adc #5
        sec
        sbc #59
        bcs @sb
        lda #0
@sb:    lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        cmp #4
        bcc @sb2
        lda #3
@sb2:   sta tmp+7           ; la búsqueda es cara: una fila de 6 puntos por cuadro (5 filas por franja)
        lda pcrow
        bne @go
        lda frame           ; nueva búsqueda: la franja de la nave, o las demás por turno
        and #4
        beq @sh
        lda frame
        lsr a
        lsr a
        lsr a
        and #3
        sta tmp+7
@sh:    lda tmp+7
        sta pcbt
@go:    ldy pcbt
        jsr caprow
        bcs @rst
        inc pcrow
        lda pcrow
        cmp #5
        bcc @r
        lda #0
        sta pcrow
        ldy pcbt
        lda pcap
        ldx pcx
        jsr newobj
        bcc @ok
        rts
@rst:   lda #0
        sta pcrow
@r:     rts
@ok:    lda OBT,x
        clc
        adc #10
        sta OY,x
        lda #0
        sta pcap
        rts

; ¿cabe una cápsula en la franja Y con x = pcx, con margen alrededor? C = 0 libre
;   6 x 5 puntos: x-6 .. x+14 cada 4 · y = arriba-6 .. abajo+7 cada 6 (la cápsula ocupa BTOP+10 .. +21)
caprow: lda pcrow           ; una fila (la pcrow) de la rejilla de capfree
        asl a
        adc pcrow
        asl a
        adc BTOP,y
        adc #4
        sta tmp+1
        lda #1
        sta tmp+2
        bne capf2
capfree:
        lda BTOP,y
        clc
        adc #4
        sta tmp+1
        lda #5
        sta tmp+2
capf2:
@fy:    lda pcx
        sec
        sbc #6
        sta tmp
        lda #6
        sta tmp+3
@fx:    lda tmp
        cmp #212
        bcs @nx
        ldy tmp+1
        jsr solidat
        bcs @busy
@nx:    lda tmp
        clc
        adc #4
        sta tmp
        dec tmp+3
        bne @fx
        lda tmp+1
        clc
        adc #6
        sta tmp+1
        dec tmp+2
        bne @fy
        clc
        rts
@busy:  sec
        rts

objects:
.if FASE = 5
        lda npar            ; el aviso de los parásitos se apaga solo si ya no queda ninguno
        beq @np
        dec npar
@np:
.endif
        ldx #MAXO-1
@l:     lda OT,x
        beq @nx
        ldy OPAT,x          ; oleada con patrón propio
        beq @nop
        jsr opat
        jmp @nx
@nop:   cmp #1
        bne @t2
        jsr ENEM1
        jmp @nx
@t2:    cmp #2
        bne @t8
        jsr ENEM2
        jmp @nx
@t8:    cmp #8
        bne @t9
        jsr orem
        jmp @nx
@t9:    cmp #9
        bne @ta
        jsr ENEM9
        jmp @nx
@ta:
.if FASE >= 4
        cmp #10
        bne @tb
        jsr ENEM10
        jmp @nx
@tb:    cmp #11
        bne @t5
        jsr onod
        jmp @nx
.endif
@t5:    cmp #5
        bne @t4
        inc OTM,x
        lda OTM,x
        cmp #18
        bcc @nx
        jsr freeobj
        jmp @nx
@t4:    cmp #6
        bcs @mv
        lda frame           ; cápsulas: van con el decorado
        and #1
        bne @nx
        dec OX,x
        lda OX,x
        cmp #36
        bcs @nx
        jsr freeobj
        jmp @nx
@mv:    jsr omove
@nx:    dex
        bpl @l
        rts

.if FASE = 1
; CARROÑERO (antes RECORTADOR): entra, arco dentro de su franja, quiebra y regresa
orec:   inc OTM,x
        lda OS,x
        bne @back
        lda OX,x
        sec
        sbc #2
        sta OX,x
        lda OTM,x
        and #63
        tay
        lda OBT,x
        clc
        adc ARC,y
        sta OY,x
        lda OTM,x
        cmp #62
        bcs @turn
        lda OX,x
        cmp #84
        bcs @r
@turn:  lda #1
        sta OS,x
@r:     rts
@back:  lda OX,x
        clc
        adc #3
        sta OX,x
        cmp #216
        bcc @r
        jmp escaped

; CHATARRÍN: zigzag dentro de su franja
ocha:   dec OX,x
        lda frame
        and #1
        beq @a
        dec OX,x
@a:     inc OTM,x
        lda OTM,x
        and #63
        tay
        lda OBT,x
        clc
        adc ZIG,y
        sta OY,x
        lda OX,x
        cmp #36
        bcs @r
        jmp escaped
@r:     rts

.endif
; UNIDAD CERO (mecha): entra, flota en su franja, avisa (destello) y dispara apuntando; 3 veces y se va
orem:   lda frame           ; flota: 0..6 líneas dentro de su franja
        lsr a
        lsr a
        lsr a
        and #7
        tay
        lda OBT,x
        clc
        adc BOB,y
        sta OY,x
        lda OS,x
        bne @s1
        dec OX,x            ; 0: entra
        lda OX,x
        cmp ODX,x
        bcs @r
        lda #1
        sta OS,x
        lda #0
        sta OTM,x
@r:     rts
@s1:    cmp #4
        beq @leave
        lda frame           ; el decorado se le echa encima: se marcha antes
        and #7
        bne @nb
        jsr ucblk
        bcc @nb
        lda #4
        sta OS,x
        rts
@nb:    inc OTM,x
        lda OTM,x
        cmp duzw
        bcc @r
        ; dispara hacia la nave
        stx tmp+7
        lda #$FD
        sta tmp+3
        lda OY,x
        clc
        adc #7
        tay
        sty tmp+1
        ldx #0
        lda shipy
        clc
        adc #5
        cmp tmp+1
        beq @f
        ldx #1
        bcs @f
        ldx #$FF
@f:     lda tmp+7
        tay
        lda OX,y
        ldy tmp+1
        jsr fireb
        ldx tmp+7
        bcs @r              ; sin hueco o demasiado cerca: sigue avisando
        jsr sfxtur
        lda #0
        sta OTM,x
        inc ODY,x
        lda ODY,x
        cmp #3
        bcc @r
        lda #4
        sta OS,x
        rts
@leave: dec OX,x
        lda frame
        and #1
        beq @l2
        dec OX,x
@l2:    lda OX,x
        cmp #36
        bcs @r
        jmp escaped
BOB:    .byte 0,1,2,3,4,3,2,1

;  UNIDAD CERO: ¿franja Y libre? (sin decorado donde se planta y con línea de tiro desde la nave) C=1 si no
ucfree: lda BTOP,y
        sta tmp+2
        ldx #11
@p:     lda UCPY,x
        clc
        adc tmp+2
        tay
        lda UCPX,x
        jsr solidat
        bcs @r
        dex
        bpl @p
        clc
@r:     rts
UCPX:   .byte 164,180,196,164,180,196,164,180,196, 96,124,150
UCPY:   .byte 1,1,1,11,11,11,21,21,21, 11,11,11
; UNIDAD CERO X en vuelo: ¿decorado delante o encima? C=1 si sí (conserva X)
ucblk:  stx tmp+7
        lda OY,x
        clc
        adc #3
        tay
        lda OX,x
        clc
        adc #24
        jsr solidat
        bcs @r
        ldx tmp+7
        lda OY,x
        clc
        adc #16
        tay
        lda OX,x
        clc
        adc #24
        jsr solidat
        bcs @r
        ldx tmp+7
        lda OY,x
        clc
        adc #10
        tay
        lda OX,x
        clc
        adc #8
        jsr solidat
@r:     ldx tmp+7
        rts
; franjas de la nave: A = la de arriba, X = la de abajo
shipband:
        lda shipy
        jsr @b
        tax
        lda shipy
        clc
        adc #12
        jsr @b
        pha
        txa
        tay
        pla
        tax
        tya
        rts
@b:     sec
        sbc #59
        bcs @p
        lda #0
@p:     lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        cmp #4
        bcc @x
        lda #3
@x:     rts

; ---------------------------------------------------------------
; PATRONES de oleada: sustituyen al movimiento propio del enemigo (el aspecto y la vida siguen siendo los suyos)
;   1 POR DETRÁS · 2 BUCLE · 3 PATRULLA · 4 CARGA · 5 ESCALERA
opat:   cpy #1
        bne @p2
        jmp pdet
@p2:    cpy #2
        bne @p3
        jmp pbuc
@p3:    cpy #3
        bne @p4
        jmp ppat
@p4:    cpy #4
        bne @p5
        jmp pcar
@p5:    jmp pesc

; POR DETRÁS: entra por la izquierda, adelanta a la nave, se gira y le dispara antes de salir por la derecha
pdet:   inc OTM,x
        lda OX,x
        clc
        adc #2
        sta OX,x
        cmp #214
        bcs @out
        lda OTM,x
        lsr a
        lsr a
        and #31
        tay
        lda OBT,x
        clc
        adc MSIN,y
        clc
        adc #4
        sta OY,x
        lda OS,x
        bne @r
        lda OX,x
        cmp #160
        bcc @r
        inc OS,x
        jmp aimshot
@out:   jmp escaped
@r:     rts

; BUCLE: avanza, da una vuelta completa dentro de su franja (disparando a media vuelta) y sigue
pbuc:   lda OS,x
        cmp #1
        beq @loop
        lda OX,x
        sec
        sbc #2
        sta OX,x
        cmp #36
        bcc @out
        lda OS,x
        bne @r
        lda OX,x
        cmp #150
        bcs @r
        lda #1
        sta OS,x
        lda OX,x
        sec
        sbc #20
        sta ODX,x           ; centro de la vuelta
        lda #0
        sta OTM,x
@r:     rts
@out:   jmp escaped
@loop:  ldy OTM,x
        lda ODX,x
        clc
        adc CIRX,y
        sta OX,x
        lda OBT,x
        clc
        adc CIRY,y
        sta OY,x
        cpy #32
        bne @nf
        jsr aimshot
@nf:    inc OTM,x
        lda OTM,x
        cmp #64
        bcc @r
        lda #2
        sta OS,x
        rts

; PATRULLA: entra, se planta (escalonados), sube y baja por su franja, dispara dos veces y se retira por la derecha
ppat:   lda OS,x
        bne @h
        dec OX,x
        dec OX,x
        lda OX,x
        cmp ODX,x
        bcs @r
        lda #1
        sta OS,x
        lda #0
        sta OTM,x
@r:     rts
@h:     cmp #2
        beq @back
        inc OTM,x
        lda OTM,x
        and #63
        tay
        lda OBT,x
        clc
        adc ZIG,y
        sta OY,x
        lda OTM,x
        cmp #48
        beq @s
        cmp #128
        beq @s
        cmp #176
        bcc @r
        lda #2
        sta OS,x
        rts
@s:     jmp aimshot
@back:  lda OX,x
        clc
        adc #2
        sta OX,x
        cmp #214
        bcc @r
        jmp escaped

; CARGA: entra despacio, se para, tiembla mientras se alinea con la nave (aviso) y embiste en línea recta
pcar:   lda OS,x
        bne @w
        dec OX,x
        lda OX,x
        cmp #184
        bcs @r
        inc OS,x
        lda #0
        sta OTM,x
@r:     rts
@w:     cmp #2
        beq @go
        inc OTM,x
        lda OTM,x
        and #2
        lsr a
        clc
        adc #183
        sta OX,x
        lda shipy           ; se alinea con la nave sin salir de su franja
        sec
        sbc OBT,x
        bcs @a
        lda #0
@a:     cmp #21
        bcc @b
        lda #20
@b:     clc
        adc OBT,x
        cmp OY,x
        beq @c
        bcc @up
        inc OY,x
        bne @c
@up:    dec OY,x
@c:     lda OTM,x
        cmp #44
        bcc @r
        lda #2
        sta OS,x
        jmp sfxtur
@go:    lda OX,x
        sec
        sbc #4
        sta OX,x
        cmp #36
        bcs @r
        jmp escaped

; ESCALERA: avanza a saltos de altura dentro de su franja
pesc:   inc OTM,x
        lda OTM,x
        and #1
        bne @y
        dec OX,x
@y:     dec OX,x
        lda OX,x
        cmp #36
        bcs @s
        jmp escaped
@s:     lda OTM,x
        and #15
        bne @r
        lda OTM,x
        lsr a
        lsr a
        lsr a
        lsr a
        and #3
        tay
        lda OBT,x
        clc
        adc STEPY,y
        sta OY,x
        lda OTM,x
        and #63
        cmp #48
        bne @r
        jmp aimshot
@r:     rts
STEPY:  .byte 0,10,20,10

; dispara una bala apuntada desde el objeto X (lo conserva)
aimshot:
        stx tmp+7
        lda #$FE
        sta tmp+3
        lda OY,x
        clc
        adc #6
        tay
        sty tmp+1
        ldx #0
        lda shipy
        clc
        adc #5
        cmp tmp+1
        beq @g
        ldx #1
        bcs @g
        ldx #$FF
@g:     ldy tmp+7
        lda OX,y
        ldy tmp+1
        jsr fireb
        ldx tmp+7
        rts

; orbe / chatarra del jefe: dentro de su franja
omove:  lda OX,x
        clc
        adc ODX,x
        sta OX,x
        cmp #36
        bcc @k
        lda frame
        and #3
        bne @r
        lda OY,x
        clc
        adc ODY,x
        sec
        sbc OBT,x
        cmp #21
        bcs @r
        adc OBT,x
        sta OY,x
@r:     rts
@k:     jmp freeobj

.if FASE = 2
; ===============================================================
; FASE 2 · enemigos propios (también se montan en la fase 1, sin usarse)
; MEDUSA DE VACÍO: deriva despacio con vaivén en seno dentro de su franja; suelta una esfera lenta
omed:   inc OTM,x
        lda OTM,x
        and #1
        bne @y
        dec OX,x
@y:     lda OTM,x
        lsr a
        lsr a
        and #31
        tay
        lda OBT,x
        clc
        adc MSIN,y
        sta OY,x
        lda OX,x
        cmp #36
        bcs @f
        jmp escaped
@f:     lda OTM,x
        and #127
        cmp #64
        bne @r
        lda OX,x
        cmp #120            ; solo dispara con espacio delante de la nave
        bcc @r
        stx tmp+7
        lda #$FE            ; esfera lenta
        sta tmp+3
        lda OY,x
        clc
        adc #6
        tay
        sty tmp+1
        ldx #0
        lda shipy
        clc
        adc #5
        cmp tmp+1
        beq @g
        ldx #1
        bcs @g
        ldx #$FF
@g:     lda tmp+7
        tay
        lda OX,y
        ldy tmp+1
        jsr fireb
        ldx tmp+7
@r:     rts

; RAYA FOTÓNICA (manta): entra en arco, cruza la pantalla y sale
oman:   inc OTM,x
        lda OX,x
        sec
        sbc #2
        sta OX,x
        cmp #36
        bcc @k
        lda OTM,x
        and #63
        tay
        lda OBT,x
        clc
        adc ARC,y
        sta OY,x
        rts
@k:     jmp escaped

; ANGUILA DE MAREA: ruta fija ondulante (1,5 píxeles por cuadro)
oang:   inc OTM,x
        lda OTM,x
        and #1
        beq @a
        dec OX,x
@a:     dec OX,x
        lda OTM,x
        and #63
        tay
        lda OBT,x
        clc
        adc WAVE,y
        sta OY,x
        lda OX,x
        cmp #36
        bcs @r
        jmp escaped
@r:     rts

.endif
.if FASE = 2
; corrientes de la tormenta gravitacional (columnas 480-719): empujan medio píxel por cuadro,
; arriba o abajo según el tramo; la nave mueve 2 por cuadro, así que siempre se puede vencer
corriente:
        lda coarse
        sec
        sbc #<480
        lda coarse+1
        sbc #>480
        bcc @r
        lda coarse
        sec
        sbc #<720
        lda coarse+1
        sbc #>720
        bcs @r
        lda shipst
        cmp #1
        beq @r
        lda frame
        and #1
        bne @r
        lda coarse
        and #32
        beq @dn
        lda shipy
        cmp #48
        bcc @r
        dec shipy
        rts
@dn:    lda shipy
        cmp #188
        bcs @r
        inc shipy
@r:     rts
.endif

.if FASE = 3
; ===============================================================
; FASE 3 · enemigos propios
; ASCORIA: roca que deriva despacio; a mitad de camino se abre y suelta dos fragmentos (arriba y abajo)
oasc:   inc OTM,x
        lda OTM,x
        and #1
        bne @m
        dec OX,x
@m:     dec OX,x
        lda OX,x
        cmp #36
        bcs @f
        jmp escaped
@f:     lda OTM,x
        cmp #60
        bne @r
        lda OX,x
        cmp #110            ; solo con espacio delante de la nave
        bcc @r
        stx tmp+7
        lda #$FE
        sta tmp+3
        lda OY,x
        tay
        sty tmp+1
        lda OX,x
        ldx #$FF
        jsr fireb
        ldx tmp+7
        lda #$FE
        sta tmp+3
        lda OY,x
        clc
        adc #6
        tay
        lda OX,x
        ldx #1
        jsr fireb
        ldx tmp+7
@r:     rts

; SERAFÍN NEGRO: vuelo en S, dispara una vez apuntando y se retira hacia la derecha
oser:   inc OTM,x
        lda OTM,x
        cmp #110
        bcs @back
        lda OX,x
        sec
        sbc #2
        sta OX,x
        cmp #36
        bcs @y
        jmp escaped
@y:     lda OTM,x
        and #63
        tay
        lda OBT,x
        clc
        adc WAVE,y
        sta OY,x
        lda OTM,x
        cmp #36             ; dispara dos veces apuntando
        beq @sh
        cmp #76
        bne @r
@sh:    lda OX,x
        cmp #110
        bcc @r
        stx tmp+7
        lda #$FD
        sta tmp+3
        lda OY,x
        clc
        adc #4
        sta tmp+1
        ldx #0
        lda shipy
        clc
        adc #5
        cmp tmp+1
        beq @g
        ldx #1
        bcs @g
        ldx #$FF
@g:     ldy tmp+7
        lda OX,y
        ldy tmp+1
        jsr fireb
        ldx tmp+7
@r:     rts
@back:  lda OX,x
        clc
        adc #3
        sta OX,x
        cmp #212
        bcc @r
        jmp escaped

; MÁRTIR DE PLASMA: se materializa (color que sube), espera y cruza en línea recta deprisa
omar:   inc OTM,x
        lda OTM,x
        cmp #48
        bcs @go
        lda OX,x            ; se acerca despacio mientras se materializa
        cmp #170
        bcc @r
        dec OX,x
@r:     rts
@go:    lda OX,x
        sec
        sbc #4
        sta OX,x
        cmp #36
        bcs @r
        jmp escaped

.endif
.if FASE = 3 .or FASE = 5
.if FASE = 3
GYC0 = $22
GYC1 = $2C
GYC2 = $3E
GYC3 = $1E
.else
GYC0 = $44                  ; pared respirante: relajada (carne) · avisando · contraída (rosa y blanco que vibran)
GYC1 = $4A
GYC2 = $4E
GYC3 = $0E
.endif
; GÉISERES: dormidos (brasa), aviso (amarillo que parpadea), erupción (fuego blanco): matan solo en erupción
geyser: inc gtm             ; ciclo de 160 cuadros (2,7 s): 64 dormido · 48 aviso · 48 erupción
        lda gtm
        cmp #160
        bcc @g
        lda #0
        sta gtm
@g:     cmp #64
        bcs @hot
        lda #GYC0
        ldx #0
        beq @set
@hot:   cmp #112
        bcs @erup
        ldx #0
        and #8
        beq @w0
        lda #GYC1
        bne @set
@w0:    lda #GYC0
        bne @set
@erup:  ldx #1
        and #4
        beq @e0
        lda #GYC2
        bne @set
@e0:    lda #GYC3
@set:   sta TPF3
        sta TPF3+32
        txa
        bne gcoll
        rts
.endif
.if FASE >= 3
; choque de la nave con los tramos activos (fuego de géiser o rejilla de puerta)
gcoll:
.ifdef PRUEBA
@x:     rts
.else
        lda cheat
        bne @x
        lda shipst
        bne @x
        ldx #NGEY-1
@l:     lda GEYCL,x
        sec
        sbc coarse
        sta tmp
        lda GEYCH,x
        sbc coarse+1
        bne @n
        lda tmp
        cmp #46
        bcs @n
        asl a
        asl a
        clc
        adc #35
        sec
        sbc fine
        sta tmp             ; x del fuego
        lda shipx
        clc
        adc #9
        cmp tmp
        bcc @n
        lda tmp
        clc
        adc #7
        sec
        sbc #2
        cmp shipx
        bcc @n
        lda shipy
        clc
        adc #8
        cmp GEYY0,x
        bcc @n
        lda GEYY1,x
        sec
        sbc #2
        cmp shipy
        bcc @n
        jmp hitship
@n:     dex
        bpl @l
@x:     rts
.endif

.endif
.if FASE >= 4
.if FASE = 4
ESCWARN = 30                ; cuadros de aviso de la raya del ESCRIBA antes del pulso
.else
ESCWARN = 24                ; fase 5: los escribas avisan menos
.endif
; una fila por cuadro (cada 32 cuadros todas): si ninguna ESCRIBA está marcando esa fila, se repone su fondo
bkfix:  and #31
        cmp #20
        bcs @r
        tay
        ldx #MAXO-1
@l:     lda OT,x
        cmp #10
        bne @n
        lda OS,x
        cmp #1
        bne @n
        tya
        cmp ODY,x
        beq @r
@n:     dex
        bpl @l
        lda BKG,y
        sta TBK,y
        sta TBK+32,y
@r:     rts

; dispara apuntando a la nave desde el objeto X: A = línea (sobre OY), tmp+3 = dx · conserva X
aimfx:  stx tmp+7
        clc
        adc OY,x
        tay
        sty tmp+1
        ldx #0
        lda shipy
        clc
        adc #5
        cmp tmp+1
        beq @f
        ldx #1
        bcs @f
        ldx #$FF
@f:     lda tmp+7
        tay
        lda OX,y
        ldy tmp+1
        jsr fireb
        ldx tmp+7
        rts

; ESCRIBA: entra, se planta, marca su raya (la fila de fondo destella) y la raya se convierte en un PULSO DE LUZ:
; la fila entera arde en blanco y mata todo lo que esté en ella por delante del escriba. No dispara balas.
oesc:   lda OS,x
        bne @s1
        dec OX,x
        dec OX,x
        dec OX,x
        lda OX,x
        cmp #184
        bcs @r
        lda #1
        sta OS,x
        lda #0
        sta OTM,x
        lda OY,x            ; fila de la raya: la de su línea central
        sec
        sbc #35
        lsr a
        lsr a
        lsr a
        sta ODY,x
@r:     rts
@s1:    cmp #1
        bne @go
        inc OTM,x
        ldy ODY,x
        lda OTM,x
        cmp descw
        bcs @beam
        lda frame           ; aviso: la raya parpadea en violeta claro
        and #4
        beq @bk
        lda #$58
        bne @st
@bk:    lda BKG,y
@st:    sta TBK,y
        sta TBK+32,y
        rts
@beam:  cmp descw1
        bne @b1
        jsr sfxtur
@b1:    lda frame           ; pulso: blanco que vibra
        and #2
        beq @w0
        lda #$0E
        bne @w1
@w0:    lda #$9E
@w1:    sta TBK,y
        sta TBK+32,y
        tya                 ; ¿la nave está en la fila y por delante?
        asl a
        asl a
        asl a
        clc
        adc #42
        sta tmp             ; primera línea de la fila
        lda shipy
        clc
        adc #7
        cmp tmp
        bcc @nb
        lda tmp
        clc
        adc #6
        cmp shipy
        bcc @nb
        lda shipx
        cmp OX,x
        bcs @nb
        txa
        pha
        jsr hitship
        pla
        tax
@nb:    lda OTM,x
        cmp descw14
        bcc @r
        jsr escbk
        lda #2
        sta OS,x
        lda #0
        sta OTM,x
        rts
@go:    inc OTM,x
        lda OTM,x
        cmp #24
        bcs *+5
        jmp @r
        lda OX,x            ; se retira por la derecha
        clc
        adc #2
        sta OX,x
        cmp #214
        bcs *+5
        jmp @r
        jmp escaped
; repone el fondo de la raya del escriba X
escbk:  ldy ODY,x
        lda BKG,y
        sta TBK,y
        sta TBK+32,y
        rts
.endif

.if FASE = 4
dnod  = gtm                 ; nodos ya colocados para la puerta en pantalla (bits 0 y 1)
dkill = lane                ; nodos destruidos de esa puerta (2 = abierta)
vcnt  = mdrop               ; vasos rotos (cada tercero suelta cápsula)

; PUERTA CEREMONIAL: la rejilla de rayos se enciende y se apaga; se pasa cuando está apagada
; (la compuerta del medio queda siempre libre). Ya no tiene nodos que destruir.
door:   lda frame
        jsr bkfix
        lda frame
        eor #16
        jsr bkfix
        ldx #NGEY-1
@f:     lda GEYCL,x
        sec
        sbc coarse
        sta tmp
        lda GEYCH,x
        sbc coarse+1
        bne @nf
        lda tmp
        cmp #46
        bcc @fd
@nf:    dex
        bpl @f
        lda #0              ; ninguna puerta a la vista
        sta dkill
        sta dnod
        rts
@fd:    ; PUERTA DE RAYOS intermitente (ciclo de 128): encendida 56 cuadros, apagada 48 y aviso de 24
        lda frame
        and #$7F
        cmp #56
        bcc @on
        cmp #104
        bcc @off
        lda frame           ; aviso: parpadeo rápido (todavía no mata)
        and #4
        beq @off
        lda #$BA
        sta TPF3
        sta TPF3+32
        rts
@off:   lda #$62            ; apagada: queda un rastro violeta, no mata
        sta TPF3
        sta TPF3+32
        rts
@on:    lda frame
        and #8
        beq @c0
        lda #$CE
        bne @c1
@c0:    lda #$BA
@c1:    sta TPF3
        sta TPF3+32
        jmp gcoll

; NODO de jade: quieto, va con el decorado
onod:   lda frame
        and #1
        bne @r
        dec OX,x
        lda OX,x
        cmp #36
        bcs @r
        jmp freeobj
@r:     rts

; ACÓLITO DE SATURNO: entra deprisa, se detiene (más o menos lejos según su franja), se carga
; destellando y suelta un disparo lento apuntado; después huye hacia la izquierda
oaco:   inc OTM,x
        lda frame
        lsr a
        lsr a
        lsr a
        and #7
        tay
        lda OBT,x
        clc
        adc BOB,y
        adc #6
        sta OY,x
        lda OS,x
        bne @s1
        dec OX,x
        dec OX,x
        lda OB,x
        asl a
        asl a
        asl a
        adc #136
        cmp OX,x
        bcc @r
        lda #1
        sta OS,x
        lda #0
        sta OTM,x
@r:     rts
@s1:    cmp #1
        bne @go
        lda OTM,x
        cmp #36
        bcc @r
        lda #$FE
        sta tmp+3
        lda #4
        jsr aimfx
        lda #2              ; dispare o no (nave encima), se va
        sta OS,x
        rts
@go:    lda OX,x
        sec
        sbc #3
        sta OX,x
        cmp #36
        bcs @r
        jmp escaped

; GUARDIÁN DEL SELLO: armadura pesada que cruza en arco
ogua:   inc OTM,x
        lda OX,x
        sec
        sbc #2
        sta OX,x
        cmp #36
        bcc @k
        lda OTM,x
        and #63
        tay
        lda OBT,x
        clc
        adc ARC,y
        sta OY,x
        rts
@k:     jmp escaped

; VASO CANÓPICO: deriva meciéndose; roto suelta cápsula (uno de cada tres) o un alma que te busca, nunca las dos
ovas:   inc OTM,x
        dec OX,x
        lda OTM,x
        lsr a
        lsr a
        and #31
        tay
        lda OBT,x
        clc
        adc MSIN,y
        sta OY,x
        lda OX,x
        cmp #36
        bcs @r
        jmp escaped
@r:     rts

.endif

.if FASE = 5
; GLÓBULO CAZADOR: cada 32 cuadros memoriza dónde estaba la nave y va hacia allí despacio (no corrige cada cuadro);
; dispara apuntando (el doble de a menudo si hay un NODO PARÁSITO vivo)
oglo:   inc OTM,x
        lda OTM,x
        and #1
        bne @m
        dec OX,x
@m:     dec OX,x
        lda OX,x
        cmp #36
        bcs @a
        jmp escaped
@a:     lda OTM,x
        and #31
        bne @mv
        lda shipy
        sec
        sbc #2
        sta ODY,x
@mv:    lda frame
        and #1
        bne @f
        lda ODY,x
        cmp OBT,x
        bcs @t1
        lda OBT,x
@t1:    sta tmp
        lda OBT,x
        clc
        adc #20
        cmp tmp
        bcs @t2
        sta tmp
@t2:    lda OY,x
        cmp tmp
        beq @f
        bcc @dn
        dec OY,x
        jmp @f
@dn:    inc OY,x
@f:     lda npar
        beq @sl
        lda OTM,x
        and #63
        jmp @c
@sl:    lda OTM,x
        and #127
@c:     cmp #40
        bne @r
        lda OX,x
        cmp #110
        bcc @r
        lda #$FE
        sta tmp+3
        lda #5
        jmp aimfx
@r:     rts

; LARVA MECÁNICA: cruza deprisa su franja y hace un único cambio de altura (al otro extremo) a media pantalla
olar:   lda OTM,x
        bne @g
        inc OTM,x
        lda OB,x
        and #1
        beq @g
        lda OBT,x
        clc
        adc #20
        sta OY,x
@g:     lda OX,x
        sec
        sbc #3
        sta OX,x
        cmp #36
        bcs @a
        jmp escaped
@a:     lda OS,x
        bne @ch
        lda OX,x
        cmp #128
        bcs @r
        lda #1
        sta OS,x
        lda OY,x
        cmp OBT,x
        beq @lo
        lda OBT,x
        sta ODY,x
        rts
@lo:    clc
        adc #20
        sta ODY,x
@r:     rts
@ch:    lda OY,x
        cmp ODY,x
        beq @r
        bcc @dn
        dec OY,x
        dec OY,x
        rts
@dn:    inc OY,x
        inc OY,x
        rts

; NODO de energía del CORAZÓN NULO (blindaje): quieto delante del jefe
onod:   lda state
        cmp #ST_BOSS
        beq @r
        lda frame
        and #1
        bne @r
        dec OX,x
        lda OX,x
        cmp #36
        bcs @r
        jmp freeobj
@r:     rts

ENEM1 = oglo
ENEM2 = olar
ENEM9 = oglo
ENEM10 = oesc
.elseif FASE = 4
ENEM10 = oesc
ENEM1 = oaco
ENEM2 = ogua
ENEM9 = ovas
.elseif FASE = 3
ENEM1 = oasc
ENEM2 = oser
ENEM9 = omar
.elseif FASE = 2
ENEM1 = omed
ENEM2 = oman
ENEM9 = oang
.else
ENEM1 = orec
ENEM2 = ocha
ENEM9 = orec
.endif

escaped:
        ldy OW,x
        cpy #48
        bcs @f
        lda #$FF
        sta WREM,y
@f:     jmp freeobj

; enemigo destruido (X): explosión en su mismo hueco, puntos, cápsula si se limpia la oleada
killobj:
        lda OT,x
        pha
        lda #5
        sta OT,x
        lda #0
        sta OTM,x
        sta OPAT,x
        pla
        stx tmp+7
        sta ktyp
        cmp #1
        bne @c
        lda #$00
        ldx #$01
        bne @add
@c:     cmp #8
        bne @c2
        lda #$00
        ldx #$05
        bne @add
@c2:    lda #$50
        ldx #$01
@add:   jsr addsc
        ldx tmp+7
        jsr sfxexpl
.if FASE = 5
        lda ktyp
        cmp #11             ; nodo del CORAZÓN NULO: con dos caídos, el ojo pierde el blindaje
        bne @p5
        inc bdk
        lda bdk
        cmp #2
        bne @q5
        jsr sfxpick
        lda #$00
        ldx #$10
        jsr addsc
@q5:    rts
@p5:    cmp #10             ; ESCRIBA: su raya se apaga con él
        bne @k5
        jsr escbk
@k5:
.endif
.if FASE = 4
        lda ktyp
        cmp #10             ; ESCRIBA: su raya se apaga con él
        bne @kn
        jsr escbk
        jmp @w
@kn:    cmp #11             ; NODO: con los dos caídos la puerta se abre (bonificación)
        bne @kv
        inc dkill
        lda dkill
        cmp #2
        bne @r0
        jsr sfxpick
        lda #$00
        ldx #$10
        jsr addsc
@r0:    rts
@kv:    cmp #9              ; VASO: cápsula (uno de cada tres, P y S alternas) o un alma apuntada; nunca las dos
        bne @k8
        inc vcnt
        lda vcnt
        and #3
        cmp #3
        bcc @soul
        lda vcnt
        and #$80
        eor #$80
        sta vcnt
        lda pcap
        bne @w
        lda vcnt
        asl a
        lda #3
        adc #0
        sta pcap
        lda OX,x
        sta pcx
        lda OB,x
        sta pcb
        jmp @w
@soul:  lda #$FE
        sta tmp+3
        lda #4
        jsr aimfx
        jmp @w
@k8:
.endif
        lda ktyp            ; el UNIDAD CERO siempre suelta cápsula: P, S, P, S...
        cmp #8
        bne @w
        lda pcap
        bne @r
        inc mdrop
        lda mdrop
        and #1
        eor #1
        clc
        adc #3
        sta pcap
        lda OX,x
        sta pcx
        lda OB,x
        sta pcb
        rts
@w:     ldy OW,x
        cpy #48
        bcs @r
        lda WREM,y
        cmp #$FF
        beq @r
        sec
        sbc #1
        sta WREM,y
        bne @r
        lda WVDROP,y
        bne @cp
        lda dif             ; FÁCIL: una oleada sí y otra no, cápsula aunque no la traiga (P y S alternas)
        bne @r
        lda dcap
        clc
        adc #1
        sta dcap
        and #1
        beq @r
        lda dcap
        and #2
        lsr a
        clc
        adc #3
@cp:    sta pcap
        lda OX,x
        sta pcx
        lda OB,x
        sta pcb
@r:     rts

; ===============================================================
; colisiones
collide:
        lda s0x
        beq @ship
        sta tmp
        lda sal
        and #1
        beq @c1
        lda s0y
        clc
        adc #3
        sta tmp+1
        lda s0x
        sta tmp
        jsr shothit
        bcc @c1
        lda sal
        and #$FE
        sta sal
@c1:    lda sal
        and #2
        beq @c2
        lda s1y
        clc
        adc #3
        sta tmp+1
        lda s0x
        sta tmp
        jsr shothit
        bcc @c2
        lda sal
        and #$FD
        sta sal
@c2:    lda sal
        and #4
        beq @c3
        lda s2y
        clc
        adc #3
        sta tmp+1
        lda s0x
        sta tmp
        jsr shothit
        bcc @c3
        lda sal
        and #$FB
        sta sal
@c3:    lda sal
        bne @ship
        sta s0x
@ship:  lda shipst
        beq @sh
        cmp #2
        beq *+5
        jmp @x
        jmp @wall
@sh:    ldx #MAXO-1
@o:     lda OT,x
        bne *+5
        jmp @on
        cmp #5
        bne *+5
        jmp @on
        tay
        lda OX,x
        clc
        adc OWID,y
        sec
        sbc #2
        cmp shipx
        bcs *+5
        jmp @on
        lda shipx
        clc
        adc #9
        cmp OX,x
        bcc @on
        lda OY,x
        clc
        adc OHIT,y
        sec
        sbc #1
        cmp shipy
        bcc @on
        lda shipy
        clc
        adc #8
        cmp OY,x
        bcc @on
        lda OT,x
        cmp #3
        beq @capp
        cmp #4
        beq @caps
.if FASE >= 4
        cmp #10             ; ESCRIBA embestido: su raya se apaga con él
        bne @ne
        jsr escbk
@ne:
.endif
        lda #5
        sta OT,x
        lda #0
        sta OTM,x
        sta OPAT,x
        txa
        pha
        jsr hitship
        pla
        tax
        jmp @on
@capp:  jsr freeobj
        lda power
        cmp #3
        beq @bon
        inc power
        lda #1
        sta hudd
        jsr sfxpick
        jmp @on
@caps:  jsr freeobj
        lda shield
        bne @bon
        lda #1
        sta shield
        sta hudd
        jsr sfxpick
        jmp @on
@bon:   txa
        pha
        lda #$00
        ldx #$05
        jsr addsc
        jsr sfxpick
        pla
        tax
@on:    dex
        bmi *+5
        jmp @o
        lda shipst
        bne @x
        lda e0x
        beq @e1
        sta tmp
        lda e0y
        sta tmp+1
        jsr bulship
        bcc @e1
        lda #0
        sta e0x
        jsr hitship
@e1:    lda e1x
        beq @wall
        sta tmp
        lda e1y
        sta tmp+1
        jsr bulship
        bcc @wall
        lda #0
        sta e1x
        jsr hitship
@wall:
.ifdef PRUEBA
        rts
.endif
        lda cheat
        bne @x
.ifdef PRUEBAJ
        lda state
        cmp #ST_BOSS
        bne @x
.endif
        lda shipst          ; invulnerable: el decorado tampoco mata (no se encadenan muertes)
        cmp #2
        beq @x
        jsr shipsolid       ; nave contra decorado
        bcc @x
        lda #0
        sta shipst
        sta shield
        lda #1
        sta wallk
        jsr hitship
        lda #0
        sta wallk
@x:     rts

bulship:
        lda tmp
        clc
        adc #3
        cmp shipx
        bcc @n
        lda shipx
        clc
        adc #10
        cmp tmp
        bcc @n
        lda tmp+1
        clc
        adc #2
        cmp shipy
        bcc @n
        lda shipy
        clc
        adc #9
        cmp tmp+1
        bcc @n
        sec
        rts
@n:     clc
        rts

; disparo (tmp, tmp+1) contra enemigos y ojo del jefe -> C=1 si impacta
shothit:
        ldx #MAXO-1
@o:     lda OT,x
        cmp #8
        bcs @t
        cmp #1
        beq @t
        cmp #2
        bne @n
@t:     tay
        lda OX,x            ; x: OX <= tmp+16  y  tmp <= OX+ancho
        sec
        sbc #16
        bcc @x1
        cmp tmp
        bcs @n
@x1:    lda OX,x
        clc
        adc OWID,y
        cmp tmp
        bcc @n
        lda OY,x            ; y: OY <= tmp+1+3  y  tmp+1 <= OY+alto+3
        sec
        sbc #3
        cmp tmp+1
        beq @y1
        bcs @n
@y1:    lda OY,x
        clc
        adc OHIT,y
        adc #3
        cmp tmp+1
        bcc @n
        dec OH,x
        bne @h
        jsr killobj
        sec
        rts
@h:     txa
        pha
        jsr sfxhit
        pla
        tax
        sec
        rts
@n:     dex
        bpl @o
        lda eyeopen         ; el ojo de FERRUM-9, solo abierto
        beq @no
        lda tmp
        cmp #EYEX0
        bcc @no
        cmp #200
        bcs @no
        lda tmp+1
        cmp #EYEY0
        bcc @no
        cmp #EYEY1
        bcs @no
        lda #4
        sta eyefl
        jsr sfxhit
        lda #$10
        ldx #0
        jsr addsc
.if FASE = 5
        lda bdk             ; el CORAZÓN NULO no recibe daño hasta que caen sus dos nodos
        cmp #2
        bcc @ok
.endif
        dec bhp
        bne @ok
        lda #0
        sta eyeopen
        lda #6
        sta bst
        lda #<240
        sta btm
        lda #0
        sta btm+1
@ok:    sec
        rts
@no:    clc
        rts

hitship:
.ifdef PRUEBA
        rts
.endif
.ifdef PRUEBAJ
        lda wallk           ; prueba del jefe: solo matan las paredes
        bne @pj
        rts
@pj:
.endif
        lda cheat
        beq @nc
        rts
@nc:    lda shipst
        bne @r
        lda shield
        beq @die
        lda #0
        sta shield
        lda #1
        sta hudd
        lda #2
        sta shipst
        lda #40
        sta shiptm
        jmp sfxhit
@die:   lda #1
        sta shipst
        lda #48
        sta shiptm
        dec lives
        lda dif             ; al morir: FÁCIL conserva el láser, NORMAL baja un nivel,
        beq @pw             ; HARDCORE lo pierde todo (y el escudo)
        cmp #2
        bne @pn
        lda #1
        sta power
        lda #0
        sta shield
        beq @pw
@pn:    lda power
        cmp #2
        bcc @pw
        dec power
@pw:    lda #1
        sta hudd
        lda #0
        sta s0x
        sta sal
        jmp sfxdeath
@r:     rts

; ===============================================================
; RENDER: todo se dibuja en el búfer oculto; al final ready=1
render: lda shown
        eor #1
        sta rb
        tax
        lda PMPAGE,x
        sta pmhi
        lda BANK,x
        sta rbk
        ; --- misiles: se borran enteros y se repintan
        lda pmhi
        clc
        adc #3
        sta dst+1
        lda #0
        sta dst
        ldy #40
@mc:    sta (dst),y
        iny
        cpy #216
        bne @mc
        lda s0x
        beq @m2
        lda sal
        lsr a
        bcc @m0b
        ldy s0y
        jsr laserd
@m0b:   lda sal
        and #2
        beq @m0c
        ldy s1y
        jsr laserd
@m0c:   lda sal
        and #4
        beq @m2
        ldy s2y
        jsr laserd
@m2:    lda e0x
        beq @m3
        ldy e0y
        ldx #3
@m2l:   lda (dst),y
        ora #$30
        sta (dst),y
        iny
        dex
        bne @m2l
@m3:    lda e1x
        beq @m4
        ldy e1y
        ldx #3
@m3l:   lda (dst),y
        ora #$C0
        sta (dst),y
        iny
        dex
        bne @m3l
@m4:    ldx rb
        lda s0x
        sta LHM0,x
        beq @h1
        clc
        adc #8
@h1:    sta LHM1,x
        lda e0x
        sta LHM2,x
        lda e1x
        sta LHM3,x
        lda shipx
        sta LHP0,x
        jsr rship
        jsr rslots
        lda #1
        sta ready
        rts

; láser cápsula en la zona de misiles (dst), desde la línea Y: M0 = cola, M1 = punta
laserd:
        ldx #0
@l:     lda (dst),y
        ora CAPSH,x
        sta (dst),y
        iny
        inx
        cpx #7
        bne @l
        rts
CAPSH:  .byte $09,$0F,$0F,$0F,$0F,$0F,$09

; nave en P0/P1 del búfer oculto (colores y X en las entradas completas 0 y 6)
rship:  lda pmhi
        clc
        adc #4
        sta dst+1
        sta src+1
        inc src+1           ; src = P1
        lda #0
        sta dst
        sta src
        ldx rb
        ldy SHY,x
        beq @d
        ldx #11
@e:     sta (dst),y
        sta (src),y
        iny
        dex
        bne @e
@d:     ldx rb
        lda #0
        sta SHY,x
        lda shipst
        cmp #1
        bne @live
        lda shiptm          ; explotando: solo P0
        cmp #8
        bcc @col
        ldy shipy
        tya
        sta SHY,x
        ldx #0
        lda frame
        and #8
        bne @b1
@b0:    lda SBOOM0,x
        sta (dst),y
        iny
        inx
        cpx #8
        bne @b0
        beq @col
@b1:    lda SBOOM1,x
        sta (dst),y
        iny
        inx
        cpx #8
        bne @b1
        beq @col
@live:  lda shipst          ; invulnerable: parpadea
        cmp #2
        bne @lv
        lda frame
        and #4
        beq @lv
        jmp @col
@lv:    ldy shipy
        tya
        sta SHY,x
        ldx #0
        lda frame
        and #4
        bne @fb
@fa:    lda SHIP_A_P0,x
        sta (dst),y
        lda SHIP_A_P1,x
        sta (src),y
        iny
        inx
        cpx #11
        bne @fa
        beq @col
@fb:    lda SHIP_B_P0,x
        sta (dst),y
        lda SHIP_B_P1,x
        sta (src),y
        iny
        inx
        cpx #11
        bne @fb
@col:   ldx #0              ; colores: normal / escudo / destello invulnerable
        lda shield
        beq @c1
        ldx #2
@c1:    lda shipst
        cmp #2
        bne @c2
        lda frame
        and #4
        beq @c2
        ldx #4
@c2:    ldy rbk
        lda SHIPCOL,x
        sta TC0,y
        sta TC0+20,y
        lda SHIPCOL+1,x
        sta TC1,y
        sta TC1+20,y
        lda shipx
        sta TX0,y
        sta TX0+20,y
        clc
        adc #4
        sta TX1,y
        sta TX1+20,y
        rts

; los 8 huecos: borra lo que había en este búfer y pinta lo que hay ahora
rslots: lda #0
        sta dst
        sta tmp+7           ; hueco
@l:     lda tmp+7
        ldx rb
        beq @i
        clc
        adc #8
@i:     sta tmp+6           ; índice en SDY / SDH
        lda tmp+7
        and #1
        clc
        adc pmhi
        adc #6
        sta dst+1           ; página de P2 o P3
        ldy tmp+6
        lda SDY,y
        beq @ne
        ldx SDH,y
        tay
        lda #0
@e:     sta (dst),y
        iny
        dex
        bne @e
@ne:    ldy tmp+6
        lda #0
        sta SDY,y
        lda tmp+7           ; primera entrada de la franja: banco + 2 + 4*franja
        and #$FE
        asl a
        clc
        adc #2
        adc rbk
        sta tmp+5
        ldx tmp+7
        lda SLOT,x
        bne @obj
        lda #0
        sta tmp+4
        sta tmp+1
        lda #BULCOL
        sta tmp+3
        jsr setband
        jmp @next
@obj:   tax
        dex                 ; X = objeto
        jsr shapeptr
        ldy OT,x
        lda OHGT,y
        sta tmp+2
        ldy tmp+6
        sta SDH,y
        lda OY,x
        sta SDY,y
        tay
        jsr cpobj
        ldy OT,x            ; P3 de las parejas: x + OPOFS (+4 desplazadas, 0 superpuestas, +8 a doble ancho)
        lda OSIZE,y
        sta tmp+1
        lda tmp+7
        and #1
        beq @nw
        lda OX,x
        clc
        adc OPOFS,y
        jmp @sx
@nw:    lda OX,x
@sx:    sta tmp+4
        jsr objcol
        sta tmp+3
        jsr setband
@next:  inc tmp+7
        lda tmp+7
        cmp #8
        beq @x
        jmp @l
@x:     rts

; 4 entradas de la franja (desde tmp+5): X = tmp+4, color = tmp+3, P2 o P3 según tmp+7
setband:
        ldy tmp+5
        lda tmp+7
        and #1
        bne @p3
        .repeat 4, K
        lda tmp+4
        sta TX2+K,y
        lda tmp+3
        sta TC2+K,y
        lda tmp+1
        sta TS2+K,y
        .endrepeat
        rts
@p3:    .repeat 4, K
        lda tmp+4
        sta TX3+K,y
        lda tmp+3
        sta TC3+K,y
        lda tmp+1
        sta TS3+K,y
        .endrepeat
        rts

; copia tmp+2 bytes de (src) a la página dst+1, desde la línea Y
cpobj:  sty dst
        ldy tmp+2
        dey
@c:     lda (src),y
        sta (dst),y
        dey
        bpl @c
        lda #0
        sta dst
        rts

; src = forma del objeto X para el hueco tmp+7
shapeptr:
        ldy OT,x
        cpy #5
        bne @n
        ldy #0              ; explosión: 3 cuadros de 6
        lda OTM,x
        cmp #6
        bcc @bk
        iny
        cmp #12
        bcc @bk
        iny
@bk:    lda BOOMTAB_L,y
        sta src
        lda BOOMTAB_H,y
        sta src+1
        rts
@n:     lda OFRM,y          ; formas por tablas: 4 por tipo (cuadro 1/2 x P2/P3)
        and frame
        beq @f0
        lda #2
@f0:    sta tmp
        lda OP,x
        cmp #2
        bne @g
        lda tmp+7
        and #1
        ora tmp
        sta tmp
@g:     tya
        asl a
        asl a
        ora tmp
        tay
        lda SHL,y
        sta src
        lda SHH,y
        sta src+1
        rts

; A = color del objeto X en el hueco tmp+7
objcol: ldy OT,x
.if FASE = 5
        cpy #10             ; ESCRIBA cargando: destello
        bne @n5
        lda OS,x
        cmp #1
        bne @n5
        lda frame
        and #4
        beq @n5
        lda #$0E
        rts
@n5:
.endif
.if FASE = 4
        cpy #10             ; ESCRIBA y ACÓLITO cargando: destello blanco
        beq @cg
        cpy #1
        bne @n4
@cg:    lda OS,x
        cmp #1
        bne @n4
        lda frame
        and #4
        beq @n4
        lda #$0E
        rts
@n4:
.endif
        cpy #8              ; UNIDAD CERO avisando antes de disparar: destello blanco
        bne @np
        lda OS,x
        beq @np
        cmp #4
        bcs @np
        lda OTM,x
        cmp duzw20
        bcc @np
        lda frame
        and #4
        beq @np
        lda #$0E
        rts
@np:    lda OP,x
        cmp #2
        bne @s
        lda tmp+7
        and #1
        beq @s
        lda OCOL3,y
        rts
@s:     lda OCOL2,y
        rts

; ===============================================================
; marcador
hudinit:
        lda #0
        sta hudmsg
        ldx #39
@c:     lda TX_HUD_TOP,x
        sta HUDTOP,x
        lda TX_HUD_BOT,x
        sta HUDBOT,x
        dex
        bpl @c
        lda #1
        sta hudd
        rts

hud:    lda hudd
        bne @c
        rts
@c:     lda bst
        cmp #1
        bne @go
        rts
@go:    lda #0
        sta hudd
        lda #<(HUDTOP+HUD_SC)
        sta dst
        lda #>(HUDTOP+HUD_SC)
        sta dst+1
        ldx #2
        jsr putbcd
        lda #<(HUDTOP+HUD_HI)
        sta dst
        lda #>(HUDTOP+HUD_HI)
        sta dst+1
        jsr puthi
        lda lives
        clc
        adc #DIG0
        sta HUDTOP+HUD_LV
        lda hudmsg
        beq @ic
        rts
@ic:    ldx #0
@pl:    lda #CH_SPACE
        cpx power
        bcs @ps
        lda #CH_ARROW
@ps:    sta HUDBOT+HUD_PW,x
        inx
        cpx #3
        bne @pl
        lda #CH_MINUS
        ldx shield
        beq @s
        lda #CH_BLOCK
@s:     sta HUDBOT+HUD_SH
        rts

; récord en dst
puthi:  lda hisc+2
        jsr put2
        lda hisc+1
        jsr put2
        lda hisc
        jmp put2
; puntuación (3 bytes BCD) en dst
putbcd: lda score+2
        jsr put2
        lda score+1
        jsr put2
        lda score
put2:   pha
        lsr a
        lsr a
        lsr a
        lsr a
        clc
        adc #DIG0
        ldy #0
        sta (dst),y
        pla
        and #15
        clc
        adc #DIG0
        iny
        sta (dst),y
        inc dst
        inc dst
        rts

; suma A (unidades BCD) y X (centenas BCD)
addsc:  sta tmp+6
        stx tmp+7
        sed
        clc
        lda score
        adc tmp+6
        sta score
        lda score+1
        adc tmp+7
        sta score+1
        lda score+2
        adc #0
        sta score+2
        cld
        lda #1
        sta hudd
        rts

; C=1 si algún punto de la nave toca decorado sólido
shipsolid:
        stx tmp+5
        lda shipx
        clc
        adc #11
        ldy shipy
        iny
        iny
        iny
        iny
        iny
        jsr solidat
        bcs @x
        lda shipx
        clc
        adc #5
        ldy shipy
        iny
        iny
        iny
        jsr solidat
        bcs @x
        lda shipx
        clc
        adc #5
        ldy shipy
        tya
        clc
        adc #8
        tay
        lda shipx
        clc
        adc #5
        jsr solidat
        bcs @x
        lda shipx
        clc
        adc #1
        ldy shipy
        iny
        iny
        iny
        iny
        iny
        jsr solidat
@x:     ldx tmp+5
        rts

; A = x de pantalla (HPOS), Y = línea -> C=1 si el carácter es sólido
solidat:
        clc
        adc fine
        sec
        sbc #35
        lsr a
        lsr a
        sta tmp+4           ; byte de la ventana
        tya
        sec
        sbc #42
        bcc @yes
        lsr a
        lsr a
        lsr a
        cmp #20
        bcs @yes
        tay
        lda ROWLL,y
        clc
        adc tmp+4
        sta src
        lda ROWLH,y
        adc #0
        sta src+1
        ldy #0
        lda (src),y
        and #$7F
        cmp solid0
        rts
@yes:   sec
        rts

; ===============================================================
; FERRUM-9 · el compactador soberano
;  bst: 1 aviso · 2 entrada · 3 Recolección · 4 Compactación · 5 Exposición · 6 derrota · 9 superada
bossstart:
.ifdef FASTCLEAR
        lda #0              ; prueba del disco: al llegar a la arena, fase superada
        sta arena
        lda #9
        sta bst
        rts
.endif
        lda #0
        sta arena
        sta nvt
        sta eyeopen
        lda #ST_BOSS
        sta state
        lda #1
        sta bst
        lda #<150
        sta btm
        lda #0
        sta btm+1
        lda #1
        sta siren
        ldx #39
@w:     lda TX_WARN_TOP,x
        sta HUDTOP,x
        lda TX_WARN_BOT,x
        sta HUDBOT,x
        dex
        bpl @w
        lda #<BOSSROM       ; la pantalla del jefe a RAM
        sta src
        lda #>BOSSROM
        sta src+1
        lda #<BOSSCR
        sta dst
        lda #>BOSSCR
        sta dst+1
        ldx #4
        ldy #0
@c:     lda (src),y
        sta (dst),y
        iny
        bne @c
        inc src+1
        inc dst+1
        dex
        bne @c
        rts

; cambio a la pantalla del jefe (un destello negro)
bossswap:
        lda #0
        sta SDMCTL
        jsr waitfr
        jsr waitfr
        ldx #0
        ldy #8
        lda #<BOSSCR
        sta tmp
        lda #>BOSSCR
        sta tmp+1
@l:     lda tmp
        sta DLBUF,y
        sta ROWLL,x
        lda tmp+1
        sta DLBUF+1,y
        sta ROWLH,x
        lda tmp
        clc
        adc #48
        sta tmp
        bcc @n
        inc tmp+1
@n:     iny
        iny
        iny
        inx
        cpx #20
        bne @l
        lda #CHHI_JEFE
        sta TCH
        sta TCH+32
        lda #SOLID0_B
        sta solid0
        lda #0
        sta fine
        sta siren
        lda #1              ; tema del jefe
        jsr musstart
.if FASE = 5
        lda #$06            ; arena biomecánica: el color 2 pasa a acero oscuro (paneles, tubos, cuenca del ojo)
        sta TPF1
        sta TPF1+32
        lda #0
        sta bdk
        sta bcyc
        ldx #148
        ldy #0
        lda #11
        jsr newobj
        bcc @n1
        inc bdk             ; (si no cabe, no blinda: nunca invulnerable para siempre)
@n1:    ldx #148
        ldy #3
        lda #11
        jsr newobj
        bcc @n2
        inc bdk
        bcs @n3
@n2:    lda OBT,x
        clc
        adc #4
        sta OY,x
@n3:
.endif
.if FASE >= 4
        jsr bkrest          ; ninguna raya de escriba se queda encendida en la arena
.endif
        jsr hudinit
.ifdef PRUEBAJ
        lda #64
        sta shipx
        lda #110
        sta shipy
.endif
        lda #$3E
        sta SDMCTL
        rts

boss:   lda btm
        bne @d
        lda btm+1
        beq @z
        dec btm+1
@d:     dec btm
@z:     lda eyefl
        beq @nf
        dec eyefl
@nf:    inc ctm
        bne @nc
        inc ctm+1
@nc:    lda bst
        cmp #1
        bne @s2
        lda btm             ; 1: aviso
        ora btm+1
        bne @r
        jsr bossswap
        lda #2
        sta bst
        lda #60
        sta btm
        lda dbhp
        sta bhp
@r:     rts
@s2:    cmp #2
        bne @s3
        lda btm
        bne @r
        jmp brec0
@s3:    cmp #3
        bne @s4
        jmp brec
@s4:    cmp #4
        bne @s5
        jmp bcomp
@s5:    cmp #5
        bne @s6
        jmp bexpo
@s6:    cmp #6
        bne @r
        jmp bdead

brec0:  lda #3
        sta bst
        lda #<BREC
        sta btm
        lda #>BREC
        sta btm+1
        jmp hudinit

; I · RECOLECCIÓN: chatarra desde las puntas de las mandíbulas (THALASSA: Canto, burbujas;
;     tras el tercer pulso la concha se abre un momento)
brec:
.if FASE >= 2
        lda btm+1
        bne @cn
        lda btm
        and #127
        cmp #76
        bne @c1
        lda #1
        jmp seteye
@c1:    cmp #68
        bne @c2
        lda #1
        sta eyeopen
        lda #2
        jmp seteye
@c2:    cmp #36
        bne @c3
        lda #0
        sta eyeopen
        lda #1
        jmp seteye
@c3:    cmp #30
        bne @cn
        lda #0
        jmp seteye
@cn:
.endif
        lda btm
        ora btm+1
        bne @g
        lda #4              ; -> Compactación (THALASSA: corriente)
        sta bst
.if FASE = 5
        inc bcyc
.endif
.if FASE = 4
        inc lane
        lda lane
        cmp #3
        bcc @ln
        lda #0
        sta lane
@ln:
.endif
        lda #0
        sta ctm
        sta ctm+1
        sta plate
.if FASE = 3
        sta RKT
        sta RKT+1
        sta RKT+2
        sta RKT+3
.endif
        ldx #39
@w:     lda TX_COMP_BOT,x
.if FASE = 5
        ldy bcyc            ; CORAZÓN NULO: un ciclo aspira, el siguiente llama a sus crías
        cpy #0
        beq @w0
        lda bcyc
        and #1
        beq @w1
        lda TX_COMP_BOT,x
        jmp @w0
@w1:    lda TX_COMP2_BOT,x
@w0:
.endif
        sta HUDBOT,x
        dex
        bpl @w
        lda #1
        sta hudmsg
        rts
@g:     lda btm
.if FASE >= 3
        and #15             ; el Tríptico y SATURNUS escupen el doble de ráfagas
.else
        and #31
.endif
        bne @r
        lda btm
        and #32
        beq @lo
        ldy #JAWY0
        bne @sp
@lo:    ldy #JAWY1
@sp:    sty tmp+2
        lda #7
        ldx #JAWX
        jsr newobjy
        bcs @r
        lda #$FE
.if FASE = 2
        bit btm             ; THALASSA: burbujas a velocidades alternas
        bvc @sv
        lda #$FD
@sv:
.endif
        sta ODX,x
        lda shipy
        cmp tmp+2
        lda #1
        bcs @dn
        lda #$FF
@dn:    sta ODY,x
@r:     rts

; II · COMPACTACIÓN: aviso (fondo rojo y sirena), las placas se cierran del todo
;     salvo la boca entre las pinzas; se mantienen y se abren
bcomp:
.if FASE = 2
        jmp bcrias          ; THALASSA: las crías de la marea
.endif
.if FASE = 3
        jmp blluvia         ; TRÍPTICO: lluvia de escoria
.endif
.if FASE = 5
        lda bcyc            ; CORAZÓN NULO: un ciclo aspira, el siguiente llama a sus crías
        and #1
        bne @asp
        jmp bcrias
@asp:   jmp bhambre
.endif
        lda ctm
        cmp dunpl
        bcs @late
        cmp dbwarn
        bcs @steps
        and #7              ; aviso: el fondo destella en rojo
        bne @r
        jsr siren1
        lda ctm
        and #8
        beq @red
        jmp bkrest
@red:   ldx #2
        lda #BKWARN
@f:     sta TBK,x
        sta TBK+32,x
        inx
        cpx #18
        bne @f
@r:     rts
@steps: cmp dbwarn
        bne @s0
        jsr bkrest
@s0:    lda ctm
        sec
        sbc dbwarn
        cmp dbstep8
        bcs @r
        ldx #0              ; ¿múltiplo del paso? (paso de placa)
@m:     cmp dbstep
        bcc @mm
        sbc dbstep
        jmp @m
@mm:    cmp #0
        bne @r
        inc plate
        jsr siren1
.if FASE = 4
        lda plate           ; SATURNUS: dos filas por paso, 6 pasos, el carril libre queda abierto
        cmp #7
        bcs @r
        lda lane
        asl a
        asl a
        sta tmp+6
        asl a
        clc
        adc tmp+6           ; lane*12
        sta tmp+6
        lda plate
        asl a
        clc
        adc tmp+6
        tax                 ; lane*12 + 2*paso
        lda LANEROWS-2,x
        beq @j1
        pha
        lda LANEROWS-1,x
        sta tmp+6
        pla
        jsr fillrow
@j1:    lda tmp+6
        beq @r
        jmp fillrow
.else
        lda plate
        clc
        adc #1
        jsr fillrow         ; fila 1+paso (baja) y 18-paso (sube)
        lda #18
        sec
        sbc plate
        jmp fillrow
.endif
@late:  lda ctm             ; ctm >= UNPLT: se abre y pasa a la Exposición
        cmp dunpl
        bne @l2
        jmp unplate
@l2:    cmp dunpl8
        bne @r
        lda #5              ; -> Exposición
        sta bst
        lda #0
        sta ctm
        sta ctm+1
        ldx #39
@w:     lda TX_EXPO_BOT,x
        sta HUDBOT,x
        dex
        bpl @w
        lda #1
        sta hudmsg
        rts

; TRÍPTICO · II HAMBRE: aviso; luego la boca-horno se abre (vulnerable) y aspira la nave hacia el altar.
;   La nave mueve 2 por cuadro y la aspiración 1 cada 2: aguantando a la izquierda se escapa; si toca el altar, muere.
.if FASE = 5
bhambre:
        lda ctm+1
        bne @late
        lda ctm
        cmp dbwarn
        bcs @on
        and #7
        bne @r
        jsr siren1
        lda ctm
        and #8
        beq @red
        jmp bkrest
@red:   ldx #2
        lda #BKWARN
@f:     sta TBK,x
        sta TBK+32,x
        inx
        cpx #18
        bne @f
@r:     rts
@on:    bne @pull
        jsr bkrest
        lda #1
        jsr seteye
        rts
@pull:  cmp dbwarn8
        bne @p1
        lda #1
        sta eyeopen
        lda #2
        jmp seteye
@p1:    lda shipst
        cmp #1
        beq @r
        lda shipx
        cmp #176
        bcs @r
        inc shipx
        rts
@late:  lda ctm
        cmp #<(282-256)
        bcc @lr
        bne @l1
        lda #0
        sta eyeopen
        lda #1
        jmp seteye
@l1:    cmp #<(290-256)
        bne @l2
        lda #0
        jmp seteye
@l2:    cmp #<(300-256)
        bne @r2
        lda #5
        sta bst
        lda #0
        sta ctm
        sta ctm+1
        ldx #39
@w:     lda TX_EXPO_BOT,x
        sta HUDBOT,x
        dex
        bpl @w
        lda #1
        sta hudmsg
@r2:    rts
@lr:    lda shipst           ; (256-281) la aspiración sigue
        cmp #1
        beq @r2
        lda shipx
        cmp #176
        bcs @r2
        inc shipx
        rts
.endif

.if FASE = 2 .or FASE = 3 .or FASE = 5
; aviso común de los ataques especiales: el fondo destella en rojo con la sirena (C=1 mientras dura)
bwarnfx:
        lda ctm+1
        bne @no
        lda ctm
        cmp dbwarn
        bcs @end
        and #7
        bne @y
        jsr siren1
        lda ctm
        and #8
        beq @red
        jsr bkrest
        sec
        rts
@red:   ldx #2
        lda #BKWARN
@f:     sta TBK,x
        sta TBK+32,x
        inx
        cpx #18
        bne @f
@y:     sec
        rts
@end:   bne @no
        jsr bkrest          ; justo al acabar el aviso
@no:    clc
        rts
; pasa a la Exposición (III)
toexpo: lda #5
        sta bst
        lda #0
        sta ctm
        sta ctm+1
        ldx #39
@w:     lda TX_EXPO_BOT,x
        sta HUDBOT,x
        dex
        bpl @w
        lda #1
        sta hudmsg
        rts
; orbe apuntado desde la boca del jefe
borb:   lda frame
        and #32
        beq @lo
        ldy #JAWY0
        bne @sp
@lo:    ldy #JAWY1
@sp:    sty tmp+2
        lda #7
        ldx #JAWX
        jsr newobjy
        bcs @r
        lda #$FE
        sta ODX,x
        lda shipy
        cmp tmp+2
        lda #1
        bcs @dn
        lda #$FF
@dn:    sta ODY,x
@r:     rts
.endif

.if FASE = 2 .or FASE = 5
; THALASSA · II LAS CRÍAS DE LA MAREA / CORAZÓN NULO · SANGRE NUEVA: tras el aviso, cada 24 cuadros sale
;   de la boca una cría (dos clases alternas) por una franja distinta, y entre medias un orbe apuntado.
;   Unos 5 s; después el ojo se abre (Exposición).
bcrias: jsr bwarnfx
        bcs @r
        lda ctm+1
        beq @g
        lda ctm
        cmp #40
        bcc @g
        jmp toexpo
@g:     lda ctm
        sec
        sbc dbwarn
        tay
        and #15
        bne @r
        tya
        and #16
        bne @o
        tya                 ; cría: franja (k mod 4) en orden 1,3,0,2 · clase alterna
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        and #3
        tay
        lda CRBAND,y
        tay
        lda ctm
        and #32
        beq @t1
        lda #2
        bne @t2
@t1:    lda #1
@t2:    ldx #JAWX
        jsr newobj
        bcs @r
        jmp sfxtur
@o:     jmp borb
@r:     rts
CRBAND: .byte 1,3,0,2
.endif

.if FASE = 3
; TRÍPTICO · II LLUVIA DE ESCORIA: tras el aviso, caen rocas del techo de la arena (2 caracteres de ancho).
;   Cada roca (2x2 caracteres) avisa parpadeando arriba 24 cuadros y luego cae una fila cada 4 cuadros. Son decorado sólido:
;   tocarlas mata. FURIA sigue escupiendo brasas. Unos 6 s; después el reactor queda expuesto.
blluvia:
        jsr bwarnfx
        bcs @r
        lda ctm+1
        beq @g
        lda ctm
        cmp #96
        bcc @g
        jsr unplate         ; se van todas las rocas
        lda #0
        sta RKT
        sta RKT+1
        sta RKT+2
        sta RKT+3
        jmp toexpo
@g:     lda ctm
        and #63
        cmp #40
        bne @nb
        jsr borb
@nb:    ldx #3
@k:     stx tmp+6
        jsr rock
        ldx tmp+6
        dex
        bpl @k
@r:     rts
; roca X
rock:   lda RKT,x
        bne @live
        lda ctm+1           ; las últimas no nacen
        bne @r
        lda ctm             ; por turnos: la roca X puede nacer cuando ctm mod 32 = 8*X
        and #31
        sta tmp
        txa
        asl a
        asl a
        asl a
        cmp tmp
        bne @r
        lda RANDOM
        and #31
        clc
        adc #4
        cmp #BOSSK0-3
        bcs @r
        sta RKC,x
        lda #2
        sta RKR,x
        lda #1
        sta RKT,x
@r:     rts
@live:  inc RKT,x
        lda RKT,x
        cmp #26
        bcs @fall
        and #4              ; aviso: parpadea en la fila de arriba
        beq @off
        jmp rkdraw
@off:   jmp rkerase
@fall:  lda RKT,x           ; cae una fila cada 4 cuadros
        and #3
        bne @r
        jsr rkerase
        ldx tmp+6
        inc RKR,x
        lda RKR,x
        cmp #17             ; la roca ocupa R y R+1: hasta la fila 17
        bcc @d
        lda #0
        sta RKT,x
        rts
@d:     jmp rkdraw
rkdraw: lda RKR,x            ; roca de 2x2 caracteres en las filas R y R+1
        jsr rowptr
        ldx tmp+6
        ldy RKC,x
        lda ROCKCH
        sta (dst),y
        iny
        lda ROCKCH+1
        sta (dst),y
        tya
        clc
        adc #47
        tay
        lda ROCKCH+2
        sta (dst),y
        iny
        lda ROCKCH+3
        sta (dst),y
        rts
rkerase:
        lda RKR,x
        jsr rowptr
        ldx tmp+6
        ldy RKC,x
        lda (src),y
        sta (dst),y
        iny
        lda (src),y
        sta (dst),y
        tya
        clc
        adc #47
        tay
        lda (src),y
        sta (dst),y
        iny
        lda (src),y
        sta (dst),y
        rts
.endif

; fondo: vuelve el degradado
bkrest: ldx #2
@b:     lda BKG,x
        sta TBK,x
        sta TBK+32,x
        inx
        cpx #18
        bne @b
        rts

; A = fila: placa en los caracteres no sólidos desde el borde hasta FILLEND
fillrow:
        tax
        lda FILLEND,x
        sta tmp+4
        txa
        jsr rowptr
        ldy #3
@f:     cpy tmp+4
        bcs @x
        lda (dst),y
        and #$7F
        cmp solid0
        bcs @n
        lda #PLATECH
        sta (dst),y
@n:     iny
        bne @f
@x:     rts
; dst = BOSSCR + A*48 ; src = BOSSROM + A*48
rowptr: tax
        lda #<BOSSCR
        sta dst
        lda #>BOSSCR
        sta dst+1
        lda #<BOSSROM
        sta src
        lda #>BOSSROM
        sta src+1
@l:     cpx #0
        beq @x
        lda dst
        clc
        adc #48
        sta dst
        bcc @a
        inc dst+1
@a:     lda src
        clc
        adc #48
        sta src
        bcc @b
        inc src+1
@b:     dex
        jmp @l
@x:     rts
; las placas se abren: filas 2-17 vuelven a ser las originales
unplate:
        lda #2
        sta tmp+5
@l:     lda tmp+5
        tax
        lda FILLEND,x
        sta tmp+4
        lda tmp+5
        jsr rowptr
        ldy #3
@c:     cpy tmp+4
        bcs @nx
        lda (src),y
        sta (dst),y
        iny
        bne @c
@nx:    inc tmp+5
        lda tmp+5
        cmp #18
        bcc @l
        lda #0
        sta plate
        rts

; ojo: A = estado (0 cerrado, 1 entreabierto, 2 abierto): 2 filas x EYENC caracteres
seteye: tax
        lda EYEL,x
        sta tmp
        lda EYEH,x
        sta tmp+1
        lda #EYEROW0
        jsr rowptr
        lda dst
        clc
        adc #EYEK0
        sta dst
        bcc @a0
        inc dst+1
@a0:    ldy #EYENC-1
@a:     lda (tmp),y
        sta (dst),y
        dey
        bpl @a
        lda dst
        clc
        adc #48
        sta dst
        bcc @b0
        inc dst+1
@b0:    lda tmp
        clc
        adc #EYENC
        sta tmp
        bcc @b1
        inc tmp+1
@b1:    ldy #EYENC-1
@b:     lda (tmp),y
        sta (dst),y
        dey
        bpl @b
        rts
EYEL:   .byte <EYE0, <EYE1, <EYE2
EYEH:   .byte >EYE0, >EYE1, >EYE2

; III · EXPOSICIÓN: el ojo se abre en tres cuadros, dispara en abanico y es vulnerable
bexpo:  lda ctm+1
        bne @lt
        lda ctm
        cmp #1
        bne @e1
        lda #1
        jmp seteye
@e1:    cmp #10
        bne @e2
        lda #1
        sta eyeopen
        lda #2
        jmp seteye
@e2:    cmp #200
        bcs @r
        cmp #20
        bcc @r
        and #63
        bne @r
        lda #$FE            ; abanico: dos balas y un orbe
        sta tmp+3
        lda #EYEPX
        ldy #EYEPY-6
        ldx #$FF
        jsr fireb
        bcs @r              ; nave demasiado cerca (dentro de la boca): no dispara
        lda #$FE
        sta tmp+3
        lda #EYEPX
        ldy #EYEPY+6
        ldx #1
        jsr fireb
        lda #6
        ldx #EYEPX-8
        ldy #EYEPY
        jsr newobjy
        bcs @r
        lda #$FE
        sta ODX,x
        lda #0
        sta ODY,x
        jmp sfxtur
@r:     rts
@lt:    lda ctm             ; ctm >= 256: se cierra y vuelve a la Recolección
        cmp #<(300-256)
        bne @c1
        lda #0
        sta eyeopen
        lda #1
        jmp seteye
@c1:    cmp #<(308-256)
        bne @r
        lda #0
        jsr seteye
        jmp brec0

; derrota: explosiones y el jefe desaparece
; muerte del jefe (4 s): destellos blancos, explosiones continuas por todo el cuerpo
; y el jefe se desmorona fila a fila de arriba abajo (sin dejar ningún bloque)
bdead:  lda btm
        ora btm+1
        bne @g
        jsr bkrest
        lda #$00
        ldx #$50
        jsr addsc
        lda #9
        sta bst
        rts
@g:     lda btm
        cmp #204
        bcc @nf
        and #7              ; primeros cuadros: el fondo destella en blanco
        bne @f2
        ldx #2
        lda #$0C
@fw:    sta TBK,x
        sta TBK+32,x
        inx
        cpx #18
        bne @fw
        beq @ex
@f2:    cmp #4
        bne @ex
        jsr bkrest
        jmp @ex
@nf:    cmp #180
        bcs @ex
        and #7              ; desmoronamiento: una fila cada 8 cuadros
        bne @ex
        lda #180
        sec
        sbc btm
        lsr a
        lsr a
        lsr a
        clc
        adc #BOSSR0
        cmp #BOSSR1
        bcs @ex
        jsr rowptr
        ldy #BOSSK0
        lda #0
@rc:    sta (dst),y
        iny
        cpy #BOSSK1
        bne @rc
        jsr sfxexpl
@ex:    lda btm
        and #1
        bne @r
        lda RANDOM
        and #63
        clc
        adc #BOSSX0
        tax
        lda RANDOM
        and #BOSSYM
        clc
        adc #BOSSY0
        tay
        lda #5
        jsr newobjy
        bcs @r
        jmp sfxexpl
@r:     rts

; copia los parámetros de la dificultad elegida
setdif: ldx dif
        lda DBULX,x
        sta dbulx
        lda DFAIR,x
        sta dfair
        lda DHPADJ,x
        sta dhp
        lda DUZW,x
        sta duzw
        sec
        sbc #20
        sta duzw20
        lda DESCW,x
        sta descw
        clc
        adc #1
        sta descw1
        adc #13
        sta descw14
        lda DBWARN,x
        sta dbwarn
        clc
        adc #8
        sta dbwarn8
        lda DBSTEP,x
        sta dbstep
        asl a
        asl a
        asl a
        sta dbstep8
        clc
        adc dbwarn
        adc #48
        sta dunpl
        adc #8
        sta dunpl8
        lda DBHP,x
        sta dbhp
        lda #0
        sta dcap
        rts
DLIVES: .byte 5, 3, 3

; ===============================================================
; final de partida y de fase
gameover:
        jsr newhi
        lda #<SCR_OVER
        ldx #>SCR_OVER
        jsr showscr
        lda #<240
        sta tmp+4
        lda P_DISK          ; disco/cartucho: de vuelta al panel de mando (programa 0, directo al menú)
        beq endwait
        jsr endwt
        lda #$80
        sta P_CHAIN
        lda #0
        jmp LOADER
cleared:
        jsr newhi
        lda #<SCR_CLEAR
        ldx #>SCR_CLEAR
        jsr showscr
        lda #250
        sta tmp+4
        lda P_DISK          ; disco: guarda la partida y carga la fase siguiente (o el final)
        beq endwait
        jsr endwt
        lda score
        sta P_SCORE
        lda score+1
        sta P_SCORE+1
        lda score+2
        sta P_SCORE+2
        lda lives
        sta P_LIVES
        lda power
        sta P_POWER
        lda shield
        sta P_SHLD
        lda #1
        sta P_CHAIN
        lda #FASE+1
        jmp LOADER
endwait:
        jsr endwt
endwait2:
        jmp title
endwt:  jsr sndoff
@w:     jsr waitfr
        dec tmp+4
        bne @w
        rts

; récord y línea de puntuación centrada
newhi:  jsr sndoff
        lda score+2
        cmp hisc+2
        bcc @line
        bne @set
        lda score+1
        cmp hisc+1
        bcc @line
        bne @set
        lda score
        cmp hisc
        bcc @line
@set:   lda score
        sta hisc
        sta P_HISC
        lda score+1
        sta hisc+1
        sta P_HISC+1
        lda score+2
        sta hisc+2
        sta P_HISC+2
@line:  lda #CH_SPACE
        ldx #39
@c:     sta SCRLINE,x
        dex
        bpl @c
        lda #<(SCRLINE+17)
        sta dst
        lda #>(SCRLINE+17)
        sta dst+1
        ldx #2
        jmp putbcd

; ===============================================================
; sonido POKEY: la música suena en los 4 canales; los efectos pisan el 3 (explosiones,
; muerte) y el 4 (disparo, cápsulas, golpes, sirena) mientras duran
sndoff: lda #0
        sta mplay
        ldx #7
@c:     sta AUDF1,x
        dex
        bpl @c
        ldx #3
@d:     sta SDUR,x
        sta SPRI,x
        dex
        bpl @d
        sta siren
        rts

; X = canal, A = índice de efecto
sfx:
.ifdef SOLOMUS
        rts                 ; grabación de música: sin efectos
.endif
        tay
        lda SXPRI,y
        cmp SPRI,x
        bcc @r
        sta SPRI,x
        lda SXF,y
        sta SFRQ,x
        lda SXS,y
        sta SFST,x
        lda SXV,y
        sta SVOL,x
        lda SXD,y
        sta SDUR,x
        lda SXC,y
        sta SCTL,x
@r:     rts
sfxshot:
        ldx #3
        lda #0
        jmp sfx
sfxexpl:
        txa
        pha
        ldx #2
        lda #1
        jsr sfx
        pla
        tax
        rts
sfxdeath:
        ldx #2
        lda #2
        jmp sfx
sfxpick:
        txa
        pha
        ldx #3
        lda #3
        jsr sfx
        pla
        tax
        rts
sfxhit: txa
        pha
        ldx #3
        lda #4
        jsr sfx
        pla
        tax
        rts
sfxtur: txa
        pha
        ldx #3
        lda #5
        jsr sfx
        pla
        tax
        rts
siren1:
.ifdef SOLOMUS
        rts
.endif
        lda #12
        sta siren
        rts
;            disparo explosión muerte cápsula golpe torreta
SXF:    .byte $18,$30,$50,$40,$10,$60
SXS:    .byte 3,2,1,$FD,6,$FE
SXV:    .byte 8,12,15,10,10,7
SXD:    .byte 8,24,64,20,6,12
SXC:    .byte $A0,$80,$80,$A0,$A0,$A0
SXPRI:  .byte 1,2,4,3,3,1

sound:  ldx #3
@l:     lda SDUR,x
        beq @off
        dec SDUR,x
        txa
        asl a
        tay
        lda SFRQ,x
        sta AUDF1,y
        lda SCTL,x
        ora SVOL,x
        sta AUDC1,y
        lda SFRQ,x
        clc
        adc SFST,x
        sta SFRQ,x
        lda frame
        and #1
        bne @n
        lda SVOL,x
        beq @n
        dec SVOL,x
        jmp @n
@off:   lda #0
        sta SPRI,x
        lda mplay           ; sin música (título, pantallas): el canal se calla al acabar el efecto
        bne @n
        txa
        asl a
        tay
        lda #0
        sta AUDC1,y
@n:     dex
        cpx #2
        bcs @l
        ; canal 4
        lda siren
        beq @bass
        lda frame
        and #8
        beq @s1
        lda #$40
        bne @s2
@s1:    lda #$58
@s2:    sta AUDF1+6
        lda #$A8
        sta AUDC1+6
        lda bst
        cmp #1
        beq @x
        dec siren
@x:     rts
@bass:  rts

        .include "music.s"
