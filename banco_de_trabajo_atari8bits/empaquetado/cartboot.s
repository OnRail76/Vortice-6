; ===============================================================
; VÓRTICE 6 · cartucho AtariMax 8 Mbit · banco de arranque (banco 0, copiado también en el 127)
;   Copia el cargador residente a $0700-$087F y empieza por la intro.
; ===============================================================
        .org $A000
cstart: ldx #0
@c:     lda ldr,x
        sta $0700,x
        lda ldr+$80,x
        sta $0780,x
        inx
        bpl @c
        ldx #$7F
@d:     lda ldr+$100,x
        sta $0800,x
        dex
        bpl @d
        jmp $0702
cinit:  rts
ldr:    .incbin "build/cartldr.bin"
        .res $BFFA - *, $FF
        .word cstart            ; $BFFA arranque
        .byte 0                 ; $BFFC cartucho presente
        .byte $04               ; $BFFD arrancar el cartucho (sin disco)
        .word cinit             ; $BFFE inicialización
