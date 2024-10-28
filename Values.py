import numpy as np

from functions import Update_range, Compute_utility_M, Mask
from poker_constants import constants

def Values(S,sigma,r1,r2, matrix): #HINT S can't be chance node, leaf chance nodes are built in NN_evaluate? or not build at all

    if S.terminal: 
        if S.action == 0:
            S.better_values = np.array([S.pot - S.parent.to_call]*constants.hand_count)
            S.opponent_values = np.array([-(S.pot - S.parent.to_call)]*constants.hand_count)
            Mask(S.better_values,np.array(S.board))
            Mask(S.opponent_values, np.array(S.board))
        elif S.street == 3:
            # v1 = Compute_utility(S,r2) 
            # v2 = Compute_utility(S,r1) #!!! not sure if multiply by bot range or choose private hands-> I think it's correct
            S.better_values = Compute_utility_M(S.pot, r2, matrix)  #HINT Regret should be higher when pot is higher and you lose. otherwise bot will always bet high to increase pot and utility but will not be penalized for losing more.
            S.opponent_values = Compute_utility_M(S.pot, r1, matrix)
        else:
            S.better_values, S.opponent_values = NN_Evaluate(S, r1, r2)  #TODO function
            Mask(S.better_values,np.array(S.board))  # because NN not 100% accurate
            Mask(S.opponent_values, np.array(S.board))
    else:
        S.better_values = np.zeros(constants.hand_count, dtype='float32')
        S.opponent_values = np.zeros(constants.hand_count, dtype='float32')
        for node in S.children:
            a = node.action
            r1a = Update_range(r1,sigma,a)
            v1a, v2a = Values(node,node.strategy,r2,r1a, matrix)
            S.better_values += v1a*sigma[:,a]
            S.opponent_values += v2a*sigma[:, a] #MOD different in paper, this way it's weighted
    return(S.opponent_values, S.better_values)  #shouldn't v1 and v2 be opposite, no because different ranges in compute utility.
