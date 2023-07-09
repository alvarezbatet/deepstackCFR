import sys
import os
import random
import time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

from test_bot_on_UI import bot_river_action

DeepStack_path = os.path.dirname(os.path.dirname(__file__))
Deuces_path = DeepStack_path + "\deuces-master\deuces"
ui_path = DeepStack_path + "\GUI\pokerUI.ui"
sys.path.insert(0, Deuces_path)
from card import Card
from evaluator import Evaluator

sys.path.insert(0, DeepStack_path)
from functions import card_to_dcs

class poker_UI(QDialog):  #TODO display speaker
    def __init__(self, Game):
        super(poker_UI, self).__init__()
        loadUi(ui_path, self)
        self.setWindowTitle('Poker application')
        self.Game = Game
        self.UI = None
        
        self.Fold_button.clicked.connect(self.clicked_Fold)
        self.Call_button.clicked.connect(self.clicked_Call)
        self.Raise_button.clicked.connect(self.clicked_Raise)
        self.All_in_button.clicked.connect(self.clicked_All_in)
        
    @pyqtSlot() 
    def clicked_Fold(self):
        self.Game.Fold(True)
        self.Game.speak_bool = not self.Game.speak_bool
    @pyqtSlot() 
    def clicked_Call(self):
        self.Game.Call(True)
        self.Game.speak_bool = not self.Game.speak_bool
    @pyqtSlot() 
    def clicked_Raise(self):
        self.Game.Raise(True)
        self.Game.speak_bool = not self.Game.speak_bool
    @pyqtSlot() 
    def clicked_All_in(self):
        self.Game.All_in(True)
        self.Game.speak_bool = not self.Game.speak_bool
        
    def update_coin_displays(self):
        self.P_stack_display.setText('P_stack: ' + str(self.Game.P_stack))
        self.Bot_stack_display.setText('Bot_stack: ' + str(self.Game.Bot_stack))
        self.Pot_display.setText('Pot: ' + str(self.Game.Pot))
        self.to_call_display.setText('to call: ' + str(self.Game.to_call))

    def update_card_displays(self):
        p_hand = [card_to_dcs(card) for card in self.Game.P_hand]
        b_hand = [card_to_dcs(card) for card in self.Game.Bot_hand]
        self.P_hand_display.setText(str(p_hand))
        self.Bot_hand_display.setText(str(b_hand))
        self.update_board_display()
        
    def update_board_display(self):
        board = [card_to_dcs(card) for card in self.Game.board]
        self.board_cards.setText(str(board))

    def Message(self, text):
        self.Message_display.setText(text)

