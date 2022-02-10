#include <stdio.h>
#include <immintrin.h>

#define SIZE 512 // Must a multiple of 4
#define UNROLL 4 

void matmul(double* C, double* A, double* B){

  for ( int i = 0; i < SIZE; i+=UNROLL*4)
    for ( int j = 0; j < SIZE; j++ ) {
      __m256d c[4];
      for ( int x = 0; x < UNROLL; x++ ){
        c[x] = _mm256_load_pd(C+i+x*4+j*SIZE);
      }

      for( int k = 0; k < SIZE; k++ ){
        __m256d b = _mm256_broadcast_sd(B+k+j*SIZE);
        for (int x = 0; x < UNROLL; x++){
          c[x] = _mm256_add_pd(c[x],
          _mm256_mul_pd(_mm256_load_pd(A+SIZE*k+x*4+i), b));
        }
      }

      for ( int x = 0; x < UNROLL; x++ ){
        _mm256_store_pd(C+i+x*4+j*SIZE, c[x]);
      }
    }
}


void debug_print_matrix(double* matrix){  
  if(SIZE > 6){
    return; // Prevent printing large matrices. Use smaller SIZE when debugging.
  }
  for (int i = 0; i < SIZE; ++i){
    for (int j = 0; j < SIZE; ++j){
       printf("%-12f ", matrix[i+j*SIZE]);
    }
    printf("\n");
  }
}

int main(){

  double A[SIZE*SIZE] __attribute__((aligned(32))) = {0}; // Ensure alignment
  double B[SIZE*SIZE] __attribute__((aligned(32))) = {0}; // Ensure alignment
  double C[SIZE*SIZE] __attribute__((aligned(32))) = {0}; // Ensure alignment

  // init
  for (int i = 0; i < SIZE; ++i){
    for (int j = 0; j < SIZE; ++j){
      A[i+j*SIZE] = i*j+i+1;
      B[i+j*SIZE] = i*j+i+2;
      C[i+j*SIZE] = 0;
    }
  }

  // core
  matmul(C, A, B);

  // debug_print_matrix(C);

  return 0;
}
