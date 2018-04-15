__author__ = 'Sergey Lavrushkin'

from Common.AlgConfig import AlgConfig

class EACConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)

    def LoadFromXmlNode(self, node):
        AlgConfig.LoadFromXmlNode(self,node)
        # number of iterations
        self.max_iter = int(node.getAttribute("max_iter"))
        # ant colony size
        self.ant_size = int(node.getAttribute("ant_size"))
        # probability to select technology for which the product between the pheromone trail
        # and the heuristic information is maximum
        self.q0 = float(node.getAttribute("q0"))
        # parameter denoting the relative importance of the heuristic information versus the pheromone trail
        self.beta = float(node.getAttribute("beta"))
        # local pheromone trail evaporation rate
        self.rho = float(node.getAttribute("rho"))
        # global pheromone trail evaporation rate
        self.rho_dash = float(node.getAttribute("rho_dash"))
        # parameter for global pheromone trail updating calculation
        self.z_equation = node.getAttribute("z")
        self.z = 0
        # initial value of the pheromone trails
        self.tau0 = float(node.getAttribute("tau0"))
        # parameter stores True if local search is used
        self.use_local_search = bool(int(node.getAttribute("use_local_search")))
        # parameter stores True if heuristic information is used
        self.use_heuristic = bool(int(node.getAttribute("use_heuristic")))
        # parameter defines function used to calculate heuristic information
        self.heuristic_func = int(node.getAttribute("heuristic_function"))
        if not ((1 <= self.heuristic_func) and (self.heuristic_func <= 4)):
            self.heuristic_func = 3
        # parameter defines function used to calculate priority grade for reliability and cost
        self.prior_func = int(node.getAttribute("priority_grade_function"))
        if not ((1 <= self.heuristic_func) and (self.heuristic_func <= 3)):
            self.prior_func = 1