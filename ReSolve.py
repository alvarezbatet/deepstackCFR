import numpy as np  #!!! try to use numpy only when necessary ie. computing complex array operations
import random
import os

from Values import Values
from UpdateSubtreeStrategies import  UpdateSubtreeStrategies
from RangeGadget import RangeGadget
from functions import Update_range,Next_P_State, Mask, cards_to_hand, Compute_win_matrix, card_to_dcs
from poker_constants import constants

# from tree_displayer import display_tree


#actions = [0,1,2,3] -> [fold,call,raise_pot_amount,all_in]

'''QUOTE: The ranges are encoded by clustering hands into 1,000 buckets, as in traditional
abstraction methods''' 

import time

# S = public state, node belonging to tree of public states, branch with actions 
# I = private cards from bot
# sigma = array(num_hands x actions), if node doesn't have strategy, call function strategy
# range = 1d array (num_hands x 1) each entry = probability of that hand given S
# R = regrets for player(num_hands x num_actions), RG = regret gadget for player2

def ReSolve(S, I, r1, r2, matrix):
    print('hand', [card_to_dcs(card) for card in I])
    I = sorted(I.copy())
    print(I)
    print([card_to_dcs(card) for card in S.board])
    print(S.to_call)
    T = constants.resolve_iters
    #r1, r2 = np.ones(constants.hand_count, dtype='float32')/constants.hand_count, np.ones(constants.hand_count, dtype='float32')/constants.hand_count
    Mask(r1, np.array(S.board))
    Mask(r2, np.array(S.board))
    v2 = S.opponent_values
    v2_t = np.full(T, None, dtype=object)
    v2_t[0] = v2
    sigmas = np.full(T,None,dtype=object)
    sigmas[0] = S.strategy
    RG = {'T':np.ones(constants.hand_count, dtype='float32'),'F':np.ones(constants.hand_count, dtype='float32')}
    t1 = time.time()
    for t in range(1,T):
        if t%10 == 0:
            print('Resolve iteration',t,'/',T)
        v1,v2_t[t] = Values(S,sigmas[t-1],r1,r2, matrix)
        sigmas[t] = UpdateSubtreeStrategies(S,S.regret)
        if S.type == 'bot':  # rangegadget not used on human resolve (intuition: bot range is determined by actions because it uses resolve strategy, human doesn't use strategy). This method makes sense when human knows bot's strategy, it's also less aggressive.
            r2,RG = RangeGadget(v2,v2_t[t],RG)  #HACK use previous range, atleast for the river ¿maybe without RG deepstack is more exploitable and aggressive?
            Mask(r2, np.array(S.board))  # shouldn't need to mask if values already masked but just to make sure.
        # TODO Prune Nodes !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print('time iters',time.time()-t1)
    # sigma = sigmas[-1]
    sigma = np.sum(sigmas[constants.skip_iters:],axis=0)/(T-constants.skip_iters)  #??? Why not just only use last sigma since regret already accounts for past iterations?because strats can oscillate
    print(sigma)
    if S.to_call == constants.skip_fold_resolve:  # skip for training NN
        sigma[:,1] += sigma[:,0]
        sigma[:,0] = np.zeros(constants.hand_count, dtype='float32')
    S.strategy = sigma
    sigma_info = np.array(sigma[cards_to_hand(I),:], dtype='float64')  #Hint because rounding can make probabilities sum higher than 1 and random.multinomial uses float64
    sigma_info /= np.sum(sigma_info)                                   # ^
    print(sigma_info)
    a = constants.actions[list(np.random.multinomial(1, sigma_info, size=1)[0]).index(1)]  #!!!check if valid action, invalid actions have P=0 (check Next_P_State)
    r1a = Update_range(r1,sigma,a)
    v2 = np.sum(v2_t[constants.skip_iters:],axis=0)/(T-constants.skip_iters)  #??? why just not v2_t[-1] or save all v1s?
    Sa = S  # to avoid errors
    for node in S.children:
        if node.action == a:
            Sa = node
            break
    return(a, Sa, r1a, v1, v2) #HACK also returns v1 so that we can train NN

