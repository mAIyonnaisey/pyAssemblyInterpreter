import os
import random

#basically a preprocessor

_LABELCHAR = ':'        #! This is the char that denotes a label at the end of a line. Change as needed.
_COMMENT_CHAR = '#'     #! This is the char that denotes a comment. Placed at the start of the line, it signals for the rest of the line to be ignored.
                            #! Change as needed.

# if macros are actually inserted in the output file
replaceMacros = True

# if labels are actually inserted in the output file
replaceLabels = True


verbose = True # mainly for debugging, enables every verbose flag that doesnt result in extreme slowdowns
extraVerbose = True # only intended for debugging, will incur major slowdown on anything more than a few lines
extraExtraVerbose = True # kind of stupid to have, literally just spits out the entire file after every step, taking up a hell of a lot of time to do so



# things get pretty complicated past here




verboseMacroInit = False # print every macro in its entirety upon startup
verboseLabelProcessing = False # print every label as it is discovered, and a list of all labels and line numbers
verboseLabels = False # prints every label replacement once processed
verboseMacros = False # prints every macro replacement once processed


# not included in general verbose
verboseLineReading = False # prints every line as it is read
verboseLineProcessing = False # prints every line as it is processed
verboseMacroProcessing = False # prints every macro as it is processed

# print after each step
verboseCommentsRemoval = False # prints the entire file all over again, just without any comments
verbosePostMacros = False # prints the entire file all over again, with macros replaced by their real code counterparts
verbosePostLabels = False # prints the entire file all over again, with labels replaced by their line number counterparts


if verbose:
    verboseMacroInit = True
    verboseLabels = True
    verboseMacros = True

    if extraVerbose:
        verboseLineReading = True
        verboseLineProcessing = True

        verboseLabelProcessing = True
        verboseMacroProcessing = True

        if extraExtraVerbose:
            verboseCommentsRemoval = True
            verbosePostMacros = True
            verbosePostLabels = True



# ///////////////////////////////////////////////////////////////////////////////////
# actual code now, not just verbosity settings
# ///////////////////////////////////////////////////////////////////////////////////



# inputFile is self explanatory, outputFile is by default None, so prefixes the current file with "sp-"
# if outputFile is defined, will attempt to create a new file with the given name, and fail if said file already exists
def go(inputFile, outputFile):
    if verboseMacroInit:
        print("Macros:")
        for i in range(len(macroNames)):
            print(macroNames[i], "->", macroFuncs[i*2]())


    # open old file and read to list
    _oldfile = open(inputFile, 'r')
    oldLines = _oldfile.readlines()
    _oldfile.close()

    # this will be written to at the macro replacement step, or simply copied to if no replacement occurs
    macroLines = []

    # this is similar, but for labels instead of macros
    labelLines = []

    #* step 0 - get rid of all comments
    # not really important, just makes processing a hell of a lot easier
    # also gets rid of empty lines

    commentsList = removeCommentsPass(oldLines)
    if verboseCommentsRemoval:
        print("\n\nWith No Comments:")
        for line in commentsList:
            print('  ', line)

    #* step 1 - get the positions of all macros
    # get all macros, even if not being printed, they are needed for replacing them
    macrosList = macrosPass(commentsList)
    if verboseMacros:
        print("\n\n All Macros:\n   ", macrosList)

    #* step 2 - replace macros with their actual code
    if replaceMacros: # this  v vv v  is why the list is created even if it is not visible
        macrosInsertionPass(macrosList, commentsList, macroLines)

    else:
        macroLines += oldLines

    if verbosePostMacros:
        print("File after macro insertion:")
        for line in macroLines:
            print("   ", line)

    #* step 3 - get positions of all labels
    # list of tuples, just names of labels and where they are, similar to macros
    labelsList = labelsPass(macroLines)

    if verboseLabels:
        print("\n\n All Labels:\n   ", labelsList)

    #* step 4 - replace all labels with their actual address
    #* ensure this is always the last step, as any other modifications to the file could tamper with the addresses that labels are replaced with
    if replaceLabels:
        labelsInsertionPass(labelsList, macroLines, labelLines)

    else:
        labelLines += macroLines

    if verbosePostLabels:
        print("File after label insertion:")
        for line in labelLines:
            print("   ", line)

    while os.path.isfile(outputFile):
        outputFile += ".p"

    fileToWriteTo = open(outputFile, 'x')

    for line in labelLines:
        fileToWriteTo.write(line)
        fileToWriteTo.write('\n')

    fileToWriteTo.close()

