; ===============================================================
; VÓRTICE 6 · INTRO (CINE=1) y FINAL (CINE=2)
;   frases en grande con fundido · imagen ANTIC E (160x192, 4 colores por franja de 4 líneas, DLI)
;   final: créditos que suben (modo 2, desplazamiento fino) y puntuación final
;   en el disco: al acabar carga el programa siguiente con el cargador residente ($0600)
; ===============================================================
        .include "hw.inc"
PERS    = $0580
P_MAGIC = PERS
P_DIF   = PERS+1
P_CHAIN = PERS+2
P_SCORE = PERS+3
P_LIVES = PERS+6
P_POWER = PERS+7
P_SHLD  = PERS+8
P_HISC  = PERS+9
P_CHEAT = PERS+12
P_DISK  = PERS+13           ; 1 = arrancado desde el disco o el cartucho (hay cargador residente)
LOADER  = $0710

        .segment "ZEROPAGE"
frame:  .res 1
trig:   .res 1
tmp:    .res 8
mbar:   .res 2
mpp:    .res 2
mins:   .res 2
src:    .res 2
dband:  .res 1
t1:     .res 1
t2:     .res 1
d1:     .res 1              ; temporales solo de la DLI
d2:     .res 1
level:  .res 1              ; brillo máximo (fundido de la imagen)
lvlw:   .res 1              ; brillo pedido
pon:    .res 1              ; 1 = imagen en pantalla (la VBI pone la franja 0)
fcol:   .res 1              ; color de las frases
scrl:   .res 1              ; créditos: desplazamiento fino
ctop:   .res 1              ; créditos: primera línea
wait:   .res 2
mt:     .res 1
mt1:    .res 1
mt2:    .res 1
mt3:    .res 1
tl:     .res 1              ; «TILÍN» (0 = callado)
crun:   .res 1              ; créditos en marcha (la VBI los desplaza)
ccnt:   .res 1
dst:    .res 2

        .segment "HIBSS"
mplay:  .res 1
msong:  .res 1
mrow:   .res 1
mbarn:  .res 1
malt:   .res 1
mtick:  .res 1
MCI:    .res 4
MCN:    .res 4
MCE:    .res 4
MCA:    .res 4
MCF:    .res 4
CURBK:  .res 64
CUR0:   .res 64
CUR1:   .res 64
CUR2:   .res 64
TXT:    .res 64             ; las dos líneas de la frase (modo 7)
DLC:    .res 128            ; lista de los créditos (se reescribe)
SCORL:  .res 64
.if CINE = 1
HTX:    .res 17*40          ; la historia: texto que se escribe letra a letra
mdif:   .res 1              ; panel: dificultad elegida
mcheat: .res 1              ; panel: modo invencible
mswp:   .res 1              ; barrido del monitor
mkk:     .res 1              ; nave de la ruta: mundo de partida
mtt:    .res 1              ; nave de la ruta: tiempo en el tramo
mcur:   .res 1              ; mundo resaltado ($FF = ninguno)
oldy:   .res 1
idle:   .res 2
chk:    .res 1
chkt:   .res 1
stkp:   .res 1
stkh:   .res 1
bp:     .res 1              ; pitido (canal 4): cuadros, frecuencia y deriva
bpf:    .res 1
bpd:    .res 1
upp:    .res 1              ; panel: arriba, arriba, FIRE = los créditos
uchk:   .res 1
ucht:   .res 1
.endif

        .segment "INITSEG"
init:   lda PORTB
        ora #$02
        sta PORTB
        rts

        .segment "PICA"
        .incbin "build/cine/pic.bin", 0, 4080
        .segment "PICB"
        .incbin "build/cine/pic.bin", 4080

        .segment "CODE"
        .include "cinedata.s"
.if CINE = 1
        .segment "MDATA"
        .include "menudata.s"
        .segment "CODE"
; el panel de mando: la misma lista que la imagen, en $8010 (filas 0-101) y $9000 (102-191)
DLMEN:  .byte $70,$70,$70
        .byte $4E, <$8010, >$8010
        .repeat 101, I
        .if (I+1) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $CE, <$9000, >$9000
        .repeat 89, I
        .if (I+103) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $41, <DLMEN, >DLMEN
; la historia: título en grande y 17 líneas de texto
DLHIST: .byte $70,$70,$70
        .byte $47
DLHT:   .word HIST0_T
        .byte $70
        .byte $42, <HTX, >HTX
        .repeat 16
        .byte $02
        .endrepeat
        .byte $41, <DLHIST, >DLHIST
.endif

