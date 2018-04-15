from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp
from GUI.Windows.ui_TSDialog import Ui_TSDialog
from Common.SysConfig import SysConfig
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.StopCondition import StopCondition 
from Algorithms.TS.TS import TS
from Algorithms.TS.TSConfig import TSConfig

import time, os, math 
    
class TSDialog(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_TSDialog()
        self.ui.setupUi(self)
        self.best = None 
        self.algconfig = TSConfig() 
        #self.ui.num.setMaximum(Module.conf.modNum) 
        #if (StopCondition.maxIterWCH != -1):
        #    self.ui.shake.setMaximum(StopCondition.maxIterWCH)  
        #elif (StopCondition.maxIter != -1):
        #    self.ui.shake.setMaximum(StopCondition.maxIter)
        self.ui.spinBox_2.setEnabled(False)        

        
    def slot2(self):  
        #algorithm = TS(parameters)
        
        Algorithm.algconf = self.algconfig
        
        algorithm = TS(self.ui.spinBox.value())
        
        if self.ui.checkBox.isChecked():
            TS.spinBox_2 = self.ui.spinBox_2.value()
        else:
            TS.spinBox_2 = 500000
        
        for i in range(self.execNum):
            algorithm.Run()
            algorithm.PrintStats()
            self.best = algorithm.currentSolution
            print "______%d of %d executions complete.______" % (i+1,self.execNum)
        
        Algorithm.result_filename = str("resultTS"+str(time.time())+".csv")
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
        TS.tlv = int(self.ui.spinBox.value())
        
            
        