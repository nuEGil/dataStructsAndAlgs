#include <iostream>
#include <cstdio>

// GPU code
__global__ void kernel() {
    printf("Hello from GPU thread %d!\n", threadIdx.x);
}
// CPU code
int main() {
    kernel<<<1, 4>>>();
    cudaDeviceSynchronize();
    printf("Hello from CPU\n");
    return 0;
}