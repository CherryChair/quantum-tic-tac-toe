# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_rules_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView



class Ui_rulesWidget(object):
    def setupUi(self, rulesWidget):
        if not rulesWidget.objectName():
            rulesWidget.setObjectName(u"rulesWidget")
        rulesWidget.resize(856, 553)
        self.horizontalLayout = QHBoxLayout(rulesWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.webEngineView = QWebEngineView(rulesWidget)
        self.webEngineView.setObjectName(u"webView")
        self.webEngineView.load(QUrl(u"https://en.wikipedia.org/wiki/Quantum_tic-tac-toe"))

        self.horizontalLayout.addWidget(self.webEngineView)


        self.retranslateUi(rulesWidget)

        QMetaObject.connectSlotsByName(rulesWidget)
    # setupUi

    def retranslateUi(self, rulesWidget):
        rulesWidget.setWindowTitle(QCoreApplication.translate("rulesWidget", u"Form", None))
    # retranslateUi

