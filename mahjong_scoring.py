"""
Ollie Lowe
07-11-22

File to score Mahjong games
"""


import pandas as pd
import numpy as np


# create class of players
class player():
    def __init__(self):
        self.name = 'dave'
        self.east_wind = 0
        self.mahjong = 0
        self.score = 0


# do at start of game
def game_start(player_list):
    # welcome message
    print('Let\'s play Mahjong!')

    # initialise player names
    for i in range(4):
        # player_list[i].name = input(f'Player {i+1} name:')
        player_list[i].name = f'p{i+1}'

    # initialise scoreboards
    round_scores = pd.DataFrame(np.zeros((4, 4)), columns=[player_list[i].name for i in range(4)])
    total_scores = pd.DataFrame(np.zeros((4, 4)), columns=[player_list[i].name for i in range(4)])

    # initialise east wind player
    east_wind = input('East wind player: ')

    for i in range(4):
        if east_wind == player_list[i].name:
            player_list[i].east_wind = 1
        else:
            player_list[i].east_wind = 0

    # let user decide when to move on
    input('Setup complete, press enter to go to round 1 scoring.')

    return player_list, round_scores, total_scores


# at end of a round
def end_round(player_list, round_scores, total_scores):
    # get mahjong player
    mahjong = input('Mahjong player: ')

    for i in range(4):
        if mahjong == player_list[i].name:
            player_list[i].mahjong = 1
        else:
            player_list[i].mahjong = 0

    # input round points and calculate corresponding scores
    for i in range(4):
        player_list[i].score = input(f'{player_list[i].name} score: ')

    return player_list, round_scores, total_scores


# initialise player classes
p1 = player()
p2 = player()
p3 = player()
p4 = player()

player_list = [p1, p2, p3, p4]

player_list, round_scores, total_scores = game_start(player_list)
player_list, round_scores, total_scores = end_round(player_list, round_scores, total_scores)

