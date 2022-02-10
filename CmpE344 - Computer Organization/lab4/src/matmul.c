#include <stdio.h>

#define SIZE 512

void matmul(double* C, double* A, double* B)
{
  for (int i = 0; i < SIZE; ++i){
    for (int j = 0; j < SIZE; ++j)
    {
      double cij = C[i+j*SIZE];
      for( int k = 0; k < SIZE; k++ )
      {
        cij += A[i+k*SIZE] * B[k+j*SIZE]; 
      }
      C[i+j*SIZE] = cij; 
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
  matmul(C, A, B);

  // debug_print_matrix(C);

  return 0;
}
