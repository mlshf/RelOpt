from Common.AlgConfig import AlgConfig
from Common.StopCondition import StopCondition
from Common.SysConfig import ModConfig, SysConfig
from Common.Module import Module

class FAConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)
        self.nagents = 40 #number of population
        self.gamma = 0.1 #absorption coefficient
        self.alpha = 1.0 #randomization parameter
        self.betta = 1.0 #attractiveness at r = 0
        self.maxIter = StopCondition.maxIter #stop contition is maximal number of iterations