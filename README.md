# deepstackCFR 

THIS IS A TEST REPOSITORY, I HAVE A WORKING VERSION BUT IT STILL NEEDS TO BE CLEANED BEFORE UPLOADING IT HERE.

Poker bot that plays "Heads Up no limit Texas Holdem".
Players' stacks are set to 200 and actions available are: Fold, Call, Raise(the amount that's in the Pot), and All in.

The code is a python adaptation of the study made by the Alberta Machine Intelligence Institute and the Charles University Grant Agency.
In the following website you can access all information about the algorithm and its creators https://www.deepstack.ai/.
The two main papers used to build this python adaptation are:
https://static1.squarespace.com/static/58a75073e6f2e1c1d5b36630/t/58b7a3dce3df28761dd25e54/1488430045412/DeepStack.pdf
https://static1.squarespace.com/static/58a75073e6f2e1c1d5b36630/t/58bed28de3df287015e43277/1488900766618/DeepStackSupplement.pdf

Libraries used:
Numpy for the matrix operations and Numba for speeding it all up.
pyQt5 for displaying the board on Windows.

A modified version of the following github repository https://github.com/worldveil/deuces was used to evaluate the player with the winning hand.

Betting rounds:
-preflop: 
-flop:
-turn:
-river:
