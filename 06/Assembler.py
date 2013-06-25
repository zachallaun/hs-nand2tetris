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
def handle_a_expr(line):
    # I could error if it has any non-allowed symbold in the variable
    # name, but I'm avoiding that for now
    # "a user-defined symbol may be any combination of letters, digits, 
    # underscore (_), dot (.), dollar sign ($), and colon (:) 
    # that does not begin with a digit." (from Ch6)
    # re.search("\+|\-|\*|/|&|\||!|@", line[1:])
    # it's a hard-coded constant (all digits!), 
    # so no need to deal with variable names
    if line[1:].isdigit():
        decnum = int(line[1:])
        binnum = bin(decnum)[2:]
        # checking bounds!
        if (0 > decnum) or (decnum >= 2**15):
            raise Exception("Assembler: out-of-range assignment to A!:  " + line)
        numdigits = min(15, len(binnum))
        numzeros = 16-numdigits
        bincmd='0'*numzeros + binnum[-numdigits:]
    # TODO: check here for '(' which is the start of labels 
    #(which don't increment the line #)
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
def segment_c_expr(line):
    # if line contains '=', figure out what registers to assign to; otherwise, 
    if '=' in line:
        tokens = line.split('=')
        dest = tokens[0]
        line = tokens[1]
    else:
        dest = None
    if ';' in line:
        tokens = line.split(';')
        expr = tokens[0]
        jump = tokens[1]
    else:
        expr = line
        jump = None
    return (dest, expr, jump)

def parse_dest(dest):
    # TODO: Ignores poorly-formed dest commands
    if dest is None:
        destcmd = '000'
    else:
        if 'A' in dest:
            destcmd = destcmd + '1'
        else:
            destcmd = destcmd + '0'
        if 'D' in dest:
            destcmd = destcmd + '1'
        else:
            destcmd = destcmd + '0'
        if 'M' in dest:
            destcmd = destcmd + '1'
        else:
            destcmd = destcmd + '0'
    return destcmd

# parses jump command - raises Exception if bad command
def parse_jump(jump):
    if jump is None:
        jumpcmd = '000'
    elif jump == 'JGT':
        jumpcmd = '001'
    elif jump == 'JEQ':
        jumpcmd = '010'
    elif jump == 'JGE':
        jumpcmd = '011'
    elif jump == 'JLT':
        jumpcmd = '100'
    elif jump == 'JNE':
        jumpcmd = '101'
    elif jump == 'JLE':
        jumpcmd = '110'
    elif jump == 'JMP':
        jumpcmd = '111'
    else:
        raise Exception("Assembler: Illegal jump command: " + jump)
    return jumpcmd
    
# there are a limited number of allowed calculations ...
# so, effectively do a switch on them
def parse_calc(calc):
    return '0000000'

def handle_c_expr(line):
    dest, calc, jump = segment_c_expr(line)
    if calc is None:
        raise Exception("Assembler: c-command must have command: " + line)
    if calc == line:
        raise Excpetion("Assembler: c-command line must contain '=' or ';' ... " + line)

    destcmd = parse_dest(dest)
    jumpcmd = parse_jump(jump)
    calccmd = parse_calc(calc)
    
    bincmd = '000' + calccmd + destcmd + jumpcmd
    return bincmd
 



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
    print hackcode

    



