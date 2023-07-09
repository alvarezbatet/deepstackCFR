import numpy as np
from numba import jit
from copy import deepcopy

from functions import make_Range_positive, nb_make_positive
from poker_constants import constants


def UpdateSubtreeStrategies(S,R):
    if S.terminal == True:
        return()
    
    for node in S.children:
        UpdateSubtreeStrategies(node,node.regret)

    mean_v = np.zeros(constants.hand_count)  
    for node in S.children:
        mean_v += node.opponent_values*S.strategy[:,node.action]
   
    for node in S.children:
        R[:,node.action] += node.opponent_values-mean_v  #??? += or just = ??? (intuition: if strategies oscillate between same values = can work but not if strategies randomly oscillate )

    strat_R = deepcopy(R)
    nb_make_positive(strat_R)
    sigma = np.full((constants.hand_count,len(constants.actions)),np.zeros(len(constants.actions), dtype='float32'))  #invalid actions are left as 0
    construct_sigma(sigma, strat_R)
    if S.to_call == constants.skip_fold:  #HINT bot folds instead of checking because v of checking is lower(will always be lower unless all rounds ahead are checked by both which is unlikely, it's probably a flaw of the algorithm)
        factor = np.ones(constants.hand_count, dtype='float32') - sigma[:,0]
        for node in S.children: #!!! barely changes output, could be removed for speedup
            if node.children != None:
                for child in node.children:
                    child.strategy = (child.strategy.transpose() * factor).transpose()  # TODO recheck
                    child.strategy[:, 0] += sigma[:, 0]

        sigma[:,1] += sigma[:,0]
        sigma[:,0] = np.zeros(constants.hand_count, dtype='float32')

    S.strategy = sigma
    return sigma

@jit(nopython=True)
def construct_sigma(sigma, R):
    for I in range(R.shape[0]):
        sm = np.sum(R[I])
        if sm != 0:
            sigma[I,:] = R[I]/sm
        else:
            sigma[I,:] = np.ones(4)/np.float32(4)
