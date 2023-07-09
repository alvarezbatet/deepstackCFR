# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:56:39 2020

@author: Roger
"""
from poker_constants import constants
import random

class Build_possible_boards():
    
    '''builds all boards possible on the next round given current board.
    Doesn't account human's nor bot's private cards'''
    
    def __init__(self,init_board):
        self.init_board = init_board #list of boards cards
        self.street = constants.cards_street_dict[len(self.init_board)]
        
    def build_boards(self,n):
        boards = []
        cards = list(range(52))
        cards = [ele for ele in cards if ele not in self.init_board]
        if self.street == 1:
            for i in range(len(cards)):
                for j in range(len(cards)):
                    if j != i:
                        for k in range(len(cards)):
                            if k != j and k != i:
                                boards.append(self.init_board+[i,j,k])
        else:
            for _ in range(n):
                boards.append(self.init_board + [random.choice(cards)])
        return boards
    
    def gen_flops(self,n):
        boards = []
        all_cards = list(range(52))
        for _ in range(n):
            cards = all_cards.copy()
            i = random.choice(cards)
            del cards[i]
            j = random.choice(cards)
            if i<j:
                del cards[j-1]
            else:
                del cards[j]
            k = random.choice(cards)
            boards.append(self.init_board+[i,j,k])
        return boards

                                
        
        
        