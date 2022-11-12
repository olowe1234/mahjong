"""
Ollie Lowe
07-11-22

File to score Mahjong games once the round points are inputted
"""


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# create class of players
class player():
    def __init__(self):
        self.name = 'dave'
        self.east_wind = 0
        self.mahjong = 0
        self.score = 0


# initialise player classes
p1 = player()
p2 = player()
p3 = player()
p4 = player()

players = [p1, p2, p3, p4]


def game_start(players):

    """Initialise names and order at beginning of the game
    Inputs:
            players - list of player objects belonging to player class, the 4 players of the game
    Outputs:
            players - list of player objects once updated
            score_inputs - DataFrame of raw scores for each round
            round_scores - DataFrame of scores for each round for each player
            total_scores - DataFrame of cumulative scores over rounds
    """

    # welcome message
    print('Let\'s play Mahjong!')

    # create list of winds (players)
    winds = ['East', 'South', 'West', 'North']

    # initialise player names
    for i in range(len(winds)):
        # players[i].name = input(f'{winds[i]} wind player name: ')
        players[i].name = f'p{i+1}'

        # initialise east wind player
        if winds[i] == 'East':
            players[i].east_wind = 1

    # initialise scoreboards
    score_inputs = pd.DataFrame(columns=[players[i].name for i in range(4)])
    round_scores = pd.DataFrame(columns=[players[i].name for i in range(4)])
    total_scores = pd.DataFrame(columns=[players[i].name for i in range(4)])

    # let user decide when to move on
    input('Setup complete, press enter to go to round 1 scoring.')

    return players, score_inputs, round_scores, total_scores


def end_round(round_num, players, round_scores, total_scores):

    """Calculate scores for a single round and update scoring DataFrames
    Inputs:
            round_num - round number
            players - list of player objects belonging to player class, the 4 players of the game
            score_inputs - DataFrame of raw scores for each round
            round_scores - DataFrame of scores for each round for each player
            total_scores - DataFrame of cumulative scores over rounds
    Outputs:
            players - list of player objects once updated
            score_inputs - updated DataFrame of raw scores for each round
            round_scores - updated DataFrame of scores for each round for each player
            total_scores - updated DataFrame of cumulative scores over rounds
    """

    # define this round string
    this_round = f'Round {round_num}'
    prev_round = f'Round {round_num - 1}'

    # get new mahjong player
    # mahjong = input('Mahjong player: ')
    mahjong = 'p2'

    for player in players:
        if mahjong == player.name:
            player.mahjong = 1
        else:
            player.mahjong = 0

    # initialise winning and losing players list for this round
    winner = []
    losers = []

    # initialise DataFrame row and take score inputs
    for player in players:

        round_scores.loc[this_round, player.name] = 0
        total_scores.loc[this_round, player.name] = 0

        # player.score = int(input(f'{player.name} score: '))
        player.score = np.random.randint(0, 56)
        score_inputs.loc[this_round, player.name] = player.score

        if player.mahjong == 1:
            mahjong_score = player.score
            winner.append(player)

            if player.east_wind == 1:
                multiplier = 2
            else:
                multiplier = 1

        else:
            losers.append(player)

    # for mahjong player
    for player in winner:
        if player.east_wind == 1:
            round_scores.loc[this_round, player.name] += 6 * mahjong_score
        else:
            round_scores.loc[this_round, player.name] += 3 * mahjong_score

    # for losing players
    for player in losers:
        round_scores.loc[this_round, player.name] -= multiplier * mahjong_score
        for other in losers:
            if player.east_wind == 1:
                diff = 2 * (player.score - other.score)
                round_scores.loc[this_round, player.name] += diff
            else:
                diff = player.score - other.score
                round_scores.loc[this_round, player.name] += diff

    # update totals
    for player in players:
        if this_round == 'Round 1':
            total_scores.loc[this_round, player.name] = round_scores.loc[this_round, player.name]
        else:
            total_scores.loc[this_round, player.name] = total_scores.loc[prev_round, player.name] + round_scores.loc[this_round, player.name]

    return players, score_inputs, round_scores, total_scores, round_num


def plotting(score_inputs, round_scores, total_scores, round_num):

    input_text = []
    round_text = []
    total_text = []

    for row in range(len(score_inputs)):
        input_text.append(score_inputs.iloc[row])
        round_text.append(round_scores.iloc[row])
        total_text.append(total_scores.iloc[row])

    fig_input = plt.figure(figsize=(11, 4), facecolor='aliceblue')
    ax1 = fig_input.add_subplot(111)

    ax1.axis('off')

    input_table = plt.table(
                    cellText=input_text,
                    colLabels=score_inputs.columns,
                    rowLabels=score_inputs.index,
                    cellLoc='center',
                    bbox=[0.06, 0, 1, 1],
                    colColours=['deepskyblue']*10,
                    rowColours=['deepskyblue']*10,
                    cellColours=[['lightblue']*4]*round_num
    )

    input_table.scale(1, 3)

    for (row, col), cell in input_table.get_celld().items():
        if row == 0 or col == -1:
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    ax1.set_title('Inputted Scores', fontweight='bold', fontsize=24)
    input_table.set_fontsize(20)


players, score_inputs, round_scores, total_scores = game_start(players)
for round in range(1, 8):
    players, score_inputs, round_scores, total_scores, round_num = end_round(round, players, round_scores, total_scores)
plotting(score_inputs, round_scores, total_scores, round_num)
