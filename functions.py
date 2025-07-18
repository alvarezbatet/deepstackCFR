import numpy as np
import sys
import os
import pickle
from numba import jit

from Nodes import Node
from poker_constants import constants

@jit(nopython=True)
def Update_range(r,sigma,action):
    '''returns normalized range given previous range, next action
    and strategy sigma'''
    s = np.sum(sigma[:,action]*r)
    if s == 0 or s == 1:
        return sigma[:,action]*r
    return sigma[:,action]*r/np.sum(sigma[:,action]*r)

def Next_P_State(S,action,terminal):  #Maybe use the rules of the game functions instead of hard coding, check if action is available
    '''returns new Public state given action and previous state S'''
    if S.all_in:
        if action not in (0,1,constants.actions[-1]):
            return(None)
        else:
            terminal = True
            
    human = S.type == 'human'
    
    if human:  #check if player can only fold or all_in
        if S.human_stack < S.to_call and action not in (0,constants.actions[-1]):
            return(None)
    else:
        if S.bot_stack < S.to_call and action not in (0,constants.actions[-1]):
            return(None)
              
    pot = S.pot
    h_stack = S.human_stack
    b_stack = S.bot_stack
    all_in = False
    if action == 0: 
        terminal = True
        amount = 0
        to_call = 0
    elif action == 1:
        amount = S.to_call
        to_call = 0
        if S.parent.type != 'chance':  #TODO check BUG, maybe S.type isn't chance but terminal shouldn't be True
            terminal = True
    elif 1 < action and action < constants.actions[-1] and (human*(constants.action_amount[action]*S.pot <= S.human_stack) or ((not human)*(constants.action_amount[action]*S.pot <= S.bot_stack))):
        amount = constants.action_amount[action]*S.pot
        to_call = amount - S.to_call  #BUG what if pot == to_call? is that possible?
    elif action == 3:
        all_in = True
        if human:
            amount = S.human_stack
        else:
            amount = S.bot_stack
        to_call = amount - S.to_call
        if to_call <= 0:
            terminal = True
            if human:
                b_stack = S.bot_stack - to_call
                pot += to_call
            else:
                h_stack = S.human_stack - to_call
                pot += to_call 
            to_call = 0
    else:
        return (None)
    if human:
        h_stack = S.human_stack - amount
    else:
        b_stack = S.bot_stack - amount
    pot = np.float32(pot)
    return Node(S, S.child_type, S.board, pot, action, amount, to_call, h_stack, b_stack, terminal,all_in=all_in)

def Compute_aprox_utility(S,r):
    path = r'C:\Users\Roger\Desktop\Computer vision online game\DeepStack\utilities'+'\\'+str(S.board) +'.txt'
    if os.path.exists(path):
        with open(path, "rb") as f:   
            strength = pickle.load(f)
            return S.pot*strength
        
    strength = np.zeros(len(r))
    print('computing aproximate utility',S.board)
    for i in range(len(r)):
        strength[i] = Compute_strength(S.board,i)
    with open(path, "wb+") as f:   
        pickle.dump(strength, f)
    return S.pot*strength

def Compute_strength(board,hand): #TODO try with score=P(winning) instead of rank
    sys.path.insert(1, r'C:\Users\Roger\Desktop\Computer vision online game\deuces-master\deuces')
    from card import Card 
    from evaluator import Evaluator   
    hand = hand_to_cards(hand)
    hand = [Card.new(card_to_dcs(card)) for card in hand]
    board = [Card.new(card_to_dcs(card)) for card in board]
    for card in board:
        if card in hand:
            return 0
    evaluator = Evaluator()
    score_board = evaluator.evaluate(board,[])
    score_hand = evaluator.evaluate(board,hand)
    score = (3822 - score_hand - (7642 - score_board))/3821
    return score

'---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'

def Compute_utility_M(pot, r, matrix):
    U = np.dot(pot*r,matrix)
    return U

@jit(nopython=True)
def Utility_M(U, pot, r, matrix):
    for i in range(len(r)):
        U[i] = np.dot(pot * r, matrix[:,i])

def Compute_win_matrix(board):
    sys.path.insert(1, r'C:\Users\Roger\Desktop\Computer vision online game\deuces-master\deuces')
    from card import Card
    from evaluator import Evaluator
    evaluator = Evaluator()

    print('computing aproximate utility',board)
    
    board = [Card.new(card_to_dcs(card)) for card in board]
    scores = np.zeros(constants.hand_count)
    for i in range(constants.hand_count):
        hand = hand_to_cards(i)
        hand = [Card.new(card_to_dcs(card)) for card in hand]
        if (hand[0] not in board) and (hand[1] not in board):
            scores[i] = evaluator.evaluate(board,hand)
    matrix = np.full((constants.hand_count,constants.hand_count),0, dtype='float32')
    fill_U_matrix(matrix, scores)
    return matrix

@jit(nopython=True)
def fill_U_matrix(matrix, scores):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            score1 = scores[j]  # TODO compute only half of matrix and copy, since it is symmetric !!!symmetric in absolute value!!! need to change sign of components
            score2 = scores[i]
            hand1 = hand_to_cards(i)
            hand2 = hand_to_cards(j)
            if score1 == 0 or score2 == 0:
                win = np.float32(0)
            elif score1 < score2:
                win = np.float32(1)
            elif score2 < score1:
                win = np.float32(-1)
            else:
                win = np.float32(0)
            for card in hand1:
                if card in hand2:
                    win = np.float32(0)
                    break
            matrix[i,j] = win

def make_positive(x):
    x[x < 0] = np.float32(0)
    return x

@jit(nopython=True)
def nb_make_positive(x):
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i,j] < 0:
                x[i,j] = np.float32(0)

@jit(nopython=True)
def make_Range_positive(R):  # Wrong
    for hand in range(1326):
        minim = min(R[hand])
        if minim < 0:
            R[hand] = np.array([val - minim for val in R[hand]])

@jit(nopython=True)
def Mask(r,board):
    for card in board:
        for hand in all_hands_with_card(card):
            r[hand] = np.float32(0)

def card_to_dcs(card):
    suit = constants.suits[card%4]
    rank = constants.ranks[card//4]
    return rank+suit

@jit(nopython=True)
def hand_to_cards0(hand):
    rang = 51
    s = 0
    while s < 1326:
        s += rang
        if hand < s:
            card1 = 51-rang
            card2 = rang - (s - (hand + 1)) + card1 
            break
        rang -= 1
    return [card1,card2]

@jit(nopython=True)
def hand_to_cards(hand):
    count = hand
    sub = 51
    while count - sub >= 0:
        count -= sub
        sub -= 1
    card1 = 51 - sub
    card2 = count + card1 + 1
    return [card1, card2]

@jit(nopython=True)
def cards_to_hand(cards):
    rang = 51
    s = 0
    for i in range(cards[0]):
        s += rang
        rang -= 1
    s += cards[1] - (51 - rang) - 1
    return s

@jit(nopython=True)
def all_hands_with_card(card):
    hands = []
    for i in range(card):
        hands.append(cards_to_hand([i, card]))
    for i in range(card + 1, 52):
        hands.append(cards_to_hand([card, i]))
    return hands
