from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy, time, math

class Velocity:
    def __init__(self):
        self.hw = [0, 0, 0]
        self.sw = [0, 0, 0]
        self.moo = 0

    def __mul__(self, other):
        for i in range(len(self.hw)):
            self.hw[i] = int(round(self.hw[i]*other)) 
            '''#check if self in [0, v_max]
            if abs(self.hw[i]) > Algorithm.algconf.v_max.hw[i]:
                if self.hw[i] > 0:
                    self.hw[i] = Algorithm.algconf.v_max.hw[i]
                else:
                    self.hw[i] = -Algorithm.algconf.v_max.hw[i]'''

        for i in range(len(self.sw)):
            self.sw[i] = int(round(self.sw[i]*other))
            '''#check if self in [0, v_max]
            if abs(self.sw[i]) > Algorithm.algconf.v_max.sw[i]:
                if self.sw[i] > 0:
                    self.sw[i] = Algorithm.algconf.v_max.sw[i]
                else:
                    self.sw[i] = -Algorithm.algconf.v_max.sw[i]'''
        
        return self

    def __add__(self, other):
        if isinstance(other, Velocity):
            new = Velocity()
            r = random.random()
            if r < 0.5: 
                new.moo = self.moo
            else:
                new.moo = other.moo
            for i in range(3):
                new.hw[i] = (self.hw[i] + other.hw[i])
                new.sw[i] = (self.sw[i] + other.sw[i])

                '''#check if new in [0, v_max]
                if abs(new.hw[i]) > Algorithm.algconf.v_max.hw[i]:
                    if new.hw[i] > 0:
                        new.hw[i] = Algorithm.algconf.v_max.hw[i]
                    else:
                        new.hw[i] = -Algorithm.algconf.v_max.hw[i]
                if abs(new.sw[i]) > Algorithm.algconf.v_max.sw[i]:
                    if new.sw[i] > 0:
                        new.sw[i] = Algorithm.algconf.v_max.sw[i]
                    else:
                        new.sw[i] = -Algorithm.algconf.v_max.sw[i]'''
        
            
            return new
        elif isinstance(other, Module):
            #new = None
            hw = []
            sw = []
            if self.moo == 0:
                #new = NONE(other.num)
                hw = [other.hw[0] + self.hw[0]]
                sw = [other.sw[0] + self.sw[0]]
               
            elif self.moo == 1:
                #new = NVP01(other.num)
                hw = [other.hw[0] + self.hw[0]]
                if len(other.sw) < 3:
                    sw = [other.sw[i] + self.sw[i] for i in range(len(other.sw))]
                    for i in range(3-len(other.sw)):
                        sw.append(self.sw[i])
                else:
                    sw = [other.sw[i] + self.sw[i] for i in range(3)]
                
            elif self.moo == 2:
                #new = NVP11(other.num)
                if len(other.hw) < 3:
                    hw = [other.hw[i] + self.hw[i] for i in range(len(other.hw))]
                    for i in range(3-len(other.hw)):
                        hw.append(self.hw[i])
                else:
                    hw = [other.hw[i] + self.hw[i] for i in range(3)]
                if len(other.sw) < 3:
                    sw = [other.sw[i] + self.sw[i] for i in range(len(other.sw))]
                    for i in range(3-len(other.sw)):
                        sw.append(self.sw[i])
                else:
                    sw = [other.sw[i] + self.sw[i] for i in range(3)]
                
            elif self.moo == 3:
                #new = RB11(other.num)
                if len(other.hw) < 2:
                    hw = [other.hw[0] + self.hw[0]]
                    hw.append(self.hw[1])
                else:
                    hw = [other.hw[i] + self.hw[i] for i in range(2)]
                if len(other.sw) < 2:
                    sw = [other.sw[0] + self.sw[0]]
                    sw.append(self.sw[1])
                else:
                    sw = [other.sw[i] + self.sw[i] for i in range(2)]

            else:
                print "ERROR: BSO:Velocity __add__ with Module\n"
                
            #new = _checkNewModule(new)
            return (other.num, hw, sw, self.moo)
            

