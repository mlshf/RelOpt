from Common.AlgConfig import AlgConfig
from Common.StopCondition import StopCondition
from Common.SysConfig import ModConfig, SysConfig
from Common.Module import Module

class BAConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)
        self.nagents = 40 #number of sources
        self.limit = 10 #abandonment parameter
        self.onlookers = 80 #number of onlookers
        self.maxIter = StopCondition.maxIter #stop contition is maximal number of iterations