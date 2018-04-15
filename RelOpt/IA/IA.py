__author__ = 'avasilenko'

from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy, time, math
from math import *

# Ssorry for English
# It is wise to understand the diagram listed in the task explanation before starting to look code
# It is also wise to follow recomindations listed at the very end of the file
# Start analysing comment from function "Run" and after that - look functions bottom to top

# You will also have to change code in
#   1) function LoadAlgConf in MainWindow class in MainWindow.py file
#   2) function Run in MainWindow class in MainWindow.py file
#   3) function retranslateUi in GUI.Windows.ui_MainWindow.py
#   4) function setupUi in GUI.Windows.ui_MainWindow.py

# All data you need about system is stored in python classes:
#   1) Module
#   2) System
#   3) Constraints
# You can find in them reliabilities, costs, etc

class IA(Algorithm):
    def __init__(self):
        # Lets call the base class constructor
        Algorithm.__init__(self)
        # In my model type population is a list of lists of 2 elements, where first element is a system, and second
        # element is its affinity
        self.population = []
        self.iterWithoutChange = 0

    def Step(self):
        self._SelectBestAffinitySystems()
        self._CloneBestAffinitySystems()

        # This order is used in GA.py algorithm
        self._Recombine()
        self._Mutate()

        self.population.sort(key=lambda x: x[1], reverse=True)
        self._RemoveIdentical()

        self._EvalPopulation()


    def Run(self):
        self.Clear()
        # Number of interations counted by our algorithm
        Algorithm.timecounts = 0
        # Number of iterations counted by model (it is no used, forgot about it)
        Algorithm.simcounts = 0
        # Time of start
        Algorithm.time = time.time()

        # POPULATION generating,
        # population consists of different combinations of our SYSTEM evaluation
        # Every instance of our population (prototype of out system) consists of SUBSYSTEMS (they are executed in system
        # one after another)
        # subsystem is one of the different MODULES - (NONE, NVP01, NVP11 or RB11) (every of the modules is some type of
        # execution subsystem with reliability mechanism - but you must not care about it at all) they are defined in
        # Module.py and are inherited from calls Module
        #
        # Remember the hierarchy - POPULATION -> consists of -> SYSTEMS -> consists of -> SUBSYSTEMS -> is one of -> MODULES
        #
        # In some articles you can see that subsystem can consist of list of modules (or "components"), but it looks like
        # in this RelOpt project subsystem is one of modules and module already consists of different components, but as
        # it has all internal values such cost, reliability, etc. Just do not bother with it
        for i in range(self.algconf.popNum):
            # Creating an instance of the system
            s = System()
            # Initializing some module for every subsystem in created system
            s.GenerateRandom(True)
            self.population.append([s, 0])
        self._RecalulatePopulationAffinities()
        # Sorting our system by affinity
        self.population.sort(key=lambda x: x[1], reverse=True)
        self.currentSolution = copy.deepcopy(self.population[0])

        # This while is going to evaluate until the StopCondition will be true
        while not self._CheckStopCondition():
            self.Step()
            print "{0:<4}".format(self.currentIter), self.currentSolution[0], "Affinity =", self.currentSolution[1]

        # Just printing some info onto standart output
        print "Best solution: ", self.currentSolution[0], "Affinity =", self.currentSolution[1]
        print "----------------------------------------------------------------------------\n"
        Algorithm.time = time.time() - Algorithm.time

        # This line will store results that will end in storing your results in .csv file
        # Just left it "as is" and everything will be okey
        self.stat.AddExecution(Execution(self.currentSolution[0], self.currentIter,
            Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))

    def Clear(self):
        # Some clear up in our algorithm for potential reuse of it
        Algorithm.Clear(self)
        self.population = []
        self.iterWithoutChange = 0

    def _RemoveIdentical(self):
        # In algorithm there was not clearly explained what really we must do in case to systems are too identical
        # It looked like I must destroy both systems, but it looks not very constructive
        # In this realization I will destroy only system that is worse
        # self.algconf.identicalThreshold - is a threashold, and all systems affinities must differ more
        i = 0
        while i < len(self.population) - 1:
            if math.fabs(self.population[i][1] - self.population[i+1][1]) < self.algconf.identicalThreshold:
                self.population.pop(i+1)
            else:
                i += 1

    def _SelectBestAffinitySystems(self):
        # I select here best systems - number of systems is indicated in parameter self.algconf.selectionBest
        self.population = self.population[:self.algconf.selectionBest]

    def _CloneBestAffinitySystems(self):
        # Cloning best systems according to their affinities
        # I use linear dependence between affinity and vacant places in population to refill population amount to
        # self.algconf.popNum
        # self.algconf.cloneNum - this is maximum number of clones, that I can create
        res_affinity = [self.__MappingFunction(i[1]) for i in self.population]
        koef = sum(res_affinity) / (self.algconf.popNum - len(self.population))
        filled_fields = 0
        for i in xrange(len(res_affinity)):
            fields = min(int(math.ceil(sum(res_affinity[:i+1])/koef)), self.algconf.cloneNum)
            for j in xrange(fields - filled_fields):
                self.population.append(copy.deepcopy(self.population[i]))
            filled_fields = fields
            if filled_fields >= self.algconf.cloneNum:
                break
        self.population.sort(key=lambda x: x[1], reverse=True)

    def __MappingFunction(self, x):
        # Here I eval function, that maps value x onto new value, this function is used in Cloning to make dependence
        # between chance of cloning and systems affinity

        # users function self.algconf.mapFunc must use variable "x" and can use any functions from math
        return eval(self.algconf.mapFunc)

    def _RecalulatePopulationAffinities(self):
        for i in xrange(len(self.population)):
            self.population[i][1] = self._ComputeSystemAffinity(self.population[i][0])

    def _ComputeSystemAffinity(self, system):
        cost = system.cost - system.constraints[0].limitCost
        return system.rel / ((cost if cost >= 0 else 0) + 1)

    def _Mutate(self):
        # This function is used for some random mutation in the system
        # It is copied from the initial GA.py algorithm implementation and is available to be reused if specification of
        # your algorithm does not describe algorithm especially in itself
        # There is 2 important variables in here (forgot about other things)
        #   1) self.algconf.mutPercent - number of systems in populations that is needed to be mutated (it is nuber
        #       from 0 to 1 - probability)
        #   2) self.algconf.Pmut - probability of mutation in the system (it is computed for every system that is
        #       chosed after first parameter)

        # Code patched for affenity
        for s, aff in self.population[int((1.0-self.algconf.mutPercent) * self.algconf.popNum):]:
            if random.random() <= self.algconf.Pmut:
                k = random.randint(0, Module.conf.modNum-1)
                #if self.currentIter > 500 and self.currentSolution[0] == None:
                #    type = "none"
                #else:
                #    type = random.choice(Module.conf.modules[k].tools)
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
                # patched
                aff = self._ComputeSystemAffinity(s)

    def _Recombine(self):
        # This function is used for some random recombination for some random pairs of the system (mixturing in other words)
        # It is copied from the initial GA.py algorithm implementation and is available to be reused if specification of
        # your algorithm does not describe algorithm especially in itself
        # There is 2 important variables in here (forgot about other things)
        #   1) self.algconf.crossPercent - probability (0 to 1) that indicates number of system in population that is
        #       going to be recombined
        #   2) self.algconf.Pcross - probability of been recombined for each picked pair

        # Code patched for affenity
        if Module.conf.modNum == 1:
            return
        new_pop = []
        notCrossNum = int((1.0 - self.algconf.crossPercent) * self.algconf.popNum)
        for i in range(notCrossNum):
            new_pop.append(copy.deepcopy(self.population[i]))
        for i in range(self.algconf.popNum/2):
            if random.random() <= self.algconf.Pcross:
                #patched
                parents = random.sample(self.population,  2)
                parent1 = parents[0][0]
                parent2 = parents[1][0]
                k = random.randint(1, Module.conf.modNum-1)
                child1 = parent1.modules[0:k] + parent2.modules[k:Module.conf.modNum]
                child2 = parent2.modules[0:k] + parent1.modules[k:Module.conf.modNum]
                parent1.modules = child1
                parent2.modules = child2
                parent1.Update()
                parents[0][1] = self._ComputeSystemAffinity(parent1)
                parent2.Update()
                parents[1][1] = self._ComputeSystemAffinity(parent2)
        self.population.sort(key=lambda x: x[1], reverse=True)
        new_pop += self.population[:self.algconf.popNum - notCrossNum]
        self.population = new_pop
        self.population.sort(key=lambda x: x[1], reverse=True)

    def _EvalPopulation(self):
        # This function reselect currentSolution if we found system with better reliability
        self.currentIter += 1
        self.iterWithoutChange += 1
        if self.population[0][0].CheckConstraints() and \
                (self.currentSolution == None or self.population[0][0].rel > self.currentSolution[0].rel):
            self.currentSolution = copy.deepcopy(self.population[0])
            self.iterWithoutChange = 0

    def _CheckStopCondition(self):
        # This function is used to check the condition for stop iterations in algorithm
        # It is copied from the initial GA.py algorithm implementation and is available to be reused if specification of
        # your algorithm does not describe algorithm especially in itself
        # There is 1 important variable in here:
        #   1) self.algconf.maxIterWithoutChange - number of maximum iterations without improvement of the currentSolution
        #   2) self.algconf.maxIter - number of maximum iterations in the algorithm
        # By default there is implemented threshold = 1000 for maximum iterations in the algorithm (to prevent cycling)
        # If we hit threshold of max iterations and there is still no currentSolution then we will generaty random system
        # and return it as an answer

        if (self.currentSolution != None and self.iterWithoutChange > self.algconf.maxIterWithoutChange) or \
           (self.currentIter >= self.algconf.maxIter):
            self.currentSolution[0].Update(use_metamodel=False)
            if self.currentSolution[0].CheckConstraints():
                return True

        if self.currentSolution == None and self.iterWithoutChange >= self.algconf.maxIterWithoutChange:
            self.currentSolution[0] = System()
            self.currentSolution[1] = self._ComputeSystemAffinity(self.currentSolution[0])
            self.currentSolution[0].rel = 0
            for m in Module.conf.modules:
                self.currentSolution[0].modules.append(NONE(m.num))
            return True
        return False
