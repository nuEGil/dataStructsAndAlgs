# This is just a template file to use assuming you have src/main.cu 

cmake_minimum_required(VERSION 3.24)
project(cuda_project LANGUAGES C CXX CUDA)

# Require a minimum CUDA version if you want (optional)
# find_package(CUDAToolkit 11.0 REQUIRED)

# Create executable from .cu files
add_executable(cuda_project src/main.cu)

# Enable proper device linking if you split code across files
set_target_properties(cuda_project PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
)

# Optimization flags (optional)
target_compile_options(cuda_project PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:
    -O3
>)