; lista de la imagen: 24 en blanco, 192 líneas modo E; DLI en la línea 2 de cada franja de 4: espera el final
; de esa línea, prepara los colores durante la 3 y los cambia justo al empezar la siguiente franja
DLPIC:  .byte $70,$70,$70
        .byte $4E, <$5010, >$5010
        .repeat 101, I
        .if (I+1) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $CE, <$6000, >$6000         ; línea 102 (no cruza 4 KB), con DLI
        .repeat 89, I
        .if (I+103) .mod 4 = 2
        .byte $8E
        .else
        .byte $0E
        .endif
        .endrepeat
        .byte $41, <DLPIC, >DLPIC
; lista de las frases: dos líneas grandes centradas en vertical
DLTXT:  .byte $70,$70,$70,$70,$70,$70,$70,$70,$70,$70,$70
        .byte $47, <TXT, >TXT
        .byte $70
        .byte $47, <(TXT+20), >(TXT+20)
        .byte $41, <DLTXT, >DLTXT

; ---------------------------------------------------------------
start:  cld
        sei
        lda #0
        sta NMIEN
        cli
        lda PORTB
        ora #$02
        sta PORTB
        lda #0
        sta SDMCTL
        sta pon
        sta mplay
        lda #3
        sta SKCTL
        lda #0
        sta AUDCTL
        lda #<dli
        sta VDSLST
        lda #>dli
        sta VDSLST+1
        lda #7
        ldy #<vbi
        ldx #>vbi
        jsr SETVBV
        lda #$40
        sta NMIEN
        lda #>FONT
        sta CHBAS
        lda #0
        sta COLOR4
        sta COLOR2
        lda #1
        sta trig
        lda #0
        sta crun
.if CINE = 2
        lda P_DISK          ; truco del panel (arriba, arriba, FIRE): solo los créditos y de vuelta al panel
        beq @nc
        lda P_CHAIN
        cmp #$81
        bne @nc
        lda #0
        jsr musstart
        jsr credits
        jsr sndoff
        lda #$80
        sta P_CHAIN
        lda #0
        jmp LOADER
@nc:
.endif
.if CINE = 1
        lda P_DISK          ; vuelta de una partida (disco o cartucho): directo al panel de mando
        beq @in
        lda P_CHAIN
        cmp #$80
        bne @in
        lda #0
        sta P_CHAIN
        jmp menu
@in:    lda #0              ; la música de la intro empieza con las frases (su parte oscura)
        jsr musstart
.endif
        ; ---- frases
        ldx #0
@fr:    stx tmp+7
        jsr frase
.if CINE = 1
        bcs @skip           ; FIRE: la intro entera se salta, directo al panel
.else
        bcs @pic            ; FIRE: directo a la imagen
.endif
        ldx tmp+7
        inx
        cpx #NFRASES
        bne @fr
@pic:   jsr cleartxt
.if CINE = 2
        lda #0              ; el final: la música entra con la imagen de Elara Voss
        jsr musstart
.endif
        jsr showpic
.if CINE = 2
        lda #<420           ; Elara, en calma: 7 s o FIRE
        ldx #>420
        jsr hold
        jsr glint           ; le brilla el ojo: «TILÍN»
        lda #<150
        ldx #>150
        jsr hold
        jsr picfadeout
        lda #<90            ; negro un momento
        ldx #>90
        jsr hold
        jsr credits
.else
        lda #<600           ; la nave: 10 s o FIRE
        ldx #>600
        jsr hold
        php
        jsr picfadeout
        plp
        bcs @menu
        jsr story           ; la historia, letra a letra (FIRE: al panel)
@menu:  jmp menu
@skip:  jsr cleartxt
        jmp menu
.endif
.if CINE = 2
        ; ---- fin del programa: la partida ha terminado (el truco se apaga)
        lda P_DISK
        beq @again
        jsr sndoff
        lda #0
        sta P_CHEAT
        lda #$80            ; al panel de mando, sin repetir la intro
        sta P_CHAIN
        lda #0
        jmp LOADER
@again: jmp start
.endif

; ---------------------------------------------------------------
; frase X: fundido de entrada, espera, fundido de salida. C=1 si se pulsa FIRE
frase:  txa
        asl a
        tay
        lda FRASES,y
        sta src
        lda FRASES+1,y
        sta src+1
        ldy #39
@c:     lda (src),y
        sta TXT,y
        dey
        bpl @c
        lda #<DLTXT
        sta SDLSTL
        lda #>DLTXT
        sta SDLSTL+1
        lda #$22            ; ANTIC: campo normal, sin jugadores
        sta SDMCTL
        lda #0
        sta fcol
@in:    jsr waitfr
        jsr fireedge
        bcs @x
        lda frame
        and #3
        bne @in
        lda fcol
        clc
        adc #1
        sta fcol
        jsr fcolor
        lda fcol
        cmp #14
        bcc @in
        lda #<200
        ldx #>200
        jsr hold
        bcs @x
