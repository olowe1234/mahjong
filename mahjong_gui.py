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
        self.setMinimumSize(QSize(700, 450))

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

        # add confirm button to names
        button_width = 75
        self.name_button = QPushButton('Confirm Names', self)
        self.name_button.move(name_in_x, name_in_y + 4 * (name_in_height + buffer))
        self.name_button.resize(2 * button_width, name_in_height)
        self.name_button.clicked.connect(self.update_names)

        # set round input distances
        round_x = name_width + name_in_width + 4 * buffer
        round_y = 2 * buffer

        # round title
        self.roundTitle = QLabel(self)
        self.roundTitle.setText('Round 1')
        self.roundTitle.move(round_x, round_y)
        self.roundTitle.resize(name_in_width, name_in_height)
        self.roundTitle.setFont(QFont("Times", weight=QFont.Bold))

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

        # add confirm button to winds
        self.wind_button = QPushButton('Confirm\nWinds', self)
        self.wind_button.move(round_x, name_y + 4 * (name_in_height + buffer))
        self.wind_button.resize(button_width, 2 * name_in_height)
        self.wind_button.clicked.connect(self.update_winds)

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

        # add confirm button to mahjong
        self.mj_button = QPushButton('Confirm\nMahjong', self)
        self.mj_button.move(tickx - 2 * buffer, name_y + 4 * (name_in_height + buffer))
        self.mj_button.resize(button_width, 2 * name_in_height)
        self.mj_button.clicked.connect(self.update_mahjong)

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

        # add confirm button to scores
        self.scores_button = QPushButton('Confirm\nScores', self)
        self.scores_button.move(score_x, name_y + 4 * (name_in_height + buffer))
        self.scores_button.resize(button_width, 2 * name_in_height)
        self.scores_button.clicked.connect(self.update_scores)
        
        # add a confirm button for all things this round
        self.round_button = QPushButton('Confirm\nRound', self)
        self.round_button.move(tickx + buffer + 2 * button_width, name_y + (name_in_height + 2 * buffer))
        self.round_button.resize(button_width, 2 * name_in_height)
        self.round_button.clicked.connect(self.update_all)

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

        return p1, p2, p3, p4

    def update_winds(self):
        """
        Update winds of players when changed
        """
        for i in range(4):
            players[i].wind = self.wind_list[i].currentText()
            print(f'{players[i].name}: {players[i].wind}')

        return p1, p2, p3, p4

    def update_mahjong(self):
        """
        Update mahjong player when changed
        """
        for i in range(4):
            players[i].mahjong = self.mj_list[i].isChecked()
            print(f'{players[i].name}: {players[i].mahjong}')

        return p1, p2, p3, p4

    def update_scores(self):
        """
        Update player scores
        """
        for i in range(4):
            players[i].score = int(self.scores_list[i].text())
            print(f'{players[i].name}: {players[i].score}')

        return p1, p2, p3, p4

    def update_all(self):
        """
        Update names, winds, mahjong and scores
        """
        self.update_names()
        self.update_winds()
        self.update_mahjong()
        self.update_scores()

        for i in range(4):
            print(f'{players[i].name}: {players[i].wind}, {players[i].mahjong}, {players[i].score}')


class player():
    def __init__(self):
        self.name = 'dave'
        self.wind = 'East'
        self.mahjong = False
        self.score = 0

# initialise player classes
p1 = player()
p2 = player()
p3 = player()
p4 = player()

players = [p1, p2, p3, p4]

# create list of winds
winds = ['East', 'South', 'West', 'North']

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec()

    for i in range(4):
        print(f'p{i}: {players[i].name}, {players[i].wind}, {players[i].mahjong}, {players[i].score}')

