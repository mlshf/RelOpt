from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy, time, math

class FA(Algorithm):

    def __init__(self):
        Algorithm.__init__(self)
        self.positions = [] #positions of agents
        self.best = 0

        print "Constraints: ", len(System.constraints), System.constraints

    def Run(self):
        self.Clear()
         # time counter (iterations counter), counted by this algorithm
        Algorithm.timecounts = 0
        # time counter (iteration counter), counted by
        Algorithm.simcounts = 0
        Algorithm.time = time.time()

        

        # generate positions for agents
        for i in range(self.algconf.nagents):
            agent = System()
            agent.GenerateRandom(True) #True means that I want to check constraints
            self.positions.append(agent)

        self._sort_and_evalBest()

        while not self._checkStopCondition():
            self.Step() 
            self._sort_and_evalBest()
            self.currentIter += 1

        print "Best solution: ", self.currentSolution, "\n\n"

        #New execution of algorithm and its results save in statistics
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(self.currentSolution, self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))
        

    def Step(self):
        for i in self.positions: #add random walk for best solution
            for j in self.positions:
                 if j.rel > i.rel: 
                    self._move(i, j) #move to new positions
                    self._updateRel(i) #update reliability

    def _move(self, pos1, pos2):
        coef = self.algconf.betta*math.exp(-self.algconf.gamma*(pos1.distance(pos2)**2))
        for i in range(Module.conf.modNum):
            #choose moo for new module configuration
            r = random.random()
            moo = None
            if r < 0.75:
                sys = random.choice([pos1.modules[i], pos2.modules[i]])
                if isinstance(sys, NONE):
                    moo = 0
                elif isinstance(sys, NVP01):
                    moo = 1
                elif isinstance(sys, NVP11):
                    moo = 2
                elif isinstance(sys, RB11):
                    moo = 3
            else:
                moo = random.randint(0, 3)

            new = None

            if moo == 0:
                #print "MOO = NONE\n"
                hw = [int(round(pos1.modules[i].hw[0] + (pos2.modules[i].hw[0] - pos1.modules[i].hw[0])*coef + self.algconf.alpha*random.gauss(0, 1)))]
                sw = [int(round(pos1.modules[i].sw[0] + (pos2.modules[i].sw[0] - pos1.modules[i].sw[0])*coef + self.algconf.alpha*random.gauss(0, 1)))]
                new = self._checkNewModule(i, hw, sw, moo)
                #new = NONE(i, hw, sw)
            elif moo == 1:
                
                hw = [int(round(pos1.modules[i].hw[0] + (pos2.modules[i].hw[0] - pos1.modules[i].hw[0])*coef + self.algconf.alpha*random.gauss(0, 1)))]
                sw = [int(round(pos1.modules[i].sw[j] + (pos2.modules[i].sw[j] - pos1.modules[i].sw[j])*coef + self.algconf.alpha*random.gauss(0, 1))) for j in range(min(len(pos1.modules[i].sw), len(pos2.modules[i].sw)))]
                if len(sw) < 3:
                    for j in range(len(sw), 3):
                        if len(pos1.modules[i].sw) > j:
                            sw.append(int(round(pos1.modules[i].sw[j] + self.algconf.alpha*random.gauss(0, 1))))
                        else:
                            sw.append(random.randint(0, len(Module.conf.modules[i].sw)-1))
                #print "MOO = NVP01", len(hw), len(sw), "\n"
                new = self._checkNewModule(i, hw, sw, moo)
                #new = NVP01(i, hw, sw)
            elif moo == 2:
                #print "MOO = NVP11\n"
                hw = [int(round(pos1.modules[i].hw[j] + (pos2.modules[i].hw[j] - pos1.modules[i].hw[j])*coef + self.algconf.alpha*random.gauss(0, 1))) for j in range(min(len(pos1.modules[i].hw), len(pos2.modules[i].hw)))]
                if len(hw) < 3:
                    for j in range(len(hw), 3):
                        if len(pos1.modules[i].hw) > j:
                            hw.append(int(round(pos1.modules[i].hw[j] + self.algconf.alpha*random.gauss(0, 1))))
                        else:
                            hw.append(random.randint(0, len(Module.conf.modules[i].hw)-1))
                sw = [int(round(pos1.modules[i].sw[j] + (pos2.modules[i].sw[j] - pos1.modules[i].sw[j])*coef + self.algconf.alpha*random.gauss(0, 1))) for j in range(min(len(pos1.modules[i].sw), len(pos2.modules[i].sw)))]
                if len(sw) < 3:
                    for j in range(len(sw), 3):
                        if len(pos1.modules[i].sw) > j:
                            sw.append(int(round(pos1.modules[i].sw[j] + self.algconf.alpha*random.gauss(0, 1))))
                        else:
                            sw.append(random.randint(0, len(Module.conf.modules[i].sw)-1))
                #print "MOO = NVP11", len(hw), len(sw), "\n"
                new = self._checkNewModule(i, hw, sw, moo)
                #new = NVP11(i, hw, sw)
            elif moo == 3:
                #print "MOO = RB11\n"
                hw = [int(round(pos1.modules[i].hw[j] + (pos2.modules[i].hw[j] - pos1.modules[i].hw[j])*coef + self.algconf.alpha*random.gauss(0, 1))) for j in range(min(len(pos1.modules[i].hw), len(pos2.modules[i].hw)))]
                if len(hw) < 2:
                    if len(pos1.modules[i].hw) > 1:
                        hw.append(int(round(pos1.modules[i].hw[1] + self.algconf.alpha*random.gauss(0, 1))))
                    else:
                        hw.append(random.randint(0, len(Module.conf.modules[i].hw)-1))
                elif len(hw) > 2:
                    hw = hw[0:2]
                sw = [int(round(pos1.modules[i].sw[j] + (pos2.modules[i].sw[j] - pos1.modules[i].sw[j])*coef + self.algconf.alpha*random.gauss(0, 1))) for j in range(min(len(pos1.modules[i].sw), len(pos2.modules[i].sw)))]
                if len(sw) < 2:
                    if len(pos1.modules[i].sw) > 1:
                        sw.append(int(round(pos1.modules[i].sw[1] + self.algconf.alpha*random.gauss(0, 1))))
                    else:
                        sw.append(random.randint(0, len(Module.conf.modules[i].sw)-1))
                elif len(sw) > 2:
                    sw = sw[0:2]
                #print "MOO = RB11", len(hw), len(sw), "\n"
                new = self._checkNewModule(i, hw, sw, moo)
                #new = RB11(i, hw, sw)
            else:
                print "ERROR (FA: _move): moo has NoneType ", moo, "\n"

            pos1.modules[i] = new

    def _updateRel(self, i):
        if not i.CheckConstraints():
            i.rel = -1.0
        else:
            #i.__computeCost()
            #i.__computeRel()
            i.Update()

    def _sort_and_evalBest(self):
        self.positions.sort(key = lambda x: x.rel, reverse = True) #reverse????
        if self.positions[0].rel > self.best:
            self.best = self.positions[0].rel
            self.currentSolution = self.positions[0] #if change order than need change number of best position 


    def _checkStopCondition(self):
        if self.currentIter >= self.algconf.maxIter:
            return True
        else:
            return False

    def _checkNewModule(self, num, hw, sw, moo): #check if components of new module is out of range
        #check constraints
        for i in range(len(hw)):
            if hw[i] < 0:
                hw[i] = 0
            elif hw[i] >= len(Module.conf.modules[num].hw):
                hw[i] = len(Module.conf.modules[num].hw) - 1

        for i in range(len(sw)):
            if sw[i] < 0:
                sw[i] = 0
            elif sw[i] >= len(Module.conf.modules[num].sw):
                sw[i] = len(Module.conf.modules[num].sw) - 1

        if len(sw) == 2 and sw[0] == sw[1]:
            if sw[1] < len(Module.conf.modules[num].sw) - 1:
                sw[1] += 1
            else:
                sw[0] -= 1

        if len(sw) == 3:
            if sw[0] == sw[1]:
                if sw[0] > 0:
                    sw[0] -= 1
                else:
                    sw[1] += 1

            if sw[1] == sw[2]:
                if sw[1] < len(Module.conf.modules[num].sw) - 1:
                    sw[2] += 1
                else:
                    if sw[1] == sw[0]+1:
                        sw[0] -= 1
                        sw[1] -= 1
                    else:
                        sw[1] -= 1

            if sw[0] == sw[2]:
                if sw[0] > 0:
                    if sw[1] == sw[0]-1:
                        if sw[1] == 0:
                            sw[2] += 1
                        else:
                            sw[0] -= 2
                    else:
                        sw[0] -= 1
                else:
                    if sw[1] == sw[0]+1:
                        sw[2] += 2
                    else:
                        sw[2] += 1
        new = None
        #create new module
        if moo == 0:
            new = NONE(num, hw, sw)
        elif moo == 1:
            new = NVP01(num, hw, sw)
        elif moo == 2:
            new = NVP11(num, hw, sw)
        elif moo == 3:
            new = RB11(num, hw, sw)
        return new

    def Clear(self):
        Algorithm.Clear(self)
        self.positions = []
        self.best = 0