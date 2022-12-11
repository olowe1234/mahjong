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
        self.setMinimumSize(QSize(1500, 700))

        ### PLAYER NAME INPUTS ###
        # define a buffer
        buffer = 10

        # define positions of name labels
        name_x = 20
        name_width = 75
        name_y = 50
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
        self.nameTitle.move(name_in_x, buffer)
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

        # add confirm button to names and
        self.name_button = QPushButton('Confirm', self)
        self.name_button.move(name_in_x, name_in_y + 4 * (name_in_height + buffer))
        self.name_button.resize(100, name_in_height)
        self.name_button.clicked.connect(self.update_names)

    def update_names(self):
        p1.name = self.name1Input.text()
        p2.name = self.name2Input.text()
        p3.name = self.name3Input.text()
        p4.name = self.name4Input.text()


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

