#include <stdio.h>

#define SIZE 512

void matmul_asm(double* C, double* A, double* B)
{
  __asm(R"(
_Z6matmulPdS_S_:
        xorl    %eax, %eax
.Label4:
        leaq    (%rdi,%rax,8), %rcx
        movq    %rdx, %r10
        xorl    %r9d, %r9d
.Label3:
        movsd   (%rcx), %xmm0
        movq    %rsi, %r11
        xorl    %r8d, %r8d
.Label2:
        movsd   (%r11), %xmm1
        mulsd   (%r10,%r8,8), %xmm1
        incq    %r8
        addq    $4096, %r11
        addsd   %xmm1, %xmm0
        cmpq    $512, %r8
        jne     .Label2
        addl    $512, %r9d
        movsd   %xmm0, (%rcx)
        addq    $4096, %r10
        addq    $4096, %rcx
        cmpl    $262144, %r9d
        jne     .Label3
        incq    %rax
        addq    $8, %rsi
        cmpq    $512, %rax
        jne     .Label4
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
