
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

class Ui_TSDialog(object):
    def setupUi(self, TSDialog):
        TSDialog.setObjectName(_fromUtf8("TSDialog"))
        TSDialog.resize(311, 263)
        self.gridLayout = QtGui.QGridLayout(TSDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton = QtGui.QPushButton(TSDialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.spinBox = QtGui.QSpinBox(TSDialog)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.verticalLayout.addWidget(self.spinBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(TSDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(TSDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 3, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.checkBox = QtGui.QCheckBox(TSDialog)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.label_2 = QtGui.QLabel(TSDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.spinBox_2 = QtGui.QSpinBox(TSDialog)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(500000)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.verticalLayout_4.addWidget(self.spinBox_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 1, 1, 2)

        self.retranslateUi(TSDialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), TSDialog.slot2)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(QString)")), TSDialog.slot1)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), TSDialog.slot4)
        QtCore.QMetaObject.connectSlotsByName(TSDialog)

    def retranslateUi(self, TSDialog):
        TSDialog.setWindowTitle(_translate("TSDialog", "Tabu Search", None))
        self.pushButton.setText(_translate("TSDialog", "Run", None))
        self.label.setText(_translate("TSDialog", "Tabu list volume", None))
        self.label_3.setText(_translate("TSDialog", " iterations", None))
        self.label_2.setText(_translate("TSDialog", "   Shake each", None))

import resources_rc