@out:   jsr waitfr
        lda frame
        and #3
        bne @out
        dec fcol
        jsr fcolor
        lda fcol
        bne @out
        clc
        rts
@x:     sec
        rts
fcolor: lda fcol            ; rojo-naranja que se enciende (tono 3), blanco al máximo
        cmp #13
        bcc @f
        lda #$0E
        sta COLOR0
        rts
@f:     ora #$30
        sta COLOR0
        rts
cleartxt:
        lda #0
        sta COLOR0
        sta SDMCTL
        rts

; ---------------------------------------------------------------
; imagen: fundido de entrada desde negro
showpic:
        lda #0
        sta level
        sta lvlw
        jsr fadecalc
        lda #<DLPIC
        sta SDLSTL
        lda #>DLPIC
        sta SDLSTL+1
        lda #$C0            ; DLI + VBI
        sta NMIEN
        lda #1
        sta pon
        lda #$22
        sta SDMCTL
@f:     jsr waitfr
        jsr waitfr
        jsr waitfr
        jsr waitfr
        inc level
        jsr fadecalc
        lda level
        cmp #15
        bcc @f
        rts
picfadeout:
@f:     jsr waitfr
        jsr waitfr
        jsr waitfr
        jsr waitfr
        dec level
        jsr fadecalc
        lda level
        bne @f
        lda #0
        sta pon
        sta SDMCTL
        lda #$40
        sta NMIEN
        rts
; colores de cada franja con el brillo limitado a «level» (negro por debajo de 2)
fadecalc:
        lda #0              ; la DLI de la última franja prepara la 48: por debajo de la imagen, negro
        sta CURBK+48
        sta CUR0+48
        sta CUR1+48
        sta CUR2+48
        ldx #NBANDS-1
@l:     lda PALBK,x
        jsr dim
        sta CURBK,x
        lda PAL0,x
        jsr dim
        sta CUR0,x
        lda PAL1,x
        jsr dim
        sta CUR1,x
        lda PAL2,x
        jsr dim
        sta CUR2,x
        dex
        bpl @l
        rts
dim:    sta t1
        and #15
        cmp level
        bcc @ok
        lda level
@ok:    cmp #2
        bcc @blk
        sta t2
        lda t1
        and #$F0
        ora t2
        rts
@blk:   lda #0
        rts

; espera A/X cuadros; C=1 si FIRE
hold:   sta wait
        stx wait+1
@w:     jsr waitfr
        jsr fireedge
        bcs @r
        lda wait
        bne @d
        lda wait+1
        beq @end
        dec wait+1
@d:     dec wait
        jmp @w
@end:   clc
@r:     rts

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
sndoff: lda #0
        sta mplay
        ldx #7
@c:     sta AUDF1,x
        dex
        bpl @c
        rts

; ---------------------------------------------------------------
vbi:    cld
        lda #0
        sta ATRACT
        inc frame
        lda pon
        beq @m
        lda #0
        sta dband
        lda CURBK
        sta COLBK
        lda CUR0
        sta COLPF0
        lda CUR1
        sta COLPF1
        lda CUR2
        sta COLPF2
@m:
.if CINE = 2
        jsr cscroll
.endif
        jsr mus
.if CINE = 2
        jsr tilin
.else
        jsr mbeep
.endif
        jmp XITVBV

dli:    sta WSYNC           ; fin de la línea 2 de la franja (el resto se hace durante la 3)
        pha
        txa
        pha
        tya
        pha
        inc dband
        ldx dband
        lda CUR1,x
        sta d1
        lda CURBK,x
        sta d2
        ldy CUR2,x
        lda CUR0,x
        ldx d1
        sta WSYNC
        sta COLPF0
        stx COLPF1
        sty COLPF2
        lda d2
        sta COLBK
        pla
        tay
        pla
        tax
        pla
        rti

.if CINE = 2
; ---------------------------------------------------------------
; DESTELLO en el ojo de Elara (jugador 0 en blanco, resolución de una línea) y «TILÍN»
GLX     = 48+68-7           ; HPOS: el centro del destello en la columna 68 (doble ancho)
GLY     = 32+84             ; línea de pantalla: fila 84 de la imagen (empieza en la 32)
PMB     = $7800             ; jugadores de una línea: P0 en PMB+$400
glint:  lda #0
        tax
@c:     sta PMB+$400,x
        inx
        bne @c
        lda #>PMB
        sta PMBASE
        lda #1
        sta SIZEP0          ; doble ancho
        lda #1              ; jugadores por delante de la imagen
        sta GPRIOR
        lda #GLX
        sta HPOSP0
        lda #$0E
        sta PCOLR0
        lda #2
        sta GRACTL
        lda #$3A            ; campo normal + jugadores, una línea
        sta SDMCTL
        lda #1
        sta tl              ; suena
        ldx #0
