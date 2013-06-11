// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.


// First, I'm going to figure out how to black the screen


// SCREEN and KBD are predefined to refer to RAM addresses 16384 (0x4000) and 24576 (0x6000),


// Need to have two states - blacking the screen and clearing
// the screen. If a key pressed, black; otherwise, clear
   
   // start by assuming no key pressed
   @WHITE
   0;JMP


(BLACK)
	// If key is no longer pressed, jump to white
	@KBD
	D=M // if no key pressed, d == 0
	@WHITE
	D; JEQ


	// Set one pixel to black
	@32767
	// setting D to what I think is the max value ... really, I want -1
	D=A 	
	@SCREEN
	M=D 

	@BLACK
	0; JMP

(WHITE)
	// before doing anythign else, check if a key pressed
	// if so, jump to BLACK
	@KBD
	D=M // if any key is pressed, d != 0
	@BLACK
	D; JNE 

	// set one pixel to white
	@0
	D=A
	@SCREEN
	M=D // setting 1st word of screen to 0's => white
	
	// need to continue drawing!
	@WHITE
	0; JMP
