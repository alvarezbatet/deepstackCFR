# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:48:20 2020

@author: Roger
"""
import sys
from functions import card_to_dcs,hand_to_cards, all_hands_with_card
sys.path.insert(1, r'C:\Users\Roger\Desktop\Computer vision online game\deuces-master\deuces')
from card import Card 
from evaluator import Evaluator

initboard = [20, 40, 7, 28, 19]
board = []
for i in range(5):
    board.append(card_to_dcs(initboard[i]))
print(board)
# for hand in range(1326):
#     print([card_to_dcs(card) for card in hand_to_cards(hand)])
inithand = [0, 13]
board = [Card.new(card) for card in board]

h = []    
for i in range(2):
    h.append(card_to_dcs(inithand[i]))
print(h)
h = [Card.new(card) for card in h]  
s = 0
evaluator = Evaluator()
bot = evaluator.evaluate(board,h)
print(bot)
for hand in range(1326):
    hand = hand_to_cards(hand)
    if hand[0] in inithand+initboard or hand[1] in inithand+initboard:
        continue       
    for i in range(2):
        hand[i] = card_to_dcs(hand[i])
    hand = [Card.new(card) for card in hand]  
    human = evaluator.evaluate(board,hand)
    if human < bot:
        s -= 1
    elif bot < human:
        s += 1
print(s,'sum')
    