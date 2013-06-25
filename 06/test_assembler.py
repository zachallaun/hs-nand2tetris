#! /usr/local/bin/python

import unittest

import Assembler
class TestCExpressions(unittest.TestCase):
    def setUp(self):
        self.asm = Assembler.hackAssembler()
    
    def testIllegalFormat(self):
        in1 = 'JMP' # need to have somethign to left of ';'
        in2 = ';JMP' # need to have somethign to left of ';'
        in3 = 'D=' # need to have somethign to right of =
        in4 = 'D=;' # but this isnt enough
        in5 = 'D=;JMP' # and neither is this
        in6 = '=0' # not ok - both dest and jump are empty
        in7 = 'D' # not OK - need at least dest or jump

    def testIllegalJump(self):
        in1 = 'D;'
        self.assertRaises(Exception, self.asm.handle_c_expr, in1)
        in2 = 'D;JJJ'
        self.assertRaises(Exception, self.asm.handle_c_expr, in2)

    def testDestParse(self):
        # NB - as it stands, silently ignores dest commands
        # that contain at least one 'A', 'D' or 'M' but are
        # otherwise ill-formed
        dest1 = None
        out1 = self.asm.parse_dest(dest1)
        self.assertEqual('000', out1)
        dest2 = 'A'
        out2 = self.asm.parse_dest(dest2)
        self.assertEqual('100', out2)
        dest3 = 'D'
        out3 = self.asm.parse_dest(dest3)
        self.assertEqual('010', out3)
        dest4 = 'M'
        out4 = self.asm.parse_dest(dest4)
        self.assertEqual('001', out4)
        dest5 = 'AM'
        out5 = self.asm.parse_dest(dest5)
        self.assertEqual('101', out5)
        dest6 = 'AD'
        out6 = self.asm.parse_dest(dest6)
        self.assertEqual('110', out6)
        dest7 = 'AMD'
        out7 = self.asm.parse_dest(dest7)
        self.assertEqual('111', out7)
        dest8 = 'DM'
        out8 = self.asm.parse_dest(dest8)
        self.assertEqual('011', out8)

    def testJumpParse(self):
        # nominal jump commands
        cmd1 = None
        out1 = self.asm.parse_jump(cmd1)
        self.assertEqual('000', out1)
        cmd2 = 'JGT'
        out2 = self.asm.parse_jump(cmd2)
        self.assertEqual('001', out2)
        cmd3 = 'JEQ'
        out3 = self.asm.parse_jump(cmd3)
        self.assertEqual('010', out3)
        cmd4 = 'JGE'
        out4 = self.asm.parse_jump(cmd4)
        self.assertEqual('011', out4)
        cmd5 = 'JLT'
        out5 = self.asm.parse_jump(cmd5)
        self.assertEqual('100', out5)
        cmd6 = 'JNE'
        out6 = self.asm.parse_jump(cmd6)
        self.assertEqual('101', out6)
        cmd7 = 'JLE'
        out7 = self.asm.parse_jump(cmd7)
        self.assertEqual('110', out7)
        cmd8 = 'JMP'
        out8 = self.asm.parse_jump(cmd8)
        self.assertEqual('111', out8)
        
        # now for the illegal expressions...
        cmd9 = 'JMP2'
        self.assertRaises(Exception, self.asm.parse_jump, cmd9)
        cmd10 = 'asdf'
        self.assertRaises(Exception, self.asm.parse_jump, cmd10)

    def testCalcParse(self):
        #nominal calc commands
        clc1 = '1'
        out1 = self.asm.parse_calc(clc1)
        self.assertEqual('0111111', out1)
        clc2 = '0'
        out2 = self.asm.parse_calc(clc2)
        self.assertEqual('0101010', out2)
        clc3 = 'M'
        out3 = self.asm.parse_calc(clc3)
        self.assertEqual('1110000', out3)
        clc4 = 'A'
        out4 = self.asm.parse_calc(clc4)
        self.assertEqual('0110000', out4)
        clc5 = 'D'
        out5 = self.asm.parse_calc(clc5)
        self.assertEqual('0001100', out5)
        clc6 = 'A|D'
        out6 = self.asm.parse_calc(clc6)
        self.assertEqual('0010101', out6)
        clc7 = 'A&D'
        out7 = self.asm.parse_calc(clc7)
        self.assertEqual('0000000', out7)
        clc8 = 'M-1'
        out8 = self.asm.parse_calc(clc8)
        self.assertEqual('1110010', out8)
        clc9 = 'D-M'
        out9 = self.asm.parse_calc(clc9)
        self.assertEqual('1010011', out9)
        clc10 = 'M&D'
        out10 = self.asm.parse_calc(clc10)
        self.assertEqual('1000000', out10)

        # bad ones ...
        bad1 = 'A+M'
        self.assertRaises(Exception, self.asm.parse_calc, bad1)
        bad2 = 'A+M+D'
        self.assertRaises(Exception, self.asm.parse_calc, bad2)
        bad3 = '1+1'
        self.assertRaises(Exception, self.asm.parse_calc, bad3)

    # This is probably overkill ... 
    def testJumpCommand(self):
        # start with the good ones
        in0 = 'D=0'
        out0 = self.asm.handle_c_expr(in0)
        self.assertEqual(out0, ['1110101010010000'])
        in1 = 'D;JGT'
        out1 = self.asm.handle_c_expr(in1)
        self.assertEqual(out1, ['1110001100000001'])
        in2 = 'D;JEQ'
        out2 = self.asm.handle_c_expr(in2)
        self.assertEqual(out2, ['1110001100000010'])
        in3 = 'D;JGE'
        out3 = self.asm.handle_c_expr(in3)
        self.assertEqual(out3, ['1110001100000011'])
        in4 = 'D;JLT'
        out4 = self.asm.handle_c_expr(in4)
        self.assertEqual(out4, ['1110001100000100'])
        in5 = 'D;JNE'
        out5 = self.asm.handle_c_expr(in5)
        self.assertEqual(out5, ['1110001100000101'])
        in6 = 'D;JLE'
        out6 = self.asm.handle_c_expr(in6)
        self.assertEqual(out6, ['1110001100000110'])
        in7 = 'D;JMP'
        out7 = self.asm.handle_c_expr(in7)
        self.assertEqual(out7, ['1110001100000111'])
            
        
    # as a first step, I'm going to only parse assignments
    def testZeroAssignment(self):
        in1 = 'A=0'
        out1 = self.asm.handle_c_expr(in1)
        self.assertEqual(out1, ['1110101010100000'])
        in2 = 'D=0'
        out2 = self.asm.handle_c_expr(in2)
        self.assertEqual(out2, ['1110101010010000'])
        in3 = 'M=0'
        out3 = self.asm.handle_c_expr(in3)
        self.assertEqual(out3, ['1110101010001000'])
        in4 = 'ADM=0'
        out4 = self.asm.handle_c_expr(in4)
        self.assertEqual(out4, ['1110101010111000'])
        
