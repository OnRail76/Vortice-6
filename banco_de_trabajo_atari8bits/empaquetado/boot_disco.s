; ===============================================================
; VÓRTICE 6 · arranque del disco (3 sectores de 128 bytes en $0700) y cargador residente
;   el SO carga los sectores 1-3 en $0700 y salta a $0706
;   LOADER ($0710): A = programa (0 intro · 1-5 fases · 6 final). Lee sus sectores de 256 bytes
;   a partir de $2000 con el SIO del sistema y salta a su arranque. El bloque de $0580 pasa intacto.
; ===============================================================
SIOV    = $E459
SETVBV  = $E45C
SYSVBV  = $E45F
XITVBV  = $E462
DDEVIC  = $0300
DUNIT   = $0301
DCOMND  = $0302
DSTATS  = $0303
DBUFLO  = $0304
DBUFHI  = $0305
DTIMLO  = $0306
DBYTLO  = $0308
DBYTHI  = $0309
DAUX1   = $030A
DAUX2   = $030B
SDMCTL  = $022F
NMIEN   = $D40E
DMACTL  = $D400
AUDCTL  = $D208
AUDF1   = $D200
COLOR4  = $02C8
COLDST  = $0244
PERS    = $0580
NPROG   = 7

        .org $0700
        .byte 0, 3
        .word $0700, $0706
        jmp boot                ; $0706
        .res $0710 - *, $EA
; ---------------------------------------------------------------
LOADER: sta prg                 ; $0710
        lda #0
        sta SDMCTL
        sta DMACTL
        lda #$40                ; solo VBI (sin DLI del programa anterior)
        sta NMIEN
        lda #6                  ; vectores de la VBI: los del sistema (el código anterior desaparece)
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
        lda #$00
        sta COLOR4
        lda prg
        asl a
        clc
        adc prg
        asl a                   ; *6
        tax
        lda PTAB,x
        sta psec
        lda PTAB+1,x
        sta psec+1
        lda PTAB+2,x
        sta pcnt
        lda PTAB+3,x
        sta pcnt+1
        lda PTAB+4,x
        sta prun
        lda PTAB+5,x
        sta prun+1
        lda #$00
        sta pdst
        lda #$20
        sta pdst+1
@rd:    lda #$31
        sta DDEVIC
        lda #1
        sta DUNIT
        lda #$52                ; 'R'
        sta DCOMND
        lda #$40
        sta DSTATS
        lda pdst
        sta DBUFLO
        lda pdst+1
        sta DBUFHI
        lda #7
        sta DTIMLO
        lda #0
        sta DBYTLO
        lda #1
        sta DBYTHI              ; 256 bytes (doble densidad)
        lda psec
        sta DAUX1
        lda psec+1
        sta DAUX2
        jsr SIOV
        bmi @rd                 ; error: se reintenta
        inc pdst+1
        inc psec
        bne @n
        inc psec+1
@n:     lda pcnt
        bne @d
        dec pcnt+1
@d:     dec pcnt
        lda pcnt
        ora pcnt+1
        bne @rd
        jmp (prun)
; ---------------------------------------------------------------
boot:   lda #$56                ; bloque compartido: válido, dificultad NORMAL, desde el disco
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
psec:    .word 0
pcnt:    .word 0
prun:    .word 0
pdst:    .word 0
; tabla de programas: sector inicial, número de sectores, arranque (la rellena mkdisk.py)
PTAB:   .res NPROG*6, 0
        .res $0880 - *, 0
