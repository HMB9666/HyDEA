import struct
import numpy as np
import scipy.sparse as sparse


def readA_sparse(filenameA, dtype='d', sparse_type='csr', shape=None):
    '''
    dtype: 'd', double (8 bytes); 'f', float (4 bytes)
    '''
    cols = []
    outerIdxPtr = []
    rows = []
    if dtype == 'd':
        len_data = 8
    elif dtype == 'f':
        len_data = 4
    #reading the bit files
    with open(filenameA, 'rb') as f:
        length = 4
        b = f.read(length)
        num_rows = struct.unpack('i', b)[0]
        b = f.read(length)
        num_cols = struct.unpack('i', b)[0]
        b = f.read(length)
        nnz = struct.unpack('i', b)[0]
        b = f.read(length)
        outS = struct.unpack('i', b)[0]
        b = f.read(length)
        innS = struct.unpack('i', b)[0]
        data = [0.0] * nnz
        outerIdxPtr = [0]*outS
        cols = [0]*nnz
        rows = [0]*nnz
        for i in range(nnz):
            b = f.read(len_data)
            data[i] = struct.unpack(dtype, b)[0]
        for i in range(outS): # Index pointer
            length = 4
            b = f.read(length)
            outerIdxPtr[i] = struct.unpack('i', b)[0]
        for i in range(nnz): # Col index
            length = 4
            b = f.read(length)
            cols[i] = struct.unpack('i', b)[0]
    outerIdxPtr = outerIdxPtr + [nnz]
    for ii in range(num_rows):
        rows[outerIdxPtr[ii]:outerIdxPtr[ii+1]] = [ii]*(outerIdxPtr[ii+1] - outerIdxPtr[ii])

    if shape is None:
        shape = [num_rows, num_cols]
    if sparse_type.lower() == 'csr':
        return sparse.csr_matrix((data, (rows, cols)), dtype=dtype, shape=shape)
    elif sparse_type.lower() == 'coo':
        return sparse.coo_matrix((data, (rows, cols)), dtype=dtype, shape=shape)
    elif sparse_type.lower() == 'csc':
        return sparse.csc_matrix((data, (rows, cols)), dtype=dtype, shape=shape)

    else:
        raise Exception("Sparse type only supports coo or csr")