def removeCommentsPass(oldLines):
    returnList = []
    for line in oldLines:
        appendThis = ""
        for i in range(len(line)):
            if line[i] == _COMMENT_CHAR:
                appendThis += '\n'
                break
            appendThis += line[i]

        appendThis = appendThis.strip(" \n")
        if appendThis:
            print(appendThis.strip(" \n"))
            returnList.append(appendThis.strip(" \n"))

    return returnList

def macrosPass(oldLines):
    if verboseMacroProcessing:
        print("\n\n")
    macrosList = [] # will be returning this

    lineNumber = 0
    for line in oldLines:
        line = line.strip(' \n') # get rid of newline chars and whitespace at the start and end of the line

        line = line.split(' ') # break the line into words so that...

        firstWord = line[0] #... the first word can be gotten much easier

        for i in range(len(macroNames)):
            if firstWord == macroNames[i]:
                appendThis = []

                match (macroFuncs[(i * 2) + 1]): # get the macro, with its arguments
                    case 0:
                        temp = macroFuncs[i*2]() # no arguments

                    case 1:
                        temp = macroFuncs[i*2](line[1]) # one argument

                    case 2:
                        temp = macroFuncs[i*2](line[1], line[2]) # two arguments

                    case _: # two many arguments
                        raise SyntaxError(f"Too many arguments - {line}")

                for word in temp.split('\n'): # split it into lines (called words for sake of consistency wiith other passes)
                    if word == '': # if nothing...
                        continue #... discard

                    appendThis.append(word.strip(' ')) # append the line without the leading and trailing whitespace...

                if verboseMacroProcessing:
                    print("Line number " + str(lineNumber + 1) + " \"" + str(oldLines[lineNumber].strip('\n')) + "\" to be replaced by macro: "+ str(temp))

                macrosList.append((appendThis, lineNumber)) #... and its line number too, zero-indexed
                break

        lineNumber += 1

    return macrosList

def macrosInsertionPass(insertThese, oldLines, writeHere):
    replaceWithThis = [] # list of macros replacement values
    linesToReplace = []  # list of lines to be replaces with macros

    # add macro defs to both lists
    for obj in insertThese:
       replaceWithThis.append(obj[0])
       linesToReplace.append(obj[1])

    for i in range(len(oldLines)):
        if i not in linesToReplace: # if line is not a macro...
            writeHere.append(oldLines[i].strip('\n')) #... just add it to the new list as is...
            continue #... and move on

        for j in range(len(linesToReplace)): # line must be a macro, so...
            if i == linesToReplace[j]: #... check where it is on the list...
                for string in replaceWithThis[j]:
                    writeHere.append(string) #... and add every line of the macro to the output list

def labelsPass(oldLines):
    if verboseLabelProcessing:
        print("\n\n")

    # initialise both lists
    labels = []

    lineNumber = 0
    for line in oldLines:
        line = line.split('\n') # remove newline chars since we dont need them
        line = line[0].split(' ') # take first element of that, for some reason empty string is attached to end of line if there is a new line

        if line[-1][-len(_LABELCHAR):] == _LABELCHAR: # if the last char(s) are the same as the label char in the last word of the line
            # add to labels list
            labelStruct = [object, object] # two object list, will be turned into tuple before being added to list

            labelStruct[0] = line[-1]                          # last word of the line
            labelStruct[0] = labelStruct[0][:-len(_LABELCHAR)] # everything of the last word except for the thing that makes it a label rather than a word

            labelStruct[1] = lineNumber                        # also add the line number to the struct

            labels.append(tuple(labelStruct)) # finally, add this to the returning list in tuple form

            if verboseLabelProcessing:
                print(f"Label \"{labels[-1][0]}\" at line {str(labels[-1][1] + 1)}")

        lineNumber += 1

    return labels

