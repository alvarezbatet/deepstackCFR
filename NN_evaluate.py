# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:18:41 2020

@author: Roger
"""
import pickle
from Build_possible_boards import Build_possible_boards
from poker_constants import constants

def NN_Evaluate(S, r1, r2):
    """quote from Deepstack's paper:' The network’s inputs are the pot size as
    a fraction of the players’ total stacks and an encoding of the players’ ranges as a function of the
    public cards.'

    The output of the network are vectors of counterfactual values for each player and hand, interpreted
    as fractions of the pot size"""
    
    #TODO get street from s.board, get model from street
    model_path = 'model' #TODO
    build = Build_possible_boards(S.board)
    boards = build.build_boards()
    
    clf = pickle.load(open(model_path, 'rb'))
    
    v1,v2 = np.zeros(constants.hand_count), np.zeros(constants.hand_count)
    
    pot = S.pot
    if S.type == 'bot':
        b_stack = S.better_stack/pot
        h_stack = S.opponent_stack/pot
    else:
        b_stack = S.opponent_stack/pot
        h_stack = S.better_stack/pot
    
    for board in boards: 
        v1,v2 += clf.predict(board,b_stack,h_stack,r1,r2) #TODO normalize inputs
    v1,v2 = pot*v1/len(boards), pot*v2/len(boards)
    
    return(v1,v2)