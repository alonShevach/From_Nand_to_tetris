// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/sort/Divide.asm

// The program input will be at R13,R14 while the result R13/R14 will be stored at R15.
// Don't change the input registers.
// The remainder should be discarded.
// You may assume both numbers are positive and larger than 0.
// The program should have a running time logarithmic with respect to the input. If a natural number 
// n is in R13 and a natural number m is in R14, then the complexity should be O(log(max(n, m))).

// R15=0
@R15
M=0 

// dividend = R13
@R13
D=M
@dividend // (16)
M=D 

// divisor = R14
@R14
D=M
@divisor // (17)
M=D 

// initialising the parameters:
@15
D=A
@iternum // (18)
M=D // num of iterations = 15
@i // (19)
M=0 // i=0
@result // the final division result. (20)
M=0 
@carry // the result of the last deduction (21)
M=0 
@lastnum // the dividend before the deduction (22)
M=0
@SHIFTLOOP
0;JMP

(SHIFTLOOP)
@iternum
D=M
@ZERO
D;JEQ 
@i
D=M-D
@DEVISION
D;JGE  // if i > iternum jump to DEVISION
@dividend
D=M
M=D>> // shifts right the dividend
@i
M=M+1
@SHIFTLOOP
0;JMP

(DEVISION)
	@lastnum
	D=M
	@dividend
	D=M-D // D = dividend af shifting - lastnum af shifting
@carry
M=M+D
D=M // adding the next number from the dividend to carry
@divisor
D=D-M
@SMALLER
D;JGE // if carry >= divisor: jump to GREATER

@GREATER
D;JLT // if carry < divisor: jump to SMALLER

(GREATER)
@result
D=M
M=D<< // shifting the result
@iternum
M=M-1
@carry
D=M
M=D<< // shifting the carry
@dividend
D=M
@lastnum
M=D // last num = the previous dividend
D=M
M=D<<
@i
M=0
@R13
D=M
@dividend
M=D
@SHIFTLOOP
0;JMP

(SMALLER)
@result
M=M+1
D=M
M=D<< // adding 1 to the result and shifting
@dividend
D=M
@lastnum
M=D // last num = the previous dividend
D=M
M=D<<
@carry
D=M
@divisor
D=D-M 
@carry
M=D
D=M
M=D<< // carry - divisor is shifted
@R13
D=M
@dividend 
M=D // dividend = the original dividend
@iternum
M=M-1
@i
M=0
@SHIFTLOOP
0;JMP

(ZERO)
@dividend
D=M
@lastnum
D=D-M
@result
D=M+D
M=D
@END
0;JMP

(END)
@result
D=M
@R15
M=D // R15 = result
@END
0;JMP

