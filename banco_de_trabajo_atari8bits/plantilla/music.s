; ===============================================================
; MÚSICA · reproductor de 4 voces (se llama en la VBI, antes de los efectos)
;   canal 1 synth · canal 2 bajo (distorsión C) · canal 3 batería · canal 4 eco/pad
;   los efectos se escriben después y pisan los canales 3 y 4 mientras suenan
;   compás = 4 patrones de 16 filas; fila = ranura(2 bits) | nota(6 bits); 0 sigue, 1 calla

; A = tema
musstart:
        tax
        lda #0
        sta mplay
        stx msong
        lda MUS_TLO,x
        sta mbar
        lda MUS_THI,x
        sta mbar+1
        lda MUS_ILO,x
        sta mins
        lda MUS_IHI,x
        sta mins+1
        lda #0
        sta mrow
        sta mbarn
        sta malt
        sta mtick
        ldx #3
        lda #$FF
@c:     sta MCI,x
        dex
        bpl @c
        lda #1
        sta mplay
        rts

mus:    lda mplay
        bne @go
        rts
@go:    dec mtick
        bmi @nrow
        jmp mupd
@nrow:  ldx msong
        lda malt
        eor #1
        sta malt
        beq @s0
        lda MUS_SPD1,x
        jmp @s1
@s0:    lda MUS_SPD0,x
@s1:    sta mtick
        ldx #3
@row:   txa
        tay
        lda (mbar),y
        tay
        lda MUS_PATLO,y
        sta mpp
        lda MUS_PATHI,y
        sta mpp+1
        ldy mrow
        lda (mpp),y
        beq @nx
        sta mt
        and #$3F
        cmp #1
        bne @note
        lda #$FF
        sta MCI,x
        bne @nx
@note:  sec
        sbc #2
        sta MCN,x
        lda mt
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        sta mt
        txa
        asl a
        asl a
        ora mt
        tay
        lda (mins),y
        sta MCI,x
        tay
        lda #0
        sta MCE,x
        sta MCA,x
        lda MI_FIX,y
        sta MCF,x
@nx:    dex
        bpl @row
        inc mrow
        lda mrow
        cmp #16
        bne mupd
        lda #0
        sta mrow
        lda mbar
        clc
        adc #4
        sta mbar
        bcc @b1
        inc mbar+1
@b1:    inc mbarn
        ldx msong
        lda mbarn
        cmp MUS_LEN,x
        bne mupd
        lda MUS_LOOP,x
        sta mbarn
        asl a
        asl a
        clc
        adc MUS_TLO,x
        sta mbar
        lda MUS_THI,x
        adc #0
        sta mbar+1

; envolventes, arpegios y escritura en el POKEY
mupd:   ldx #3
@ch:    txa
        asl a
        sta mt
        ldy MCI,x
        bpl @on
        ldy mt
        lda #0
        sta AUDC1,y
        jmp @cn
@on:    sty mt3
        lda MI_ENV,y
        clc
        adc MCE,x
        tay
        lda MUS_ENVT,y
        sta mt1
        ldy mt3
        lda MCE,x
        cmp MI_ENVL,y
        bcs @e1
        inc MCE,x
@e1:    lda MI_TAB,y
        cmp #2
        bne @tone
        lda MCF,x               ; sonido fijo con desliz (bombo, caja, charles, tom)
        sta mt2
        clc
        adc MI_SLD,y
        bcc @f1
        lda #$FF
@f1:    sta MCF,x
        jmp @out
@tone:  lda MI_ARP,y
        clc
        adc MCA,x
        tay
        lda MUS_ARPT,y
        clc
        adc MCN,x
        sta mt2
        ldy mt3
        inc MCA,x
        lda MCA,x
        cmp MI_ARPL,y
        bcc @a1
        lda #0
        sta MCA,x
@a1:    lda MI_TAB,y
        ldy mt2
        cmp #1
        beq @z
        lda MUS_PURA,y
        jmp @w
@z:     lda MUS_ZUMB,y
@w:     sta mt2
        ldy mt3
        lda MI_WOB,y
        beq @out
        lda frame
        and #1
        clc
        adc mt2
        sta mt2
@out:   ldy mt3
        lda MI_CTL,y
        ora mt1
        ldy mt
        sta AUDC1,y
        lda mt2
        sta AUDF1,y
@cn:    dex
        bmi @r
        jmp @ch
@r:     rts

        .include "musdata.s"
