import struct
import scipy.io as io
import numpy as np

def writeA_sparse(A, filenameA, dtype='d'):
    '''
    dtype: 'd', double (8 bytes); 'f', float (4 bytes)
    '''
    num_rows, num_cols = A.shape
    nnz = A.nnz
    outS = len(A.indptr)

    innS = outS
    with open(filenameA, 'wb') as f:
        b = struct.pack('i', num_rows)
        f.write(b)
        b = struct.pack('i', num_cols)
        f.write(b)
        b = struct.pack('i', nnz)
        f.write(b)
        b = struct.pack('i', outS)
        f.write(b)
        b = struct.pack('i', innS)
        f.write(b)
        for i in range(nnz):
            b = struct.pack(dtype, A.data[i])
            f.write(b)
        for i in range(outS):
            b = struct.pack('i', A.indptr[i])
            f.write(b)
        for i in range(nnz):
            b = struct.pack('i', A.indices[i])
            f.write(b)

