################################################################################
##
## PHP 2650 Homework 2: Brain Wiring
##
## By Heesoo Kim
##
## Due March 10, 2018
##
## This code is written in Python 2.7
##
################################################################################

import numpy as np
import pandas as pd
import glob
import time

start_time = time.time()

# Return the author name
def authors():
    print 'The author of this code is Heesoo Kim.'
    return ['Heesoo Kim']

normed_matrices = []
zt_matrices = []
subj_ID = []

# Read every .txt files in the current working directory.
for file in glob.glob('*.txt'):

    try:
        matrix = pd.read_table(file, delim_whitespace=True, header=None)
        # Center the mean of the matrices to 0 and normalize the variance to 1.
        normed_matrices += [(
            matrix - np.mean(matrix, axis=0))/np.std(matrix, axis=0)]
        # Calculate the matrix correlation for the purpose of z-transform.
        cor = matrix.corr()
        # Set the diagonal of the correlated matrix to 0
        for i in range(cor.shape[0]):
            cor[i][i] = 0
        # Perform z-transform on the matrix.
        zt_matrices += [0.5 * np.log((1 + cor)/(1 - cor))]

        # Store the associated subject ID of the matrix.
        subj_ID += [int(file[3:9])]

    except:
        # If the read data is corrupted, continue to read the rest of the files.
        continue

# Stack matrices
stacked_zt = np.stack(zt_matrices)

np.savetxt('Fn.csv', np.mean(stacked_zt, axis=0), delimiter=',')
np.savetxt('Fv.csv', np.var(stacked_zt, axis=0), delimiter=',')

# Quicksort algorithm
def sort(array):
    if len(array) > 1:
        less, equal, greater = [], [], []
        pivot = array[np.random.randint(len(array))]
        for e in array:
            if e < pivot:
                less += [e]
            elif e == pivot:
                equal += [e]
            elif e > pivot:
                greater += [e]
        return sort(less) + sort(equal) + sort(greater)
    else:
        return array

# Sort the subject ID in an ascending order
sorted_subj_ID = sort(subj_ID)

# Add the matrices & normalized matrices associated with the IDs in the first
# sorted half to the training matrices, and the rest to the test matrices.
f_train_matrices, f_test_matrices = [], []
x_train_matrices, x_test_matrices = [], []
train_size = int(0.5 * len(sorted_subj_ID))
for i in range(train_size):
    train_index = subj_ID.index(sorted_subj_ID[i])
    test_index = subj_ID.index(sorted_subj_ID[i + train_size])
    f_train_matrices += [zt_matrices[train_index]]
    f_test_matrices += [zt_matrices[test_index]]
    x_train_matrices += [normed_matrices[train_index]]
    x_test_matrices += [normed_matrices[test_index]]
f_train = np.stack(f_train_matrices)
f_test = np.stack(f_test_matrices)
x_train = np.concatenate(x_train_matrices)
x_test = np.concatenate(x_test_matrices)

np.savetxt('Ftrain.csv', np.mean(f_train, axis=0), delimiter=',')
np.savetxt('Ftest.csv', np.mean(f_test, axis=0), delimiter=',')

# Factorize the x_train matrix using singular variable decomposition method.
U, S, Vt = np.linalg.svd(x_train, full_matrices=False)
G = np.dot(np.diag(S), Vt)
UG = np.dot(U, G)

# Calculate the covariances of the reconstructed x_train, x_train, and x_test.
c_UG = np.cov(UG.T)
c_train = np.cov(x_train.T)
c_test = np.cov(x_test.T)

# Calculate the Frobinius norm distance between the covariance matrices of the
# reconstructed x_train & x_test, and between that of x_train & x_test.
c_UG_c_test = np.linalg.norm(c_UG - c_test)
c_train_c_test = np.linalg.norm(c_train - c_test)

np.savetxt('U.csv', U, delimiter=',')
np.savetxt('G.csv', G, delimiter=',')
np.savetxt('CUG.csv', c_UG, delimiter=',')
np.savetxt('Ctrain.csv', c_train, delimiter=',')
np.savetxt('Ctest.csv', c_test, delimiter=',')
np.savetxt('CUGCtest.csv', c_UG_c_test.reshape(1))
np.savetxt('CtrainCtest.csv', c_train_c_test.reshape(1))

print 'The program runtime is %s seconds.' % (time.time() - start_time)
