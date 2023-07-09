    # -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:46:57 2020

@author: Roger
"""
import numpy as np
from poker_constants import constants

class Node():
    def __init__(self, parent, node_type, board, pot, action, amount, to_call, h_stack, b_stack, terminal, chance_next=None, all_in=False, street=None):
        self.parent = parent
        self.type = node_type  #Can be chance, human or bot
        self.board = board
        if street == None: 
            if node_type == 'chance':  #??? does chance have parent?
                self.street = parent.street + 1
            else:
                self.street = parent.street    
        else:  #!!! manually assign street if parent == None
            self.street = street
        self.pot = pot
        self.pot += np.float32(amount)
        self.action = action
        self.human_stack = h_stack
        self.bot_stack = b_stack
        self.to_call = to_call
        self.children = None
        self.regret = np.full((constants.hand_count,len(constants.actions)),np.zeros(len(constants.actions), dtype='float32'), order='F')
        self.strategy = np.full((constants.hand_count,len(constants.actions)),np.ones(len(constants.actions), dtype='float32', order='F')/np.float32(4))
        self.better_values = np.zeros(constants.hand_count, dtype='float32')
        self.opponent_values = np.zeros(constants.hand_count, dtype='float32')
        self.terminal = terminal
        if terminal:
            self.child_type = 'chance'
        elif self.type == 'human':
            self.child_type = 'bot'
        elif self.type == 'bot': 
            self.child_type = 'human'
        elif self.type == 'chance':
            self.child_type = chance_next
        self.all_in = all_in
