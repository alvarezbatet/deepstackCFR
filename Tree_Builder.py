# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:44:38 2020

Limit tree depth with limited number of raises, raise_count var in node.
"""
from poker_constants import constants
import Build_possible_boards
from Nodes import Node
from functions import Next_P_State

class Tree_Builder():
    def __init__(self):
        self.max_depth = constants.max_depth
        pass

    @staticmethod
    def build_first_node(board,pot,street, h_stack, b_stack, better1): # doesn't build preflop because no blinds
        '''builds first node for streets 1,2,3 as chance node with public cards as board and no parent,
        manually assigns street'''
        node = Node(None,'chance',board,pot,None, 0, 0, h_stack, b_stack, False, chance_next=better1, street=street)
        return node
   
    @staticmethod
    def build_second_node(root):
        node = Node(root,root.child_type,root.board,root.pot,None, 0, 0, root.human_stack, root.bot_stack, False, street=root.street)
        return node
    
    def build_tree(self,root,depth=1,actions=constants.actions,terminal=False):
        '''Builds tree from root until max_depth, only 0 and 1 actions at max_depth'''
        #!!! maybe build different trees for human and bot with different boards will be faster as there is no need to check if node is possible given private hands.
        
        tree = self.build_action_nodes(root,actions,terminal)
        if depth < self.max_depth-1:
            for node in tree.children:
                if node.terminal == False:
                    self.build_tree(node,depth+1) 
        elif depth == self.max_depth-1:
            actions = [0,1]
            for node in tree.children:
                if node.terminal == False:
                    self.build_tree(node,depth+1,actions=actions,terminal=True)
        if depth == 1:
            return root

    @staticmethod
    def build_chance_nodes(root):  #!!! consider deleting invalid boards to compute cfvs???, maybe not because nodes are used for strategies of both players/check template
        '''builds 'chance' nodes for root.children'''
        children = []
        boards_builder = Build_possible_boards(root.board)
        boards = boards_builder.build_boards()
        for board in boards:
            children.append(Node(root,'chance', board, root.pot, None, 0, 0, root.human_stack, root.bot_stack, False, chance_next=root.child_type))
        root.children = children
        return root


    @staticmethod
    def build_action_nodes(root,actions,terminal=False):
        '''Returns root with list of nodes for each possible action'''
        children = []
        human = root.type == 'human'
        if root.terminal:
            return(None)
        if root.all_in: #BUG check bugs ie. impossible actions
            if human:  #BUG if call converts to all in there will be two all in nodes in children
                if root.to_call < root.human_stack:
                    actions = [0, 1]
            else:
                if root.to_call < root.bot_stack:
                    actions = [0, 1]

        if human: #check if player can only fold or all_in
            if root.human_stack <= root.to_call:
                actions = [0,constants.actions[-1]]
        else:
            if root.bot_stack <= root.to_call:
                actions = [0,constants.actions[-1]]

        for action in actions:
            children.append(Next_P_State(root,action,terminal))
        root.children = [child for child in children if child is not None]

        return root  #!!! not necessary
