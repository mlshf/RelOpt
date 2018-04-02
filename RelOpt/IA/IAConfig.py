__author__ = 'avasilenko'

from Common.AlgConfig import AlgConfig

class IAParameter:
    def __init__(self, min, norm, max):
        self.min = min
        self.norm = norm
        self.max = max
        self.cur = norm


class IAConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)

        # Number of systems in population
        self.popNum = 30
        # Threshold that is the minimal difference between different systems
        self.identicalThreshold = 0.001
        # Number of systems in populations that is selected as best systems
        self.selectionBest = 25
        # Function (python code, that must be able to be evaled) - this is function that dictates dependence between affinity of the system
        # and its cloning koefficient
        self.mapFunc = "x"

        # number of maximum iterations without improvement of the currentSolution
        self.maxIterWithoutChange = 1500
        # number of maximum iterations without improving the currentSolution
        self.maxIter = 10000
        # number of maximum clones that can be made at one time
        self.cloneNum = 10

        # number of systems in populations that is needed to be mutated (it is nuber from 0 to 1 - probability)
        self.mutPercent = 0.8
        # probability of mutation in the system (it is computed for every system that is chosed after first parameter)
        self.Pmut = 0.75
        # probability (0 to 1) that indicates number of system in population that is going to be recombined
        self.crossPercent = 0.8
        # probability of been recombined for each picked pair
        self.Pcross = 0.75

    def LoadFromXmlNode(self, node):
        AlgConfig.LoadFromXmlNode(self,node)
        try:
            self.popNum = int(node.getAttribute("popNum"))
            self.identicalThreshold = float(node.getAttribute("identicalThreshold"))
            self.selectionBest = int(node.getAttribute("selectionBest"))
            self.mapFunc = node.getAttribute("mapFunc")
            self.maxIter = int(node.getAttribute("maxIter"))
            self.maxIterWithoutChange = int(node.getAttribute("maxIterWithoutChange"))
            self.mutPercent = float(node.getAttribute("mutPercent"))
            self.Pmut = float(node.getAttribute("Pmut"))
            self.crossPercent = float(node.getAttribute("crossPercent"))
            self.Pcross = float(node.getAttribute("Pcross"))
            self.cloneNum = int(node.getAttribute("cloneNum"))
        except ValueError as e:
            print "Algorithm properties loading failed."