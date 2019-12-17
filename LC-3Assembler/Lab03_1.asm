	.ORIG	x3000

	ST	R7, SaveR


GCD	NOT	R2, R1
	ADD	R2, R2, #1
	ADD	R2, R2, R0
	BRzp	SKIP1

	; swap R0 with R1, to make sure R0 >= R1
	AND	R3, R1, R1
	AND	R1, R0, R0
	AND	R0, R3, R3
	
	NOT	R2, R2		; let R2 = R0' - R1'= R1 - R0
	ADD	R2, R2, #1

SKIP1	AND	R1, R1, R1	; repeat until R1 == 0
	BRz	ENDGCD
	AND	R0, R2, R2
	BRnzp	GCD

ENDGCD	LD	R7, SaveR7
	HALT


SaveR7	.BLKW	#1

	.END
