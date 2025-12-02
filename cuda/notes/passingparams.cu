#include <iostream>

// GPU function
__global__ void add(int a, int b, int *c){
    *c = a + b; 
}

// CPU function
int main( void ){
    int c;
    int *dev_c; 
    // GPU results need to live on the GPU so 
    cudaMalloc((void**) &dev_c, sizeof(int)); // allocate memory on GPU heap -- &dev_c is the adress of the pointer itself
    add<<<1,1>>>(2, 7, dev_c); // call the GPU funciton with a pointer to the
    cudaMemcpy(&c, dev_c, sizeof(int), cudaMemcpyDeviceToHost); // this brings the answer back from the GPU to the CPU
    
    printf("2 + 7 = %d\n", c);
    cudaFree(dev_c); // free to prevent memory leaks

    return 0;

}