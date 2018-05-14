from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy, time

def _checkNewModule(self): #check if components of new module is out of range
    for i in range(len(self.hw)):
        if self.hw[i] < 0:
            self.hw[i] = 0
        elif self.hw[i] >= len(Module.conf.modules[self.num].hw):
            self.hw[i] = len(Module.conf.modules[self.num].hw) - 1

    for i in range(len(self.sw)):
        if self.sw[i] < 0:
            self.sw[i] = 0
        elif self.sw[i] >= len(Module.conf.modules[self.num].sw):
            self.sw[i] = len(Module.conf.modules[self.num].sw) - 1

    if len(self.sw) == 2 and self.sw[0] == self.sw[1]:
        if self.sw[1] < len(Module.conf.modules[self.num].sw) - 1:
            self.sw[1] += 1
        else:
            self.sw[0] -= 1

    if len(self.sw) == 3:
        if self.sw[0] == self.sw[1]:
            if self.sw[0] > 0:
                self.sw[0] -= 1
            else:
                self.sw[1] += 1

        if self.sw[1] == self.sw[2]:
            if self.sw[1] < len(Module.conf.modules[self.num].sw) - 1:
                self.sw[2] += 1
            else:
                if self.sw[1] == self.sw[0]+1:
                    self.sw[0] -= 1
                    self.sw[1] -= 1
                else:
                    self.sw[1] -= 1

        if self.sw[0] == self.sw[2]:
            if self.sw[0] > 0:
                if self.sw[1] == self.sw[0]-1:
                    if self.sw[1] == 0:
                        self.sw[2] += 1
                    else:
                        self.sw[0] -= 2
                else:
                    self.sw[0] -= 1
            else:
                if self.sw[1] ==self.sw[0]+1:
                    self.sw[2] += 2
                else:
                    self.sw[2] += 1
    new = None
    #it is necessary to computes rel and cost
    if isinstance(self, NONE):
        new = NONE(self.num, self.hw, self.sw)
    elif isinstance(self, NVP01):
        new = NVP01(self.num, self.hw, self.sw)
    elif isinstance(self, NVP11):
        new = NVP11(self.num, self.hw, self.sw)
    elif isinstance(self, RB11):
        new = RB11(self.num, self.hw, self.sw)
    return new


        


class Velocity:
    def __init__(self):
        self.hw = [0, 0, 0]
        self.sw = [0, 0, 0]
        self.moo = 0

    def __mul__(self, other):
        for i in range(len(self.hw)):
            self.hw[i] = int(round(self.hw[i]*other)) 
            #check if self in [0, v_max]
            if abs(self.hw[i]) > Algorithm.algconf.v_max.hw[i]:
                if self.hw[i] > 0:
                    self.hw[i] = Algorithm.algconf.v_max.hw[i]
                else:
                    self.hw[i] = -Algorithm.algconf.v_max.hw[i]

        for i in range(len(self.sw)):
            self.sw[i] = int(round(self.sw[i]*other))
            #check if self in [0, v_max]
            if abs(self.sw[i]) > Algorithm.algconf.v_max.sw[i]:
                if self.sw[i] > 0:
                    self.sw[i] = Algorithm.algconf.v_max.sw[i]
                else:
                    self.sw[i] = -Algorithm.algconf.v_max.sw[i]
        
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

                #check if new in [0, v_max]
                if abs(new.hw[i]) > Algorithm.algconf.v_max.hw[i]:
                    if new.hw[i] > 0:
                        new.hw[i] = Algorithm.algconf.v_max.hw[i]
                    else:
                        new.hw[i] = -Algorithm.algconf.v_max.hw[i]
                if abs(new.sw[i]) > Algorithm.algconf.v_max.sw[i]:
                    if new.sw[i] > 0:
                        new.sw[i] = Algorithm.algconf.v_max.sw[i]
                    else:
                        new.sw[i] = -Algorithm.algconf.v_max.sw[i]
        
            
            return new
        elif isinstance(other, Module):
            new = None
            if self.moo == 0:
                new = NONE(other.num)
                new.hw = [other.hw[0] + self.hw[0]]
                new.sw = [other.sw[0] + self.sw[0]]
               
            elif self.moo == 1:
                new = NVP01(other.num)
                new.hw = [other.hw[0] + self.hw[0]]
                if len(other.sw) < 3:
                    new.sw = [other.sw[i] + self.sw[i] for i in range(len(other.sw))]
                    for i in range(3-len(other.sw)):
                        new.sw.append(self.sw[i])
                else:
                    new.sw = [other.sw[i] + self.sw[i] for i in range(3)]
                
            elif self.moo == 2:
                new = NVP11(other.num)
                if len(other.hw) < 3:
                    new.hw = [other.hw[i] + self.hw[i] for i in range(len(other.hw))]
                    for i in range(3-len(other.hw)):
                        new.hw.append(self.hw[i])
                else:
                    new.hw = [other.hw[i] + self.hw[i] for i in range(3)]
                if len(other.sw) < 3:
                    new.sw = [other.sw[i] + self.sw[i] for i in range(len(other.sw))]
                    for i in range(3-len(other.sw)):
                        new.sw.append(self.sw[i])
                else:
                    new.sw = [other.sw[i] + self.sw[i] for i in range(3)]
                
            elif self.moo == 3:
                new = RB11(other.num)
                if len(other.hw) < 2:
                    new.hw = [other.hw[0] + self.hw[0]]
                    new.hw.append(self.hw[1])
                else:
                    new.hw = [other.hw[i] + self.hw[i] for i in range(2)]
                if len(other.sw) < 2:
                    new.sw = [other.sw[0] + self.sw[0]]
                    new.sw.append(self.sw[1])
                else:
                    new.sw = [other.sw[i] + self.sw[i] for i in range(2)]
                
            new = _checkNewModule(new)
            return new
            
            


