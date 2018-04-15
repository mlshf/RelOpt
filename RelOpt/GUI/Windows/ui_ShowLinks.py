
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

class Ui_ShowLinks(object):
    def setupUi(self, ShowLinks):
        ShowLinks.setObjectName(_fromUtf8("ShowLinks"))
        ShowLinks.resize(457, 352)
        self.gridLayout = QtGui.QGridLayout(ShowLinks)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graph = QtGui.QGraphicsView(ShowLinks)
        self.graph.setMinimumSize(QtCore.QSize(429, 279))
        self.graph.setObjectName(_fromUtf8("graph"))
        self.verticalLayout_2.addWidget(self.graph)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_2 = QtGui.QPushButton(ShowLinks)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(ShowLinks)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.retranslateUi(ShowLinks)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), ShowLinks.SaveDigraphAs)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ShowLinks.SaveImageAs)
        QtCore.QMetaObject.connectSlotsByName(ShowLinks)

    def retranslateUi(self, ShowLinks):
        ShowLinks.setWindowTitle(_translate("ShowLinks", "Dialog", None))
        self.pushButton_2.setText(_translate("ShowLinks", "Save digraph as ...", None))
        self.pushButton.setText(_translate("ShowLinks", "Save image as ...", None))