class BSO(Algorithm):

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

        self.r = self.algconf.r_0 #pulse rate
        self.a = self.algconf.a_0 #loudness

        # generate positions and velocity for agents
        for i in range(self.algconf.nagents):
            agent = System()
            agent.GenerateRandom(True) #True means that I want to check constraints
            
            v = [Velocity() for idx in range(Module.conf.modNum)] #velocity of one agent
            #self.velocity.append(v)
            self.positions.append([agent, v])

        self._sort_and_evalBest()

        while not self._checkStopCondition():
            self.Step() 
            self._sort_and_evalBest()
            self.a = self.a*self.algconf.alpha #change loudness
            self.r = self.r*(1-math.exp(-self.algconf.gamma*self.currentIter)) #change pulse rate
            self.currentIter += 1

        print "Best solution: ", self.currentSolution, "\n\n"

        #New execution of algorithm and its results save in statistics
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(self.currentSolution, self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))
        

    def Step(self):
        for i in self.positions: 
            new = self._globalMove(i)
            new = self._localMove(new)
            if i[0].rel < new.rel or (i[0].rel > new.rel and random.random() < self.a): #accept new solution with probability self.a
                i[0] = new


    def _globalMove(self, pos):
        f = self.algconf.f_min + random.random()*(self.algconf.f_max - self.algconf.f_min)
        tmp = self._systemsDif(pos[0], self.currentSolution)
        newpos = System()
        for i in range(Module.conf.modNum):
            pos[1][i] = pos[1][i] + tmp[i]*f
            num, hw, sw, moo = pos[1][i] + pos[0].modules[i]
            new = self._checkNewModule(num, hw, sw, moo)
            newpos.modules.append(new)
        self._updateRel(newpos)
        return newpos

    def _systemsDif(self, sys1, sys2):
        dif = []
        for i in range(Module.conf.modNum):
            new = Velocity()
            r = random.random()
            moosys = None
            if r < 0.5: 
                moosys = sys1
            else:
                moosys = sys2
            if isinstance(moosys.modules[i], NONE):
                new.moo = 0
            elif isinstance(moosys.modules[i], NVP01):
                new.moo = 1
            elif isinstance(moosys.modules[i], NVP11):
                new.moo = 2
            elif isinstance(moosys.modules[i], RB11):
                new.moo = 3

            for idx in range(min(len(sys1.modules[i].hw), len(sys2.modules[i].hw))):
                new.hw[idx] = (sys1.modules[i].hw[idx] - sys2.modules[i].hw[idx])

            for idx in range(min(len(sys1.modules[i].sw), len(sys2.modules[i].sw))):
                new.sw[idx] = (sys1.modules[i].sw[idx] - sys2.modules[i].sw[idx])

            dif.append(new)

        return dif

    def _localMove(self, pos):
        if random.random() < self.r:
            tmp = random.randint(0, self.algconf.nagents//4) #select a solution among the best solutions
            best = self.positions[tmp][0]
            newpos = System()
            for idx in best.modules:
                moo = None
                if isinstance(idx, NONE):
                    moo = 0
                elif isinstance(idx, NVP01):
                    moo = 1
                elif isinstance(idx, NVP11):
                    moo = 2
                elif isinstance(idx, RB11):
                    moo = 3

                #new = None

                hw = [int(round(idx.hw[j] + random.uniform(-1, 1)*self.a)) for j in range(len(idx.hw))]
                sw = [int(round(idx.sw[j] + random.uniform(-1, 1)*self.a)) for j in range(len(idx.sw))]

                new = self._checkNewModule(idx.num, hw, sw, moo)

                newpos.modules.append(new)
            self._updateRel(newpos)
            return newpos
        else:
            newpos = self._randomWalk(pos)
            return newpos
                

    def _randomWalk(self, pos):
        newpos = System()
        for idx in pos.modules:
            moo = None
            if random.random() < 0.75:
                if isinstance(idx, NONE):
                    moo = 0
                elif isinstance(idx, NVP01):
                    moo = 1
                elif isinstance(idx, NVP11):
                    moo = 2
                elif isinstance(idx, RB11):
                    moo = 3
            else:
                moo = random.randint(0, 3)    

            new = None

            if moo == 0:
                hw = [int(round(idx.hw[0] + random.gauss(0, 1)))]
                sw = [int(round(idx.sw[0] + random.gauss(0, 1)))]
                new = self._checkNewModule(idx.num, hw, sw, moo)
            elif moo == 1: 
                hw = [int(round(idx.hw[0] + random.gauss(0, 1)))]
                sw = [int(round(idx.sw[j] + random.gauss(0, 1))) for j in range(len(idx.sw))]
                if len(sw) < 3:
                    for j in range(len(sw), 3):
                        sw.append(random.randint(0, len(Module.conf.modules[idx.num].sw)-1))
                new = self._checkNewModule(idx.num, hw, sw, moo)
            elif moo == 2:
                hw = [int(round(idx.hw[j] + random.gauss(0, 1))) for j in range(len(idx.hw))]
                if len(hw) < 3:
                    for j in range(len(hw), 3):
                        hw.append(random.randint(0, len(Module.conf.modules[idx.num].hw)-1))
                sw = [int(round(idx.sw[j] + random.gauss(0, 1))) for j in range(len(idx.sw))]
                if len(sw) < 3:
                    for j in range(len(sw), 3):
                        sw.append(random.randint(0, len(Module.conf.modules[idx.num].sw)-1))
                new = self._checkNewModule(idx.num, hw, sw, moo)
            elif moo == 3:
                hw = [int(round(idx.hw[j] + random.gauss(0, 1))) for j in range(len(idx.hw))]
                if len(hw) < 2:
                    hw.append(random.randint(0, len(Module.conf.modules[idx.num].hw)-1))
                elif len(hw) > 2:
                    hw = hw[0:2]
                sw = [int(round(idx.sw[j] + random.gauss(0, 1))) for j in range(len(idx.sw))]
                if len(sw) < 2:
                    sw.append(random.randint(0, len(Module.conf.modules[idx.num].sw)-1))
                elif len(sw) > 2:
                    sw = sw[0:2]
                new = self._checkNewModule(idx.num, hw, sw, moo)
            else:
                print "ERROR (BSO: _randomWalk): moo has NoneType ", moo, "\n"

            newpos.modules.append(new)

        self._updateRel(newpos)
        return newpos

    def _updateRel(self, i):
        if not i.CheckConstraints():
            i.rel = -1.0
        else:
            #i.__computeCost()
            #i.__computeRel()
            i.Update()

    def _sort_and_evalBest(self):
        self.positions.sort(key = lambda x: x[0].rel, reverse = False) #reverse????
        if self.positions[Module.conf.modNum][0].rel > self.best:
            self.currentSolution = self.positions[Module.conf.modNum][0] #if change order than need change number of best position 
            self.best = self.currentSolution.rel

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
        #self.velocity = []