@st:    stx tmp+6
        lda GLSEQ,x
        bmi @done
        jsr glshape
        lda #3
        sta tmp+7
@w:     jsr waitfr
        lda frame           ; titila: blanco / gris claro
        and #2
        ora #$0C
        sta PCOLR0
        dec tmp+7
        bne @w
        ldx tmp+6
        inx
        bne @st
@done:  lda #0
        sta GRACTL
        sta HPOSP0
        lda #$22
        sta SDMCTL
        rts
; dibuja la forma A (0 nada · 1 punto · 2 pequeña · 3 media · 4 grande), 13 líneas centradas en GLY
glshape:
        asl a
        tay
        lda GLSH,y
        sta src
        lda GLSH+1,y
        sta src+1
        ldy #12
@l:     lda (src),y
        sta PMB+$400+GLY-6,y
        dey
        bpl @l
        rts
GLSEQ:  .byte 1,2,3,4,4,3,4,4,4,3,4,3,2,3,2,1,1,0,$FF
GLSH:   .word GL0, GL1, GL2, GL3, GL4
GL0:    .byte 0,0,0,0,0,0,0,0,0,0,0,0,0
GL1:    .byte 0,0,0,0,0,0,$10,0,0,0,0,0,0
GL2:    .byte 0,0,0,0,0,$10,$38,$10,0,0,0,0,0
GL3:    .byte 0,0,0,$10,$10,$38,$FE,$38,$10,$10,0,0,0
GL4:    .byte $10,$10,$10,$10,$54,$38,$FE,$38,$54,$10,$10,$10,$10
; «TILÍN»: canal 4, tono puro. «TI» corto y «LÍN» más agudo que se apaga (en la VBI, tras la música)
tilin:  lda tl
        beq @r
        inc tl
        cmp #7
        bcs @lin
        lda #$14            ; ~1,5 kHz
        sta AUDF4
        lda #$AB
        sta AUDC4
@r:     rts
@lin:   sec
        sbc #7
        lsr a
        lsr a               ; /4
        eor #$FF
        clc
        adc #16             ; 15 - (t/4)
        bmi @off
        beq @off
        ora #$A0
        sta AUDC4
        lda frame           ; un leve temblor de campana
        and #1
        clc
        adc #$0E            ; ~2,1 kHz
        sta AUDF4
        rts
@off:   lda #0
        sta tl
        sta AUDC4
        rts

; ---------------------------------------------------------------
; CRÉDITOS: 24 líneas de modo 2 que suben con desplazamiento fino; al final, la puntuación
credits:
        lda #0
        sta ctop
        sta scrl
        sta ccnt
        sta VSCROL
        jsr dlcred
        lda #<DLC
        sta SDLSTL
        lda #>DLC
        sta SDLSTL+1
        lda #$0E
        sta COLOR1
        lda #0
        sta COLOR2
        sta COLOR4
        lda #$22
        sta SDMCTL
        lda #1              ; el desplazamiento lo hace la VBI: VSCROL y la dirección cambian juntos, antes de pintar
        sta crun
@l:     jsr waitfr
        lda crun
        bne @l
        lda #<300           ; la última línea, quieta 5 s
        ldx #>300
        jsr hold
        lda P_CHAIN         ; solo los créditos (truco del panel): no hay puntuación
        cmp #$81
        beq @x
        ; pantalla final: puntuación
        lda #0
        sta VSCROL
        jsr scoreline
        lda #<DLSC
        sta SDLSTL
        lda #>DLSC
        sta SDLSTL+1
        lda #<1200
        ldx #>1200
        jmp hold
@x:     rts
; lista de los créditos: 24 líneas seguidas desde una sola dirección (la primera con LMS), todas con desplazamiento
; vertical salvo la última; la VBI solo cambia esa dirección y VSCROL
dlcred: lda #$70
        sta DLC
        sta DLC+1
        lda #$62
        sta DLC+2
        lda #<CRED
        sta DLC+3
        lda #>CRED
        sta DLC+4
        ldx #22
        lda #$22
@c:     sta DLC+4,x
        dex
        bne @c
        lda #$02
        sta DLC+27
        lda #$41
        sta DLC+28
        lda #<DLC
        sta DLC+29
        lda #>DLC
        sta DLC+30
        rts
; VBI: un píxel cada 4 cuadros; cada 8, la lista avanza una línea (40 bytes)
cscroll:
        lda crun
        beq @r
        inc ccnt
        lda ccnt
        and #3
        bne @w
        inc scrl
        lda scrl
        cmp #8
        bcc @w
        lda #0
        sta scrl
        lda DLC+3
        clc
        adc #40
        sta DLC+3
        bcc @h
        inc DLC+4
@h:     inc ctop
        lda ctop
        cmp #NCRED-24
        bcc @w
        lda #0
        sta crun
