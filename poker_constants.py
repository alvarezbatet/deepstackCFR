# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:06:08 2020

@author: Roger
"""
import numpy as np

class constants(): #TODO add path constant
    def __init__(self):
        self.cards_street_dict = {2:1,3:2,4:3,5:4}
        self.actions = [0,1,2,3]  #fold,call,raise,all_in
        self.action_amount = [None,None,1,None]
        self.max_depth = 100  # how many total bet actions per round, I think pystack only uses 2 in round 2,3,4
        self.hand_count = 1326  # 52*51/2
        self.resolve_iters = 100
        self.skip_iters = 0  # self.resolve_iters * 75 // 100
        self.stack_smaller_pot = {3: 0.03}
        self.pdf_stack_river = (72.31057215086028, 3.074064405979694, -1.306612026841533e-05, 34.405826795074134)
        self.gen_flop = 1
        self.suits = ['s','c','d','h']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.num_train_samples = 10**5
        self.chance_next = 'bot'
        self.init_pot = np.float32(1)
        self.skip_fold = -1  # if 0 fold probabilities in sigma move to call, if -1 ignored.
        self.skip_fold_resolve = 0

constants = constants()  # no need
