/*
Julia set is given by Z_n+1 = Z_n^2 + C
so square a value, at a constant and just keep doing that

https://en.wikipedia.org/wiki/Julia_set

install this 
sudo apt-get install freeglut3-dev libglu1-mesa-dev libgl1-mesa-dev

and then compile with these flags 
-lglut -lGLU -lGL

*/
// CUDA book calls it C, but this is clearly a c++ class.
#include "../common/book.h"
#include "../common/cpu_bitmap.h"

#define DIM 1024

struct cuComplex{
    float r; // real 
    float i; // imaginary
    
    // behold a constructor! this is c++ lol
    __device__ cuComplex( float a, float b) : r(a), i(b) {}   
    __device__ float magnitude2 (void) { //__device__ runs on GPU
        return (r * r) + (i *i);
    }// its a square mag -- real mag needs a sqrt
    
    // define behavior of * and + operator on this type. 
    __device__ cuComplex operator * (const cuComplex& a){
        // complex numbers multiply by FOIL  https://en.wikipedia.org/wiki/Complex_number
        return cuComplex(r * a.r - i * a.i, i * a.r + r*a.i);
    }

    __device__ cuComplex operator + (const cuComplex& a){
        // complex numbers element wise sum 
        return cuComplex(r + a.r, i + a.i);
    }

};

// this is a device function only happens on the GPU
__device__ int julia(int x, int y){ // take a pixel coordinate as input
    const float scale = 1.5; // position scaling x and y to DIM for the image
    float jx = scale * (float) (DIM / 2 - x ) / (DIM / 2);
    float jy = scale * (float) (DIM / 2 - y) / (DIM / 2);

    cuComplex c(-0.8, 0.156); // complex number -- real + imaginary
    cuComplex a(jx, jy);

    int i = 0;
    for (i=0; i<200; i++){ // 200 iterations of julia set sequence
        a = a*a + c; // a^2 + C like in the equation up above
        if (a.magnitude2() >1000) // here we just threshold to see if this point is a julia set member
            return 0; // not in the set 
    }
    return 1; // yes in the set
}

__global__ void kernel(unsigned char *ptr){// basically at every pixel we compute 200 itterations of the julia sequence
    
    //GPU can look at threadIdx/BlockIdx 
    // so we are putting each pixel on a block idx 
    int x = blockIdx.x;
    int y = blockIdx.y;

    int offset = x + y * gridDim.x;
    int juliaValue = julia(x, y); // compute julia value - 0 or 1
            
    // now this is color mapping ... so it is RGB, 
    ptr[offset*4 + 0] = 0; // 0 or 255
    ptr[offset*4 + 1] = 255* juliaValue;
    ptr[offset*4 + 2] = 0;
    ptr[offset*4 + 3] = 255; // constant color channel max... interesting. 
}

// globals needed by the update routine
struct DataBlock {
    unsigned char   *dev_bitmap;
};


int main( void ){
   DataBlock   data;
    CPUBitmap bitmap( DIM, DIM, &data );
    unsigned char    *dev_bitmap;

    HANDLE_ERROR( cudaMalloc( (void**)&dev_bitmap, bitmap.image_size() ) );
    data.dev_bitmap = dev_bitmap;

    dim3    grid(DIM,DIM);
    kernel<<<grid,1>>>( dev_bitmap );

    HANDLE_ERROR( cudaMemcpy( bitmap.get_ptr(), dev_bitmap,
                              bitmap.image_size(),
                              cudaMemcpyDeviceToHost ) );
                              
    HANDLE_ERROR( cudaFree( dev_bitmap ) );
                              
    bitmap.display_and_exit();

    cudaFree(dev_bitmap);
}