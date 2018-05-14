from Common.AlgConfig import AlgConfig
from Common.StopCondition import StopCondition
from PSO import Velocity
from Common.SysConfig import ModConfig, SysConfig
from Common.Module import Module

class PSOConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)
        self.nagents = 40
        self.w = 0.9
        self.w_min = 0.4
        self.w_max = 0.9
        self.alpha1 = 2.05
        self.alpha2 = 2.05
        self._init_v_max()
        self.maxIter = StopCondition.maxIter

    def _init_v_max(self):
        maxhw = 0
        maxsw = 0
        for i in Module.conf.modules:
            hwl = len(i.hw)
            swl = len(i.sw)
            if maxhw < hwl:
                maxhw = hwl
            if maxsw < swl:
                maxsw = swl

        self.v_max = Velocity()
        self.v_max.hw = [int(round(maxhw*0.45)) for i in range(3)]
        self.v_max.sw = [int(round(maxsw*0.45)) for i in range(3)]
        print "PSO: v_max.hw = ", [self.v_max.hw[i] for i in range(3)]
        print "PSO: v_max.sw = ", [self.v_max.sw[i] for i in range(3)]

    def LoadFromXmlNode(self, node):
        pass

        '''
           
        nagents = 0 #parameter: number of agents
        w = 0 #parameter
        rnd1, rnd2 = 0, 0 #parameters
        alpha1, alpha2 = 0, 0 #parameters
        v_min = 0 #parameter: minimal velocity
        v_max = 0 #parameter: maximal velocity
        '''