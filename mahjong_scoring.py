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
        self.wind = 'east'
        self.mahjong = False
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

    default_names = ['Darren', 'Karen', 'Ollie', 'Tilly']

    # initialise player names
    all_good = 0
    while all_good == 0:
        for i in range(len(winds)):
            # players[i].name = f'{default_names[i]}'
            count = 0
            while count == 0:
                name = input(f'{winds[i]} wind player name: ')
                if type(name) == str:
                    players[i].name = name
                    players[i].wind = winds[i]
                    proceed = input(f'{winds[i]} wind is {players[i].name}, yes? (y/n)')
                    if proceed == 'y':
                        count = 1
        names = [f'{players[j].name}' for j in range(4)]
        all_names = input(f'{names[0]}, {names[1]}, {names[2]} and {names[3]}, yes? (y/n)')
        if all_names == 'y':
            all_good = 1


    # initialise scoreboards
    score_inputs = pd.DataFrame(columns=[players[i].name for i in range(4)])
    round_scores = pd.DataFrame(columns=[players[i].name for i in range(4)])
    total_scores = pd.DataFrame(columns=[players[i].name for i in range(4)])

    # let user decide when to move on
    count = 0
    while count == 0:
        proceed = input('Setup complete, press enter to go to round 1 scoring.')
        if proceed == '':
            count = 1
        else:
            pass

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
    mahjong = input('Mahjong player: ')

    # mahjong = 'Karen'
    # adjust mahjong attribute for each player
    for player in players:
        if mahjong == player.name:
            player.mahjong = True
        else:
            player.mahjong = False

    # initialise winning and losing players list for this round
    winner = []
    losers = []

    for player in players:

        # initialise DataFrame row and take score inputs
        round_scores.loc[this_round, player.name] = 0
        total_scores.loc[this_round, player.name] = 0

        # player.score = int(input(f'{player.name} score: '))
        player.score = np.random.randint(0, 56)
        score_inputs.loc[this_round, player.name] = player.score

        if player.mahjong:

            # save score of mahjong player
            mahjong_score = player.score

            # add mahjong player to winners list
            winner.append(player)

        else:
            # add losing players to losers list
            losers.append(player)

    # for mahjong player
    for player in winner:

        if player.wind == 'East':
            east_win = True
            round_scores.loc[this_round, player.name] += 6 * mahjong_score
        else:
            east_win = False
            round_scores.loc[this_round, player.name] += 4 * mahjong_score

    # for losing players
    for player in losers:
        # subtract mahjong score, doubled if east was mahjong
        if east_win or player.wind == 'East':
            round_scores.loc[this_round, player.name] -= 2 * mahjong_score
        else:
            round_scores.loc[this_round, player.name] -= mahjong_score

        for other in losers:
            # don't want player compared to themselves
            if other != player:
                if player.wind == 'East' or other.wind == 'East':
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

    # create list of winds (players)
    winds = ['East', 'South', 'West', 'North']

    # changing winds
    for player in players:
        # if east goes mahjong they remain east
        if player.mahjong and player.wind == 'East':
            pass

        else:
            idx = winds.index(player.wind)
            player.wind = winds[idx - 3]

    return players, score_inputs, round_scores, total_scores, round_num


def plotting(round_num, score_inputs, round_scores, total_scores):

    """Plots tables and graphs of scores
    Inputs:
        round_num - round number
        score_inputs - DataFrame of raw scores for each round
        round_scores - DataFrame of scores for each round for each player
        total_scores - DataFrame of cumulative scores over rounds
    No Outputs
    """

    # turn dataframes into table formats
    input_text = []
    round_text = []
    total_text = []

    for row in range(len(score_inputs)):
        input_text.append(score_inputs.iloc[row])
        round_text.append(round_scores.iloc[row])
        total_text.append(total_scores.iloc[row])

    fig = plt.figure(figsize=(12, 5), facecolor='whitesmoke')
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    ax1.axis('off')
    ax2.axis('off')
    ax3.axis('off')

    ax1.set_title('Inputted Scores \n', fontweight='bold')
    ax2.set_title('Round Scores \n', fontweight='bold')
    ax3.set_title('Total Scores \n', fontweight='bold')

    # input scores
    input_table = ax1.table(
                    cellText=input_text,
                    colLabels=score_inputs.columns,
                    rowLabels=score_inputs.index,
                    cellLoc='center',
                    loc='center',
                    colColours=['deepskyblue']*4,
                    rowColours=['deepskyblue']*10,
                    cellColours=[['lightblue']*4]*round_num
    )

    for (row, col), cell in input_table.get_celld().items():
        if row == 0 or col == -1:
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    input_table.set_fontsize(12)

    # round scores
    round_table = ax2.table(
                    cellText=round_text,
                    colLabels=round_scores.columns,
                    rowLabels=round_scores.index,
                    cellLoc='center',
                    loc='center',
                    colColours=['orange']*4,
                    rowColours=['orange']*10,
                    cellColours=[['moccasin']*4]*round_num
    )

    for (row, col), cell in round_table.get_celld().items():
        if row == 0 or col == -1:
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    round_table.set_fontsize(12)
    
    # total scores
    total_table = ax3.table(
                    cellText=total_text,
                    colLabels=total_scores.columns,
                    rowLabels=total_scores.index,
                    cellLoc='center',
                    loc='center',
                    colColours=['green']*4,
                    rowColours=['green']*10,
                    cellColours=[['palegreen']*4]*round_num
    )

    for (row, col), cell in total_table.get_celld().items():
        if row == 0 or col == -1:
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    total_table.set_fontsize(12)

    fig.tight_layout(pad=1)


players, score_inputs, round_scores, total_scores = game_start(players)
for round in range(1, 4):
    players, score_inputs, round_scores, total_scores, round_num = end_round(round, players, round_scores, total_scores)
plotting(round_num, score_inputs, round_scores, total_scores)
