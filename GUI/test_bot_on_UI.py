import sys
import os 

DeepStack_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, DeepStack_path)
from ReSolve import ReSolve
from Tree_Builder import Tree_Builder
from poker_constants import constants
from functions import Update_range

import numpy as np

def bot_river_action(game, root, rbot, rhum, humaction, matrix):
    b_stack = np.float32(game.Bot_stack)
    h_stack = np.float32(game.P_stack)
    pot = np.float32(game.Pot)
    board = game.board

    if root is None:  #TODO if human speaker -> r2a
        builder = Tree_Builder()
        root = builder.build_first_node(board, np.float32(1), 3, h_stack/pot, b_stack/pot, 'bot')
        bot_node = builder.build_second_node(root)
        bot_node.to_call = game.to_call
        builder.build_tree(root=bot_node)
    else:
        for child in root.children:
            if child.action == humaction:
                bot_node = child
                break
        rhum = Update_range(rhum, root.strategy, humaction)
    a, Sa, r1a, v2, v1 = ReSolve(bot_node, game.Bot_hand, rbot, rhum, matrix)
    return(a, Sa, r1a, rhum)
