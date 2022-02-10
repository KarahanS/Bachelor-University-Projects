.text
.globl main
main:

	la $t1, array     # $t1 = addressOf(array)
	addi $t5, $t5, 0  # index 
    lw $t2, 0($t1)    # $t2 stores maximum element (first element for now)
    mult $t2, $zero   # {hi, lo} = max_element * index

loop:
 	lw $t3, 0($t1)        # $t3 = value of the i(th) element in the array
	beq $t3, $zero, end   # if $t3 == 0, jump to end
    
    slt $t6, $t3, $t2             #  $t6 = $t3 < $t2 ? 1 : 0 ( $t3 >= $t2 --> 0)
    beq $t6, $zero, update        # if $t6 == 0, then update $t2
    j cont

update:
    add $t2, $zero, $t3  # $t2 = $t3 + 0
    mult $t2, $t5

cont:
	addi $t5, $t5, 1      # i++
    addi $t1, $t1, 4      # $t1 += 4 (word)
 	j loop		          # jump to loop

end:
    # mfhi $t7  # 11110000 (4 byte)
    mflo $t8  # 00001111 (4 byte)
    # sll $t7, $t7, 4
    # add $t8, $t8, $t7
    sw $t8, 0x10010130
  

 	li $v0, 10            # termination system call
 	syscall


.data

array:  .word 7 5 5 4 0
