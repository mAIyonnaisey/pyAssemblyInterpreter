import pygame

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

import CoreInterpreter.asmInterpreter as asm
import CoreSpicifier.asmSpicifier as spicifier

"""
uses pygame to emulate a keyboad input and a screen display output from the asm interpreter
uses memory mapped I/O and literally just moves inputs over a location so it gets output again
"""

os.remove("spitOutASCIIKEYS.p.p")

spicifier.go("spitOutASCIIKeys.p", "spitOutASCIIKeys.p.p")

asm.go("spitOutASCIIKeys.p.p")

pygame.display.set_mode((100,100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            asm.threadStop = True
            selfStop = True

        if event.type == pygame.KEYDOWN:
            asm.Memory[0] = event.key

    if asm.Memory[1] != 0:
        print((asm.Memory[1]))
        asm.Memory[1] = 0

    if not asm.Thread.is_alive():
        break