@w:     lda scrl
        sta VSCROL
@r:     rts
; línea con la puntuación final (BCD de 3 bytes en P_SCORE)
scoreline:
        ldx #39
        lda #CH_SPACE
@c:     sta SCORL,x
        dex
        bpl @c
        lda P_MAGIC
        cmp #$56
        bne @r
        ldx #2
        ldy #17
@d:     lda P_SCORE,x
        lsr a
        lsr a
        lsr a
        lsr a
        clc
        adc #DIG0
        sta SCORL,y
        iny
        lda P_SCORE,x
        and #15
        clc
        adc #DIG0
        sta SCORL,y
        iny
        dex
        bpl @d
@r:     rts
DLSC:   .byte $70,$70,$70,$70,$70,$70,$70,$70,$70,$70
        .byte $42, <TXSCORE, >TXSCORE
        .byte $70
        .byte $42, <SCORL, >SCORL
        .byte $70,$70,$70
        .byte $42, <TXFIRE, >TXFIRE
        .byte $41, <DLSC, >DLSC
.endif

.if CINE = 1
; ===============================================================
; LA HISTORIA: dos páginas que se escriben letra a letra (C=1 si se pulsa FIRE)
story:  ldx #0
@p:     stx tmp+6
        jsr hpage
        bcs @x
        ldx tmp+6
        inx
        cpx #2
        bne @p
        clc
@x:     rts
HTLO:   .byte <HIST0_T, <HIST1_T
HTHI:   .byte >HIST0_T, >HIST1_T
HSLO:   .byte <HIST0, <HIST1
HSHI:   .byte >HIST0, >HIST1
HNL:    .byte HIST0_N, HIST1_N
hpage:  lda #0
        sta SDMCTL
        lda HTLO,x
        sta DLHT
        lda HTHI,x
        sta DLHT+1
        lda HSLO,x
        sta src
        lda HSHI,x
        sta src+1
        lda HNL,x           ; letras: líneas * 40
        sta tmp+4
        lda #0
        sta tmp+5
        ldy #3
@m8:    asl tmp+4           ; *8
        rol tmp+5
        dey
        bne @m8
        lda tmp+4
        sta tmp
        lda tmp+5
        sta tmp+1
        asl tmp+4           ; *32
        rol tmp+5
        asl tmp+4
        rol tmp+5
        lda tmp+4
        clc
        adc tmp
        sta tmp+4
        lda tmp+5
        adc tmp+1
        sta tmp+5           ; *40
        lda #<HTX           ; página en blanco
        sta dst
        lda #>HTX
        sta dst+1
        ldx #3
        ldy #0
        lda #CH_SPACE
@cl:    sta (dst),y
        iny
        bne @cl
        inc dst+1
        dex
        bne @cl
        lda #<HTX
        sta dst
        lda #>HTX
        sta dst+1
        lda #$1C            ; título en oro, texto cian sobre azul noche
        sta COLOR0
        lda #$0E
        sta COLOR1
        lda #$90
        sta COLOR2
        lda #0
        sta COLOR4
        lda #<DLHIST
        sta SDLSTL
        lda #>DLHIST
        sta SDLSTL+1
        lda #$22
        sta SDMCTL
@t:     jsr waitfr
        jsr fireedge
        bcs @x
        lda frame           ; una letra cada 2 cuadros (los espacios, de golpe)
        and #1
        bne @t
@ch:    ldy #0
        lda (src),y
        sta (dst),y
        inc src
        bne @a
        inc src+1
@a:     inc dst
        bne @b
        inc dst+1
@b:     lda tmp+4
        bne @d
        dec tmp+5
@d:     dec tmp+4
        lda tmp+4
        ora tmp+5
        beq @done
        ldy #0
        lda (src),y
        cmp #CH_SPACE
        beq @ch
        lda #CH_CUR         ; cursor
        sta (dst),y
        jmp @t
@done:  lda #<420           ; la página, 7 s
        ldx #>420
        jsr hold
        bcs @x
        lda #0
        sta SDMCTL
        clc
@x:     rts

; ===============================================================
; PANEL DE MANDO: ruta de los 5 mundos en un monitor con barrido, dificultad, récord y PULSA FIRE
menu:   jsr cleartxt
        lda #$40
        sta NMIEN
        lda #0
        sta pon
        jsr unrle           ; el panel a $8010
        lda mplay
        bne @mu
        lda #0
        jsr musstart
@mu:    lda P_MAGIC         ; primera vez: NORMAL, sin truco, sin récord
        cmp #$56
        beq @v
        lda #$56
        sta P_MAGIC
        lda #1
        sta P_DIF
        lda #0
        sta P_HISC
        sta P_HISC+1
        sta P_HISC+2
        sta P_CHEAT
@v:     lda P_DIF
        cmp #3
        bcc @d
        lda #1
