import numpy as np

from functions import Update_range, Compute_utility_M, Mask
from poker_constants import constants

def Values(S,sigma,r1,r2, matrix): #HINT S can't be chance node, leaf chance nodes are built in NN_evaluate? or not build at all
    bot = S.type == 'bot'

    if S.terminal:
        if S.action == 0:
            if bot:
                S.better_values = np.array([S.pot - S.parent.to_call]*constants.hand_count)
                S.opponents_values = np.array([-(S.pot - S.parent.to_call)]*constants.hand_count)
            Mask(S.better_values,np.array(S.board))
            Mask(S.opponents_values, np.array(S.board))
        elif S.street == 3:
            # v1 = Compute_utility(S,r2)
            # v2 = Compute_utility(S,r1) #!!! not sure if multiply by bot range or choose private hands-> I think it's correct
            S.better_values = Compute_utility_M(S.pot, r2, matrix)  #HINT Regret should be higher when pot is higher and you lose. otherwise bot will always bet high to increase pot and utility but will not be penalized for losing more.
            S.opponents_values = Compute_utility_M(S.pot, r1, matrix)
        else:
            S.better_values, S.opponents_values = NN_Evaluate(S, r1, r2)  #TODO function
    else:
        S.better_values = np.zeros(constants.hand_count, dtype='float32')
        S.opponents_values = np.zeros(constants.hand_count, dtype='float32')
        for node in S.children:
            a = node.action
            r1a = Update_range(r1,sigma,a)
            v1a, v2a = Values(node,node.strategy,r2,r1a, matrix)
            if bot:
                S.better_values += v1a*sigma[:,a]
                S.opponents_values += v2a*np.sum(sigma[:, a]*r1)  #HACK different in paper, this way it's weighted

    return(S.opponents_values, S.better_values)  #shouldn't v1 and v2 be opposite, no because different ranges in compute utility.s