# these are OK
# '=0;JMP' # computes 0, JMP
# '0;JMP' # same thing



# this tests A-epxressions without any vars
class TestAExpression(unittest.TestCase):
    def setUp(self):
        self.asm = Assembler.hackAssembler()

    def testNominal(self):
        in1 = '@2'
        out1 = self.asm.handle_a_expr(in1)
        self.assertEqual(out1, ['0000000000000010'])

        in2 = '@3'
        out2 = self.asm.handle_a_expr(in2)
        self.assertEqual(out2, ['0000000000000011'])

        in2 = '@20000'
        out2 = self.asm.handle_a_expr(in2)
        self.assertEqual(out2, ['0100111000100000'])

    # The provided assembler doesn't warn about this...
    def testOverflow(self):
        in1 = '@32768'
        self.assertRaises(Exception, self.asm.handle_a_expr, in1)

    def testVarNames(self):
        in1 = '@0f1'
        self.assertRaises(Exception, self.asm.handle_a_expr, in1)
        in2 = '@-1'
        self.assertRaises(Exception, self.asm.handle_a_expr, in2)


class TestVars(unittest.TestCase):
    def setUp(self):
        self.asm = Assembler.hackAssembler()

    # checks that next_addr increments as expected, and 
    # repeated variables get the same address
    def testSimple1(self):
        self.assertEqual(16, self.asm.next_addr)
        cmd1 = "@foo"
        out1 = self.asm.handle_a_expr(cmd1)
        self.assertEqual(17, self.asm.next_addr)
        self.assertEqual(['0000000000010000'], out1)
        cmd2 = "@bar"
        out2 = self.asm.handle_a_expr(cmd2)
        self.assertEqual(18, self.asm.next_addr)
        self.assertEqual(['0000000000010001'], out2)
        out3 = self.asm.handle_a_expr(cmd1)
        self.assertEqual(18, self.asm.next_addr)
        self.assertEqual(['0000000000010000'], out3)



# add A expressions with vars? 
# test this by defining variables in sequence, then checking their addresses
# will require turning the self.asm into a class s.t. it can keep track of  
# that state. 
# in1 = '@f00' # this one is ok
# in2 = '@foo'
# in3 = '@bar'

if __name__=="__main__":
    unittest.main()
