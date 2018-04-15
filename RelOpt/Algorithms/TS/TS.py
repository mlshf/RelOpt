__author__ = ''
from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
from Common.StopCondition import StopCondition
import random, copy, time
import math   
     
def mutateSolution(candidate, nm):
    if len(candidate.modules[nm].sw) == 1:
        new = NONE(nm)
        candidate.modules[nm] = new
    elif len(candidate.modules[nm].hw) == 1:
        new = NVP01(nm)
        candidate.modules[nm] = new
    elif len(candidate.modules[nm].hw) == 2:
        new = RB11(nm)
        candidate.modules[nm] = new
    else:
        new = NVP11(nm)
        candidate.modules[nm] = new
 
def mutateMods(candidate):
    modstochange = []
    for i in range(Module.conf.modNum-1):
        prob = random.randint(0, 2)
        if prob != 0:
            modstochange.append(i)
    
    for i in modstochange:
        mutateSolution(candidate, i) 
    
class TS(Algorithm):
    def __init__(self, tlv = 1000):
        Algorithm.__init__(self)
        self.currIterWithoutChanging = 0
        self.iteration = 0        
        self.tl = []          
        self.tlh = 0
        self.tlv = tlv
        self.system = System()
        self.candidate = None
        self.Probability = 0
        
    def getHarlemShake(self):
        pass

    def Clear(self):
        Algorithm.Clear(self)
        self.iteration = 0
        self.currIterWithoutChanging = 0
        self.tl = []
        self.tlh = 0
        self.candidate = None
        self.Probability = 0

    def _checkStopCondition(self):
        if StopCondition.maxIter != -1:
            if self.system != None and self.iteration >= StopCondition.maxIter:
                print "currIter > Max = ", StopCondition.maxIter, " \n"
                return True

        if StopCondition.maxIterWCH != -1:
            if self.system != None and self.currIterWithoutChanging >= StopCondition.maxIterWCH:
                print "currIterWithoutChanging = ", self.currIterWithoutChanging, " \n"
                return True
                
        if StopCondition.minRel != -1:
            if self.best != None and self.best.rel >= StopCondition.minRel:
                print "minRel = ", self.best.rel, " \n"
                return True
        
        return False


    def Step(self):
        
        self.candidate = copy.deepcopy(self.system)
        
        if (self.iteration % self.spinBox_2 == 0 and self.iteration != 0):# DoAHarlemShake!
            self.candidate.GenerateRandom(True, self.tl)
            print "Shakiiiing!\n"
        else:   
            mutateMods(self.candidate)
            if self.candidate.modules not in self.tl:
                self.candidate.Update(use_metamodel=False, add=False)

        ############################################    
        
        if self.candidate.modules not in self.tl:
            if (self.candidate.rel * self.candidate.penalty > self.system.rel * self.system.penalty):
                self.system = copy.deepcopy(self.candidate)
                if ((self.candidate.rel > self.best.rel) and self.candidate.CheckConstraints()):
                    self.currIterWithoutChanging = 0
                    self.best = copy.deepcopy(self.candidate)
                else:
                    self.currIterWithoutChanging += 1
            else:
                self.currIterWithoutChanging += 1
            if len(self.tl) >= self.tlv:
                self.tl.pop(0)
            self.tl.append(self.candidate.modules)
        else:
            self.tlh += 1
                                   
        #####################################################    
        
        
    def Run(self):
        self.Clear()
        Algorithm.time = time.time()
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        
        self.system.GenerateRandom(True)
        self.best = copy.deepcopy(self.system)
        self.tl.append(self.system.modules)
        
        while not self._checkStopCondition():
            self.Step()
            self.iteration += 1
            print "Iteration =", self.iteration,';', self.best

        print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n"
        print "Best solution: ", self.best
        print "Hits in TL:", self.tlh

        print "--------------------------------------\n"
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(copy.deepcopy(self.system), self.iteration, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts, self.tlh))
        self.Clear()