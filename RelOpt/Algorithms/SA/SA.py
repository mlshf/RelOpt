__author__ = 'poziTiff'
from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
from Common.StopCondition import StopCondition
import random, copy, time
import math


def randrange_float(a,b):
    return random.random()*(b-a)+a  
    
def newMod(mNum, type):
    if type == "none":
        new = NONE(mNum)
    elif type == "nvp01":
        new = NVP01(mNum)
    elif type == "nvp11":
        new = NVP11(mNum)
    else:
        new = RB11(mNum) 
        
    return new
    
def chooseMods(modNum,numModsToChange):
    mods = []
    while len(mods) < numModsToChange:
        n = random.randint(0, modNum-1)
        if n not in mods:
            mods.append(n)
    
    return mods

def Rand(candidate, number):
    mods = chooseMods(Module.conf.modNum, number)
            
    for mNum in mods:
        type = random.choice(Module.conf.modules[mNum].tools)
        new = newMod(mNum, type)
        candidate.modules[mNum] = new

def RandRand(candidate, number):
    num = random.randint(1, number)
    Rand(candidate, num)

def mutationType2(candidate):
    l = random.randint(0, Module.conf.modNum-1)
    k = random.randint(0, Module.conf.modNum-1)
    while k == l:
        l = random.randint(0, Module.conf.modNum-1)
     
    count = 0
    new = candidate.modules[k]
    while (new.cost >= candidate.modules[k].cost):
        type = random.choice(Module.conf.modules[k].tools)
        new = newMod(k, type)
        if count > 100:
            k = random.randint(0, Module.conf.modNum-1)
            while k == l:
                k = random.randint(0, Module.conf.modNum-1)
            new = candidate.modules[k]
            count = 0
        count += 1
                
    candidate.modules[k] = new
     
    new = candidate.modules[l]
    count = 0
    while (new.cost <= candidate.modules[l].cost): 
        type = random.choice(Module.conf.modules[l].tools)
        new = newMod(l, type)
        if count > 100:
            l = random.randint(0, Module.conf.modNum-1)
            while k == l:
                l = random.randint(0, Module.conf.modNum-1)
            new = candidate.modules[l]
            count = 0
        count += 1
                
    candidate.modules[l] = new

def Combine(candidate, number):
    type = random.randint(0, 1)
    if type == 0:
        Rand(candidate, number)
    else:
        mutationType2(candidate)

def mutateSolution(mutType, candidate, number):
    if mutType == 0:
        Rand(candidate, number)
    elif mutType == 1:
        RandRand(candidate, number)
    elif mutType == 2:
        mutationType2(candidate)
    elif mutType == 3:
        Combine(candidate, number)
            
class SA(Algorithm):
    def __init__(self, startTemperature = 300, mutType = 0, mutNumber = 1, tempReduceType = 0):
        Algorithm.__init__(self)
        self.currIterWithoutChanging = 0
        self.mutType = mutType
        self.mutNumber = mutNumber
        self.tempReduceType = tempReduceType
        self.iteration = 0
        self.startTemperature = startTemperature
        self.temperature = self.startTemperature
        self.system = System()
        self.candidate = None
        self.Probability = 0

    def getHarlemShake(self):
        pass

    def Clear(self):
        Algorithm.Clear(self)
        self.iteration = 0
        self.temperature = self.startTemperature
        self.currIterWithoutChanging = 0
        self.candidate = None
        self.Probability = 0


    def __reducing(self):
        self.temperature -= self.val
        
    def __powerReducing(self):
        self.temperature -= math.pow(self.iteration, self.val)

    def __extinguishing(self):
        self.temperature *= self.val

    def __randExtinguishing(self):
        self.temperature *= randrange_float(self.val, self.val + 0.5)
        if self.temperature > self.startTemperature:
            self.temperature = self.startTemperature

    def __BolcmanLaw(self):
        self.temperature = self.startTemperature / math.log(1 + self.iteration)

    def __KoshiLaw(self):
        self.temperature = self.startTemperature / self.iteration

    def __ultrafast(self):
        self.temperature = self.startTemperature * math.exp( -self.iteration * self.val)

    def __XinYao(self):
        self.temperature = self.startTemperature * math.exp( -math.exp(self.iteration * self.val))

    def _reduceTemperature(self):
        self.iteration += 1
        if self.tempReduceType == 0:
            self.__reducing()
        elif self.tempReduceType == 1:
            self.__powerReducing()
        elif self.tempReduceType == 2:
            self.__extinguishing()
        elif self.tempReduceType == 3:
            self.__randExtinguishing()
        elif self.tempReduceType == 4:
            self.__BolcmanLaw()
        elif self.tempReduceType == 5:
            self.__KoshiLaw()
        elif self.tempReduceType == 6:
            self.__ultrafast()
        elif self.tempReduceType == 7:
            self.__XinYao()
            
        if self.temperature < 0:
            self.temperature = 0

    def _checkStopCondition(self):
        if self.system != None and self.temperature <= self.Zero:
                print "temperature < ", self.Zero, " \n"
                return True
                
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

        if (self.currIterWithoutChanging % self.shake == 0 and self.currIterWithoutChanging != 0):# DoAHarlemShake! 
            self.candidate.GenerateRandom(True)
            print "Shakiiiing!\n"
        else:   
            mutateSolution(self.mutType, self.candidate, self.mutNumber)
            self.candidate.Update(use_metamodel=False, add=False)
            
        ####################################
        
        if (self.candidate.rel * self.candidate.penalty > self.system.rel * self.system.penalty):
            self.Probability = 1.0
            if ((self.candidate.rel > self.best.rel) and self.candidate.CheckConstraints()):
                self.currIterWithoutChanging = 0
                self.best = copy.deepcopy(self.candidate)
            else:
                self.currIterWithoutChanging += 1
        else:
            self.currIterWithoutChanging += 1
            
            if (self.candidate.rel * self.candidate.penalty == self.system.rel * self.system.penalty):
                self.Probability = 0.5 * self.candidate.penalty
            else:
                self.Probability = (0.5 * self.candidate.penalty * self.temperature ) / self.startTemperature
                
        prob = randrange_float(0.0, 1.0)
        if prob <= self.Probability:
            self.system = copy.deepcopy(self.candidate)


    def Run(self):
        self.Clear()
        Algorithm.time = time.time()
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        
        self.system.GenerateRandom(True)
        self.best = copy.deepcopy(self.system)

        while not self._checkStopCondition():
            self.Step()
            self._reduceTemperature()
            print "Iteration =", self.iteration,';'
            print "Temperature =", self.temperature,';', self.best

        print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n"
        print "Best solution: ", self.best

        print "--------------------------------------\n"
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(copy.deepcopy(self.system), self.iteration, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))
        self.Clear()