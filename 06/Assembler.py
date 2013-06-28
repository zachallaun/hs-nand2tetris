#! /usr/local/bin/python

import re
import sys

class hackAssembler():

    def __init__(self):
        # Where we store the labels and variables
        # TODO: Actually, it might make more sense to have separate dicts?
        # @_label_ isn't followed immeidately by a jump ...
        # initialize w/ the predefined symbols
        self.vardict = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
                        'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5,
                        'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11':11,
                        'R12':12, 'R13':13, 'R14':14, 'R15':15,
                        'SCREEN':16384, 'KBD':24576}
        # if we encounter a label this is the line that it'll refer to
        #next_line = 1
        # if we encounter a variable name, this is the address it'll get
        self.next_addr = 16

    # generates the appropriate a command from a given int
    def cmd_from_num(self, num):
        if (0 > num) or (num >= 2**15):
            raise Exception("Assembler: out-of-range assignment to A!:  " + line)
        return '{:016b}'.format(num)

    # returns whether or not the input string is a legal variable namex
    # TODO: better way to set allowed symbols/characters?
    def is_legal_var_name(self, str):
        illegal_chars = {'-', '*', '+', '/', '&', '|', '!'}
        return not (str[0].isdigit() or
                    any((c in illegal_chars) for c in str))

    # line[0] will be '@'
    def handle_a_expr(self, line):
        if line[1:].isdigit():
            decnum = int(line[1:])
            bincmd = self.cmd_from_num(decnum)
        # TODO: check here for '(' which is the start of labels
        #(which don't increment the line #)
        elif self.is_legal_var_name(line[1:]):
            # TODO: define this earlier?
            varname = line[1:]
            if varname in self.vardict.keys():
                addr = self.vardict[varname]
                bincmd = self.cmd_from_num(addr)
            else:
                bincmd = self.cmd_from_num(self.next_addr)
                self.vardict[varname] = self.next_addr;
                self.next_addr += 1;
                # TODO: check that we haven't overflowed our available memory?

        else:
            raise Exception("Assembler: illegal variable name:  " + line)

        return [bincmd]



    # NB - format of a C expr is
    # x=y;JMP
    def segment_c_expr(self, line):
        m = re.match(r'((?P<dest>.*)=)?(?P<expr>[^;]*)(;(?P<jump>.*))?',
                     line).groupdict()
        return (m['dest'], m['expr'], m['jump'])

    def parse_dest(self, dest):
        # TODO: Ignores poorly-formed dest commands
        if dest is None:
            return '000'
        else:
            return ''.join('1' if c in dest else '0'
                           for c in ['A', 'D', 'M'])

    # parses jump command - raises Exception if bad command
    def parse_jump(self, jump):
        jumps = { None: '000', 'JGT': '001', 'JEQ': '010',
                 'JGE': '011', 'JLT': '100', 'JNE': '101',
                 'JLE': '110', 'JMP': '111' }
        if jump in jumps:
            return jumps[jump]
        else:
            raise Exception("Assembler: Illegal jump command: " + jump)

    def parse_calc(self, calc):
        calc_cmds = {'0':   '0101010',
                     '1':   '0111111',
                     '-1':  '0111010',
                     'D':   '0001100',
                     'A':   '0110000',
                     '!D':  '0001101',
                     '!A':  '0110001',
                     '-D':  '0001111',
                     '-A':  '0110011',
                     'D+1': '0011111',
                     '1+D': '0011111',
                     'A+1': '0110111',
                     '1+A': '0110111',
                     'D-1': '0001110',
                     'A-1': '0110010',
                     'D+A': '0000010',
                     'A+D': '0000010',
                     'D-A': '0010011',
                     'A-D': '0000111',
                     'D&A': '0000000',
                     'A&D': '0000000',
                     'D|A': '0010101',
                     'A|D': '0010101',
                     'M':   '1110000',
                     '!M':  '1110001',
                     '-M':  '1110011',
                     'M+1': '1110111',
                     '1+M': '1110111',
                     'M-1': '1110010',
                     'D+M': '1000010',
                     'M+D': '1000010',
                     'D-M': '1010011',
                     'M-D': '1000111',
                     'D&M': '1000000',
                     'M&D': '1000000',
                     'D|M': '1010101',
                     'M|D': '1010101'}

        if calc in calc_cmds:
            return calc_cmds[calc]
        else:
            raise Exception("Assembler: illegal calculation: " + calc)

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

    # this function assumes that the input is an array of lines,
    # some of which will be labels.
    # it returns an array w/ the labels removed and their appropriate
    # line numbers added to the vardict
    def handle_labels(self, inlines):
        outlines = []
        # if we have a label, this will be the line it refers to (0-indexed)
        next_line = 0
        for line in inlines:
            # if it's a label
            if line[0] == '(' and line[-1] == ')':
                labelname = line[1:-1]
                if labelname in self.vardict.keys():
                    raise Exception("Assembler: attempted to add already-existing label: " + line)
                self.vardict[labelname] = next_line
            else:
                next_line += 1
                outlines.append(line)
        return outlines


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

    # command line arguments!
    args = sys.argv
    if len(args) != 3:
        print "Usage: ./Assembler.py infile outfile"
        exit

    infile = args[1]
    outfile = args[2]

    # I'm doing this in two passes - the first to get all labels assigned,
    # the second to properly encode all the asm->hack commands
    # NB - unless I misunderstand how this is supposed to work, @label will
    # have really weird behavior if it's not followed by 0;JMP
    # todo: I think this is kinda ugly ... I'm not happy w/ which functions
    #     are class member functions
    cleanlines = clean_file(infile)
    myassembler = hackAssembler()
    codelines = myassembler.handle_labels(cleanlines)

    hackcode = []
    for line in codelines:
        if line[0] == '@':
            cmd = myassembler.handle_a_expr(line)
            hackcode.append(cmd)
        else:
            cmd = myassembler.handle_c_expr(line)
            hackcode.append(cmd)

    outfile = open(outfile, 'w');
    for cmd in hackcode:
        outfile.write(cmd[0] + '\n')
    outfile.close()
