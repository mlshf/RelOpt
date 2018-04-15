from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp
from PyQt4.QtCore import QTranslator
from GUI.Windows.ui_MainWindow import Ui_MainWindow
from GUI.ConfigDialog import ConfigDialog
from GUI.Windows.ui_ShowLinks import Ui_ShowLinks
from GUI.ShowLinks import ShowLinks
from Common.SysConfig import SysConfig
from Common.Constraints import CostConstraints, TimeConstraints
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.Penalty import Penalty 
from Common.StopCondition import StopCondition 
from GUI.GADialog import GADialog
from GUI.SLGADialog import SLGADialog
from GUI.GreedyDialog import GreedyDialog
from GUI.SADialog import SADialog
from GUI.HybridDialog import HybridDialog
from GUI.TSDialog import TSDialog
from GUI.TSSADialog import TSSADialog
from GUI.TSRADialog import TSRADialog
from GUI.RADialog import RADialog

import xml.dom.minidom, time, os


class MainWindow(QMainWindow):
    sysconfig = None
    sysconfigfile = None
    constraints = []

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sysConfigFilter = self.tr("System Configuration files (*.xml)")
        self.algConfigFilter = self.tr("Algorithm Configuration files (*.xml)")
        self.ui.result_filename.setText("result"+str(time.time())+".csv")
        self.best = None
        translator = QTranslator(qApp)
        translator.load("GUI/Windows/Translations/relopt_ru.qm")
        qApp.installTranslator(translator)
        self.ui.retranslateUi(self)
        self.ui.number.setEnabled(False)
        self.ui.maxIter.setEnabled(True)
        self.ui.maxIterWCH.setEnabled(False)
        self.ui.MinRel.setEnabled(False)
        self.stopConditionType = [0,0,0]
        StopCondition.maxIter = -1
        StopCondition.maxIterWCH = -1
        StopCondition.minRel = -1
        self.use_StopConditionMaxIter()
        self.use_StopConditionMaxIterWCH()
        self.use_StopConditionMinRel()
        self.ui.limittimes.setText("") 
        GADialog.meta = False
        SLGADialog.meta = False
        self.ui.limittimes.setEnabled(False)

    def LoadSysConf(self):
        if self.ui.sysconfname.text() == None or self.ui.sysconfname.text() == '':
            return
        self.sysconfig = SysConfig()
        self.sysconfig.loadXML(self.ui.sysconfname.text())
        self.constraints = []
        if self.sysconfig.limitcost != None:
            self.constraints.append(CostConstraints(self.sysconfig.limitcost))
        if self.ui.checktime_yes.isChecked():
            c = self.sysconfig.getLimitTimes()     
            if c != None:
                self.constraints.append(TimeConstraints(c))

    def SetAlgParameters(self):
        algidx = self.ui.algorithm.currentIndex()
        if self.sysconfig == None:
            QMessageBox.critical(self, "An error occurred", "System configuration must be defined")
            return
        Penalty.type = self.ui.penalty.currentIndex()
        Module.conf = self.sysconfig
        if self.ui.number.text() == '' and Penalty.type == 2:
            QMessageBox.critical(self, "An error occurred", "your power must be defined")
            return
        if self.constraints == None:
            QMessageBox.critical(self, "An error occurred", "Constraints must be defined")
            return
        if not self.ui.MI.isChecked() and not self.ui.MIWCH.isChecked() and not self.ui.MR.isChecked() and not(algidx == 3 or algidx == 4):
            QMessageBox.critical(self, "An error occurred", "StopConditions must be defined")
            return
        System.constraints = self.constraints
            
        if Penalty.type == 2:
            Penalty.power = int(self.ui.number.text())
        
        if self.stopConditionType[0] != 0:       
            StopCondition.maxIter = self.ui.maxIter.value()
        else:
            StopCondition.maxIter = -1
            
            
        if self.stopConditionType[1] != 0:       
            StopCondition.maxIterWCH = self.ui.maxIterWCH.value()
        else:
            StopCondition.maxIterWCH = -1
        
        if self.stopConditionType[2] != 0: 
            StopCondition.minRel = self.ui.MinRel.value()
        else:
            StopCondition.minRel = -1
          
        Algorithm.result_filename = str(self.ui.result_filename.text())
          
        if algidx==0:
             win = GADialog()
             GADialog.HGA = False
             GADialog.execNum = self.ui.execNum.value()
        elif algidx==1:
             win = GADialog()
             GADialog.HGA = True
             GADialog.execNum = self.ui.execNum.value()
        elif algidx==2:
             win = GreedyDialog()
             GreedyDialog.execNum = self.ui.execNum.value()
        elif algidx==3:
             win = SADialog()
             SADialog.execNum = self.ui.execNum.value()
        elif algidx==4:
             win = HybridDialog()
             HybridDialog.execNum = self.ui.execNum.value()
        elif algidx==5:
             win = TSDialog()
             TSDialog.execNum = self.ui.execNum.value()
        elif algidx==6:
             win = TSSADialog()
             TSSADialog.execNum = self.ui.execNum.value()
        elif algidx==7:
             win = TSRADialog()
             TSRADialog.execNum = self.ui.execNum.value()
        elif algidx==8:
             win = RADialog()
             RADialog.execNum = self.ui.execNum.value()
        elif algidx==9:
             win = SLGADialog()
             SLGADialog.execNum = self.ui.execNum.value()			 
        
        win.exec_()
        
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
            os.remove("tempconf" + str(os.getpid()) + ".xml")
        except:
            pass
                
    def showLinks(self):
        if self.sysconfig == None:
            QMessageBox.critical(self, "An error occurred", "System configuration must be defined")
            return
            
        shwlnks = ShowLinks(self.sysconfig, self.sysconfigfile)
        shwlnks.exec_()
        
        try:
            os.remove(shwlnks.filename + ".gv")
            os.remove(shwlnks.filename + ".png")
        except:
            pass
            
    def OpenSysConf(self):
        name = unicode(QFileDialog.getOpenFileName(directory = "SysConfigs/",filter=self.sysConfigFilter))
        if name == None or name == '':
            return
        self.sysconfigfile = name
        self.ui.sysconfname.setText(name)
        self.LoadSysConf()
        costrange = self.sysconfig.costInterval()
        timerange = self.sysconfig.timeInterval()
        self.ui.maxcost.setText(str(costrange[1]))
        self.ui.mincost.setText(str(costrange[0]))
        self.ui.maxtime.setText(str(timerange[1]).replace("]","").replace("[",""))
        self.ui.mintime.setText(str(timerange[0]).replace("]","").replace("[",""))
        self.ui.limitcost.setText(str(self.sysconfig.limitcost) if self.sysconfig.limitcost != None else "")
        l = []
        for constr in self.constraints:
            if isinstance(constr,TimeConstraints):
                l = constr.limitTimes
        if l == []:
            self.ui.limittimes.setText("")
        else:
            self.ui.limittimes.setText(str(l).replace("]","").replace("[",""))

    def Random(self):
        d = ConfigDialog()
        d.exec_()
        if d.result() == QDialog.Accepted: 
            dict = d.GetResult()
        else:
            return
        self.sysconfig = SysConfig()
        self.sysconfig.generateRandom(dict)
        costrange = self.sysconfig.costInterval()
        timerange = self.sysconfig.timeInterval()
        self.ui.maxcost.setText(str(costrange[1]))
        self.ui.mincost.setText(str(costrange[0]))
        self.ui.maxtime.setText(str(timerange[1]).replace("]","").replace("[",""))
        self.ui.mintime.setText(str(timerange[0]).replace("]","").replace("[",""))
        limitCount = lambda x,y,z: (int((y - x) * (float(z) / 100) + x))
        lc = limitCount(costrange[0], costrange[1], self.sysconfig.CPC)
        lt = [limitCount(timerange[0][i], timerange[1][i], self.sysconfig.modules[i].TPC) for i in range(len(timerange[1]))]
        self.ui.limitcost.setText(str(lc).replace("]","").replace("[",""))
        self.ui.limittimes.setText(str(lt).replace("]","").replace("[",""))
        self.ui.sysconfname.setText("")
        self.constraints = []
        self.InputCostLimit()
        self.InputTimeLimits()
        self.sysconfigfile = "tempconf" + str(os.getpid()) + ".xml"

    def InputTimeLimits(self):
        if self.ui.limittimes.text() == "":
            return
        for constr in self.constraints:
            if isinstance(constr,TimeConstraints):
                self.constraints.remove(constr)
                break
        l = []
        for c in self.ui.limittimes.text().split(","):
            l.append(int(c))
        self.constraints.append(TimeConstraints(l))
        for m,t in zip(self.sysconfig.modules, l):
            m.limittime = t

    def InputCostLimit(self):
        if self.ui.limitcost.text() == "":
            return
        for constr in self.constraints:
            if isinstance(constr,CostConstraints):
                self.constraints.remove(constr)
                break
        c = int(self.ui.limitcost.text())
        self.constraints.append(CostConstraints(c))
        self.sysconfig.limitcost = c

    def SaveSysConf(self):
        name = unicode(QFileDialog.getSaveFileName(directory = "SysConfigs/",filter=self.sysConfigFilter))
        if name == None or name == '':
            return
        self.sysconfig.saveXML(name)

    def no_checked(self):
        if self.ui.checktime_yes.isChecked():
            return
        for constr in self.constraints:
            if isinstance(constr,TimeConstraints):
                self.constraints.remove(constr)
                break
        self.ui.limittimes.setText("") 
        self.ui.limittimes.setEnabled(False)
        GADialog.meta = False
        SLGADialog.meta = False

    def yes_checked(self):
        if not self.ui.checktime_yes.isChecked():
            return
        self.ui.limittimes.setEnabled(True)
        if self.sysconfig == None:
            return

        c = self.sysconfig.getLimitTimes() 
        GADialog.meta = True  
        SLGADialog.meta = True 		
        if c != None:
            self.constraints.append(TimeConstraints(c))
            self.ui.limittimes.setText(str(c).replace("]","").replace("[",""))
            
    def changedPenalty(self):
        Penalty.type = self.ui.penalty.currentIndex()
            
        if Penalty.type != 2 :
            self.ui.number.setEnabled(False)
        else:
            self.ui.number.setEnabled(True)
         
    def AlgChanged(self):
        StopCondition.maxIter = -1
        StopCondition.maxIterWCH = -1
        StopCondition.minRel = -1
        algidx = self.ui.algorithm.currentIndex()
        if algidx==0:
            self.ui.result_filename.setText("resultGA"+str(time.time())+".csv")
        if algidx==1:
            self.ui.result_filename.setText("resultHGA"+str(time.time())+".csv")
        if algidx==9:
            self.ui.result_filename.setText("resultSLGA"+str(time.time())+".csv")
        if algidx==3:
            self.ui.result_filename.setText("resultSA"+str(time.time())+".csv")
        if algidx==4:
            self.ui.result_filename.setText("resultHybrid"+str(time.time())+".csv")
        if algidx==5:
            self.ui.result_filename.setText("resultTS"+str(time.time())+".csv")
        if algidx==6:
            self.ui.result_filename.setText("resultTSSA"+str(time.time())+".csv")
        if algidx==7:
            self.ui.result_filename.setText("resultTSRA"+str(time.time())+".csv")
        if algidx==8:
            self.ui.result_filename.setText("resultRA"+str(time.time())+".csv")
        if algidx==2:
            self.ui.result_filename.setText("resultGreedy"+str(time.time())+".csv")
            self.ui.execNum.setEnabled(False)
            self.ui.MR.setChecked(False)
            self.ui.MR.setEnabled(False)
            self.ui.MinRel.setEnabled(False)
            self.ui.MIWCH.setChecked(False)
            self.ui.MIWCH.setEnabled(False)
            self.ui.maxIterWCH.setEnabled(False)
            self.ui.execNum.setValue(1)
        else:
            self.ui.execNum.setEnabled(True)
            self.ui.MIWCH.setEnabled(True)
            self.ui.MR.setEnabled(True)
            self.use_StopConditionMaxIter()
            self.use_StopConditionMaxIterWCH()
            self.use_StopConditionMinRel()
             
    def editPen(self):
        if Penalty.type != 2 :
            Penalty.power = int(self.ui.number.text())
        
    def use_StopConditionMaxIter(self):
        if not self.ui.MI.isChecked():
            self.ui.maxIter.setEnabled(False)
            self.stopConditionType[0] = 0
        else:
            self.ui.maxIter.setEnabled(True)
            self.stopConditionType[0] = 1
        
    def use_StopConditionMaxIterWCH(self):
        if not self.ui.MIWCH.isChecked():
            self.ui.maxIterWCH.setEnabled(False)
            self.stopConditionType[1] = 0
        else:
            self.ui.maxIterWCH.setEnabled(True)
            self.stopConditionType[1] = 1
        
    def use_StopConditionMinRel(self):
        if not self.ui.MR.isChecked():
            self.ui.MinRel.setEnabled(False)
            self.stopConditionType[2] = 0
        else:
            self.ui.MinRel.setEnabled(True)
            self.stopConditionType[2] = 1
