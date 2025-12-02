# working through book samples 
CUDA by Example: an Introductions to general purpose GPU programming - Jason Sanders, Edward Kandrot, 2010. 

but im using nvcc 11, and gcc 11

## Installation
Visual studio latest version does not have support for cuda -- would have to install an older version. Use VSCode because it does have support.

C/C++ and NVCC compilers will make you an executable for whatever OS you are on, so if I compile it on windows it wont run on linux - multiplatform cuda uses CMake . So keep a version of cuda toolkit on windows, but keep a version on wsl2 to go with gcc -- inside wsl2 

    sudo apt install build-essential 
    sudo apt install nvidia-cuda-toolkit

then you should have these to use.  
    nvcc --version 
    nvidia-smi
    gcc --version 

## Compiling and cmake(optional just be aware)

Need to compile CPU code and compile GPU code. nvcc compiles .cu files. Compile with 

    nvcc file.cs -o executable.exe

cuda code is c++ code by default, but you can force c mode with 

    nvcc -x cu -Xcompiler "-x c" file.cu -o app.exe

CMake instructions with that cmake list text -- assumes you have 
cuda_project/
    CMakeLists.txt
    src/
        main.cu

commands       
    mkdir build
    cd build
    cmake ..
    cmake --build .
    ./cuda_project

## code notes 
CUDA kerel is a function that runs on gpu and is executed by many threads in parallel. define it like this 

    __global__ void kernel(void){}

Call the kernel with 
    
    kernel<<<1,1>>>(); 

<<<gridSize, blockSize>>>


cudaMalloc -- memory allocation on the gpu 
cudaMemcpy -- copy information between host and device -- per doc its (*dst, *src, kind) - in the passing example i happen to use cudaMemcpyDeviceToHost so move data back from GPU to the host cpu

cudaFree -- release allocated memory - remember this prevents memory leaks. 

rules 
    * can pass pointers allocated with cudaMalloc() to functions that execute on the device
    * can use pointers allocated with cudaMalloc() to read or write memory from code that executs on the device -- this is cudamemcpy() 
    * can pass pointers allocated with cudaMalloc() to functions that execute on the host.
    * cannot use pointers allocated with cudaMalloc() to read or write memory from code that executes on host.


this literally means cudaMalloc is used for these things
device kernel __global__ 
device only functions  __device__
to host functions __host__ / normal C/C++

you can only dereference (read/write) cudaMalloc pointer on the GPU.....

dont mix malloc() calloc() free() with  cudaMalloc() and cudaFree().... stick with cuda functions 

Kernels return a status code visible to the runtime API..... 
__global__ void add(int a, int b, int *c) -- this just keeps data on the GPU no return value - unsure which thread.... but 

__device__ int helper(int x){
    return x+1; // GPU -> CPU only. 
}

cudaGetDeviceCOunt(&count);
cudaDeviceProp struct can be found at  
https://docs.nvidia.com/cuda/cuda-runtime-api/structcudaDeviceProp.html#structcudaDeviceProp