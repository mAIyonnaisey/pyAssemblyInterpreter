ldb 27

start:
  mov a 0x0
  push a
  jz start

resetLoc0:
  push a
  lda 0
  mov 0x0 a
  pop a

check27:
  mov 0x3 a
  sub
  push a
  jz exit

notNULL:
  mov a 0x3
  mov 0x1 a
  jmp start

exit:
  halt