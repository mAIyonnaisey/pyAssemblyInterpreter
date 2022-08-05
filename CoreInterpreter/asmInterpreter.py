#WASDONE rewrite this in C++
#                     or Java

# done, wrote an asm language in C++

#TODO more major, add more registers, as a list preferably
import threading
import time
import sys

debug = False # debug mode, forces line by line
debugNextLine = False # raise to move on to next line

threadStop = False # raise to halt
done = False # goes high when halted, or gets pulled high to halt

_rawInputFile = ""

_MEMORY_LOCS = 65536

Memory = [0x0] * _MEMORY_LOCS


# i suppose these could be in a list or a dictionary but eh this is fine for now
# Registers
A = 0
B = 0

# interpret a file as asm
def asm(File):
    global _rawInputFile
    global Memory
    global debug
    global debugNextLine
    global threadStop
    global done
    global A
    global B


    # in the case we want an actual file, not a triple quoted string
    def actualFile(file=""):
        global _rawInputFile
        if file == "": # in case of no input file
            load = input("file: ")
            openedFile = open(load, 'r')

            for line in openedFile.readlines():
                _rawInputFile = _rawInputFile + line

        else: # in case of input file
            openedFile = open(file, 'r')

            for line in openedFile.readlines():
                _rawInputFile = _rawInputFile + line

    # double check stack is fine, IndexError if not, with explanation
    def stackCheck():
        if len(stack) == 0:
            print(line)
            raise IndexError("stack cannot be popped with 0 elements")

        if len(stack) == 1024:
            print(line)
            raise IndexError("stack cannot have more than 256 elements")

    # push to stack
    def push(thing):
        stack.append(thing)
        stackCheck()

    # pop off of top of stack
    def pop():
        stackCheck()
        return stack.pop()

    actualFile(File)

    _rawInputFile = _rawInputFile.split('\n')

    _inputFile = [""] * _MEMORY_LOCS # need this so we dont get an IndexError all the time

    # can probably use map() but eh
    for i in range(len(_rawInputFile)):
        _inputFile[i] = _rawInputFile[i]

    IP = 0 # instruction pointer, cannot be read, only written to with jmp

    stack = []

    print(str(_MEMORY_LOCS) + " locs")

    _REGISTER_SET_MODULUS = 65536 # the value the registers are modulo'd by when they are set to a value

    # enter main program at line 0, and run until halt or end of file
    while (IP < _MEMORY_LOCS) and (not threadStop):
        if debug: # debug halt
            while not debugNextLine:
                time.sleep(0.01)

            debugNextLine = False


        line = _inputFile[IP]

        print(line)

        # empty line check
        if (twords := line.split(' '))[0] == '':
            IP += 1
            continue

        # comment line check
        if twords[0][0] == '#':
            IP += 1
            continue

        words = []
        for thing in twords:
            if thing != '':
                words.append(thing)

        IP += 1

        # first word is always operand
        match words[0]:
            case "add":
                #TODO make no arguments be A + B by default, if arguments then parse them
                A = A + B

                A %= _REGISTER_SET_MODULUS


                #add A to B, store in A

                #nothing because A and B

            case "sub":
                #TODO make no arguments be A - B by default, if arguments then parse them
                A = A - B

                A %= _REGISTER_SET_MODULUS


                #subtract B from A, store in A

                #nothing because A and B


            case "lda": #load A
                A = int(words[1])

                A %= _REGISTER_SET_MODULUS


                #value

            case "mov": #move
                firstArg = words[1]
                secondArg = words[2]

                match firstArg:
                    case "a":
                        match secondArg:
                            case "a":
                                pass

                            case "b":
                                A = B & B

                            case "*a":
                                A = Memory[A] | 0

                            case "*b":
                                A = Memory[B] | 0

                            case _:
                                A = Memory[int(secondArg, 16)] % _REGISTER_SET_MODULUS

                    case "b":
                        match secondArg:
                            case "a":
                                B = A & A

                            case "b":
                                pass

                            case "*a":
                                B = Memory[A] | 0

                            case "*b":
                                B = Memory[B] | 0

                            case _:
                                B = Memory[int(secondArg, 16)] % _REGISTER_SET_MODULUS

                    case "*a":
                        match secondArg:
                            case "a":
                                Memory[A] = A & A

                            case "b":
                                Memory[A] = B & B

                            case _:
                                raise SyntaxError(f"Cannot move memory from a location to a dereferenced location - {words}")

                    case "*b":
                        match secondArg:
                            case "a":
                                Memory[B] = A & A

                            case "b":
                                Memory[B] = B & B

                            case _:
                                raise SyntaxError(f"Cannot move memory from a location to a dereferenced location - {words}")

                    case _:
                        match secondArg:
                            case "a":
                                Memory[int(firstArg, 16)] = A

                            case "b":
                                Memory[int(firstArg, 16)] = B

                            case _:
                                raise SyntaxError(f"Cannot move memory to another memory location - {words}")

                #move second one into first one

                #register or address
                #register or address

                #address is base 16, e.g. "0xff"

            case "halt": # stop excecution completely with no recovery
                threadStop = True


            case "and":
                #TODO make no arguments be A & B by default, if arguments then parse them
                A = A & B


                #and A and B together. store in A

                #nothing because A and B

            case "or":
                #TODO make no arguments be A | B by default, if arguments then parse them
                A = A | B


                #or A and B together. store in A

                #nothing because A and B, dtored in a


            case "push":
                if len(stack) == 32:
                    raise OverflowError("Too many elements on stack")

                match words[1]:
                    case "a":
                        push(int(A))

                    case "b":
                        push(int(B))

                    case "i":                   # this enables jsr macro
                        push(IP)

                    case _:
                        print(words)
                        raise NotImplementedError(f"invalid register {words}")

                #register

            case "pop":
                match words[1]:
                    case "a":
                        A = pop()

                    case "b":
                        B = pop()

                    case _:
                        print(words)
                        raise NotImplementedError(f"invalid register {words}")


                #register

            case "drop":
                pop()
                #discard top of stack


            case "jz": #jump if zero
                if pop() == 0:
                    IP = int(words[1])


                #jump if top of stack is zero. discard top of stack
                #register or address

                #address is base 10 e.g. "10"

            case "jnz": #jump if not zero
                if pop() != 0:
                    IP = int(words[1])


                #jump if top of stack is not zero. discard top of stack
                #register or address

                #address is base 10 e.g. "10"

            case "jeq": # jump if (A == B)
                if A == B:
                    IP = int(words[1])

            case "jne": # jump if !(A == B)
                if A != B:
                    IP = int(words[1])

            case "jmp": #just jump
                match words[1]:
                    case "a":
                        IP = A & A

                    case "b":
                        IP = B & B

                    case _:
                        IP = int(words[1])

                #jump unconditionally
                #address

                #address is base 10 e.g. "105"

            case "jsr":
                push(IP)
                IP = int(words[1])

            case "ret":
                IP = pop()

            case "_debugprint":
                match words[1]:
                    case "a":
                        print(A, end='')

                    case "b":
                        print(B, end='')

                #debugging register dump basically

            case "_debugprintc":
                match words[1]:
                    case "a":
                        print(chr(A), end='')

                    case "b":
                        print(chr(B), end='')

                #debugging register dump basically

            case "_memorydump":
                dump = None
                try:
                    dump = open("memorydump.pmd", 'x')

                except FileExistsError:
                    dump = open("memorydump.pmd", 'w')

                dump.write("IP: " + str(IP))
                dump.write('\n\n\n')
                for byte in Memory:
                    otherbyte = str(byte)
                    templength = len(otherbyte)
                    dump.write(otherbyte)
                    dump.write(' ' * (3 - templength))

                dump.close()

                del dump, templength

                sys.exit("memory dumped")

                #just a flat out memory dump and exit


            case "nop": # literally nothing
                pass


            case _:
                raise SyntaxError(f"Not a valid instruction: {words}")
    done = True

Thread = None

def go(File):
    global Thread
    Thread = threading.Thread(target=asm, args=(File,), daemon=True)
    Thread.start()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("need an argument for a file to run")

    go(sys.argv[1])

    while Thread.is_alive():
        ...