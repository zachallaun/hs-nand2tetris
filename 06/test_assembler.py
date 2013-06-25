#! /usr/local/bin/python

import unittest

import Assembler
class TestCExpressions(unittest.TestCase):
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
        self.assertRaises(Exception, Assembler.handle_c_expr, in1)
        in2 = 'D;JJJ'
        self.assertRaises(Exception, Assembler.handle_c_expr, in2)

    def testJumpParse(self):
        # nominal jump commands
        cmd1 = None
        out1 = Assembler.parse_jump(cmd1)
        self.assertEqual('000', out1)
        cmd2 = 'JGT'
        out2 = Assembler.parse_jump(cmd2)
        self.assertEqual('001', out2)
        cmd3 = 'JEQ'
        out3 = Assembler.parse_jump(cmd3)
        self.assertEqual('010', out3)
        cmd4 = 'JGE'
        out4 = Assembler.parse_jump(cmd4)
        self.assertEqual('011', out4)
        cmd5 = 'JLT'
        out5 = Assembler.parse_jump(cmd5)
        self.assertEqual('100', out5)
        cmd6 = 'JNE'
        out6 = Assembler.parse_jump(cmd6)
        self.assertEqual('101', out6)
        cmd7 = 'JLE'
        out7 = Assembler.parse_jump(cmd7)
        self.assertEqual('110', out7)
        cmd8 = 'JMP'
        out8 = Assembler.parse_jump(cmd8)
        self.assertEqual('111', out8)
        
        # now for the illegal expressions...
        cmd9 = 'JMP2'
        self.assertRaises(Exception, Assembler.parse_jump, cmd9)
        cmd10 = 'asdf'
        self.assertRaises(Exception, Assembler.parse_jump, cmd10)




#    def testJumpCommand(self):
        # start with the good ones
#        in0 = 'D=0'
#        out0 = Assembler.handle_c_expr(in0)
#        self.assertEqual(out0, ['0000101010010000'])
#        in1 = 'D;JGT'
#        out1 = Assembler.handle_c_expr(in1)
#        self.assertEqual(out1, ['0000101010010001'])
#        in2 = 'D;JEQ'
#        out2 = Assembler.handle_c_expr(in2)
#        self.assertEqual(out2, ['0000101010010010'])
#        in3 = 'D;JGE'
#        out3 = Assembler.handle_c_expr(in3)
#        self.assertEqual(out3, ['0000101010010011'])
#        in4 = 'D;JLT'
#        out4 = Assembler.handle_c_expr(in4)
#        self.assertEqual(out4, ['0000101010010100'])
#        in5 = 'D;JNE'
#        out5 = Assembler.handle_c_expr(in5)
#        self.assertEqual(out5, ['0000101010010101'])
#        in6 = 'D;JLE'
#        out6 = Assembler.handle_c_expr(in6)
#        self.assertEqual(out6, ['0000101010010110'])
#        in7 = 'D;JMP'
#        out7 = Assembler.handle_c_expr(in7)
#        self.assertEqual(out7, ['0000101010010111'])


    # as a first step, I'm going to only parse assignments
#    def testZeroAssignment(self):
#        in1 = 'A=0'
#        out1 = Assembler.handle_c_expr(in1)
#        self.assertEqual(out1, ['0000101010100000'])
#        in2 = 'D=0'
#        out2 = Assembler.handle_c_expr(in2)
#        self.assertEqual(out2, ['0000101010010000'])
#        in3 = 'M=0'
#        out3 = Assembler.handle_c_expr(in3)
#        self.assertEqual(out3, ['0000101010001000'])
#        in4 = 'ADM=0'
#        out4 = Assembler.handle_c_expr(in4)
#        self.assertEqual(out4, ['0000101010111000'])

        # these are OK
        # '=0;JMP' # computes 0, JMP
        # '0;JMP' # same thing



# this tests A-epxressions without any vars
class TestAExpression(unittest.TestCase):
    def testNominal(self):
        in1 = '@2'
        out1 = Assembler.handle_a_expr(in1)
        self.assertEqual(out1, ['0000000000000010'])

        in2 = '@3'
        out2 = Assembler.handle_a_expr(in2)
        self.assertEqual(out2, ['0000000000000011'])

        in2 = '@20000'
        out2 = Assembler.handle_a_expr(in2)
        self.assertEqual(out2, ['0100111000100000'])

    # The provided assembler doesn't warn about this...
    def testOverflow(self):
        in1 = '@32768'
        self.assertRaises(Exception, Assembler.handle_a_expr, in1)

    def testVarNames(self):
        in1 = '@0f1'
        self.assertRaises(Exception, Assembler.handle_a_expr, in1)

        in2 = '@-1'
        self.assertRaises(Exception, Assembler.handle_a_expr, in2)
        
# add A expressions with vars? 
# test this by defining variables in sequence, then checking their addresses
# will require turning the Assembler into a class s.t. it can keep track of  
# that state. 
# in1 = '@f00' # this one is ok
# in2 = '@foo'
# in3 = '@bar'

if __name__=="__main__":
    unittest.main()
