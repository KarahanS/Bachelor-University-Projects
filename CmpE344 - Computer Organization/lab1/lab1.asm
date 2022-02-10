.text
.globl main
main:

	la $t1, array1
	la $t2, array2
	
loop:
 	lb $t3, 0($t1)     
	lb $t4, 0($t2)
	beq $t3, $zero, end
	sub $t5, $t3, $t4
	sb $t5, 0($t1)
	addi $t1, $t1, 1
	addi $t2, $t2, 1
 	j loop		        
end:
 	li $v0, 10
 	syscall

.data

array1:  .byte 41, 82, 25, 19, -7, -1, 6, 2, 0 
array2:  .byte 3, 2, 1, -9, -6, -3, 14, 15, 0
