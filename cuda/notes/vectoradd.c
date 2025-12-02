#include<stdio.h>
#define N 150

void add(int *a, int *b, int *c){
    int tid = 0;
    while (tid < N){
        c[tid] = a[tid] + b[tid];
        tid += 1; // only have one cpu -- increment ends the while loop
    }
}

int main(void){
    // initialize arrays with 0s.
    int a[N] = {0};
    int b[N] = {0};
    int c[N] = {0};
    
    // overwrite for actual values -a and b^2
    for (int i=0; i<N; ++i){
        a[i] = -i;
        b[i] = i * i;
    }

    add(a, b, c); // arrays have pointers to their first element... 
    for (int i=0; i<N; ++i){
        printf(" summing : %d + %d = %d\n", a[i], b[i], c[i]);

    }

}