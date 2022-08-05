#Label - start:
mov b 0x0
push b
jz 0
jsr 8
jmp 0
#Label - exit:
halt
#Label - keycheck:
lda 27
jeq 6
lda 8
jne 14
jsr 23
#Label - noBackspace:
mov 0x1 b
push a
lda 0
push a
pop b
pop a
mov 0x0 b
ret
#Label - Backspace:
lda 8
mov 0x1 a
#Label - backspaceNotZeroMidCheckOne:
mov a 0x1
push a
jnz 26
lda 32
mov 0x1 a
#Label - backspaceNotZeroMidCheckThree:
mov a 0x1
push a
jnz 32
ret
