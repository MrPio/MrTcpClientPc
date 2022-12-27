import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from view.res import my_res

class MyMainWindow(QMainWindow):
    def __init__(self, uiFile):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        loadUi(uiFile, self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
