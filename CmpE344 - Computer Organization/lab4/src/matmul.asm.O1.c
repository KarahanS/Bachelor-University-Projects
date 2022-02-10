#include <stdio.h>

#define SIZE 512

void matmul_asm(double* C, double* A, double* B)
{
  __asm(R"(
_Z6matmulPdS_S_:
        pushq   %rbp
        pushq   %rbx
        movq    %rsi, %rcx
        movq    %rdx, %rbx
        movq    %rsi, %r9
        addq    $2097152, %rcx
        movq    %rdi, %r11
        movl    $0, %ebp
        leaq    2097152(%rdx), %r10
        jmp     .Label4
.Label10:
        movsd   %xmm1, (%r8)
        addq    $4096, %rsi
        addq    $4096, %rdi
        cmpq    %r10, %rdi
        je      .Label9
.Label3:
        movq    %rsi, %r8
        movsd   (%rsi), %xmm1
        movq    %rdi, %rdx
        movq    %r9, %rax
.Label2:
        movsd   (%rax), %xmm0
        mulsd   (%rdx), %xmm0
        addsd   %xmm0, %xmm1
        addq    $4096, %rax
        addq    $8, %rdx
        cmpq    %rcx, %rax
        jne     .Label2
        jmp     .Label10
.Label9:
        addl    $1, %ebp
        addq    $8, %r9
        addq    $8, %rcx
        addq    $8, %r11
        cmpl    $512, %ebp
        je      .Label11
.Label4:
        movq    %rbx, %rdi
        movq    %r11, %rsi
        jmp     .Label3
.Label11:
        popq    %rbx
        popq    %rbp
  )");
}

int main(){

  double A[SIZE*SIZE]; 
  double B[SIZE*SIZE];
  double C[SIZE*SIZE];

  // init
  for (int i = 0; i < SIZE; ++i){
    for (int j = 0; j < SIZE; ++j){
      A[i+j*SIZE] = i*j+i+1;
      B[i+j*SIZE] = i*j+i+2;
      C[i+j*SIZE] = 0;
    }
  }

  // core
  matmul_asm(C, A, B);

  return 0;
}
