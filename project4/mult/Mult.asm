// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@R2
M=0
@R0
D=M
@n
M=D
@R1
D=M
@num
M=D
@i
M=1
@mul
M=0
@LOOP
0;JMP

(LOOP)
	@i
	D=M
	@n
	D=D-M
	@STOP
	D;JGT
	
	@num
	D=M
	@mul
	M=D+M
	
	@i
	M=M+1
	@LOOP
	0;JMP
	
(STOP)
	@mul
	D=M
	@R2
	M=D

(END)
	@END
	0;JMP
