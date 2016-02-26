import numpy as np

import sys
sys.path.append('./tools/')
from nwspgr import nwspgr


#sparse grid generation
samples_spgr, weights_spgr = nwspgr('GQU', 3,4, 'symmetric')

np.savetxt('./samples/3d/sparse_grid/gqu3_sample.csv', samples_spgr, delimiter=',')
np.savetxt('./samples/3d/sparse_grid/gqu3_weight.csv', weights_spgr, delimiter=',')


#Monte-Carlo generation
N = 200
mean = (0,0)
cov = [[1, 0], [0, 1]]
samples_mtcl = np.random.multivariate_normal(mean, cov, N)

np.savetxt('./samples/3d/monte_carlo/mc_normal_' + str(N) + '.csv', samples_spgr, delimiter=',')

