import pyopencl as cl
from pyopencl import array
import numpy



def runParallel(vector, matrix, k, epsilon, ancho):

    ## Step #1. Obtain an OpenCL platform.
    platform = cl.get_platforms()[0]

    ## It would be necessary to add some code to check the check the support for
    ## the necessary platform extensions with platform.extensions

    ## Step #2. Obtain a device id for at least one device (accelerator).
    device = platform.get_devices()[1]
    print(platform.get_devices())

    ## It would be necessary to add some code to check the check the support for
    ## the necessary device extensions with device.extensions

    ## Step #3. Create a context for the selected device.
    context = cl.Context([device])

    ## Step #4. Create the accelerator program from source code.
    ## Step #5. Build the program.
    ## Step #6. Create one or more kernels from the program functions.

    program = cl.Program(context, open('paralelo.cl').read()).build()


    ## Step #7. Create a command queue for the target device.
    queue = cl.CommandQueue(context)

    ## Step #8. Allocate device memory and move input data from the host to the device memory.
    mem_flags = cl.mem_flags
    matrix_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=matrix)
    vector_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=vector)

    matrix_dot_vector = numpy.zeros(vector.shape[0], numpy.int32) #VECTOR DE LARGO N

    destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, matrix_dot_vector.nbytes)

    ## Step #9. Associate the arguments to the kernel with kernel object.
    ## Step #10. Deploy the kernel for device execution.

    program.isCore(queue, matrix_dot_vector.shape , None, vector_buf, matrix_buf, destination_buf,
                    numpy.int32(k), numpy.float32(epsilon), numpy.int32(ancho))

    ## Step #11. Move the kernel’s output data to host memory.
    cl.enqueue_copy(queue, matrix_dot_vector, destination_buf)

    ## Step #12. Release context, program, kernels and memory.
    ## PyOpenCL performs this step for you, and therefore,
    ## you don't need to worry about cleanup code


    program.isBorder(queue, matrix_dot_vector.shape, None, vector_buf, matrix_buf, destination_buf,
                     numpy.float32(epsilon), numpy.int32(ancho))

    cl.enqueue_copy(queue, matrix_dot_vector, destination_buf)

    return matrix_dot_vector

def runParallelNxN(vector, k, epsilon, ancho):

    ## Step #1. Obtain an OpenCL platform.
    platform = cl.get_platforms()[0]

    ## It would be necessary to add some code to check the check the support for
    ## the necessary platform extensions with platform.extensions

    ## Step #2. Obtain a device id for at least one device (accelerator).
    device = platform.get_devices()[1]
    print(platform.get_devices())

    ## It would be necessary to add some code to check the check the support for
    ## the necessary device extensions with device.extensions

    ## Step #3. Create a context for the selected device.
    context = cl.Context([device])

    ## Step #4. Create the accelerator program from source code.
    ## Step #5. Build the program.
    ## Step #6. Create one or more kernels from the program functions.

    program = cl.Program(context, open('paralelo.cl').read()).build()


    ## Step #7. Create a command queue for the target device.
    queue = cl.CommandQueue(context)

    ## Step #8. Allocate device memory and move input data from the host to the device memory.
    mem_flags = cl.mem_flags
    vector_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=vector)

    matrix_dot_vector = numpy.zeros(vector.shape[0], numpy.int32) #VECTOR DE LARGO N

    destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, matrix_dot_vector.nbytes)

    ## Step #9. Associate the arguments to the kernel with kernel object.
    ## Step #10. Deploy the kernel for device execution.

    program.isCoreNxN(queue, matrix_dot_vector.shape , None, vector_buf, destination_buf,
                    numpy.int32(k), numpy.float32(epsilon), numpy.int32(ancho))

    ## Step #11. Move the kernel’s output data to host memory.
    cl.enqueue_copy(queue, matrix_dot_vector, destination_buf)

    ## Step #12. Release context, program, kernels and memory.
    ## PyOpenCL performs this step for you, and therefore,
    ## you don't need to worry about cleanup code


    program.isBorderNxN(queue, matrix_dot_vector.shape, None, vector_buf, destination_buf,
                     numpy.float32(epsilon), numpy.int32(ancho))

    cl.enqueue_copy(queue, matrix_dot_vector, destination_buf)

    return matrix_dot_vector

if __name__ == "__main__":
    vector = numpy.zeros((1, 4), cl.array.vec.float2)
    matrix = numpy.zeros((4, 4), cl.array.vec.float2)
    matrix[0, 0] = (0, 1)
    matrix[0, 1] = (0, 2)
    matrix[0, 2] = (0, 3)
    matrix[0, 3] = (0, 4)
    matrix[1, 0] = (1, 1)
    matrix[1, 1] = (1, 2)
    matrix[1, 2] = (1, 3)
    matrix[1, 3] = (1, 4)
    matrix[2, 0] = (2, 1)
    matrix[2, 1] = (2, 2)
    matrix[2, 2] = (2, 3)
    matrix[2, 3] = (2, 4)
    matrix[3, 0] = (3, 1)
    matrix[3, 1] = (3, 2)
    matrix[3, 2] = (3, 3)
    matrix[3, 3] = (3, 4)

    vector[0, 0] = (0, 0)
    vector[0, 1] = (1, -1)
    vector[0, 2] = (2, -1)
    vector[0, 3] = (3, -1)

    k = 2
    epsilon = 2.0
    ancho = 4

    result = runParallel(vector, matrix, k, epsilon, ancho)
    print(result)