#! /usr/local/bin/python

import re

infile = open('test.asm', 'r')

# In hack's assembly language, @# indicates that the 
# input number should be written to the A register
# The equivalent machine language representation is
# '0' then 15 digits of # in binary (ignoring overflow)
#
# Symbols may be used in place of the '#'
#
# I assume that I should be raising exceptions rather than printing
# errors, but I'm being lazy for debugging while I look up the 
# required python functions. I'll refactor later
#
# This has to return the binary translation, b/c
def handle_a_expr(line):
    bincmd = '0'*16

    # I could error if it has any non-allowed symbold in the variable
    # name, but I'm avoiding that for now
    # "a user-defined symbol may be any combination of letters, digits, 
    # underscore (_), dot (.), dollar sign ($), and colon (:) 
    # that does not begin with a digit." (from Ch6)
    # re.search("\+|\-|\*|/|&|\||!|@", line[1:])

    # it's a hard-coded constant, no need to deal with variable names
    if line[1:].isdigit():
        decnum = int(line[1:])
        binnum = bin(decnum)[2:]
        # checking bounds!
        if (0 > decnum) or (decnum >= 2**15):
            raise Exception("Assembler: out-of-range assignment to A!:  " + line)
        numdigits = min(15, len(binnum))
        numzeros = 16-numdigits
        bincmd='0'*numzeros + binnum[-numdigits:]
    else:
        # TODO: better way to set allowed symbols/characters?
        if line[1].isdigit() or line[1] in ['-', '*', '+', '/']:
            raise Exception("Assembler: illegal variable name:  " + line)
        print "Assembler: Variables NYI!: " + line
    return [bincmd]

# Questions:
# * Can multiple registers be set as the output of an assignment?
#    e.g.: A,D=D+1. => Yup! MD=D+1
#
# I'm building this up incrementally, starting w/ single 

# NB - format of a C expr is
# x=y;JMP
def handle_c_expr(line):
    bincmd = '0'*16
    return [line]

    # check that it contains '=' or ';' - otherwise, it's an invalid expression

    # if line contains '=', figure out what registers to assign to; otherwise, 
    # bincmd[3, 4, 5] = 0  (split on =, registers are before it, rest of cmd is after)

    # if line contains ';', figure out what the jump is and fill in bincmd [0, 1, 2]
 



if __name__ == "__main__":

    # First, I'm trying to strip out all whitespace and comments
    cleanlines = []
    for line in infile:
        tokens = re.split(r"//", line)
        cleaned = re.sub("\n|\r|\t| ", "", tokens[0])
        if cleaned != '':
            cleanlines.append(cleaned)
    infile.close()
    print cleanlines

    # next step is handling all of the A-commands
    print("\n\n  Assembling:\n")
    outfile = open('test.hack', 'w');
    hackcode = []
    for line in cleanlines:
        print line
        if line[0] == '@':
            cmd = handle_a_expr(line)
            hackcode.append(cmd)
        else:
            cmd = handle_c_expr(line)
            hackcode.append(cmd)

        print cmd

    



