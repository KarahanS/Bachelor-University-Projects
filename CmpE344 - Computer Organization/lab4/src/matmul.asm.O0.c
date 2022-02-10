#include <stdio.h>

#define SIZE 512

void matmul_asm(double* C, double* A, double* B)
{
  __asm(R"(
_Z6matmulPdS_S_:
        pushq   %rbp
        movq    %rsp, %rbp
        movq    %rdi, -40(%rbp)
        movq    %rsi, -48(%rbp)
        movq    %rdx, -56(%rbp)
        movl    $0, -4(%rbp)
.Label7:
        cmpl    $511, -4(%rbp)
        jg      .Label8
        movl    $0, -8(%rbp)
.Label6:
        cmpl    $511, -8(%rbp)
        jg      .Label3
        movl    -8(%rbp), %eax
        sall    $9, %eax
        movl    %eax, %edx
        movl    -4(%rbp), %eax
        addl    %edx, %eax
        cltq
        leaq    0(,%rax,8), %rdx
        movq    -40(%rbp), %rax
        addq    %rdx, %rax
        movsd   (%rax), %xmm0
        movsd   %xmm0, -16(%rbp)
        movl    $0, -20(%rbp)
.Label5:
        cmpl    $511, -20(%rbp)
        jg      .Label4
        movl    -20(%rbp), %eax
        sall    $9, %eax
        movl    %eax, %edx
        movl    -4(%rbp), %eax
        addl    %edx, %eax
        cltq
        leaq    0(,%rax,8), %rdx
        movq    -48(%rbp), %rax
        addq    %rdx, %rax
        movsd   (%rax), %xmm1
        movl    -8(%rbp), %eax
        sall    $9, %eax
        movl    %eax, %edx
        movl    -20(%rbp), %eax
        addl    %edx, %eax
        cltq
        leaq    0(,%rax,8), %rdx
        movq    -56(%rbp), %rax
        addq    %rdx, %rax
        movsd   (%rax), %xmm0
        mulsd   %xmm1, %xmm0
        movsd   -16(%rbp), %xmm1
        addsd   %xmm1, %xmm0
        movsd   %xmm0, -16(%rbp)
        addl    $1, -20(%rbp)
        jmp     .Label5
.Label4:
        movl    -8(%rbp), %eax
        sall    $9, %eax
        movl    %eax, %edx
        movl    -4(%rbp), %eax
        addl    %edx, %eax
        cltq
        leaq    0(,%rax,8), %rdx
        movq    -40(%rbp), %rax
        addq    %rdx, %rax
        movsd   -16(%rbp), %xmm0
        movsd   %xmm0, (%rax)
        addl    $1, -8(%rbp)
        jmp     .Label6
.Label3:
        addl    $1, -4(%rbp)
        jmp     .Label7
.Label8:
        nop
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
