"""
2. Card Abstraction Method
Pluribus uses a clustering technique based on hand strength and potential.

Specifically, it calculates features like:

Hand strength: Probability that a given hand will win against random opponents if no more cards are dealt.

Potential: How the hand might improve or weaken on future cards.

Board texture: Characteristics of the community cards affecting hand strength (e.g., flush or straight possibilities).

Hands with similar features are grouped into the same bucket.


3. Board Abstraction
Boards themselves can be abstracted based on their texture:

Number of connected cards (possible straights)

Number of suited cards (flush draws)

High card values

Paired boards, etc.

Boards with similar strategic impact are grouped.


Summary
Feature calculation	Hand strength, potential, board texture
Clustering	Group hands and boards with similar features
Bucketing	Assign each hand+board combo to a bucket
Result	Manageable abstract game tree for solving

"""
from numba import jit
from pathlib import Path
import sys
import os


def get_h_strength_board(hand, file_path):
    strength = 0
    norm_count = 0
    for opponent_h in range(1326):
        opponent_h= hand_to_cards(opponent_h)
        if hands_are_compatible(hand, opponent_h):
            with open(file_path, "r") as f:
                for line in f:
                    board = [int(card) for card in line.strip().split()]
                    if board_is_compatible(hand, opponent_h, board):
                        win, draw = hand_wins(hand, opponent_h, board)
                        if win:
                            strength += 1 
                        if not draw:
                            norm_count += 1
    strength = strength / norm_count    
    return strength


def get_flop_potential(hand, file_path):
    flop_potential = 0
    strenght_flop = 0
    norm_count = 0
    with open(file_path, "r") as f:
        print(hand, norm_count, "/", 22100)
        for line in f:
            flop = [int(card) for card in line.strip().split()]
            if not street_is_compatible(hand, flop):
                continue
            deck = list(range(52))
            deck.remove(hand[0])
            deck.remove(hand[1])
            deck.remove(flop[0])
            deck.remove(flop[1])
            deck.remove(flop[2])
            str_flop = strength(hand, flop)
            strenght_flop =+ str_flop
            norm_count += 1
            if norm_count % 10 == 0:
                print(hand, flop, norm_count, "/", 22100)
            for card in deck:
                if new_card_is_compatible(card, hand, flop):
                    str_turn = strength(hand, flop + [card])  #strenght the lower the better
                    if str_turn < str_flop:  #if str decreases it means next street has higher strength so there is more potential at current street.
                        flop_potential += 1
                    if str_turn > str_flop:
                        flop_potential -= 1
    return flop_potential, strenght_flop / norm_count

def get_turn_potential(hand, file_path):
    turn_potential = 0
    strenght_turn = 0
    with open(file_path, "r") as f:
        for line in f:
            turn = [int(card) for card in line.strip().split()]
            if not street_is_compatible(hand, turn):
                continue
            deck = list(range(52))
            deck.remove(hand[0])
            deck.remove(hand[1])
            deck.remove(turn[0])
            deck.remove(turn[1])
            deck.remove(turn[2])
            deck.remove(turn[3])
 
            str_turn = strength(hand, turn)
            strenght_turn =+ str_turn
            norm_count += 1
            for card in deck:
                str_river = strength(hand, turn  + [card])  #strenght the lower the better
                if str_river < str_turn:
                    turn_potential += 1
                if str_river > str_turn:
                    turn_potential -= 1
    return turn_potential, strenght_turn / norm_count

@jit(nopython=True)
def hand_to_cards(hand):
    count = hand
    sub = 51
    while count - sub >= 0:
        count -= sub
        sub -= 1
    card1 = 51 - sub
    card2 = count + card1 + 1
    return [card1, card2]

@jit(nopython=True)
def cards_to_hand(cards):
    rang = 51
    s = 0
    for i in range(cards[0]):
        s += rang
        rang -= 1
    s += cards[1] - (51 - rang) - 1
    return s

@jit(nopython=True)
def all_hands_with_card(card):
    hands = []
    for i in range(card):
        hands.append(cards_to_hand([i, card]))
    for i in range(card + 1, 52):
        hands.append(cards_to_hand([card, i]))
    return hands 

