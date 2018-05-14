
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

class Ui_BADialog(object):
    def setupUi(self, BADialog):
        BADialog.setObjectName(_fromUtf8("BADialog"))
        BADialog.resize(333, 79)
        self.gridLayout = QtGui.QGridLayout(BADialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Run = QtGui.QPushButton(BADialog)
        self.Run.setObjectName(_fromUtf8("Run"))
        self.horizontalLayout.addWidget(self.Run)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(BADialog)
        QtCore.QObject.connect(self.Run, QtCore.SIGNAL(_fromUtf8("clicked()")), BADialog.run)
        QtCore.QMetaObject.connectSlotsByName(BADialog)

    def retranslateUi(self, BADialog):
        BADialog.setWindowTitle(_translate("BADialog", "Bees Algorithm", None))
        self.Run.setText(_translate("BADialog", "Run", None))

import resources_rc
