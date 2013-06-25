#! /usr/local/bin/python

import unittest

import Assembler

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
