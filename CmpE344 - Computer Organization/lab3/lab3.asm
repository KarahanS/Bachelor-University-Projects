.text
.globl main
main:
    li $s1,102;li $s2,103;li $s3,104  # every time the made_up procedure ends,
    li $s4,232;li $s5,232  # these registers’ original values must be restored
    li $s6,23;li $s7,12  # VALUES WILL CHANGE, use stack to store-restore
    
    addi $sp, $sp, -4
    sw   $ra, 0($sp)     # push($ra)
    li   $s0, 0          # $s0 = array indexer
main_loop:
    lw   $a0, A($s0)     # $a0 = A[$s0]
    beqz $a0, main_done  # end loop if A[$s0] == 0
    lw   $a1, B($s0)     # $a1 = B[$s0]
    jal  made_up         # $v0 = made_up($a0, $a1)
    sw   $v0, M($s0)     # M[$s0] = $v0
    addi $s0, $s0, 4     # $s0 += 4
    b    main_loop       # loop
main_done:
    sw   $zero, M($s0)   # mark the end of the array M
    lw   $ra, 0($sp)     # pop($ra)
    addi $sp, $sp, 4
    jr   $ra

# DO NOT CHANGE THE CODE ABOVE
made_up:
    # WRITE YOUR CODE HERE
    # set $a0 to the input of the fibonacci
    # a0
    addi $sp, $sp, -32
    sw $ra, 28($sp)
    sw $s1, 24($sp)
    sw $s2, 20($sp)
    sw $s3, 16($sp)
    sw $s4, 12($sp)
    sw $s5, 8($sp)
    sw $s6, 4($sp)
    sw $s7, 0($sp)


    #add $s4, $zero, $ra
    sub $s7, $a0, $a1   # s7 = a0 - a1
    add $s6, $zero, $a1  # store value of $a1
    jal fibonacci  # stored in $v0
    add $s1, $zero, $v0  # s1 = f(a0)
    add $a0, $zero, $s6  # a0 = a1
    jal fibonacci        # f(a1)
    add $s2, $zero, $v0
    add $a0, $zero, $s7
    jal fibonacci    # fibonacci(a0 - a1)
    add $s3, $zero, $v0   # ra jumps to here
    mult $s1, $s2
    mflo $s1   # s1 = f(a1) * f(a0)
    div $s1, $s3
    mflo $s5
    add $v0, $zero, $s5  # result


    lw $s7, 0($sp)
    lw $s6, 4($sp)
    lw $s5, 8($sp)
    lw $s4, 12($sp)
    lw $s3, 16($sp)
    lw $s2, 20($sp)
    lw $s1, 24($sp)
    lw $ra, 28($sp)
    addi $sp, $sp, 32

    jr $ra   # put the result into $v0
    
# DO NOT CHANGE THE CODE BELOW (you can change the data arrays)

fibonacci:
    li $a1,0;li $a2,0;li $a3,0;li $v1,0 # made_up procedure
    li $t1,0;li $t2,0;li $t3,0          # should not rely on these
    li $t4,0;li $t5,0;li $t6,0          # being preserved, because...
    li $t7,0;li $t8,0;li $t9,0  # all the temporaries are cleared!

    beqz $a0, fibonacci_zero  # fibonacci(0) = 0
    li   $t0, 0
    li   $v0, 1
fibonacci_loop:
    addi $a0, $a0, -1         # $a0 -= 1
    beqz $a0, fibonacci_done  # end loop if $a0 == 0
    add  $v0, $v0, $t0        # $v0 += $t0
    sub  $t0, $v0, $t0        # $t0 = $v0 - $t0
    b    fibonacci_loop       # loop
fibonacci_zero:
    li   $v0, 0
fibonacci_done:
    jr   $ra
.data
A: .word  2, 20, 17, 24, 0
B: .word  1, 6, 1, 23, 0
M: .word  0