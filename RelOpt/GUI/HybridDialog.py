from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp
from GUI.Windows.ui_HybridDialog import Ui_HybridDialog
from Common.SysConfig import SysConfig
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.StopCondition import StopCondition 
from Algorithms.Hybrid.Hybrid import Hybrid
from Algorithms.Hybrid.HybridConfig import HybridConfig 

import time, os, math 
    
class HybridDialog(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_HybridDialog()
        self.ui.setupUi(self)
        self.best = None 
        self.algconfig = HybridConfig()  
        self.ui.num.setMaximum(Module.conf.modNum) 
        if (StopCondition.maxIterWCH != -1):
            self.ui.shake.setMaximum(StopCondition.maxIterWCH)  
        elif (StopCondition.maxIter != -1):
            self.ui.shake.setMaximum(StopCondition.maxIter)
        self.ui.shake.setEnabled(False) 
            

    def run(self):  
        #if (self.ui.divide.value() == ''):
        #    QMessageBox.critical(self, "An error occurred", "Temperature Reduce Parameter must be defined")
        #    return
            
        Algorithm.algconf = self.algconfig

        Algorithm.val = self.ui.divide.value()
         
        #print self.ui.tempRed.currentIndex()
        algorithm = Hybrid(self.ui.temperature.value(), self.ui.mutType.currentIndex(), self.ui.num.value(), self.ui.tempRed.currentIndex())
        Hybrid.Zero = self.ui.Zero.value()
        if self.ui.shaking.isChecked():
            Hybrid.shake = self.ui.shake.value()
        else:
            Hybrid.shake = 500000
        
        for i in range(self.execNum):
            #if algorithm.algconf.comboBox:
            #    algorithm.algconf.comboBox.Clear()
            algorithm.Run()
            algorithm.PrintStats()
            self.best = algorithm.currentSolution
            print "______%d of %d executions complete.______" % (i+1,self.execNum)
        
        Algorithm.result_filename = str("resultHybrid"+str(time.time())+".csv")
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
        except:
            pass

            
            
    def mutateChange(self):
        if self.ui.mutType.currentIndex() == 2:
            self.ui.num.setEnabled(False)  
        else:
            self.ui.num.setEnabled(True)  
            
        if self.ui.mutType.currentIndex() == 1:
            self.ui.num.setMinimum(2) 
            self.ui.num.setProperty("value", 2)
        else:
            self.ui.num.setMinimum(1)
            self.ui.num.setProperty("value", 1)
            
    def initTempChange(self):
        self.ui.Zero.setMaximum(self.ui.temperature.value())
        if (self.ui.Zero.value() > self.ui.temperature.value()):
            self.ui.Zero.setProperty("value", self.ui.temperature.value())
            
    def shakingSwitch(self):
        if (StopCondition.maxIterWCH != -1):
            self.ui.shake.setMaximum(StopCondition.maxIterWCH)  
        elif (StopCondition.maxIter != -1):
            self.ui.shake.setMaximum(StopCondition.maxIter) 
        else:
            self.ui.shake.setMaximum(500000)
        if not self.ui.shaking.isChecked():
            self.ui.shake.setEnabled(False)
        else:
            self.ui.shake.setEnabled(True)
            
            
    def tempReduceChange(self):
        r = self.ui.tempRed.currentIndex()
        
        if ((r == 4) or (r == 5)):
            self.ui.divide.setEnabled(False)
        else:
            self.ui.divide.setEnabled(True)
        
        if r == 0:
            self.ui.divide.setMaximum(self.ui.temperature.value())
            self.ui.divide.setProperty("value", 1.0)
        elif r == 1:
            self.ui.divide.setMaximum(self.ui.temperature.value())
            self.ui.divide.setProperty("value", 1.0)
        elif r == 2:
            self.ui.divide.setMaximum(1.0)
            self.ui.divide.setProperty("value", 0.9)
        elif r == 3:
            #self.ui.divide.setMinimum(0.3)
            self.ui.divide.setProperty("value", 0.75)
            self.ui.divide.setMaximum(0.8)
        elif r >= 6:
            self.ui.divide.setMaximum(1000000000.0)
            self.ui.divide.setProperty("value", 1.0)
                
            
        