start:
    mov b 0x0
    push b
    jz start
    jsr keycheck
    jmp start

exit:
    halt

keycheck:
    lda 27
    jeq exit
    lda 8
    jne noBackspace
    jsr Backspace
noBackspace:
    mov 0x1 b
    ldb 0
    mov 0x0 b
    ret

Backspace:
    lda 8
    mov 0x1 a
backspaceNotZeroMidCheckOne:
    mov a 0x1
    push a
    jnz backspaceNotZeroMidCheckOne
    lda 32
    mov 0x1 a
backspaceNotZeroMidCheckThree:
    mov a 0x1
    push a
    jnz backspaceNotZeroMidCheckThree
    ret