class Game():
    def __init__(self):
        self.game_over = False
        self.P_stack = 100  #TODO retrieve stack from elsewhere
        self.Bot_stack = 100  #TODO
        self.blind = 1  #TODO      
        self.init_P_speaker = False
        self.speak_bool = True
        self.ended = False
        # HINT rest of variables assigned with self.start_game()

    def set_widget(self, widget):
        self.widget = widget
        self.start_game()        
    
    def Fold(self, P):
        if P:
            self.widget.Message('Player folded')  
            self.end_game(False)
        else:
            self.widget.Message('Bot folded')  
            self.end_game(True)

    def Call(self, P):
        """makes sure player can call
           updates P_stack
           updates Pot
           updates to_call to 0
           calls self.end_round
        """
        if P:
            if (self.round == 0) and (self.to_call == self.blind) and (self.init_P_speaker):  # HINT call blind
                self.P_stack -= self.to_call
                self.Pot += self.to_call
                self.to_call = 0
                self.widget.Message('Player called the blind')
            elif self.to_call == 0:
                self.widget.Message('Player checked')
                if not self.P_speaker:
                    self.end_round()
            elif self.P_stack > self.to_call:
                self.P_stack -= self.to_call
                self.Pot += self.to_call
                self.widget.Message('Player called')
                self.end_round()
            else:
                self.widget.Message('Player called with all_in')
                self.All_in(True)
        else:
            if (self.round == 0) and (self.to_call == self.blind) and (not self.init_P_speaker):  #??? do we need -> and (not self.init_P_speaker) ?
                self.Bot_stack -= self.to_call
                self.Pot += self.to_call
                self.to_call = 0
                self.widget.Message('Bot called the blind')
            elif self.to_call == 0:
                self.widget.Message('Bot checked')
                if self.P_speaker:
                    self.end_round()
            elif self.Bot_stack > self.to_call:
                self.Bot_stack -= self.to_call
                self.Pot += self.to_call
                self.widget.Message('Bot called')                
                self.end_round()
            else:
                self.widget.Message('Bot called with all_in')
                self.All_in(False)
                
    def Raise(self, P):
        """makes sure player can Raise
           updates P_stack
           updates Pot
           updates to_call to Pot-to_call
        """
        if P:
            if self.Bot_stack == 0:
                self.Call(True)
            elif self.to_call <= self.Pot < self.P_stack:
                if self.to_call == self.Pot:
                    self.widget.Message('Player raised Pot = called') 
                    QApplication.processEvents()
                    time.sleep(1)
                    self.Call(True)
                else:
                    self.P_stack -= self.Pot
                    self.to_call = self.Pot - self.to_call
                    self.Pot += self.Pot
                    self.P_speaker = True
                    self.widget.Message('Player raised')
            else:
                self.widget.Message('Player tried to raise')  # !!!
                QApplication.processEvents()
                time.sleep(1)
                self.All_in(True)
        else:
            if self.P_stack == 0:
                self.Call(False)
            elif self.to_call <= self.Pot < self.Bot_stack:
                if self.to_call == self.Pot:
                    self.widget.Message('Bot raised Pot = called') 
                    QApplication.processEvents()
                    time.sleep(1)
                    self.Call(False)
                else:
                    self.Bot_stack -= self.Pot
                    self.to_call = self.Pot - self.to_call
                    self.Pot += self.Pot
                    self.P_speaker = False
                    self.widget.Message('Bot raised')
            else:
                self.widget.Message('Bot tried to raise')  #!!! this reveals info to opponent
                QApplication.processEvents()
                time.sleep(1)
                self.All_in(False)
    
    def All_in(self, P):
        """checks if player_stack>to_call
           updates player_stack
           updates Pot
           updates to_call to player_stack-to_call if negative update
        """
        if P:
            if self.Bot_stack == 0 and self.P_stack > self.to_call:
                self.Call(True)
            elif self.P_stack > self.to_call:
                self.Pot += self.P_stack
                self.to_call = self.P_stack - self.to_call
                self.P_stack = 0
                self.P_speaker = True
                self.widget.Message('Player made all_in')
            else:
                difference = self.to_call - self.P_stack
                self.Pot += self.P_stack - difference
                self.Bot_stack += difference
                self.P_stack = 0
                self.to_call = 0
                self.end_game()
            
        else:
            if self.P_stack == 0 and self.Bot_stack > self.to_call:
                self.Call(False)
            elif self.Bot_stack > self.to_call:
                self.Pot += self.Bot_stack
                self.to_call = self.Bot_stack - self.to_call
                self.Bot_stack = 0
                self.P_speaker = False
                self.widget.Message('Bot made all_in') 
            else:
                difference = self.to_call - self.Bot_stack
                self.Pot += self.Bot_stack - difference
                self.P_stack += difference
                self.Bot_stack = 0
                self.to_call = 0
                self.end_game()
            
    def end_game(self,P_winner=None):
        """P_winner = boolean
           updates winner's stack
           resets game variables
           restarts game
        """
        self.UI.update_coin_displays()
        QApplication.processEvents()
        time.sleep(3)
        if P_winner is None:
            self.get_all_board_cards() 
            P_winner = self.evaluate_cards()

        if P_winner == 'draw':
            self.P_stack += self.Pot/2
            self.Bot_stack += self.Pot/2
            self.Pot = 0
        elif P_winner:
            self.P_stack += self.Pot
            self.Pot = 0
        else:
            self.Bot_stack += self.Pot
            self.Pot = 0
        self.ended = True
        if self.P_stack == 0 or self.Bot_stack == 0:
            self.widget.Message('Game Over, P_won :'+str(P_winner))
            self.UI.update_coin_displays()
            self.game_over = True
            return()
        else:
            self.widget.Message('P_won :'+str(P_winner))
        self.UI.update_coin_displays()
        QApplication.processEvents()
        time.sleep(1)
        self.start_game()  

    def end_round(self):
        """checks if round 3 to call self.end_game
           otherwise shows next board card
        """
        if self.P_stack == 0 or self.Bot_stack == 0:
            self.to_call = 0
            self.end_game()

        if self.round == 3:
            self.end_game()
        else:
            self.to_call = 0
            self.round += 1
            self.next_board_card() 
            
    def start_game(self):
        self.round = 0
        self.deck = self.get_deck() 
        self.init_P_speaker = not self.init_P_speaker
        # self.init_P_speaker = True  # HACK to test resolve
        self.P_speaker = self.init_P_speaker
        self.board = []
        self.to_call = self.blind
        self.Bot_hand = self.get_hand()  
        self.P_hand = self.get_hand()
        self.Pot = self.blind 
        if self.init_P_speaker:
            self.Bot_stack -= self.blind
        else:
            self.P_stack -= self.blind
        self.widget.update_card_displays()

    @staticmethod
    def get_deck():
        """returns a deck with all cards"""
        return list(range(52))

    def get_hand(self):
        hand = [random.choice(self.deck)]
        self.deck.remove(hand[0])
        hand.append(random.choice(self.deck))
        self.deck.remove(hand[1])
        return hand
    
    def next_board_card(self):
        if self.round == 1:
            for _ in range(3):
                self.board.append(random.choice(self.deck))
                self.deck.remove(self.board[-1])
        elif self.round in (2,3):
            self.board.append(random.choice(self.deck))
            self.deck.remove(self.board[-1])
        else:
            raise ValueError("invalid round")
        self.widget.update_board_display()

    def get_all_board_cards(self):
        while self.round < 3:
            self.round += 1
            self.next_board_card()

    def evaluate_cards(self):
        """returns True if P won, False if Bot won, or draw"""
        evaluator = Evaluator()
        board = [Card.new(card_to_dcs(card)) for card in self.board]
        p_hand = [Card.new(card_to_dcs(card)) for card in self.P_hand]
        bot_hand = [Card.new(card_to_dcs(card)) for card in self.Bot_hand]
        p_score = evaluator.evaluate(board, p_hand)
        bot_score = evaluator.evaluate(board, bot_hand)
        if p_score < bot_score:
            return True
        elif bot_score < p_score:
            return False
        else:
            return 'draw'


