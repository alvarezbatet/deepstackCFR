import time
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication


import os

GUI_path = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(0, GUI_path)
from pokerUI_main import poker_UI, Game, get_bot_action, execute_bot_action

DeepStack_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(0, DeepStack_path)
from poker_constants import constants
from ReSolve import ReSolve
from Tree_Builder import Tree_Builder
from functions import Compute_win_matrix


def build_human_root(GAME):  #TODO maybe save function elsewhere
    builder = Tree_Builder()
    chance_root = builder.build_first_node(GAME.board, np.float32(1), 3, np.float32(GAME.P_stack/GAME.Pot),
                                           np.float32(GAME.Bot_stack/GAME.Pot), 'human')
    human_root = builder.build_second_node(chance_root)
    builder.build_tree(root=human_root)
    return human_root


if __name__ == '__main__':
    game = Game()
    app = QApplication(sys.argv)
    UI = poker_UI(game)
    game.UI = UI
    game.set_widget(UI)
    UI.show()
    next_node, humaction = None, None
    r1 = np.ones(constants.hand_count, dtype='float32')/constants.hand_count
    r2 = np.ones(constants.hand_count, dtype='float32')/constants.hand_count
    turn_bool = game.init_P_speaker
    matrix = None

    while not game.game_over:
        UI.update_coin_displays()
        QApplication.processEvents()
        game.ended = False

        if turn_bool:  # human action
            if game.round != 3:
                game.Call(True)
            else:
                if matrix is None:
                    matrix = Compute_win_matrix(game.board)

                speak_bool = game.speak_bool

                if next_node is None:
                    next_node = build_human_root(game)
                print('------------------Human Resolve------------------')
                ReSolve(next_node, game.P_hand, r2, r1, matrix)
                print('P_speaker:', game.P_speaker)
                while speak_bool == game.speak_bool:
                    QApplication.processEvents()
            if game.P_stack == 0:
                humaction = 3
            elif game.to_call != 0:
                humaction = 2
            else:
                humaction = 1
        else:  # bot action
            if game.round == 3 and matrix is None:
                matrix = Compute_win_matrix(game.board)

            bot_action, next_node, r1, r2 = get_bot_action(game, next_node, r1, r2, humaction, matrix)
            execute_bot_action(game, bot_action)
            UI.update_coin_displays()
            QApplication.processEvents()

        turn_bool = not turn_bool

        if game.ended:
            if game.game_over:
                break
            else:
                next_node, humaction = None, None
                r1 = np.ones(constants.hand_count, dtype='float32')/constants.hand_count
                r2 = np.ones(constants.hand_count, dtype='float32')/constants.hand_count
                turn_bool = game.init_P_speaker
                matrix = None
                continue
