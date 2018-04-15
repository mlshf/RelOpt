__author__ = ''
from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
from Common.StopCondition import StopCondition
import random, copy, time
import math  
import sys

def checkMOO(modules):
    if len(modules[0].sw) == 1:
        m0 = "none"
    elif len(modules[0].hw) == 1:
        m0 = "nvp01"
    elif len(modules[0].hw) == 2:
        m0 = "rb11"
    else:
        m0 = "nvp11"
    m1 = "empty"
    if len(modules) > 1:
        if len(modules[1].sw) == 1:
            m1 = "none"
        elif len(modules[1].hw) == 1:
            m1 = "nvp01"
        elif len(modules[1].hw) == 2:
            m1 = "rb11"
        else:
            m1 = "nvp11"
    return (m0, m1)

def mutateMinMod2(candidate, nm): 
    new = candidate.modules[nm]
    count = 0
    while (new.rel <= candidate.modules[nm].rel and count < 100):
        if "rb11" in Module.conf.modules[nm].tools:
            new = RB11(nm)
        elif "nvp11" in Module.conf.modules[nm].tools:
            new = NVP11(nm)
        elif "nvp01" in Module.conf.modules[nm].tools:
            new = NVP01(nm)
        else:
            new = NONE(nm)
        count = count + 1
        new._computeRel()
    candidate.modules[nm] = new
    
def mutateMinMod1(candidate, nm): 
    new = candidate.modules[nm]
    count = 0
    while (new.rel <= candidate.modules[nm].rel and count < 100):
        type = random.choice(Module.conf.modules[nm].tools)
        if type == "none":
            new = NONE(nm)
        elif type == "nvp01":
            new = NVP01(nm)
        elif type == "nvp11":
            new = NVP11(nm)
        else:
            new = RB11(nm)
        count = count + 1
        new._computeRel()
    candidate.modules[nm] = new
 
def mutateMinMod(candidate, nm): 
    type = random.choice(Module.conf.modules[nm].tools)
    if type == "none":
        new = NONE(nm)
    elif type == "nvp01":
        new = NVP01(nm)
    elif type == "nvp11":
        new = NVP11(nm)
    else:
        new = RB11(nm)
    candidate.modules[nm] = new
 
def seekMinMods(candidate):
    modstochange = []
    candidate.modules[0]._computeRel()
    minrel = candidate.modules[0].rel
    minrelmodnum = 0
    for i in range(1, Module.conf.modNum-1):
        candidate.modules[i]._computeRel()
        if candidate.modules[i].rel < minrel:
            minrel = candidate.modules[i].rel
            minrelmodnum = i
            
    for i in range(Module.conf.modNum-1):
        if candidate.modules[i].rel == candidate.modules[minrelmodnum].rel:
            modstochange.append(i)
       
    for i in modstochange:
        mutateMinMod(candidate, i) 
 
class TSRA(Algorithm):
    def __init__(self, tlv = 1000, mutType = 0):
        Algorithm.__init__(self)
        self.currIterWithoutChanging = 0
        self.iteration = 0  
        self.tl = []       
        self.tlh = 0
        self.tlv = tlv
        self.mutType = mutType
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
    
        if (self.mutType == 0 and self.iteration % self.spinBox_2 == 0 and self.iteration != 0):# DoAHarlemShake! 
            self.candidate.GenerateRandom(True, self.tl)
            print "Shakiiiing!\n"
        elif (self.mutType == 1 and self.currIterWithoutChanging % self.spinBox_2 == 0 and self.currIterWithoutChanging != 0):
            self.candidate.GenerateRandom(True, self.tl)
            print "Shakiiiing!\n"
        else: 
            seekMinMods(self.candidate)
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