def execute_bot_action(game_var, bot_action):
    if bot_action == 0:
        game_var.Fold(False)
    elif bot_action == 1:
        game_var.Call(False)
    elif bot_action == 2:
        game_var.Raise(False)
    elif bot_action == 3:
        game_var.All_in(False)
    else:
        raise ValueError('Invalid action by Bot')


def get_bot_action(game_var, root, r1, r2, humaction, matrix):
    if game_var.round < 3:
        return 1, None, r1, r2
    else:
        action, next_node, r1a, r2a = bot_river_action(game_var, root, r1, r2, humaction, matrix)
        return action, next_node, r1a, r2a


if __name__ == '__main__':
    game = Game()
    app = QApplication(sys.argv)  #??? why app isn't used instead of QApplication.processEvents()
    UI = poker_UI(game)
    game.UI = UI
    game.set_widget(UI)
    UI.show()

    while not game.game_over:  #TODO copy loop like river_game.py
        UI.update_coin_displays()
        QApplication.processEvents()
        game.ended = False

        if game.P_speaker:  #TODO make sure player can't click while bot thinking
            speak_bool = game.speak_bool
            while speak_bool == game.speak_bool:
                QApplication.processEvents()
            if game.ended:
                if game.game_over:
                    break
                else:
                    continue
            UI.update_coin_displays()
            QApplication.processEvents()
            time.sleep(1.5)
            bot_action, next_node, r1a = get_bot_action(game)
            execute_bot_action(game, bot_action)  #HINT with two functions can change bot with get bot action
        else:
            time.sleep(1.5)
            bot_action, next_node, r1a = get_bot_action(game)
            execute_bot_action(game, bot_action)
            UI.update_coin_displays()
            QApplication.processEvents()
            if game.ended:
                if game.game_over:
                    break
                else:
                    continue
            speak_bool = game.speak_bool
            while speak_bool == game.speak_bool:
                QApplication.processEvents()
    sys.exit()
    #TODO exit on console close(not only on game_over)
