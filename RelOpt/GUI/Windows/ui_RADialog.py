
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

class Ui_RADialog(object):
    def setupUi(self, RADialog):
        RADialog.setObjectName(_fromUtf8("RADialog"))
        RADialog.resize(370, 263)
        self.gridLayout = QtGui.QGridLayout(RADialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.checkBox = QtGui.QCheckBox(RADialog)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.label_2 = QtGui.QLabel(RADialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton = QtGui.QPushButton(RADialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.spinBox_2 = QtGui.QSpinBox(RADialog)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(500000)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.verticalLayout_4.addWidget(self.spinBox_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox = QtGui.QComboBox(RADialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 2)

        self.retranslateUi(RADialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), RADialog.slot2)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), RADialog.slot4)
        QtCore.QMetaObject.connectSlotsByName(RADialog)

    def retranslateUi(self, RADialog):
        RADialog.setWindowTitle(_translate("RADialog", "Random Algorithm", None))
        self.label_2.setText(_translate("RADialog", "   Shake each", None))
        self.pushButton.setText(_translate("RADialog", "Run", None))
        self.comboBox.setItemText(0, _translate("RADialog", "iterations", None))
        self.comboBox.setItemText(1, _translate("RADialog", "iterations without changing", None))

import resources_rc