@jit(nopython=True)
def hands_are_compatible(hand1, hand2):
    for card1 in hand1:
        if card1 in hand2:
            return False
    return True

@jit(nopython=True)
def street_is_compatible(hand,board):
    for cardh in hand:
        if cardh in board:
            return False
    return True
@jit(nopython=True)
def board_is_compatible(hand1, hand2, board):
    for card1 in hand1:
        if card1 in board:
            return False
    for card2 in hand2:
        if card2 in board:
            return False
    return True



@jit(nopython=True)
def card_to_dcs(card):
    suits = ['s','c','d','h']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suit = suits[card%4]
    rank = ranks[card//4]
    return rank+suit

def hand_wins(hand, opponent_h, board):
    sys.path.insert(1, r'C:\Users\Roger\Desktop\programing\pluribus\deuces-master\deuces')
    from card import Card 
    from evaluator import Evaluator   
    evaluator = Evaluator()
    hand = [Card.new(card_to_dcs(card)) for card in hand]
    board = [Card.new(card_to_dcs(card)) for card in board]
    opponent_h = [Card.new(card_to_dcs(card)) for card in opponent_h]
    score1 = evaluator.evaluate(board,hand)
    score2 = evaluator.evaluate(board,opponent_h)
    if score1 < score2: #score the lower the better
        return True, False
    elif score1 > score2: #score the lower the better
        return False, False
    return True, True

@jit(nopython=True)
def new_card_is_compatible(card, hand, board):
    if card in hand:
        return False
    if card in board:
        return False
    return True


def strength(hand, board):
    sys.path.insert(1, r'C:\Users\Roger\Desktop\programing\pluribus\deuces-master\deuces')
    from card import Card 
    from evaluator import Evaluator   
    evaluator = Evaluator()
    hand = [Card.new(card_to_dcs(card)) for card in hand]
    board = [Card.new(card_to_dcs(card)) for card in board]
    score = evaluator.evaluate(board, hand)
    return score

def get_similar_hands():
    similar_hands = {}
    for hand_ind in range(1325):
        hand = hand_to_cards(hand_ind)
        hand = [card_to_dcs(card) for card in hand]
        ranks = [card[0] for card in hand]
        key = tuple(ranks)
        if key in similar_hands.keys():
            similar_hands[key].append(hand_ind)
        else:
            similar_hands[key] = [hand_ind]
    inds_rank = {}
    count = 0
    for rank, hand_inds in similar_hands.items():
        for ind in hand_inds:
            inds_rank[ind] = (rank, count)
        count += 1
    return similar_hands, inds_rank

file_path = Path(r"C:\Users\Roger\Desktop\programing\pluribus\hand_abstraction_features.txt")
file_path.touch(exist_ok=True) 
f = open(r"C:\Users\Roger\Desktop\programing\pluribus\hand_abstraction_features.txt", "w")
similar_hands, inds_rank = get_similar_hands()
try:
    for hand_ind in range(1326):
        hand = hand_to_cards(hand_ind)
        
        strength_river = str(get_h_strength_board(hand, r"C:\Users\Roger\Desktop\programing\pluribus\poker_rivers.txt"))

        flop_potential, strength_flop = str(get_flop_potential(hand, r"C:\Users\Roger\Desktop\programing\pluribus\poker_flops.txt"))
        turn_potential, strenght_turn = str(get_turn_potential(hand, r"C:\Users\Roger\Desktop\programing\pluribus\poker_turns.txt"))
        
        suit_isomorphism = inds_rank[hand_ind][1]
        print([strength_river, strength_flop, strenght_turn, flop_potential, turn_potential, suit_isomorphism])
        f.write(" ".join([strength_river, strength_flop, strenght_turn, flop_potential, turn_potential, suit_isomorphism]) + "\n")
except KeyboardInterrupt:
    print("\nKeyboard interrupt detected. Saving progress...")
finally:
    f.close()
    print("File saved and closed.")