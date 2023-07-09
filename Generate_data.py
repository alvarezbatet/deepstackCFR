# -*- coding: utf-8 -*-
"""
Created on Sun May  3 20:02:33 2020

@author: Roger
"""
import numpy as np
import random 
import pickle
import os
from scipy.stats import powerlognorm
import scipy.stats as st

from Build_possible_boards import Build_possible_boards
from poker_constants import constants
from Tree_Builder import Tree_Builder
from functions import Compute_win_matrix
from ReSolve import ReSolve

class my_pdf(st.rv_continuous):
    def _pdf(self,x):
        return 2*x

class Generate_data():
    def __init__(self):
        self.path = r'C:\Users\Roger\Desktop\Computer vision online game\DeepStack\models'
        self.params = {3: constants.pdf_stack_river}  #TODO for each street
        self.diff = {3: 546.5}
        self.minim = {3: 1}
        self.linear_pdf_river = my_pdf(a=0, b=1)
    @staticmethod
    def gen_rand_boards(street):
        if street == 1:  #TODO figure how streets correspond
            flop_builder = Build_possible_boards([])
            return(flop_builder.build_boards())
        elif street == 2:
            flop_builder = Build_possible_boards([])
            flops = flop_builder.gen_flops(constants.gen_flop)  # get iterations from constants
            
            result = []
            for flop in flops:
                turn_builder = Build_possible_boards(flop)
                result.append(turn_builder.build_boards())
        elif street == 3:
            flop_builder = Build_possible_boards([])
            flops = flop_builder.gen_flops(int(constants.gen_flop))
            result = []
            for flop in flops:
                turn_builder = Build_possible_boards(flop)
                for turn in turn_builder.build_boards(1):
                    river_builder = Build_possible_boards(turn)
                    result += river_builder.build_boards(1)
            return result

    @staticmethod
    def gen_rand_range(board):
        r = np.zeros(constants.hand_count)
        for i in range(constants.hand_count):
            r[i] = random.randrange(0, 1000)
        for card in board:
            r[card] = 0
        r = r.astype('float32')
        r /= np.sum(r)
        return r
    
    @staticmethod
    def gen_rand_hand(board):
        cards = list(range(52))
        while True:
            hand1 = random.choice(cards)
            if hand1 not in board:
                del cards[hand1]
                break
        while True:
            hand2 = random.choice(cards)
            if hand2 not in board:
                break
        return [hand1, hand2]

    def gen_rand_stack(self, street): #TODO
        '''generates random stack inputs for bot and human to train the Neural Network,
        stack inputs are represented as fractions stack/pot.
        With probability x chooses 0<stack<1 else 1<stack<'''
        stack_smaller_pot = constants.stack_smaller_pot[street] #HINT should depend on street, higher pots higher the street
        if random.random() > stack_smaller_pot:
            stack = powerlognorm.rvs(loc=self.params[street][-2], scale=self.params[street][-1], *self.params[street][:-2]) * self.diff[street] + self.minim[street]
        else:
            stack = self.linear_pdf_river.rvs()
        stack = np.float32(stack)
        return stack
    
    def generate(self, street):
        '''generates inputs and uses them to call resolve and generate outputs, then saves the data'''
        path = self.path + '\\' + str(street) +r'\raw'   
        if os.path.exists(path+"\inputs1.txt"):
            with open(path+"\inputs1.txt", "rb") as f:
                inputs = pickle.load(f)
        else:
            for inp in range(10):
                inputs = []
                print('generating boards')
                for _ in range(constants.num_train_samples//10):
                    inputs.append(self.gen_rand_boards(street)[0])
                print('first board -> ',inputs[0])
                for i in range(len(inputs)):
                    print('generating inputs',i,'/',len(inputs))
                    inputs[i] = [inputs[i],self.gen_rand_stack(street),self.gen_rand_stack(street),self.gen_rand_range(inputs[i]),self.gen_rand_range(inputs[i])] #HINT Unnormalized data

                with open(path+r"\inputs"+str(inp)+".txt", "wb+") as f:
                    pickle.dump(inputs, f)

        for inp in range(10):
            with open(path+r"\inputs"+str(inp)+".txt", "rb") as f:
                inputs = pickle.load(f)
            cfvs = []
            count = 0
            num = 0
            for sample in inputs:
                print('building tree',500*num + count + 1,'/',len(inputs),'----------------------')
                builder = Tree_Builder()
                root = builder.build_first_node(sample[0], constants.init_pot, street, sample[1], sample[2], constants.chance_next)
                bot_node = builder.build_second_node(root)
                builder.build_tree(root=bot_node)

                matrix = Compute_win_matrix(sample[0])
                a,S,r1a,v1,v2 = ReSolve(bot_node,self.gen_rand_hand(sample[0]), sample[3], sample[4], matrix)
                cfvs.append([v1,v2])
                count += 1

                if count >= 500:
                    with open(path+"\outputs_"+str(inp)+"_"+str(num)+".txt", "wb+") as f:
                        pickle.dump(cfvs, f)
                    cfvs = []
                    count = 0
                    num += 1
    
    def convert_to_tf(self,model): #TODO
        '''retrieves training data from text file into an array and converts to tensorflow data'''
        path = self.path + str(model) +'\\tf_data\\'
        with open(path+"\inputs.txt", "rb") as f:   
            inputs = pickle.load(f)
        with open(path+"\outputs.txt", "rb") as f:   
            outputs = pickle.load(f)
            
generate_data = Generate_data()



