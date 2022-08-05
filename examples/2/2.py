import pygame

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../..')) # puts us into the parent folder

import CoreInterpreter.asmInterpreter as asm

asm.go("examples/2/subroutineTester.pp")

pygame.display.set_mode((100,100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            asm.threadStop = True
            selfStop = True

        if event.type == pygame.KEYDOWN:
            asm.Memory[0] = event.key

    if asm.Memory[1] != 0:
        print(chr(asm.Memory[1]), end="", flush=True)
        asm.Memory[1] = 0

    if not asm.Thread.is_alive():
        break