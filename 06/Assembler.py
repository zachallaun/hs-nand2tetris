#! /usr/local/bin/python

import re

class hackAssembler():

    def __init__(self):
        # Where we store the labels and variables
        # TODO: Actually, it might make more sense to have separate dicts?
        # @_label_ isn't followed immeidately by a jump ... 
        vardict = {}
        # if we encounter a label this is the line that it'll refer to
        next_line = 1
        # if we encounter a variable name, this is the address it'll get
        next_addr = 16

    def handle_a_expr(self, line):
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
            if line[1].isdigit() or line[1] in ['-', '*', '+', '/', '&', '|', '!']:
                raise Exception("Assembler: illegal variable name:  " + line)
            print "Assembler: Variables NYI!: " + line
        return [bincmd]

    # NB - format of a C expr is
    # x=y;JMP
    def segment_c_expr(self, line):
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

    def parse_dest(self, dest):
        # TODO: Ignores poorly-formed dest commands
        if dest is None:
            destcmd = '000'
        else:
            destcmd = ''
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
    def parse_jump(self, jump):
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
    # so, effectively do a switch on them. This feels dirty.
    def parse_calc(self, calc):
        if calc == '0':
            calccmd = '0101010'
        elif calc == '1':
            calccmd = '0111111'
        elif calc == '-1':
            calccmd = '0111010'
        elif calc == 'D':
            calccmd = '0001100'
        elif calc == 'A':
            calccmd = '0110000'
        elif calc == '!D':
            calccmd = '0001101'
        elif calc == '!A':
            calccmd = '0110001'
        elif calc == '-D':
            calccmd = '0001111'
        elif calc == '-A':
            calccmd = '0110011'
        elif calc == 'D+1' or calc == '1+D':
            calccmd = '0011111'
        elif calc == 'A+1' or calc == '1+A':
            calccmd = '0110111'
        elif calc == 'D-1':
            calccmd = '0001110'
        elif calc == 'A-1':
            calccmd = '0110010'
        elif calc == 'D+A' or calc == 'A+D':
            calccmd = '0000010'
        elif calc == 'D-A':
            calccmd = '0010011'
        elif calc == 'A-D':
            calccmd = '0000111'
        elif calc == 'D&A' or calc == 'A&D':
            calccmd = '0000000'
        elif calc == 'D|A' or calc == 'A|D':
            calccmd = '0010101'
        elif calc == 'M':
            calccmd = '1110000'
        elif calc == '!M':
            calccmd = '1110001'
        elif calc == '-M':
            calccmd = '1110011'
        elif calc == 'M+1' or calc == '1+M':
            calccmd = '1110111'
        elif calc == 'M-1':
            calccmd = '1110010'
        elif calc == 'D+M' or calc == 'M+D':
            calccmd = '1000010'
        elif calc == 'D-M':
            calccmd = '1010011'
        elif calc == 'M-D':
            calccmd = '1000111'
        elif calc == 'D&M' or calc == 'M&D':
            calccmd = '1000000'
        elif calc == 'D|M' or calc == 'M|D':
            calccmd = '1010101'
        else:
            raise Exception("Assembler: illegal calculation: " + calc)
        return calccmd

    def handle_c_expr(self, line):
        dest, calc, jump = self.segment_c_expr(line)
        if calc is None:
            raise Exception("Assembler: c-command must have command: " + line)
        if calc == line:
            raise Excpetion("Assembler: c-command line must contain '=' or ';' ... " + line)

        destcmd = self.parse_dest(dest)
        jumpcmd = self.parse_jump(jump)
        calccmd = self.parse_calc(calc)
    
        bincmd = '111' + calccmd + destcmd + jumpcmd
        return [bincmd]
 
# preprocessing, not part of the assembler itself
def clean_file(filename):
    infile = open(filename, 'r')
    # First, I'm trying to strip out all whitespace and comments
    cleanlines = []
    for line in infile:
        tokens = re.split(r"//", line)
        cleaned = re.sub("\n|\r|\t| ", "", tokens[0])
        if cleaned != '':
            cleanlines.append(cleaned)
    infile.close()
    return cleanlines


if __name__== "__main__":

    cleanlines = clean_file('test.asm')

    # I'm doing this in two passes - the first to get all labels assigned,
    # the second to properly encode all the asm->hack commands
    # NB - unless I misunderstand how this is supposed to work, @label will
    # have really weird behavior if it's not followed by 0;JMP
    myassembler = hackAssembler()


    # next step is handling all of the A-commands
    print("\n\n  Assembling:\n")

    hackcode = []
    for line in cleanlines:
        print line
        if line[0] == '@':
            cmd = myassembler.handle_a_expr(line)
            hackcode.append(cmd)
        else:
            cmd = myassembler.handle_c_expr(line)
            hackcode.append(cmd)
        print cmd

    outfile = open('test.hack', 'w');
    for cmd in hackcode:
        outfile.write(cmd[0] + '\n')
    outfile.close()

    