class PSO(Algorithm):

    def __init__(self):
        Algorithm.__init__(self)

        '''
        Algorithm.__init__(self) contains next fields:

        # Indicates current best solution in algorithm
        self.currentSolution = None
        # Indicates number of iterations in the algorithm
        self.currentIter = 0
        self.stat = Statistics()

        class fields:

        algconf = None
        timecounts = 0
        simcounts = 0
        time = None
        result_filename = "result.csv"
        '''

        #random.seed(time.time())

        self.positions = [] #positions of agents
        self.local_best = [] #best solutions from all agents
        self.velocity = [] # velocity of every agent

        '''#all parameters must be defined in AlgConfig, should to implement it
        nagents = 0 #parameter: number of agents
        w = 0 #parameter
        rnd1, rnd2 = 0, 0 #parameters
        alpha1, alpha2 = 0, 0 #parameters
        v_min = 0 #parameter: minimal velocity
        v_max = 0 #parameter: maximal velocity

        #all parameters should be here, I think
        algconf = None'''

    def Run(self):
        self.Clear()
         # time counter (iterations counter), counted by this algorithm
        Algorithm.timecounts = 0
        # time counter (iteration counter), counted by
        Algorithm.simcounts = 0
        Algorithm.time = time.time()

        # generate positions and velocities for agents
        for i in range(self.algconf.nagents):
            agent = System()
            agent.GenerateRandom(True) #True means that I want to check constraints
            self.positions.append(agent)
            self.local_best.append(agent)           
            v = [Velocity() for idx in range(Module.conf.modNum)]
            self.velocity.append(v)

        self._firstBest() #evaluate best solution

        while not self._checkStopCondition():
            self.Step() #move to new positions
            self._updateRel() #update reliability of each agent
            self._evalBest() #evaluate new best solutions
            self.algconf.w = (self.algconf.w_max - self.algconf.w_min)*(self.algconf.maxIter-self.currentIter)/self.algconf.maxIter+self.algconf.w_min
            self.currentIter += 1

        print "Best solution: ", self.currentSolution, "\n\n"

        #New execution of algorithm and its results save in statistics
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(self.currentSolution, self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))
        

    def _firstBest(self):
        rel = 0
        for i in self.positions:
            if i.rel > rel:
                rel = i.rel
                self.currentSolution = i

    def _evalBest(self):
        for idx, pos in enumerate(self.positions):
            if self.local_best[idx] < pos.rel:
                self.local_best[idx] = pos
                if self.currentSolution.rel < pos.rel:
                    self.currentSolution = pos

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

            if len(sys1.modules[i].hw) == len(sys2.modules[i].hw):
                for idx in range(len(sys1.modules[i].hw)):
                    new.hw[idx] = (sys1.modules[i].hw[idx] - sys2.modules[i].hw[idx]) 
                    if abs(new.hw[idx]) > Algorithm.algconf.v_max.hw[idx]:
                        if new.hw[idx] > 0:
                            new.hw[idx] = Algorithm.algconf.v_max.hw[idx]
                        else:
                            new.hw[idx] = -Algorithm.algconf.v_max.hw[idx]
            else:
                if len(sys1.modules[i].hw) < len(sys2.modules[i].hw):
                    for idx in range(len(sys1.modules[i].hw)):
                        new.hw[idx] = (sys1.modules[i].hw[idx] - sys2.modules[i].hw[idx]) 
                        if abs(new.hw[idx]) > Algorithm.algconf.v_max.hw[idx]:
                            if new.hw[idx] > 0:
                                new.hw[idx] = Algorithm.algconf.v_max.hw[idx]
                            else:
                                new.hw[idx] = -Algorithm.algconf.v_max.hw[idx]
                else:
                    for idx in range(len(sys2.modules[i].hw)):
                        new.hw[idx] = (sys1.modules[i].hw[idx] - sys2.modules[i].hw[idx])
                        if abs(new.hw[idx]) > Algorithm.algconf.v_max.hw[idx]:
                            if new.hw[idx] > 0:
                                new.hw[idx] = Algorithm.algconf.v_max.hw[idx]
                            else:
                                new.hw[idx] = -Algorithm.algconf.v_max.hw[idx]
                '''    for idx in range(len(sys2.modules[i].hw), len(sys1.modules[i].hw)):
                        new.hw[idx] = (sys1.modules[i].hw[idx])
                        if abs(new.hw[idx]) > Algorithm.algconf.v_max.hw[idx]:
                            if new.hw[idx] > 0:
                                new.hw[idx] = Algorithm.algconf.v_max.hw[idx]
                            else:
                                new.hw[idx] = -Algorithm.algconf.v_max.hw[idx]'''

            if len(sys1.modules[i].sw) == len(sys2.modules[i].sw):
                for idx in range(len(sys1.modules[i].sw)):
                    new.sw[idx] = (sys1.modules[i].sw[idx] - sys2.modules[i].sw[idx]) 
                    if abs(new.sw[idx]) > Algorithm.algconf.v_max.sw[idx]:
                        if new.sw[idx] > 0:
                            new.sw[idx] = Algorithm.algconf.v_max.sw[idx]
                        else:
                            new.sw[idx] = -Algorithm.algconf.v_max.sw[idx]
            else:
                if len(sys1.modules[i].sw) < len(sys2.modules[i].sw):
                    for idx in range(len(sys1.modules[i].sw)):
                        new.sw[idx] = (sys1.modules[i].sw[idx] - sys2.modules[i].sw[idx]) 
                        if abs(new.sw[idx]) > Algorithm.algconf.v_max.sw[idx]:
                            if new.sw[idx] > 0:
                                new.sw[idx] = Algorithm.algconf.v_max.sw[idx]
                            else:
                                new.sw[idx] = -Algorithm.algconf.v_max.sw[idx]
                else:
                    for idx in range(len(sys2.modules[i].sw)):
                        new.sw[idx] = (sys1.modules[i].sw[idx] - sys2.modules[i].sw[idx])
                        if abs(new.sw[idx]) > Algorithm.algconf.v_max.sw[idx]:
                            if new.sw[idx] > 0:
                                new.sw[idx] = Algorithm.algconf.v_max.sw[idx]
                            else:
                                new.sw[idx] = -Algorithm.algconf.v_max.sw[idx]
                '''    for idx in range(len(sys2.modules[i].sw), len(sys1.modules[i].sw)):
                        new.sw[idx] = (sys1.modules[i].sw[idx])
                        if abs(new.sw[idx]) > Algorithm.algconf.v_max.sw[idx]:
                            if new.sw[idx] > 0:
                                new.sw[idx] = Algorithm.algconf.v_max.sw[idx]
                            else:
                                new.sw[idx] = -Algorithm.algconf.v_max.sw[idx]'''

            dif.append(new)

        return dif

    def Step(self):
        for idx in range(self.algconf.nagents):
            
            #rnd1 = random.random()
            #rnd2 = random.random()
            rnd1 = random.gauss(0, 1)
            rnd2 = random.gauss(0, 1)

            tmp1 = self._systemsDif(self.local_best[idx], self.positions[idx]) 
            tmp2 = self._systemsDif(self.currentSolution, self.positions[idx])
            
            tmp1 = [i * self.algconf.alpha1 * rnd1 for i in tmp1]
            tmp2 = [i * self.algconf.alpha2 * rnd2 for i in tmp2]

            for i in range(Module.conf.modNum):
                self.velocity[idx][i] = self.velocity[idx][i] * self.algconf.w + tmp1[i] + tmp2[i] #changed velocity
                self.positions[idx].modules[i] = self.velocity[idx][i] + self.positions[idx].modules[i] #changed position

    def _updateRel(self):
        for i in self.positions:
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

    
    def Clear(self):
        Algorithm.Clear(self)
        self.positions = [] #positions of agents
        self.local_best = [] #best solutions from all agents
        self.velocity = [] # velocity of every agent

    '''
        maybe need to reimplement
    '''
    #def PrintStats(self):

    