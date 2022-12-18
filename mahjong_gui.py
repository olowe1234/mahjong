"""
Ollie Lowe
10-12-2022
"""

"""
Script to run a GUI to keep score for Mahjong games
Intention is to save as an executable and be user friendly
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # set name and size of window
        self.setWindowTitle("Mahjong Scorer")
        self.setMinimumSize(QSize(650, 400))

        # set round number
        self.round_num = 1
        self.high_round = 0

        # define a buffer
        buffer = 10

        # define positions of name labels
        name_x = 20
        name_width = 75
        name_y = 100
        name_height = 40

        # define positions of name inputs
        name_in_x = name_x + name_width + buffer
        name_in_width = 150
        name_in_y = name_y
        name_in_height = name_height

        # name title
        self.nameTitle = QLabel(self)
        self.nameTitle.setText('Player Names')
        self.nameTitle.setFont(QFont("Times", weight=QFont.Bold))
        self.nameTitle.move(name_in_x, name_y - 4 * buffer)
        self.nameTitle.resize(name_in_width, name_in_height)

        # create name labels
        self.name1Label = QLabel(self)
        self.name2Label = QLabel(self)
        self.name3Label = QLabel(self)
        self.name4Label = QLabel(self)

        # set name labels
        self.name1Label.setText('Player 1:')
        self.name2Label.setText('Player 2:')
        self.name3Label.setText('Player 3:')
        self.name4Label.setText('Player 4:')
        self.name_label_list = [self.name1Label, self.name2Label, self.name3Label, self.name4Label]
        for i in range(4):
            self.name_label_list[i].setFont(QFont("Times", weight=QFont.Bold))

        # move name labels into position
        self.name1Label.move(name_x, name_y)
        self.name2Label.move(name_x, name_y + name_height + buffer)
        self.name3Label.move(name_x, name_y + 2 * (name_height + buffer))
        self.name4Label.move(name_x, name_y + 3 * (name_height + buffer))

        # resize name labels
        self.name1Label.resize(name_width, name_height)
        self.name2Label.resize(name_width, name_height)
        self.name3Label.resize(name_width, name_height)
        self.name4Label.resize(name_width, name_height)

        # create input lines for names
        self.name1Input = QLineEdit(self)
        self.name2Input = QLineEdit(self)
        self.name3Input = QLineEdit(self)
        self.name4Input = QLineEdit(self)

        # move name inputs
        self.name1Input.move(name_in_x, name_in_y)
        self.name2Input.move(name_in_x, name_in_y + name_in_height + buffer)
        self.name3Input.move(name_in_x, name_in_y + 2 * (name_in_height + buffer))
        self.name4Input.move(name_in_x, name_in_y + 3 * (name_in_height + buffer))

        # resize name inputs
        self.name1Input.resize(name_in_width, name_in_height)
        self.name2Input.resize(name_in_width, name_in_height)
        self.name3Input.resize(name_in_width, name_in_height)
        self.name4Input.resize(name_in_width, name_in_height)

        self.name_list = [self.name1Input, self.name2Input, self.name3Input, self.name4Input]

        # set round input distances
        round_x = name_width + name_in_width + 4 * buffer
        round_y = 2 * buffer

        # round title
        self.roundTitle = QLabel(self)
        self.roundTitle.setText('Round 1')
        self.roundTitle.move(round_x, round_y)
        self.roundTitle.resize(name_in_width, name_in_height)
        self.roundTitle.setFont(QFont("Times", 10, weight=QFont.Bold))

        # wind and mahjong titles
        self.windTitle = QLabel(self)
        self.windTitle.setText('Wind')
        self.windTitle.move(round_x + buffer, name_y - 4 * buffer)
        self.windTitle.resize(name_in_width, name_in_height)
        self.windTitle.setFont(QFont("Times", weight=QFont.Bold))

        self.mjTitle = QLabel(self)
        self.mjTitle.setText('Mahjong')
        self.mjTitle.move(round_x + 9 * buffer, name_y - 4 * buffer)
        self.mjTitle.resize(name_in_width, name_in_height)
        self.mjTitle.setFont(QFont("Times", weight=QFont.Bold))

        # add wind dropdowns
        self.wind1List = QComboBox(self)
        self.wind1List.addItems(winds)
        self.wind1List.move(round_x, name_y)
        self.wind1List.resize(name_width, name_in_height)
        self.wind1List.setCurrentIndex(0)

        self.wind2List = QComboBox(self)
        self.wind2List.addItems(winds)
        self.wind2List.move(round_x, name_y + name_in_height + buffer)
        self.wind2List.resize(name_width, name_in_height)
        self.wind2List.setCurrentIndex(1)

        self.wind3List = QComboBox(self)
        self.wind3List.addItems(winds)
        self.wind3List.move(round_x, name_y + 2 * (name_in_height + buffer))
        self.wind3List.resize(name_width, name_in_height)
        self.wind3List.setCurrentIndex(2)

        self.wind4List = QComboBox(self)
        self.wind4List.addItems(winds)
        self.wind4List.move(round_x, name_y + 3 * (name_in_height + buffer))
        self.wind4List.resize(name_width, name_in_height)
        self.wind4List.setCurrentIndex(3)

        # auto change winds if one is changed by using auto_wind function
        wind1_slot = lambda: self.auto_wind(1)
        wind2_slot = lambda: self.auto_wind(2)
        wind3_slot = lambda: self.auto_wind(3)
        wind4_slot = lambda: self.auto_wind(4)
        self.wind1List.activated.connect(wind1_slot)
        self.wind2List.activated.connect(wind2_slot)
        self.wind3List.activated.connect(wind3_slot)
        self.wind4List.activated.connect(wind4_slot)

        self.wind_list = [self.wind1List, self.wind2List, self.wind3List, self.wind4List]

        # add mahjong check boxes
        tickx = round_x + 11 * buffer
        ticky = name_y + 5

        self.mj_tick1 = QCheckBox(self)
        self.mj_tick1.move(tickx, ticky)
        self.mj_tick1 = self.set_tick_style(self.mj_tick1)

        self.mj_tick2 = QCheckBox(self)
        self.mj_tick2.move(tickx, ticky + name_in_height + buffer)
        self.mj_tick2 = self.set_tick_style(self.mj_tick2)

        self.mj_tick3 = QCheckBox(self)
        self.mj_tick3.move(tickx, ticky + 2 * (name_in_height + buffer))
        self.mj_tick3 = self.set_tick_style(self.mj_tick3)

        self.mj_tick4 = QCheckBox(self)
        self.mj_tick4.move(tickx, ticky + 3 * (name_in_height + buffer))
        self.mj_tick4 = self.set_tick_style(self.mj_tick4)

        self.mj_list = [self.mj_tick1, self.mj_tick2, self.mj_tick3, self.mj_tick4]

        # automatically unchecks other mahjong boxes when one is clicked
        mahjong1 = lambda: self.auto_mahjong(1)
        mahjong2 = lambda: self.auto_mahjong(2)
        mahjong3 = lambda: self.auto_mahjong(3)
        mahjong4 = lambda: self.auto_mahjong(4)
        self.mj_tick1.clicked.connect(mahjong1)
        self.mj_tick2.clicked.connect(mahjong2)
        self.mj_tick3.clicked.connect(mahjong3)
        self.mj_tick4.clicked.connect(mahjong4)

        # score box positions
        score_x = tickx + name_width

        # add scores label
        self.scoresTitle = QLabel(self)
        self.scoresTitle.setText('Score')
        self.scoresTitle.move(score_x + buffer, name_y - 4 * buffer)
        self.scoresTitle.resize(name_width, name_height)
        self.scoresTitle.setFont(QFont("Times", weight=QFont.Bold))

        # allow only integers
        self.int_val = QIntValidator()

        # add score inputs
        self.score1 = QLineEdit(self)
        self.score1.setValidator(self.int_val)
        self.score1.setText('0')
        self.score1.move(score_x, name_y)
        self.score1.resize(name_width, name_height)

        self.score2 = QLineEdit(self)
        self.score2.setValidator(self.int_val)
        self.score2.setText('0')
        self.score2.move(score_x, name_y + (name_in_height + buffer))
        self.score2.resize(name_width, name_height)

        self.score3 = QLineEdit(self)
        self.score3.setValidator(self.int_val)
        self.score3.setText('0')
        self.score3.move(score_x, name_y + 2 * (name_in_height + buffer))
        self.score3.resize(name_width, name_height)

        self.score4 = QLineEdit(self)
        self.score4.setValidator(self.int_val)
        self.score4.setText('0')
        self.score4.move(score_x, name_y + 3 * (name_in_height + buffer))
        self.score4.resize(name_width, name_height)

        self.scores_list = [self.score1, self.score2, self.score3, self.score4]
        
        # add a confirm button for all things this round
        button_width = name_width
        self.round_button = QPushButton('Confirm\nRound', self)
        self.round_button.move(tickx + 2 * buffer + 2 * button_width, name_y)
        self.round_button.resize(button_width, 2 * name_in_height)
        self.round_button.clicked.connect(self.update_all)
        self.round_button.setStyleSheet("background-color: mediumorchid")
        self.round_button.setFont(QFont("Times", weight=QFont.Bold))

        # add a previous round button to go to previous round
        self.previous_button = QPushButton('Previous Round', self)
        self.previous_button.move(name_in_x + 4 * buffer, name_y + buffer + 4 * (name_in_height + buffer))
        self.previous_button.resize(2 * button_width, name_in_height)
        self.previous_button.setStyleSheet("background-color: lightblue")
        self.previous_button.clicked.connect(self.previous_round)
        self.previous_button.setFont(QFont("Times", weight=QFont.Bold))

        # add a next round button to go to next round
        self.next_button = QPushButton('Next Round', self)
        self.next_button.move(name_in_x + 3 * (button_width), name_y + buffer + 4 * (name_in_height + buffer))
        self.next_button.resize(2 * button_width, name_in_height)
        self.next_button.setStyleSheet("background-color: lightblue")
        self.next_button.clicked.connect(self.next_round)
        self.next_button.setFont(QFont("Times", weight=QFont.Bold))

        # add a scoring button to calculate and show scores
        self.score_button = QPushButton('Show\nScores', self)
        self.score_button.move(tickx + 2 * buffer + 2 * button_width, name_y + 2 * (name_in_height + buffer))
        self.score_button.resize(button_width, 2 * name_in_height)
        self.score_button.setStyleSheet("background-color: mediumorchid")
        self.score_button.clicked.connect(self.plotting)
        self.score_button.setFont(QFont("Times", weight=QFont.Bold))

        # create green tick to represent a round being confirmed
        self.green_tick = QLabel(self)
        self.green_tick_pic = QPixmap('green_tick_final.jpg')
        self.green_tick.setPixmap(self.green_tick_pic)
        self.green_tick.setAlignment(Qt.AlignCenter)
        self.green_tick.move(tickx, round_y + buffer)
        self.green_tick.resize(40, 20)
        self.green_tick.setScaledContents(True)
        self.green_tick.setHidden(True)

    def set_tick_style(self, checkbox):
        """
        Change styling of tick boxes
        """
        checkbox.setStyleSheet("QCheckBox::indicator"
                               "{"
                               "width :30;"
                               "height : 30;"
                               "}")
        return checkbox

    def auto_mahjong(self, mj_num):
        """
        Uncheck other mahjong boxes when one is checked
        """
        # uncheck all
        for mj_tick in self.mj_list:
            mj_tick.setChecked(False)

        # check appropriate one
        self.mj_list[mj_num - 1].setChecked(True)

        return self.mj_tick1, self.mj_tick2, self.mj_tick3, self.mj_tick4

    def auto_wind(self, wind_num):
        """
        Take wind that has been changed by user and change the other winds accordingly.
        """
        idx = self.wind_list[wind_num - 1].currentIndex()
        self.wind_list[wind_num - 2].setCurrentText(winds[idx - 1])
        self.wind_list[wind_num - 3].setCurrentText(winds[idx - 2])
        self.wind_list[wind_num - 4].setCurrentText(winds[idx - 3])
        return self.wind1List, self.wind2List, self.wind3List, self.wind4List

    def update_names(self):
        """
        Update names of players when inputs are confirmed
        """
        for i in range(4):
            players[i].name = self.name_list[i].text()
            print(f'{players[i].name}')

        # initialise scoreboards
        for df in df_list:
            df.columns = [players[i].name for i in range(4)]

        return p1, p2, p3, p4

    def update_winds(self):
        """
        Update winds of players when changed
        """
        for i in range(4):
            players[i].wind[self.round_num - 1] = self.wind_list[i].currentText()
            print(f'{players[i].name}: {players[i].wind[self.round_num - 1]}')

        for player in players:
            wind_inputs.loc[f'Round {self.round_num}', f'{player.name}'] = player.wind[self.round_num - 1]

        return p1, p2, p3, p4

    def update_mahjong(self):
        """
        Update mahjong player when changed
        """
        for i in range(4):
            players[i].mahjong[self.round_num - 1] = self.mj_list[i].isChecked()
            print(f'{players[i].name}: {players[i].mahjong[self.round_num - 1]}')

        for player in players:
            mj_inputs.loc[f'Round {self.round_num}', f'{player.name}'] = player.mahjong[self.round_num - 1]

        return p1, p2, p3, p4

    def update_scores(self):
        """
        Update player scores
        """
        for i in range(4):
            players[i].score[self.round_num - 1] = int(self.scores_list[i].text())
            print(f'{players[i].name}: {players[i].score[self.round_num - 1]}')

        # update score inputs DataFrame
        for i in range(4):
            score_inputs.loc[f'Round {self.round_num}', f'{players[i].name}'] = players[i].score[self.round_num - 1]

        return p1, p2, p3, p4

    def update_round_scores(self):
        """
        Calculate round scores from score inputs
        """

        # go back through all rounds and calculate round scores
        self.rounds = [f'Round {rnd + 1}' for rnd in range(len(score_inputs))]

        # for all rounds
        for round in self.rounds:
            self.losers = []

            # for each player
            for player in players:
                if mj_inputs.loc[round, player.name]:
                    # define mahjong score and winner
                    self.mahjong_score = score_inputs.loc[round, player.name]
                    self.winner = player
                else:
                    self.losers.append(player)

            # if East wins
            if wind_inputs.loc[round, f'{self.winner.name}'] == 'East':
                self.east_win = True
                round_scores.loc[round, f'{self.winner.name}'] = 6 * self.mahjong_score
            # if East hasn't won
            else:
                self.east_win = False
                round_scores.loc[round, f'{self.winner.name}'] = 3 * self.mahjong_score

            # for losing players
            for player in self.losers:
                round_scores.loc[round, player.name] = 0
                # subtract mahjong score, doubled if East or mahjong was East
                if self.east_win or wind_inputs.loc[round, player.name] == 'East':
                    round_scores.loc[round, player.name] -= 2 * self.mahjong_score
                else:
                    round_scores.loc[round, player.name] -= self.mahjong_score

                for other in self.losers:
                    # don't want player compared to themselves
                    if other != player:
                        if wind_inputs.loc[round, player.name] == 'East' or wind_inputs.loc[round, other.name] == 'East':
                            self.diff = 2 * (score_inputs.loc[round, player.name] - score_inputs.loc[round, other.name])
                            round_scores.loc[round, player.name] += self.diff
                        else:
                            self.diff = score_inputs.loc[round, player.name] - score_inputs.loc[round, other.name]
                            round_scores.loc[round, player.name] += self.diff

    def update_total_scores(self):
        """
        Calculate total scores from round scores
        """
        self.rounds = [f'Round {rnd + 1}' for rnd in range(len(score_inputs))]

        # for all rounds
        for round in self.rounds:
            for player in players:
                if round == 'Round 1':
                    total_scores.loc[round, player.name] = round_scores.loc[round, player.name]
                else:
                    self.prev_round = self.rounds[self.rounds.index(round) - 1]
                    total_scores.loc[round, player.name] = total_scores.loc[self.prev_round, player.name] + round_scores.loc[round, player.name]

    def update_all(self):
        """
        Update names, winds, mahjong and scores
        """
        self.mj_tick_list = [self.mj_tick1.isChecked(), self.mj_tick2.isChecked(), self.mj_tick3.isChecked(), self.mj_tick4.isChecked()]
        self.score_input_list = [int(self.score1.text()), int(self.score2.text()), int(self.score3.text()), int(self.score4.text())]

        if sum(self.mj_tick_list) > 0 and sum(self.score_input_list) > 0:

            self.update_names()
            self.update_winds()
            self.update_mahjong()
            self.update_scores()
            self.update_round_scores()
            self.update_total_scores()

            for i in range(4):
                self.round_idx = self.round_num - 1
                print(f'{players[i].name}: {players[i].wind[self.round_idx]}, {players[i].mahjong[self.round_idx]}, {players[i].score[self.round_idx]}')

            if self.round_num > self.high_round:
                self.high_round = self.round_num
                self.green_tick.setHidden(False)

            print(score_inputs)
            print(round_scores)
            print(total_scores)

        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            if sum(self.mj_tick_list) == 0 and sum(self.score_input_list) == 0:
                self.msg.setText("No Mahjong player ticked\nNo scores")
            elif sum(self.mj_tick_list) == 0:
                self.msg.setText("No Mahjong player ticked")
            elif sum(self.score_input_list) == 0:
                self.msg.setText("No scores")
            self.msg.setWindowTitle("Can't Confirm Round")
            self.msg.exec_()

    def next_round(self):
        """
        Move onto next round
        """
        # increase round number
        self.round_num += 1

        # green tick if already confirmed round
        if len(total_scores) >= self.round_num:
            self.green_tick.setHidden(False)
        else:
            self.green_tick.setHidden(True)

        # change round label
        self.roundTitle.setText(f'Round {self.round_num}')

        # if never saved a round this high
        if self.round_num > self.high_round:

            # change winds based on who was mahjong
            no_change = False
            for i in range(4):
                if self.mj_list[i].isChecked() and self.wind_list[i].currentText() == 'East':
                    no_change = True

            for wind in self.wind_list:
                if not no_change:
                    idx = wind.currentIndex()
                    wind.setCurrentText(winds[idx - 1])

            # untick Mahjong boxes
            for box in self.mj_list:
                box.setChecked(False)

            # add an empty item to score list for each player
            for player in players:
                player.wind.append('Unknown')
                player.mahjong.append(False)
                player.score.append(0)

            # reset scores to 0 for next round
            for score in self.scores_list:
                score.setText('0')

        # if already have things saved
        else:
            # change winds, mahjong and scores back to what they were in that round
            for i in range(4):
                self.wind_list[i].setCurrentText(f'{players[i].wind[self.round_num - 1]}')
                if players[i].mahjong[self.round_num - 1]:
                    self.mj_list[i].setChecked(True)
                else:
                    self.mj_list[i].setChecked(False)
                self.scores_list[i].setText(f'{players[i].score[self.round_num - 1]}')

    def previous_round(self):
        """
        Move back to previous round
        """

        # change round number (can't go to round 0)
        if self.round_num != 1:
            self.round_num -= 1

        # green tick if already confirmed round
        if len(total_scores) >= self.round_num:
            self.green_tick.setHidden(False)
        else:
            self.green_tick.setHidden(True)

        # change round label
        self.roundTitle.setText(f'Round {self.round_num}')

        # change winds, mahjong and scores back to what they were in that round
        for i in range(4):
            self.wind_list[i].setCurrentText(f'{players[i].wind[self.round_num - 1]}')
            if players[i].mahjong[self.round_num - 1]:
                self.mj_list[i].setChecked(True)
            else:
                self.mj_list[i].setChecked(False)
            self.scores_list[i].setText(f'{players[i].score[self.round_num - 1]}')

    def plotting(self):
        """
        Plots tables of scores
        """

        plt.close('all')

        # turn dataframes into table formats
        input_text = []
        round_text = []
        total_text = []

        for row in range(len(score_inputs)):
            input_text.append(score_inputs.iloc[row])
            round_text.append(round_scores.iloc[row])
            total_text.append(total_scores.iloc[row])

        fig = plt.figure(figsize=(10, 9), facecolor='whitesmoke')
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
            colColours=['deepskyblue'] * 4,
            rowColours=['deepskyblue'] * 10,
            cellColours=[['lightblue'] * 4] * self.high_round
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
            colColours=['orange'] * 4,
            rowColours=['orange'] * 10,
            cellColours=[['moccasin'] * 4] * self.high_round
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
            colColours=['green'] * 4,
            rowColours=['green'] * 10,
            cellColours=[['palegreen'] * 4] * self.high_round
        )

        for (row, col), cell in total_table.get_celld().items():
            if row == 0 or col == -1:
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))

        total_table.set_fontsize(12)

        fig.tight_layout(pad=1)

class player():
    def __init__(self):
        self.name = ['dave']
        self.wind = ['East']
        self.mahjong = [False]
        self.score = [0]

# initialise player classes
p1 = player()
p2 = player()
p3 = player()
p4 = player()

players = [p1, p2, p3, p4]

# create list of winds
winds = ['East', 'South', 'West', 'North']

# initialise scoreboards
score_inputs = pd.DataFrame(columns=['p1', 'p2', 'p3', 'p4'])
round_scores = pd.DataFrame(columns=['p1', 'p2', 'p3', 'p4'])
total_scores = pd.DataFrame(columns=['p1', 'p2', 'p3', 'p4'])
wind_inputs = pd.DataFrame(columns=['p1', 'p2', 'p3', 'p4'])
mj_inputs = pd.DataFrame(columns=['p1', 'p2', 'p3', 'p4'])
df_list = [score_inputs, round_scores, total_scores, wind_inputs, mj_inputs]

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec()
