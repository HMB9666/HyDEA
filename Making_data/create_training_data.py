import numpy as np
import scipy
import time
import scipy.linalg
from read_data import readA_sparse
import pickle

# Lanczos Algorithm
def _lanczos_algorithm(A, init_v, num_ritz_vec, ortho_iters=0, cut_off_tol=1e-10):
    assert A.shape[0] == A.shape[1], "A is not square"
    n = A.shape[0]
    m = num_ritz_vec
    V = np.zeros((m, n))
    alpha = np.zeros(m)
    beta = np.zeros(m-1)
    V[0] = init_v / np.linalg.norm(init_v)
    w = A @ V[0]
    alpha[0] = w.dot(V[0])
    w = w - alpha[0] * V[0]

    for j in range(1, m):
        print(j)
        beta[j-1] = np.linalg.norm(w)
        if beta[j-1] < cut_off_tol:
            print("Cut off at", j)
            return V[:j], alpha[:j], beta[:j-1]
        else:
            V[j] = w / beta[j-1]
        w = A @ V[j]
        alpha[j] = w.dot(V[j])
        w = w - alpha[j] * V[j] - beta[j-1] * V[j-1]
        it = min(max(j-1, 0), ortho_iters)

        # Fully reorthogonalized
        for k in reversed(range(it)):
            w = w - V[k].dot(w) * V[k]
    return V, alpha, beta

# Create Ritz vector
def createRitzVec(A, rhs, num_ritz_vectors, ortho=True):
    print("Lanczos Iteration is running...")
    start = time.time()
    if ortho:
        W, diagonal, sub_diagonal = _lanczos_algorithm(A, rhs, num_ritz_vectors, np.inf)
    else:
        W, diagonal, sub_diagonal = _lanczos_algorithm(A, rhs, num_ritz_vectors, 0)
    print("Lanczos Iteration took", time.time() - start, 's')
    print("Calculating eigenvectors of the tridiagonal matrix")
    start = time.time()
    ritz_vals, Q = scipy.linalg.eigh_tridiagonal(diagonal, sub_diagonal, select='a')
    print("Calculating eigenvectors took", time.time() - start, 's')
    ritz_vectors = (W.T @ Q[:, :num_ritz_vectors]).T # m x n
    return ritz_vals, ritz_vectors


#Create training data
def createTrainingData(ritz_vectors, sample_size, nxn):
    small_matmul_size = sample_size

    for_outside = int(sample_size/small_matmul_size)
    b_rhs_temp = np.zeros([small_matmul_size, nxn])
    cut_idx = int(num_ritz_vectors * 0.6)
    sample_size = small_matmul_size  #
    coef_matrix = np.zeros([len(ritz_vectors), sample_size])

    for it in range(for_outside):
        coef_matrix[:] = np.random.normal(0, 1, [len(ritz_vectors), sample_size])
        coef_matrix[0:cut_idx] *= 9
        b_rhs_temp[:] = coef_matrix.T @ ritz_vectors
        l_b = small_matmul_size * it
        r_b = small_matmul_size * (it+1)

        for i in range(l_b, r_b):
            b_rhs_temp[i-l_b] = b_rhs_temp[i-l_b]/np.linalg.norm(b_rhs_temp[i-l_b])
    print(b_rhs_temp.shape)

    return b_rhs_temp


projDir = '../../..'


filenameA = '../../../DBNG'+'/DGsparse'  #Coefficient matrix
A = readA_sparse(filenameA,'f','csr')  #Read Coefficient matrix

num_ritz_vectors = 7000  #Number of Lanczos iterations
num_rhs = 54000  #Number of training data

N = 192  #Grid-resolution, 192x192

if __name__ == '__main__':
    rand_vec_x_init = np.random.normal(0,1,[N**2])
    rand_vec_x_init_used = A.dot(rand_vec_x_init)

    #Create Ritz vector
    ritz_vals, ritz_vectors = createRitzVec(A,rand_vec_x_init_used,num_ritz_vectors)
    #Creare training data
    b_rhs_temp = createTrainingData(ritz_vectors,num_rhs,N**2)

    f = open(projDir + '/b_rhs/' + '_b_rhs', 'wb')
    pickle.dump(b_rhs_temp, f)
    f.close()