@d:     sta mdif
        lda P_CHEAT
        and #1
        sta mcheat
        jsr mdifd
        jsr mlbl
        jsr mrec
        lda #0              ; nave de la ruta (jugador 0, una línea)
        tax
@pc:    sta $AC00,x
        inx
        bne @pc
        sta mkk
        sta mtt
        sta mswp
        sta idle
        sta idle+1
        sta chk
        sta chkt
        sta uchk
        sta ucht
        sta level
        sta bp
        lda #1
        sta stkp
        sta stkh
        sta upp
        sta trig
        lda #$FF
        sta mcur
        lda #32
        sta oldy
        lda #$A8
        sta PMBASE
        lda #0
        sta SIZEP0
        lda #1
        sta GPRIOR
        lda #$0E
        sta PCOLR0
        jsr mcalc
        lda #<DLMEN
        sta SDLSTL
        lda #>DLMEN
        sta SDLSTL+1
        lda #$C0
        sta NMIEN
        lda #1
        sta pon
        lda #2
        sta GRACTL
        lda #$3A            ; campo normal + jugadores en resolución de una línea
        sta SDMCTL
@lp:    jsr waitfr
        lda level           ; fundido de entrada (un paso por vuelta)
        cmp #15
        bcs @f
        inc level
@f:     jsr mcalc
        jsr mship
        jsr minput
        bcs @go
        lda idle+1          ; 45 s sin tocar nada: vuelve a empezar la intro
        cmp #>2700
        bcc @lp
        lda idle
        cmp #<2700
        bcc @lp
        jsr mfade
        jmp start
@go:    lda #$08            ; despegue: barrido de tono
        ldx #40
        ldy #1
        jsr beep
        lda mdif
        sta P_DIF
        tax
        lda DLIVES,x
        sta P_LIVES
        lda mcheat
        sta P_CHEAT
        lda #0
        sta P_SCORE
        sta P_SCORE+1
        sta P_SCORE+2
        sta P_SHLD
        lda #1
        sta P_POWER
        sta P_CHAIN         ; la fase 1 empieza directamente
        lda #$56
        sta P_MAGIC
        jsr mfade
        lda P_DISK
        beq @nod
        jsr sndoff
        lda #1
        jmp LOADER
@nod:   lda #0              ; (intro suelta en XEX: no hay fases que cargar)
        sta P_CHAIN
        jmp start
DLIVES: .byte 5, 3, 3

; fundido a negro del panel
mfade:  jsr waitfr
        jsr waitfr
        jsr mcalc
        jsr mship
        dec level
        bpl mfade
        lda #0
        sta level
        sta GRACTL
        sta HPOSP0
        sta pon
        sta SDMCTL
        lda #$40
        sta NMIEN
        rts

; descomprime el panel (RLE: n<128 = n+1 bytes tal cual; n>128 = 257-n veces el siguiente; $80 = fin)
unrle:  lda #<MENURLE
        sta src
        lda #>MENURLE
        sta src+1
        lda #<MENA
        sta dst
        lda #>MENA
        sta dst+1
@l:     ldy #0
        lda (src),y
        cmp #$80
        beq @x
        bcs @rep
        tax                 ; n+1 bytes literales
        inx
@cp:    jsr @in
        jsr @out
        dex
        bne @cp
        beq @nx
@rep:   eor #$FF            ; 257-n = (~n)+2
        clc
        adc #2
        tax
        jsr @in
@rp:    jsr @out
        dex
        bne @rp
@nx:    jsr @in
        jmp @l
@x:     rts
@in:    inc src             ; avanza la entrada y deja en A el byte siguiente
        bne @i1
        inc src+1
@i1:    ldy #0
        lda (src),y
        rts
@out:   ldy #0
        sta (dst),y
        inc dst
        bne @o1
        inc dst+1
@o1:    rts

; copia un bloque: src -> dst, tmp+2 bytes de ancho, tmp+3 filas (paso de 40)
blit:   ldy tmp+2
        dey
@c:     lda (src),y
        sta (dst),y
        dey
        bpl @c
        lda src
        clc
        adc tmp+2
        sta src
        bcc @a
        inc src+1
@a:     lda dst
        clc
        adc #40
        sta dst
        bcc @b
        inc dst+1
@b:     dec tmp+3
        bne blit
        rts
DIFRL:  .byte <DIFR0, <DIFR1, <DIFR2
DIFRH:  .byte >DIFR0, >DIFR1, >DIFR2
mdifd:  ldx mdif
        lda DIFRL,x
        sta src
        lda DIFRH,x
        sta src+1
        lda #<DIFADR
        sta dst
        lda #>DIFADR
        sta dst+1
        lda #DIFW
        sta tmp+2
        lda #8
        sta tmp+3
        jmp blit
