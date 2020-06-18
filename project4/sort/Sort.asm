// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/sort/Sort.asm

// The program should sort the array starting at the address in R14 with length as specified in R15. 
// Don't change these registers.
// no assumptions can be made about the length of the array.
// You can assume that each value in the array (x) is -16384 < x < 16384.
// One can assume the array is allocated in the heap, meaning that the address in R14 is at least >= 2048, 
// and that R14 + R15 <= 16383.
// The sort is in descending order - the largest number at the head of the array.
// You can implement any sorting algorithm as long as it's runtime complexity is at most C*O(N^2).
// The sort works by the bubble sort.

@R15
D = M
@icount
M = D - 1 // icount = R15 - 1

@i
M = 0 // i = 0

(OUTER)
	@i
	D = M
	@icount
	D = M - D
	@END_OUTER
	D; JLE // if i >= R15-1: goto END_OUTER
	
	@R14
	D = M
	@j
	M = D // j = R14
	@jcount
	M = D // jcount = R14

	@icount
	D = M
	@i
	D = D - M
	@jcount
	M = M + D // jcount = R15 - 1 - i + R14
(INNER)
	@j
	D = M
	@jcount
	D = M - D
	@END_INNER
	D; JLE // if j >= R15-1-i + R14: goto END_INNER
	
	@j
	A = M
	D = M
	A = A + 1
	D = D - M
	@NO_SWAP
 	D; JGE // if RAM[j] >= RAM[j+1]: goto NO_SWAP

	@j
	A = M
	D = M
	@temp
	M = D // temp = RAM[j]

	@j
	A = M + 1
	D = M
	A = A - 1
	M = D // RAM[j] = RAM[j+1]

	@temp
	D = M
	@j
	A = M + 1
	M = D // RAM[j+1] = temp
(NO_SWAP)
	@j
	M = M + 1 // j++
	@INNER
	0; JMP // goto INNER	
(END_INNER)
	@i
	M = M + 1 // i++
	@OUTER
	0; JMP // goto OUTER

(END_OUTER)



