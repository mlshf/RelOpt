
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

class Ui_FADialog(object):
    def setupUi(self, FADialog):
        FADialog.setObjectName(_fromUtf8("FADialog"))
        FADialog.resize(333, 79)
        self.gridLayout = QtGui.QGridLayout(FADialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Run = QtGui.QPushButton(FADialog)
        self.Run.setObjectName(_fromUtf8("Run"))
        self.horizontalLayout.addWidget(self.Run)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(FADialog)
        QtCore.QObject.connect(self.Run, QtCore.SIGNAL(_fromUtf8("clicked()")), FADialog.run)
        QtCore.QMetaObject.connectSlotsByName(FADialog)

    def retranslateUi(self, FADialog):
        FADialog.setWindowTitle(_translate("FADialog", "Firefly Algorithm", None))
        self.Run.setText(_translate("FADialog", "Run", None))

import resources_rc
