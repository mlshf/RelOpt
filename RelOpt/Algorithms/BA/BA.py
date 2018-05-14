from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy, time, math
            

class BA(Algorithm):

    def __init__(self):
        Algorithm.__init__(self)
        self.positions = [] #positions and velocity of agents
        self.best = 0 #best reliability
        #self.velocity = [] #velocity of agents

    def Run(self):
        self.Clear()
         # time counter (iterations counter), counted by this algorithm
        Algorithm.timecounts = 0
        # time counter (iteration counter), counted by
        Algorithm.simcounts = 0
        Algorithm.time = time.time()


        # generate positions
        for i in range(self.algconf.nagents):
            agent = System()
            agent.GenerateRandom(True) #True means that I want to check constraint
            self.positions.append([agent, self.algconf.limit])


        while not self._checkStopCondition():
            self.Step() 
            self.currentIter += 1

        print "Best solution: ", self.currentSolution, "\n\n"

        #New execution of algorithm and its results save in statistics
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(self.currentSolution, self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))
        

    def Step(self):
        for i in range(self.algconf.nagents): 
            new = self._move(i)
            if new.rel > self.positions[i][0]:
                self.positions[i][0] = new
                self.positions[i][1] = self.algconf.limit
            else:
                self.positions[i][1] -= 1

        relsum = 0.0
        for i in self.positions:
            relsum += i[0].rel

        for i in range(self.algconf.nagents):
            n = int(round(self.algconf.onlookers*self.positions[i][0].rel/relsum))
            for j in range(n):
                new = self._move(i)
                if new.rel > self.positions[i][0]:
                    self.positions[i][0] = new
                    self.positions[i][1] = self.algconf.limit

        for i in range(self.algconf.nagents):
            if self.positions[i][1] <= 0:
                agent = System()
                agent.GenerateRandom(True)
                self.positions[i] = [agent, self.algconf.limit]

        for i in self.positions:
            if i[0].rel > self.best:
                self.currentSolution = i[0]
                self.best = i[0].rel


    def _move(self, i):
        coef = random.uniform(-2, 2)
        k = i
        while k == i:
            k = random.randint(0, self.algconf.nagents-1)
        j = random.randint(0, Module.conf.modNum-1)

        v = System()
        v.modules = copy.deepcopy(self.positions[i][0].modules)
        
        #creating new module
        r = random.random()
        moosys = None
        moo = 0
        if r < 0.5: 
            moosys = v.modules[j]
        else:
            moosys = self.positions[k][0].modules[j]
        if isinstance(moosys, NONE):
            moo = 0
        elif isinstance(moosys, NVP01):
            moo = 1
        elif isinstance(moosys, NVP11):
            moo = 2
        elif isinstance(moosys, RB11):
            moo = 3

        new = None
        mod1 = v.modules[j]
        mod2 = self.positions[k][0].modules[j]

        if moo == 0:
            hw = [int(round(mod1.hw[0] + (mod1.hw[0] - mod2.hw[0])*coef))]
            sw = [int(round(mod1.sw[0] + (mod1.sw[0] - mod2.sw[0])*coef))]
            new = self._checkNewModule(j, hw, sw, moo)
        elif moo == 1: 
            hw = [int(round(mod1.hw[0] + (mod1.hw[0] - mod2.hw[0])*coef))]
            sw = [int(round(mod1.sw[idx] + (mod1.sw[idx] - mod2.sw[idx])*coef)) for idx in range(min(len(mod1.sw), len(mod2.sw)))]
            if len(sw) < 3:
                for idx in range(len(sw), 3):
                    if len(mod1.sw) > idx:
                        sw.append(mod1.sw[idx])
                    else:
                        sw.append(random.randint(0, len(Module.conf.modules[j].sw)-1))
            new = self._checkNewModule(j, hw, sw, moo)
        elif moo == 2:
            hw = [int(round(mod1.hw[idx] + (mod1.hw[idx] - mod2.hw[idx])*coef)) for idx in range(min(len(mod1.hw), len(mod2.hw)))]
            if len(hw) < 3:
                for idx in range(len(hw), 3):
                    if len(mod1.hw) > idx:
                        hw.append(mod1.hw[idx])
                    else:
                        hw.append(random.randint(0, len(Module.conf.modules[j].hw)-1))
            sw = [int(round(mod1.sw[idx] + (mod1.sw[idx] - mod2.sw[idx])*coef)) for idx in range(min(len(mod1.sw), len(mod2.sw)))]
            if len(sw) < 3:
                for idx in range(len(sw), 3):
                    if len(mod1.sw) > idx:
                        sw.append(mod1.sw[idx])
                    else:
                        sw.append(random.randint(0, len(Module.conf.modules[j].sw)-1))
            new = self._checkNewModule(j, hw, sw, moo)
        elif moo == 3:
            hw = [int(round(mod1.hw[idx] + (mod1.hw[idx] - mod2.hw[idx])*coef)) for idx in range(min(len(mod1.hw), len(mod2.hw)))]
            if len(hw) < 2:
                if len(mod1.hw) > 1:
                    hw.append(mod1.hw[1])
                else:
                    hw.append(random.randint(0, len(Module.conf.modules[j].hw)-1))
            elif len(hw) > 2:
                hw = hw[0:2]
            sw = [int(round(mod1.sw[idx] + (mod1.sw[idx] - mod2.sw[idx])*coef)) for idx in range(min(len(mod1.sw), len(mod2.sw)))]
            if len(sw) < 2:
                if len(mod1.sw) > 1:
                    sw.append(mod1.sw[1])
                else:
                    sw.append(random.randint(0, len(Module.conf.modules[j].sw)-1))
            elif len(sw) > 2:
                sw = sw[0:2]
            new = self._checkNewModule(j, hw, sw, moo)
        else:
            print "ERROR: moo has NoneType\n"

        v.modules[j] = new
        self._updateRel(v)
        return v


    def _updateRel(self, i):
        if not i.CheckConstraints():
            i.rel = -1.0
        else:
            #i.__computeCost()
            #i.__computeRel()
            i.Update()

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