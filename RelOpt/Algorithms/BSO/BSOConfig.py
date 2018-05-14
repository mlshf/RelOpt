from Common.AlgConfig import AlgConfig
from Common.StopCondition import StopCondition
from Common.SysConfig import ModConfig, SysConfig
from Common.Module import Module

class BSOConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)
        self.nagents = 40 #number of population
        self.f_min = 0 #minimal frequency
        self.f_max = 2 #maximal frequency
        self.a_0 = 1 #initial loudness
        self.a_min = 0 #final loudness
        self.alpha = 0.9 #loudness parameter
        self.gamma = 0.9 #pulse rate parameter
        self.r_0 = 0.75 #initial pulse rate (value selected randomly!!!!!!!!!!!!!!!! check it)
        self.maxIter = StopCondition.maxIter #stop contition is maximal number of iterations