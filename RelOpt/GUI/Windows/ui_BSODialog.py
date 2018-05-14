
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

class Ui_BSODialog(object):
    def setupUi(self, BSODialog):
        BSODialog.setObjectName(_fromUtf8("BSODialog"))
        BSODialog.resize(333, 79)
        self.gridLayout = QtGui.QGridLayout(BSODialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Run = QtGui.QPushButton(BSODialog)
        self.Run.setObjectName(_fromUtf8("Run"))
        self.horizontalLayout.addWidget(self.Run)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(BSODialog)
        QtCore.QObject.connect(self.Run, QtCore.SIGNAL(_fromUtf8("clicked()")), BSODialog.run)
        QtCore.QMetaObject.connectSlotsByName(BSODialog)

    def retranslateUi(self, BSODialog):
        BSODialog.setWindowTitle(_translate("BSODialog", "Bat Swarm Optimisation", None))
        self.Run.setText(_translate("BSODialog", "Run", None))

import resources_rc
