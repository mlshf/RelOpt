__author__ = 'A'
from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
from Common.Constraints import CostConstraints
import random, copy, time

import reliability_pymodule as rel

class BranchBound(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self.task = None
        self.algo = None
        self.currentSolution = None

    def Prep(self):
        self.currentSolution = System()

        self.task = rel.ReliabilityTask()
        for c in self.currentSolution.constraints:
            if isinstance(c, CostConstraints):
                self.task.maxCost = c.limitCost
        pm = []
        for mod in Module.conf.modules:
            m = rel.Module(len(mod.hw), len(mod.sw))

            m.qrv = mod.qrv
            m.qd = mod.qd
            m.qall = mod.qall

            hws = []
            for i in range(len(mod.hw)):
                hws.append(rel.ModuleComponent(mod.hw[i].rel, mod.hw[i].cost))
            m.hw = hws
            sws = []
            for i in range(len(mod.sw)):
                sws.append(rel.ModuleComponent(mod.sw[i].rel, mod.sw[i].cost))
            m.sw = sws
            for tool in mod.tools:
                if tool == 'none':
                    m.addSelector(rel.FaultTolerantSelectors.SELECTOR_NONE)
                if tool == 'nvp01':
                    m.addSelector(rel.FaultTolerantSelectors.SELECTOR_NVP01)
                if tool == 'nvp11':
                    m.addSelector(rel.FaultTolerantSelectors.SELECTOR_NVP11)
                if tool == 'rb11':
                    m.addSelector(rel.FaultTolerantSelectors.SELECTOR_RB11)
            pm.append(m)
        self.task.modules = pm

    def Step(self):
        self.algo.step()

    def Run(self):
        self.Clear()
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        Algorithm.time = time.time()
        self.Prep()
        for c in self.currentSolution.constraints:
            if isinstance(c, CostConstraints):
                self.task.maxCost = c.limitCost
        rel.xrand()
        self.algo = rel.Algorithm(rel.ALGORITHM.BRANCHBOUNDFAST, self.task)
        self.algo.run()
        solution = str(self.algo.solution)
        solution = solution.split('\n')
        mds = len(self.task.modules)
        solution = solution[mds:2*mds]
        
        for i in range(len(solution)):
            tool,p = solution[i].split(':')
            hw,sw = p.split(';')
            hw = hw.split(',')
            sw = sw.split(',')
            hw = [int(q) for q in hw]
            sw = [int(q) for q in sw]
            if tool == 'none':
                self.currentSolution.modules.append(NONE(Module.conf.modules[i].num, hw, sw))
            if tool == 'nvp01':
                self.currentSolution.modules.append(NVP01(Module.conf.modules[i].num, hw, sw))
            if tool == 'nvp11':
                self.currentSolution.modules.append(NVP11(Module.conf.modules[i].num, hw, sw))
            if tool == 'rb11':
                self.currentSolution.modules.append(RB11(Module.conf.modules[i].num, hw, sw))
            print(tool, hw, sw)
        self.currentSolution.Update()
        print "Best solution: ", self.currentSolution
        print "--------------------------------------\n"
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(self.currentSolution, self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))
        self.Clear()

    def Clear(self):
        Algorithm.Clear(self)
