from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
from Common.StopCondition import StopCondition 
from Common.AdaptiveMethods import adaptate
from Common.AdaptiveMethods import count_variance, count_avg
import random, copy, time

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
            


class SLGA(Algorithm):
    def __init__(self, corrMode = 0, corrPar1 = 0.1, corrPar2 = 0.1):
        Algorithm.__init__(self)
        self.population = []
        self.iterWithoutChange = 0
        self.corrMode = corrMode
        self.corrPar1 = corrPar1
        self.corrPar2 = corrPar2
        #self.mutProb = [self.algconf.Pmut.cur for j in range(0, self.algconf.popNum)]
        #self.crossProb = [self.algconf.Pcross.cur for j in range(0, self.algconf.popNum)]
        self.mutProb = [random.uniform(0.1, 0.9) for j in range(0, self.algconf.popNum)]
        self.crossProb = [random.uniform(0.1, 0.9) for j in range(0, self.algconf.popNum)]

    def Step(self):
        self._select()
        self._recombine()
        self._mutate()
        self._evalPopulation()

    def Run(self):
        self.Clear()
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        Algorithm.time = time.time()
        for i in range(self.algconf.popNum):
            s = System()
            s.GenerateRandom(True)
            self.population.append(s)
        if Algorithm.algconf.metamodel:
            Algorithm.algconf.metamodel.Update()
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)
        while not self._checkStopCondition():
            self.Step()
            print "Iteration =",self.currentIter,';', '%.10f' % self.currentSolution.rel, self.currentSolution
            
        print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n"
        print "Best solution (found on", self.currentIter, "iteration):", self.currentSolution
        print "--------------------------------------\n"
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(copy.deepcopy(self.currentSolution), self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))

    def Clear(self):
        Algorithm.Clear(self)
        self.population = []
        self.iterWithoutChange = 0
        self.candidate = None 
        #self.mutProb = [self.algconf.Pmut.cur for j in range(0, self.algconf.popNum)]
        #self.crossProb = [self.algconf.Pcross.cur for j in range(0, self.algconf.popNum)]
        self.mutProb = [random.uniform(0.1, 0.9) for j in range(0, self.algconf.popNum)]
        self.crossProb = [random.uniform(0.1, 0.9) for j in range(0, self.algconf.popNum)]

    def _mutate(self):
        sp = c = int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum)
        if self.corrMode == 10:
            old_popul = copy.deepcopy(self.population)
        for s in self.population[sp:]:
            k = random.randint(0, Module.conf.modNum-1)
            if random.random() <= self.mutProb[c]:
                # k = random.randint(0, Module.conf.modNum-1)
                old = copy.deepcopy(s)
                if self.currentIter > 500 and self.currentSolution == None:
                    type = "none"
                else:
                    type = random.choice(Module.conf.modules[k].tools)
                if type == "none":
                    new = NONE(k)
                elif type == "nvp01":
                    new = NVP01(k)
                elif type == "nvp11":
                    new = NVP11(k)
                else:
                    new = RB11(k)
                s.modules[k] = new
                s.Update()
                
                ##############################################################################
                
                if self.corrMode == 10:
                    self.corrPar1 = count_variance(old_popul)
                    self.corrPar2 = count_variance(self.population)
                
                if self.corrMode == 5:
                    self.corrPar2 = count_avg(self.population)
                    adaptate(self.mutProb[c], s, self.corrPar2, max([j.rel for j in self.population]), self.corrPar1)
                else:
                    adaptate(self.mutProb[c], s, old, self.corrMode, self.corrPar1, self.corrPar2)
                
                ##############################################################################
                
            c += 1
                
    ######################################################            
      
    def _mutate1(self):
        for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
        #for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
            if random.random() <= self.algconf.Pmut.cur:
                Rand(s, 2)
                s.Update()
                
    def _mutate2(self):
        for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
        #for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
            if random.random() <= self.algconf.Pmut.cur:
                RandRand(s, 2)
                s.Update()
                
    def _mutate3(self):
        for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
        #for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
            if random.random() <= self.algconf.Pmut.cur:
                mutationType2(s)
                s.Update()
                
    def _mutate4(self):
        for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
        #for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
            if random.random() <= self.algconf.Pmut.cur:
                Combine(s, 2)
                s.Update()
                
    ######################################################
            
    def _select(self):
        probabilities = []
        sum = 0.0 
        for s in self.population:
            val = s.rel*s.penalty
            sum += val
            probabilities.append(val)
        for p in range(self.algconf.popNum):
            probabilities[p] = probabilities[p]/sum
        nums = range(self.algconf.popNum)
        events = dict(zip(nums, probabilities))
        new_pop = []
        for i in nums:
            new_pop.append(self.population[genEvent(events)])
        self.population = new_pop
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)

    def _recombine(self):
        if Module.conf.modNum == 1:
            return
        new_pop = []
        notCrossNum =  int((1.0 - self.algconf.crossPercent.cur) * self.algconf.popNum)
        if self.corrMode == 10:
            old_popul = self.population
        for i in range(notCrossNum):
            new_pop.append(copy.deepcopy(self.population[i]))
        for i in range(self.algconf.popNum/2):
            p1 = random.randint(0, self.algconf.popNum - 1)
            p2 = random.randint(0, self.algconf.popNum - 1)
            while p1 == p2:
                p2 = random.randint(0, self.algconf.popNum - 1)
            parents = [self.population[p1], self.population[p2]]
            k = random.randint(1,Module.conf.modNum-1)
            rr = random.random()
            
            if rr <= self.crossProb[p1] and rr <= self.crossProb[p2]:
                # parents = random.sample(self.population,  2)
                # k = random.randint(1,Module.conf.modNum-1)
                old0 = copy.deepcopy(parents[0])
                old1 = copy.deepcopy(parents[1])
                child1 = parents[0].modules[0:k] + parents[1].modules[k:Module.conf.modNum]
                child2 = parents[1].modules[0:k] + parents[0].modules[k:Module.conf.modNum]
                parents[0].modules = child1
                parents[1].modules = child2
                parents[0].Update()
                parents[1].Update()
                
                #######################################################################################
                
                if self.corrMode == 10:
                    self.corrPar2 = count_variance(old_popul)
                    self.corrPar1 = count_variance(self.population)
                    
                if self.corrMode == 5:
                    self.corrPar2 = count_avg(self.population)
                    adaptate(self.crossProb[p1], parents[0], self.corrPar2, max([j.rel for j in self.population]), self.corrPar1)
                    self.corrPar2 = count_avg(self.population)
                    adaptate(self.crossProb[p2], parents[1], self.corrPar2, max([j.rel for j in self.population]), self.corrPar1)
                else:
                    adaptate(self.crossProb[p1], parents[0], old1, self.corrMode, self.corrPar1, self.corrPar2)
                    adaptate(self.crossProb[p2], parents[1], old1, self.corrMode, self.corrPar1, self.corrPar2)
                
                #adaptate(self.crossProb[p1], parents[0], old0, self.corrMode, self.corrPar1, self.corrPar2) 
                    
                #adaptate(self.crossProb[p2], parents[1], old1, self.corrMode, self.corrPar1, self.corrPar2)
                
                #######################################################################################
                
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)
        new_pop += self.population[:self.algconf.popNum - notCrossNum]
        self.population = new_pop
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)

    def _evalPopulation(self):
        self.currentIter += 1
        self.iterWithoutChange += 1
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)
        not_use_metamodel = Algorithm.algconf.metamodel==None or random.random() <= self.algconf.pop_control_percent
        for s in self.population:
            if not_use_metamodel:
                if self.candidate:
                    self.candidate.Update(use_metamodel=False)
                    if self.candidate.CheckConstraints() and (self.currentSolution == None or self.candidate.rel > self.currentSolution.rel):
                            self.currentSolution = copy.deepcopy(self.candidate)
                            self.iterWithoutChange = 0
                s.Update(use_metamodel=False)
                if s.CheckConstraints() and (self.currentSolution == None or s.rel > self.currentSolution.rel):
                    self.currentSolution = copy.deepcopy(s)
                    self.iterWithoutChange = 0
                    self.candidate = None
                    break
            else:
                if s.CheckConstraints() and (self.currentSolution == None or self.candidate == None or s.rel > self.candidate.rel):
                    self.candidate = copy.deepcopy(s)
                    break
        if not_use_metamodel and Algorithm.algconf.metamodel:
            Algorithm.algconf.metamodel.Update()

    def _checkStopCondition(self):
        if StopCondition.maxIter != -1:
            if self.currentSolution != None and self.currentIter >= self.algconf.maxIter:
                self.currentSolution.Update(use_metamodel=False)
                if self.currentSolution.CheckConstraints():
                    return True

        if StopCondition.maxIterWCH != -1:
            #if self.currentSolution == None and self.iterWithoutChange >= self.algconf.maxIterWithoutChange:
            if self.currentSolution != None and self.iterWithoutChange >= self.algconf.maxIterWithoutChange:
                self.currentSolution.Update(use_metamodel=False)
                if self.currentSolution.CheckConstraints():
                    return True
                '''
                self.currentSolution = System()
                self.currentSolution.rel = 0
                for m in Module.conf.modules:
                    self.currentSolution.modules.append(NONE(m.num))
                return True
                '''
                
        if StopCondition.minRel != -1:
            if self.currentSolution != None and self.currentSolution.rel >= self.algconf.minRel:
                self.currentSolution.Update(use_metamodel=False)
                if self.currentSolution.CheckConstraints():
                    return True
        
        return False