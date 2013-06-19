// nominal cases
@2 // testing that comments are removed correctly @5
@3
@20000
// and, out-of-bounds
@-1
@32768 // the provided assembler just considers the first variable name...
// which doesn't match the spec!
//non-numeric case (NYI!, but legal)
@foo  // 
@bar
//mixed variable names
@f00 //OK
@0f1 //NOT OK, but the provided assembler treats it as yet another variable! 
