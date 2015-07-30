# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Tue Jul 28 20:05:50 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FlyApp(object):
    def setupUi(self, FlyApp):
        FlyApp.setObjectName("FlyApp")
        FlyApp.resize(800, 600)
        FlyApp.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtGui.QWidget(FlyApp)
        self.centralwidget.setObjectName("centralwidget")
        self.gameField_w = QtGui.QWidget(self.centralwidget)
        self.gameField_w.setGeometry(QtCore.QRect(0, 0, 801, 491))
        self.gameField_w.setObjectName("gameField_w")
        FlyApp.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FlyApp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        FlyApp.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FlyApp)
        self.statusbar.setObjectName("statusbar")
        FlyApp.setStatusBar(self.statusbar)
        self.actionNewGame = QtGui.QAction(FlyApp)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionExit = QtGui.QAction(FlyApp)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNewGame)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(FlyApp)
        QtCore.QMetaObject.connectSlotsByName(FlyApp)

    def retranslateUi(self, FlyApp):
        FlyApp.setWindowTitle(QtGui.QApplication.translate("FlyApp", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("FlyApp", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("FlyApp", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewGame.setText(QtGui.QApplication.translate("FlyApp", "New Game", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("FlyApp", "Exit", None, QtGui.QApplication.UnicodeUTF8))