mlbl:   lda mcheat
        beq @n
        lda #<LBLR1
        ldx #>LBLR1
        bne @s
@n:     lda #<LBLR0
        ldx #>LBLR0
@s:     sta src
        stx src+1
        lda #<LBLADR
        sta dst
        lda #>LBLADR
        sta dst+1
        lda #LBLW
        sta tmp+2
        lda #6
        sta tmp+3
        jmp blit
; récord: 6 cifras de la fuente pequeña (BCD en P_HISC, la más alta en +2)
mrec:   ldx #0              ; cifra en pantalla
        ldy #2              ; byte BCD
@b:     sty tmp+6
        lda P_HISC,y
        lsr a
        lsr a
        lsr a
        lsr a
        jsr @dig
        ldy tmp+6
        lda P_HISC,y
        and #15
        jsr @dig
        ldy tmp+6
        dey
        bpl @b
        rts
@dig:   sta tmp
        asl a
        asl a
        clc
        adc tmp             ; *5
        tay
        lda DIGB,y
        sta RECADR,x
        lda DIGB+1,y
        sta RECADR+40,x
        lda DIGB+2,y
        sta RECADR+80,x
        lda DIGB+3,y
        sta RECADR+120,x
        lda DIGB+4,y
        sta RECADR+160,x
        inx
        rts

; colores de cada franja con los efectos: barrido del monitor, EUROSHOOTER que late, brillo del logotipo,
; mundo resaltado, PULSA FIRE, luces de la consola, aviso del modo invencible y fundido
mcalc:  lda #0
        sta CURBK+48
        sta CUR0+48
        sta CUR1+48
        sta CUR2+48
        ldx #47
@c:     lda MPALBK,x
        sta CURBK,x
        lda MPAL0,x
        sta CUR0,x
        lda MPAL1,x
        sta CUR1,x
        lda MPAL2,x
        sta CUR2,x
        dex
        bpl @c
        inc mswp            ; barrido: baja una franja por vuelta; una pausa entre pasadas
        lda mswp
        cmp #48
        bcc @s0
        lda #0
        sta mswp
@s0:    lda mswp
        clc
        adc #MON_B0-2
        tax
        lda #6
        sta t1
@sw:    cpx #MON_B0
        bcc @sn
        cpx #MON_B1+1
        bcs @sn
        lda CURBK,x
        clc
        adc t1
        sta CURBK,x
@sn:    dex
        dec t1
        dec t1
        bne @sw
        lda frame           ; EUROSHOOTER: la franja cambia de tono y el texto brilla
        lsr a
        lsr a
        and #15
        tay
        lda EUROBG,y
        sta CURBK+10
        sta CURBK+11
        lda EUROTX,y
        sta CUR1+10
        sta CUR1+11
        lda frame           ; logotipo: un destello baja por las letras cada 2 s
        and #127
        lsr a
        lsr a
        cmp #7
        bcs @nl
        tax
        lda #$0E
        sta CUR1,x
@nl:    ldy mcur            ; el mundo donde está la nave: su nombre parpadea en blanco
        bmi @nw
        lda frame
        and #8
        beq @nw
        lda ENTB0,y
        tax
@w1:    lda #$0E
        sta CUR2,x
        txa
        cmp ENTB1,y
        inx
        bcc @w1
@nw:    lda frame           ; PULSA FIRE
        lsr a
        lsr a
        and #15
        tay
        lda FIRETAB,y
        sta CUR1+43
        sta CUR1+44
        lda frame           ; luces de la consola
        and #16
        beq @l1
        lda #$36
        bne @l2
@l1:    lda #$32
@l2:    sta CUR0+47
        lda frame
        and #32
        beq @l3
        lda #$C8
        bne @l4
@l3:    lda #$C2
@l4:    sta CUR1+47
        lda frame
        and #8
        beq @l5
        lda #$1C
        bne @l6
@l5:    lda #$14
@l6:    sta CUR2+47
        lda mcheat          ; modo invencible: el rótulo parpadea en rojo
        beq @nc
        lda frame
        and #16
        beq @nc
        lda #$36
        sta CUR2+38
        sta CUR2+39
@nc:    lda level
        cmp #15
        bcs @r
        ldx #47
@fd:    lda CURBK,x
        jsr dim
        sta CURBK,x
        lda CUR0,x
        jsr dim
        sta CUR0,x
        lda CUR1,x
        jsr dim
        sta CUR1,x
        lda CUR2,x
        jsr dim
        sta CUR2,x
        dex
        bpl @fd
@r:     rts

; la nave recorre la ruta: se para en cada mundo (que se resalta) y vuela al siguiente
mship:  inc mtt
        lda mtt
        cmp #60
        bcs @fly
        lda mkk              ; parada
        sta mcur
        tay
        lda PATHX,y
        sta tmp
        lda PATHY,y
        sta tmp+1
        jmp @draw
