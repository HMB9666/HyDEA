from petsc4py import PETSc
import scipy.sparse
import numpy as np
from write_data import writeA_sparse


filenameDBNG = '/../../DBNG/DGsparse'   #DGsparse is the name of the output matrix document

dt = 0.002  #Time step of CFD case

viewer = PETSc.Viewer().createBinary('/../../Matrix/DBNGMatrix.bin', 'r')

mat_petsc = PETSc.Mat().create()
mat_petsc.load(viewer)

rows, cols = mat_petsc.getSize()

values = mat_petsc.getValuesCSR()
num = values[0]
col = values[1]
valueresult = values[2]

DBNG_scipy = scipy.sparse.csr_matrix((valueresult,col,num),shape=(rows,cols))
DG_scipy = -1*DBNG_scipy/dt

writeA_sparse(DG_scipy,filenameDBNG,'f')





