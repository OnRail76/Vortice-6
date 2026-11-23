; ===============================================================
; VÓRTICE 6 · cartucho AtariMax 8 Mbit (1 MB, bancos de 8 KB en $A000-$BFFF)
;   Bloque residente en $0700-$087F (lo copia el banco 0 al arrancar).
;   LOADER ($0710): misma interfaz que el disco. A = programa (0 intro · 1-5 fases · 6 final).
;   Copia sus páginas desde los bancos a $2000, desconecta el cartucho ($A000-$BFFF = RAM)
;   y salta a su arranque. El bloque de $0580 pasa intacto.
; ===============================================================
SETVBV  = $E45C
SYSVBV  = $E45F
XITVBV  = $E462
SDMCTL  = $022F
NMIEN   = $D40E
DMACTL  = $D400
AUDCTL  = $D208
AUDF1   = $D200
COLOR4  = $02C8
PORTB   = $D301
TRIG3   = $D013
GINTLK  = $03FA
CBANK   = $D500             ; $D500+n: banco n · $D580: cartucho fuera
COFF    = $D580
PERS    = $0580
NPROG   = 7
src     = $CB               ; punteros en página cero (libre mientras se carga)
dst     = $CD

        .org $0700
        .byte "V6"
        jmp cboot               ; $0702: entrada desde el banco 0
        .res $0710 - *, $EA
; ---------------------------------------------------------------
LOADER: sta prg                 ; $0710
        lda #0
        sta SDMCTL
        sta DMACTL
        lda #$40
        sta NMIEN
        lda #6                  ; VBI del sistema
        ldy #<SYSVBV
        ldx #>SYSVBV
        jsr SETVBV
        lda #7
        ldy #<XITVBV
        ldx #>XITVBV
        jsr SETVBV
        lda #0                  ; silencio
        ldx #7
@s:     sta AUDF1,x
        dex
        bpl @s
        sta AUDCTL
        sta COLOR4
        sta NMIEN               ; sin NMI mientras cambia el cartucho (el SO vigila TRIG3)
        lda PORTB               ; BASIC fuera
        ora #$02
        sta PORTB
        lda prg
        asl a
        clc
        adc prg
        asl a                   ; *6
        tax
        lda PTAB,x
        sta pbank
        lda PTAB+1,x
        clc
        adc #$A0
        sta src+1
        lda PTAB+2,x
        sta pcnt
        lda PTAB+3,x
        sta pcnt+1
        lda PTAB+4,x
        sta prun
        lda PTAB+5,x
        sta prun+1
        lda #0
        sta src
        sta dst
        lda #$20
        sta dst+1
@pg:    ldx pbank
        sta CBANK,x
        ldy #0
@cp:    lda (src),y
        sta (dst),y
        iny
        bne @cp
        inc dst+1
        inc src+1
        lda src+1
        cmp #$C0
        bne @n
        lda #$A0
        sta src+1
        inc pbank
@n:     lda pcnt
        bne @d
        dec pcnt+1
@d:     dec pcnt
        lda pcnt
        ora pcnt+1
        bne @pg
        sta COFF                ; cartucho fuera: $A000-$BFFF = RAM
        lda TRIG3
        sta GINTLK
        lda #$40
        sta NMIEN
        jmp (prun)
; ---------------------------------------------------------------
cboot:  lda #$56                ; bloque compartido: válido, NORMAL, cargador residente
        sta PERS
        lda #1
        sta PERS+1
        sta PERS+13
        lda #0
        sta PERS+2
        sta PERS+9
        sta PERS+10
        sta PERS+11
        sta PERS+12
        lda #0
        jmp LOADER              ; intro
prg:    .byte 0
pbank:  .byte 0
pcnt:   .word 0
prun:   .word 0
; tabla: banco, página dentro del banco, páginas, arranque (la rellena mkcart.py)
        .res $0840 - *, 0
PTAB:   .res NPROG*6, 0
        .res $0880 - *, 0
