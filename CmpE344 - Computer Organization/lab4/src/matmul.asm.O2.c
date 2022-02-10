#include <stdio.h>

#define SIZE 512

void matmul_asm(double* C, double* A, double* B)
{
  __asm(R"(
_Z6matmulPdS_S_:
        pushq   %rbx
        movq    %rdx, %r11
        movq    %rsi, %r8
        leaq    2097152(%rsi), %rcx
        movq    %rdi, %r10
        xorl    %ebx, %ebx
        leaq    2097152(%rdx), %r9
.Label4:
        movq    %r11, %rdi
        movq    %r10, %rsi
.Label3:
        movsd   (%rsi), %xmm1
        movq    %rdi, %rdx
        movq    %r8, %rax
.Label2:
        movsd   (%rax), %xmm0
        mulsd   (%rdx), %xmm0
        addq    $4096, %rax
        addq    $8, %rdx
        addsd   %xmm0, %xmm1
        cmpq    %rax, %rcx
        jne     .Label2
        addq    $4096, %rdi
        movsd   %xmm1, (%rsi)
        addq    $4096, %rsi
        cmpq    %rdi, %r9
        jne     .Label3
        addl    $1, %ebx
        addq    $8, %r8
        addq    $8, %rcx
        addq    $8, %r10
        cmpl    $512, %ebx
        jne     .Label4
        popq    %rbx
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
