push a
lda 27
push a
pop b
pop a
#Label - start:
mov a 0x0
push a
jz 5
#Label - resetLoc0:
push a
lda 0
mov 0x0 a
pop a
#Label - check27:
mov 0x3 a
sub
push a
jz 24
#Label - check65:
#Label - notNULL:
mov a 0x3
mov 0x1 a
jmp 5
#Label - exit:
halt
