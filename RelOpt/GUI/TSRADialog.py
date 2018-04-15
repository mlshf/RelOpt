from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp
from GUI.Windows.ui_TSRADialog import Ui_TSRADialog
from Common.SysConfig import SysConfig
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.StopCondition import StopCondition 
from Algorithms.TSRA.TSRA import TSRA
from Algorithms.TSRA.TSRAConfig import TSRAConfig

import time, os, math 
    
class TSRADialog(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_TSRADialog()
        self.ui.setupUi(self)
        self.best = None 
        self.algconfig = TSRAConfig() 
        #self.ui.num.setMaximum(Module.conf.modNum) 
        #if (StopCondition.maxIterWCH != -1):
        #    self.ui.shake.setMaximum(StopCondition.maxIterWCH)  
        #elif (StopCondition.maxIter != -1):
        #    self.ui.shake.setMaximum(StopCondition.maxIter)
        self.ui.spinBox_2.setEnabled(False)        

        
    def slot2(self):  
        #algorithm = TSRA(parameters)
        
        Algorithm.algconf = self.algconfig
        
        algorithm = TSRA(self.ui.spinBox.value(), self.ui.comboBox.currentIndex())
        
        if self.ui.checkBox.isChecked():
            TSRA.spinBox_2 = self.ui.spinBox_2.value()
        else:
            TSRA.spinBox_2 = 500000
        
        for i in range(self.execNum):
            algorithm.Run()
            algorithm.PrintStats()
            self.best = algorithm.currentSolution
            print "______%d of %d executions complete.______" % (i+1,self.execNum)
        
        Algorithm.result_filename = str("resultTSRA"+str(time.time())+".csv")
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
        except:
            pass
            
    def slot4(self):
        if not self.ui.checkBox.isChecked():
            self.ui.spinBox_2.setEnabled(False)
        else:
            self.ui.spinBox_2.setEnabled(True)

    def slot1(self):  
        TSRA.tlv = int(self.ui.spinBox.value())
        
            
        