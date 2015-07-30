# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FlyApp(object):
    def setupUi(self, FlyApp):
        FlyApp.setObjectName(_fromUtf8("FlyApp"))
        FlyApp.resize(800, 600)
        FlyApp.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtGui.QWidget(FlyApp)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gameField_w = QtGui.QWidget(self.centralwidget)
        self.gameField_w.setGeometry(QtCore.QRect(0, 0, 801, 491))
        self.gameField_w.setObjectName(_fromUtf8("gameField_w"))
        FlyApp.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FlyApp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        FlyApp.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FlyApp)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        FlyApp.setStatusBar(self.statusbar)
        self.actionNewGame = QtGui.QAction(FlyApp)
        self.actionNewGame.setObjectName(_fromUtf8("actionNewGame"))
        self.actionExit = QtGui.QAction(FlyApp)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNewGame)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(FlyApp)
        QtCore.QMetaObject.connectSlotsByName(FlyApp)

    def retranslateUi(self, FlyApp):
        FlyApp.setWindowTitle(_translate("FlyApp", "MainWindow", None))
        self.menuFile.setTitle(_translate("FlyApp", "File", None))
        self.menuAbout.setTitle(_translate("FlyApp", "About", None))
        self.actionNewGame.setText(_translate("FlyApp", "New Game", None))
        self.actionExit.setText(_translate("FlyApp", "Exit", None))

