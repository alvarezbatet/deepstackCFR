# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:06:08 2020

@author: Roger
"""
import os

class constants():
    def __init__(self):
        self.cards_street_dict = {0:1,3:2,4:3,5:4}
        self.actions = [0,1,2,3] #fold,call,raise,all_in
        self.action_amount = [None,None,1,'stack']
        self.max_depth = 4  # how many total bet actions per round, I think pystack only uses 2 in round 2,3,4
        self.hand_count = 1326 # 52*51/2
        self.resolve_iters = 100
        self.stack_bigger_pot = 0.9
        self.suits = ['s','c','d','h']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.dir_name = os.path.dirname(__file__)
