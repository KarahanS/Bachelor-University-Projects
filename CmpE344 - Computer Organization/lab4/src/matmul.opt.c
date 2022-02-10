#include <stdio.h>
#include <immintrin.h>

#define SIZE 512 // Must a multiple of 4

void matmul(double* C, double* A, double* B) {
  for ( size_t i = 0; i < SIZE; i+=4 ){
    for ( size_t j = 0; j < SIZE; j++ ) {
      __m256d c0 = _mm256_load_pd(C+i+j*SIZE);
      for( size_t k = 0; k < SIZE; k++ )
        c0 = _mm256_add_pd(c0, /* c0 += A[i][k]*B[k][j] */
              _mm256_mul_pd(_mm256_load_pd(A+i+k*SIZE),
              _mm256_broadcast_sd(B+k+j*SIZE)));

      _mm256_store_pd(C+i+j*SIZE, c0); /* C[i][j] = c0 */

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