def labelsInsertionPass(insertThese, oldLines, writeHere):
    # sort list of label definitions by length of label
    # this prevents a bug where labels which contain a substring that happens to be the same as
    #   another label get the substring replaced, causing the rest of the label to not be replaced
    insertThese.sort(key=lambda t: len(t[0]), reverse=True) #* see https://stackoverflow.com/questions/19729928/python-sort-a-list-by-length-of-value-in-tuple

    labelNames = []
    lineNumbers = []

    for obj in insertThese: # get names of labels and their respective line numbers and put them into their own lists
        labelNames.append(obj[0])
        lineNumbers.append(obj[1])

    for line in oldLines: # then for every line in the file...
        if line.strip(" \n\t\r"): # if the line actually has something in it other than new lines and whitespace...
            if line[-1] == _LABELCHAR: # if the line is a label then essentially ignore it
                writeHere.append(f"#Label - {line}")
                continue

            for i in range(len(labelNames)): # for every label we replace it with its numerical value using str.replace()
                # print(f"#'{line}'            '{labelNames[i]}'        '{lineNumbers[i]}'")# debugging line
                if line == labelNames[i]:
                    line = ""
                    break

                line = line.replace(labelNames[i], str(lineNumbers[i])) # replacing it

            writeHere.append(line) #adding the final line onto the list we are writing to

class Macro: #macro definitions
    @staticmethod
    def STDLIBINC():
        return """a
        b
        c
        d
        e
        f
        g
        h
        i
        j
        k
        l
        m"""

    @staticmethod
    def RSWAP(): # swap the value of the registers about
        return f"""
        push a
        push b
        pop a
        pop b"""

    @staticmethod
    def MEMSWAP(arg1="ADDRESS1", arg2="ADDRESS2"): # swap the value of two memory locations about
        return f"""
        push a
        mov a {arg1}
        push a
        mov a {arg2}
        mov {arg1} a
        pop a
        mov {arg2} a
        pop a"""

    @staticmethod
    def INCA():
        return """
        push b
        push a
        lda 1
        push a
        pop b
        pop a
        add
        pop b"""

    @staticmethod
    def INCB():
        return """
        push a
        lda 1
        add
        push a
        pop b
        pop a"""

    @staticmethod
    def LDB(arg1="VALUE1"):
        return f"""
        push a
        lda {arg1}
        push a
        pop b
        pop a"""

    @staticmethod
    def SJSR(arg1="LABEL1"):
        return f"""
        push a
        push b
        jsr {arg1}"""

    @staticmethod
    def SRET(arg1="LABEL1"):
        return f"""
        pop b
        pop a
        ret"""


# just the name of every macro
macroNames = ["rswap",
              "mswap",
              "inca",
              "incb",
              "ldb",
              "sjsr",
              "sret",
              "_stdLib"
]

# has the function for every macro followed by how many arguments that macro's function takes
macroFuncs = [Macro. RSWAP,     0,
              Macro. MEMSWAP,   2,
              Macro. INCA,      0,
              Macro. INCB,      0,
              Macro. LDB,       1,
              Macro. SJSR,      1,
              Macro. SRET,      1,
              Macro. STDLIBINC, 0
]

if __name__ == "__main__":
    import sys
    import os

    if(len(sys.argv) < 3):
        print("need two arguments")
        print("input file, then output file")
        sys.exit(-1)

    if "-OW" in sys.argv:
        if os.path.exists(sys.argv[2]):
            os.remove(sys.argv[2])

    go(sys.argv[1], sys.argv[2])