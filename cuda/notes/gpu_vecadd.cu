#include<stdio.h>
#define N 10
// gpu function for adding -- you have each thread add one array element each. nice. 

__global__ void add(int *a, int *b, int *c){
    int tid = blockIdx.x;
    // dont need the while loop 
    if (tid < N){
        c[tid] = a[tid] + b[tid];
        printf("Hello from GPU thread %d!\n", tid);
    }
}

int main(void){
    // start CPU arrays
    int a[N] = {0};
    int b[N] = {0};
    int c[N] = {0};

    // pointers
    int *dev_a;
    int *dev_b;
    int *dev_c;

    // allocate memory
    cudaMalloc((void**) &dev_a, N * sizeof(int));
    cudaMalloc((void**) &dev_b, N * sizeof(int));
    cudaMalloc((void**) &dev_c, N * sizeof(int));

    // fill arrays on CPU
    for (int i=0; i<N; i++){
        a[i] = -i;
        b[i] = i*i;
    }
    // move a and b to GPU 
    cudaMemcpy(dev_a, a, N*sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b, b, N*sizeof(int), cudaMemcpyHostToDevice);

    // blocksize N, gridsize 1, getting N copies of the kernel on a 1d grid. . 
    add<<<N,1>>>(dev_a, dev_b, dev_c);
    // now copy back the result from the device to host ie GPU->CPU
    cudaMemcpy(c, dev_c, N * sizeof(int), cudaMemcpyDeviceToHost);

    // display
    for (int i=0; i<N; i++){
        printf("summing : %d + %d = %d\n", a[i], b[i], c[i]);
    }

    cudaFree(dev_a);
    cudaFree(dev_b);
    cudaFree(dev_c);

}