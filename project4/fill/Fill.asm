// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(KBCHECK)
@SCREEN
D=A
@address
M=D // address = SCREEN
@8192 
D=A 
@iternum
M=D // iternum = 8192
@i
M=0 // i = 0

@KBD
D=M
@BLACK
D;JNE // if D != 0: jump to BLACK

@WHITE
D;JEQ // if D == 0: jump to WHITE

(WHITE)
@n
M=0 
@LOOP
0;JMP

(BLACK)
@n
M=-1
@LOOP
0;JMP

(LOOP)
	@iternum
	D=M
@i
D=D-M 
@KBCHECK
D;JEQ // if i > iternum: jump to KBCHECK

@n
D=M
@address
A=M
M=D //RAM[SCREEN] = n

@i
M=M+1 // i++
@address
M=M+1 // address++
@LOOP
0;JMP 
