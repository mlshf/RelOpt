from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp
from GUI.Windows.ui_GreedyDialog import Ui_GreedyDialog
from Common.Algorithm import Algorithm 
from Algorithms.Greedy.Greedy import Greedy
from Common.AlgConfig import AlgConfig

import time, os


class GreedyDialog(QDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.ui = Ui_GreedyDialog()
		self.algconfig = AlgConfig()
		self.ui.setupUi(self)
		self.best = None
		

	def run(self):			 
		algorithm = Greedy()
		Algorithm.algconf = self.algconfig
		#if algorithm.algconf.comboBox:
		#	 algorithm.algconf.comboBox.Clear()
		algorithm.Run()
		algorithm.PrintStats()
		self.best = algorithm.currentSolution
		
		Algorithm.result_filename = str("resultGreedy"+str(time.time())+".csv")
		try:
			os.remove("sch" + str(os.getpid()) + ".xml")
			os.remove("res" + str(os.getpid()) + ".xml")
		except:
			pass