@fly:   lda #$FF
        sta mcur
        lda mkk
        cmp #4
        bne @f2
        lda mtt              ; tras el último mundo, vuelta al primero
        cmp #90
        bcc @hide
        lda #0
        sta mkk
        sta mtt
        rts
@hide:  lda #0
        sta HPOSP0
        rts
@f2:    lda mtt
        cmp #96
        bcc @mv
        inc mkk
        lda #0
        sta mtt
        rts
@mv:    sec                 ; 36 cuadros de vuelo: y avanza media línea por cuadro
        sbc #60
        lsr a
        ldy mkk
        clc
        adc PATHY,y
        sta tmp+1
        lda mtt
        sec
        sbc #60
        lsr a
        lsr a
        cmp #10
        bcc @xx
        lda #10
@xx:    sta tmp+2
        lda PATHX+1,y
        cmp PATHX,y
        lda PATHX,y
        bcs @xr
        sec
        sbc tmp+2
        jmp @xs
@xr:    clc
        adc tmp+2
@xs:    sta tmp
@draw:  ldx oldy            ; borra la anterior
        lda #0
        sta $AC00,x
        sta $AC01,x
        sta $AC02,x
        sta $AC03,x
        lda tmp+1
        clc
        adc #32-2
        sta oldy
        tax
        lda #$C6
        sta $AC00,x
        lda #$6C
        sta $AC01,x
        lda #$38
        sta $AC02,x
        lda #$10
        sta $AC03,x
        lda tmp
        clc
        adc #48-3
        sta HPOSP0
        lda frame
        and #4
        beq @c1
        lda #$0E
        bne @c2
@c1:    lda #$9C
@c2:    sta PCOLR0
        rts

; mando: izquierda/derecha = dificultad · abajo, abajo, FIRE = modo invencible · FIRE = despegue (C=1)
minput: inc idle
        bne @i
        inc idle+1
@i:     lda chkt
        beq @k
        dec chkt
        bne @k
        lda #0
        sta chk
@k:     lda ucht
        beq @k2
        dec ucht
        bne @k2
        lda #0
        sta uchk
@k2:    lda STICK0
        and #1
        bne @uu
        lda upp
        bne @k3
        lda #1
        sta upp
        lda uchk
        cmp #2
        bcs @k3
        inc uchk
        lda #240
        sta ucht
        bne @k3
@uu:    lda #0
        sta upp
@k3:    lda STICK0
        cmp #15
        beq @n0
        ldx #0
        stx idle
        stx idle+1
@n0:    and #12
        cmp #12
        beq @nlr
        ldx stkh
        bne @lr
        inc stkh
        and #4
        bne @rt
        lda mdif
        beq @lr
        dec mdif
        jmp @chg
@rt:    lda mdif
        cmp #2
        bcs @lr
        inc mdif
@chg:   jsr mdifd
        lda #$30
        ldx #8
        ldy #0
        jsr beep
        jmp @lr
@nlr:   lda #0
        sta stkh
@lr:    lda STICK0
        and #2
        bne @up
        lda stkp
        bne @fi
        lda #1
        sta stkp
        lda chk
        cmp #2
        bcs @fi
        inc chk
        lda #240
        sta chkt
        jmp @fi
@up:    lda #0
        sta stkp
@fi:    jsr fireedge
        bcc @no
        lda #0
        sta idle
        sta idle+1
        lda chk
        cmp #2
        bne @go
        lda #0
        sta chk
        lda mcheat
        eor #1
        sta mcheat
        jsr mlbl
        lda #$10
        ldx #30
        ldy #0
        jsr beep
@no:    clc
        rts
@go:    lda uchk            ; arriba, arriba, FIRE: los créditos (solo en disco o cartucho)
        cmp #2
        bcc @gg
        lda #0
        sta uchk
        lda P_DISK
        beq @no
        lda #$18
        ldx #30
        ldy #$FF
        jsr beep
        lda mdif
        sta P_DIF
        lda mcheat
        sta P_CHEAT
        lda #$81
        sta P_CHAIN
        jsr mfade
        jsr sndoff
        lda #6
        jmp LOADER
@gg:    sec
        rts

; pitido en el canal 4: A = frecuencia, X = cuadros, Y = deriva por cuadro
beep:   sta bpf
        sty bpd
        stx bp
        rts
mbeep:  lda bp
        beq @r
        dec bp
        lda bpf
        clc
        adc bpd
        sta bpf
        sta AUDF4
        lda bp
        lsr a
        cmp #15
        bcc @v
        lda #15
@v:     ora #$A0
        sta AUDC4
        lda bp
        bne @r
        lda #0
        sta AUDC4
@r:     rts
.endif

        .include "music.s"
