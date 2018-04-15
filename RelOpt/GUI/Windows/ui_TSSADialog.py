
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

class Ui_TSSADialog(object):
    def setupUi(self, TSSADialog):
        TSSADialog.setObjectName(_fromUtf8("TSSADialog"))
        TSSADialog.resize(491, 325)
        self.gridLayout = QtGui.QGridLayout(TSSADialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_12 = QtGui.QVBoxLayout()
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.init = QtGui.QLabel(TSSADialog)
        self.init.setObjectName(_fromUtf8("init"))
        self.horizontalLayout_6.addWidget(self.init)
        self.temperature = QtGui.QDoubleSpinBox(TSSADialog)
        self.temperature.setDecimals(4)
        self.temperature.setMinimum(1.0)
        self.temperature.setMaximum(1000000001.0)
        self.temperature.setSingleStep(0.0001)
        self.temperature.setProperty("value", 300.0)
        self.temperature.setObjectName(_fromUtf8("temperature"))
        self.horizontalLayout_6.addWidget(self.temperature)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(TSSADialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.Zero = QtGui.QDoubleSpinBox(TSSADialog)
        self.Zero.setDecimals(6)
        self.Zero.setMinimum(1e-06)
        self.Zero.setMaximum(1000000000.0)
        self.Zero.setSingleStep(1e-06)
        self.Zero.setProperty("value", 0.05)
        self.Zero.setObjectName(_fromUtf8("Zero"))
        self.horizontalLayout_2.addWidget(self.Zero)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_11.addLayout(self.verticalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(TSSADialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.tempRed = QtGui.QComboBox(TSSADialog)
        self.tempRed.setObjectName(_fromUtf8("tempRed"))
        self.tempRed.addItem(_fromUtf8(""))
        self.tempRed.addItem(_fromUtf8(""))
        self.tempRed.addItem(_fromUtf8(""))
        self.tempRed.addItem(_fromUtf8(""))
        self.tempRed.addItem(_fromUtf8(""))
        self.tempRed.addItem(_fromUtf8(""))
        self.tempRed.addItem(_fromUtf8(""))
        self.tempRed.addItem(_fromUtf8(""))
        self.horizontalLayout_8.addWidget(self.tempRed)
        self.divide = QtGui.QDoubleSpinBox(TSSADialog)
        self.divide.setDecimals(4)
        self.divide.setMinimum(0.0001)
        self.divide.setMaximum(1000000000.0)
        self.divide.setSingleStep(0.0001)
        self.divide.setProperty("value", 1.0)
        self.divide.setObjectName(_fromUtf8("divide"))
        self.horizontalLayout_8.addWidget(self.divide)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.verticalLayout_11.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(TSSADialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.mutType = QtGui.QComboBox(TSSADialog)
        self.mutType.setObjectName(_fromUtf8("mutType"))
        self.mutType.addItem(_fromUtf8(""))
        self.mutType.addItem(_fromUtf8(""))
        self.mutType.addItem(_fromUtf8(""))
        self.mutType.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.mutType)
        self.num = QtGui.QSpinBox(TSSADialog)
        self.num.setMinimum(1)
        self.num.setProperty("value", 1)
        self.num.setObjectName(_fromUtf8("num"))
        self.horizontalLayout_5.addWidget(self.num)
        self.verticalLayout_11.addLayout(self.horizontalLayout_5)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_5 = QtGui.QLabel(TSSADialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.spinBox = QtGui.QSpinBox(TSSADialog)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout_3.addWidget(self.spinBox)
        self.shaking = QtGui.QCheckBox(TSSADialog)
        self.shaking.setEnabled(True)
        self.shaking.setText(_fromUtf8(""))
        self.shaking.setObjectName(_fromUtf8("shaking"))
        self.horizontalLayout_3.addWidget(self.shaking)
        self.label_4 = QtGui.QLabel(TSSADialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.shake = QtGui.QSpinBox(TSSADialog)
        self.shake.setMinimum(2)
        self.shake.setMaximum(500000)
        self.shake.setProperty("value", 10)
        self.shake.setObjectName(_fromUtf8("shake"))
        self.horizontalLayout_3.addWidget(self.shake)
        self.label_6 = QtGui.QLabel(TSSADialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.verticalLayout_11.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem4)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.pushButton = QtGui.QPushButton(TSSADialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_4.addWidget(self.pushButton)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout_11.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_11)
        self.verticalLayout_12.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_12, 0, 0, 1, 1)

        self.retranslateUi(TSSADialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), TSSADialog.run)
        QtCore.QObject.connect(self.mutType, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), TSSADialog.mutateChange)
        QtCore.QObject.connect(self.tempRed, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), TSSADialog.tempReduceChange)
        QtCore.QObject.connect(self.shaking, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), TSSADialog.shakingSwitch)
        QtCore.QObject.connect(self.temperature, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), TSSADialog.initTempChange)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), TSSADialog.slot1)
        QtCore.QMetaObject.connectSlotsByName(TSSADialog)

    def retranslateUi(self, TSSADialog):
        TSSADialog.setWindowTitle(_translate("TSSADialog", "Tabu Search Simulated Annealing Algorithm", None))
        self.init.setText(_translate("TSSADialog", "Initial Temperature:", None))
        self.label.setText(_translate("TSSADialog", "Zero-temperature level:", None))
        self.label_3.setText(_translate("TSSADialog", "Temperature reduce function type:", None))
        self.tempRed.setItemText(0, _translate("TSSADialog", "Reduce", None))
        self.tempRed.setItemText(1, _translate("TSSADialog", "Power Reduce", None))
        self.tempRed.setItemText(2, _translate("TSSADialog", "Extinguishing", None))
        self.tempRed.setItemText(3, _translate("TSSADialog", "Random Existinguishing", None))
        self.tempRed.setItemText(4, _translate("TSSADialog", "Bolcman Law", None))
        self.tempRed.setItemText(5, _translate("TSSADialog", "Cawshi Law", None))
        self.tempRed.setItemText(6, _translate("TSSADialog", "Ultrafast", None))
        self.tempRed.setItemText(7, _translate("TSSADialog", "Xin Yao", None))
        self.label_2.setText(_translate("TSSADialog", "Mutation type:", None))
        self.mutType.setItemText(0, _translate("TSSADialog", "Random", None))
        self.mutType.setItemText(1, _translate("TSSADialog", "RandomRandom", None))
        self.mutType.setItemText(2, _translate("TSSADialog", "Type 2", None))
        self.mutType.setItemText(3, _translate("TSSADialog", "Combine", None))
        self.label_5.setText(_translate("TSSADialog", "Tabu list volume", None))
        self.label_4.setText(_translate("TSSADialog", "Shaking after each", None))
        self.label_6.setText(_translate("TSSADialog", "Iterations Without Changing", None))
        self.pushButton.setText(_translate("TSSADialog", "Run", None))

import resources_rc
