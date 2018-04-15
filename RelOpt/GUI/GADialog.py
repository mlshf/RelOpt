from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp
from GUI.Windows.ui_GADialog import Ui_GADialog
from GUI.MetamodelsRes import MetamodelsRes
from GUI.Windows.ui_MetamodelsResDialog import Ui_MetamodelsResDialog
from Common.SysConfig import SysConfig
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.AlgConfig import AlgConfig
from Common.StopCondition import StopCondition 
from Algorithms.GA.GA import GA 
from Algorithms.GA.HGA import HGA
from Algorithms.GA.GAConfig import GAConfig
from Algorithms.GA.GAConfig import GAParameter

import xml.dom.minidom, time, os
try:
    from Metamodels.NeuralNetwork import NeuralNetwork
    from Metamodels.Averaging import Averaging
    from Metamodels.Polynomial import Polynomial
    from Metamodels.KNearestNeighbours import KNearestNeighbours
    from Metamodels.Svr import Svr
    from Metamodels.Random import Random
except:
    print "Warning: Couldn't import metamodels"


class MetamodelsResDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_MetamodelsResDialog()
        self.ui.setupUi(self)

    def Load(self, v):
        self.ui.id.setText(v.id)
        self.ui.speed.setText(str(v.speed))
        self.ui.ram.setText(str(v.ram))

    def SetResult(self, v):
        v.id = self.ui.id.text()
        v.speed = int(self.ui.speed.text())
        v.ram = int(self.ui.ram.text()) 
    
class GADialog(QDialog):
    algconfig = None
    algconfigfile = None
    
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_GADialog()
        self.algConfigFilter = self.tr("Algorithm Configuration files (*.xml)")
        self.ui.setupUi(self)
        self.best = None
        if self.meta == False:
            self.ui.use_metamodels.setEnabled(False)
        self.ui.algconfname.setEnabled(False)
        self.ui.toolButton.setEnabled(False)

    def use_metamodels(self):
        if not self.ui.use_metamodels.isChecked():
            self.ui.comboBox.setEnabled(False)
            self.ui.popControl.setEnabled(False)
        else:
            self.ui.comboBox.setEnabled(True)
            self.ui.popControl.setEnabled(True)

    def draw_metamodels(self):
        d = MetamodelsResDialog()
        d.exec_()
        if not d.result():
            return
        if d.ui.random.isChecked():
            d1 = MetamodelsRes(self.best, True)
        else:
            d1 = MetamodelsRes(self.best, False)
        d1.exec_()
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
        except:
            pass

    def pressNo(self):
        self.ui.algconfname.setEnabled(False)
        self.ui.toolButton.setEnabled(False)
        
        self.ui.popNum.setEnabled(True)
        self.ui.cp1.setEnabled(True)
        self.ui.cp2.setEnabled(True)
        self.ui.cp3.setEnabled(True)
        self.ui.pc1.setEnabled(True)
        self.ui.pc2.setEnabled(True)
        self.ui.pc3.setEnabled(True)
        self.ui.mp1.setEnabled(True)
        self.ui.mp2.setEnabled(True)
        self.ui.mp3.setEnabled(True)
        self.ui.pm1.setEnabled(True)
        self.ui.pm2.setEnabled(True)
        self.ui.pm3.setEnabled(True)
        
    def pressYes(self):
        self.ui.algconfname.setEnabled(True)
        self.ui.toolButton.setEnabled(True)
        
        self.ui.popNum.setEnabled(False)
        self.ui.cp1.setEnabled(False)
        self.ui.cp2.setEnabled(False)
        self.ui.cp3.setEnabled(False)
        self.ui.pc1.setEnabled(False)
        self.ui.pc2.setEnabled(False)
        self.ui.pc3.setEnabled(False)
        self.ui.mp1.setEnabled(False)
        self.ui.mp2.setEnabled(False)
        self.ui.mp3.setEnabled(False)
        self.ui.pm1.setEnabled(False)
        self.ui.pm2.setEnabled(False)
        self.ui.pm3.setEnabled(False)

    def openDialog(self):
        name = unicode(QFileDialog.getOpenFileName(directory = "AlgConfigs/",filter=self.algConfigFilter))
        if name == None or name == '':
            return
        self.algconfigfile = name
        #na = name.split('/')
        #n = na[na.length() - 1]
        self.ui.algconfname.setText(name)
        self.loadAlgConf()
        

    def loadAlgConf(self):
        f = open(unicode(self.ui.algconfname.text()), "r")
        dom = xml.dom.minidom.parse(f)
        root = dom.childNodes[0]
        self.algconfig = GAConfig()
        self.algconfig.LoadFromXmlNode(root)
        #self.ui.iterNum.setEnabled(False)
        

    def run(self):  
        Algorithm.algconf = self.algconfig
        if Algorithm.algconf == None:
            Algorithm.algconf = AlgConfig()
        if self.ui.use_metamodels.isChecked():
            Algorithm.algconf.use_metamodel = True
            modelidx = self.ui.comboBox.currentIndex()
            if modelidx == 0:
                Algorithm.algconf.comboBox = Averaging()
            elif modelidx == 1:
                Algorithm.algconf.comboBox = KNearestNeighbours(10) #TODO user should define this number
            elif modelidx == 2:
                Algorithm.algconf.comboBox = NeuralNetwork(self.sysconfig) #TODO add settings
            elif modelidx == 3:
                Algorithm.algconf.comboBox = Svr(self.sysconfig)
            elif modelidx == 4:
                Algorithm.algconf.comboBox = Polynomial(self.sysconfig)
            elif modelidx == 5:
                Algorithm.algconf.comboBox = Random()
            Algorithm.algconf.pop_control_percent = float(self.ui.popControl.value())/100.0

        Algorithm.algconf.popNum = self.ui.popNum.value()
        Algorithm.algconf.maxIter = StopCondition.maxIter 
        Algorithm.algconf.maxIterWithoutChange = StopCondition.maxIterWCH
        Algorithm.algconf.minRel = StopCondition.minRel
        Algorithm.algconf.crossPercent = GAParameter(self.ui.cp1.value(), self.ui.cp2.value(), self.ui.cp3.value())
        Algorithm.algconf.Pcross = GAParameter(self.ui.pc1.value(), self.ui.pc2.value(), self.ui.pc3.value())
        Algorithm.algconf.mutPercent = GAParameter(self.ui.mp1.value(), self.ui.mp2.value(), self.ui.mp3.value())
        Algorithm.algconf.Pmut = GAParameter(self.ui.pm1.value(), self.ui.pm2.value(), self.ui.pm3.value())
         
        if self.HGA:
            algorithm = HGA()
        else:
            algorithm = GA()
        for i in range(self.execNum):
            #if algorithm.algconf.comboBox:
            #    algorithm.algconf.comboBox.Clear()
            algorithm.Run()
            algorithm.PrintStats()
            self.best = algorithm.currentSolution
            print "__%d of %d executions complete.__" % (i+1,self.execNum)
            
        if self.HGA:
            Algorithm.result_filename = str("resultHGA"+str(time.time())+".csv")
        else:
            Algorithm.result_filename = str("resultGA"+str(time.time())+".csv")
        
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
        except:
            pass

    def showMetamodelsRes(self):
        d = MetamodelsResDialog()
        d.exec_()
        if not d.result():
            return
        if d.ui.random.isChecked():
            d1 = MetamodelsRes(self.best, True)
        else:
            d1 = MetamodelsRes(self.best, False)
        d1.exec_()
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
        except:
            pass