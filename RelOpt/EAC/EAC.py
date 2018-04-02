__author__ = 'Sergey Lavrushkin'

from Common.Algorithm import Algorithm
from Common.System import System
from Common.Module import Module, NONE
from Common.Statistics import Execution
import random
import copy
import time

# class for subsystem representation in tree(array)
class SubsystemTree:
    # calculate heuristic information with function F1 * F2
    def HeuristicFunc1(self, rel, cost):
        return rel * cost

    # calculate heuristic information with average(F1, F2)
    def HeuristicFunc2(self, rel, cost):
        return (rel + cost) / 2.0

    # calculate heuristic information with function min(F1, F2)
    def HeuristicFunc3(self, rel, cost):
        return min(rel, cost)

    # calculate heuristic information with function max(F1, F2)
    def HeuristicFunc4(self, rel, cost):
        return max(rel, cost)

    # calculate heuristic information
    def CalculateHeuristic(self, heuristic_func, prior_func):
        calc_heur = None
        if heuristic_func == 1:
            calc_heur = self.HeuristicFunc1
        elif heuristic_func == 2:
            calc_heur = self.HeuristicFunc2
        elif heuristic_func == 3:
            calc_heur = self.HeuristicFunc3
        elif heuristic_func == 4:
            calc_heur = self.HeuristicFunc4

        # calculate base for the priority grade calculation according to reliability
        rel_prior_grade_base = [comp.rel / self.rel_sum for comp in self.comps]
        # calculate base for the priority grade calculation according to cost
        cost_prior_grade_base = [(1.0 / comp.cost) / self.rcost_sum for comp in self.comps]

        # calculate priority grade according to reliability and cost
        rel_prior_grade = None
        cost_prior_grade = None
        if prior_func == 1:
            rel_prior_grade = copy.deepcopy(rel_prior_grade_base)
            cost_prior_grade = copy.deepcopy(cost_prior_grade_base)
        else:
            # sort bases for the priority grade calculation
            sort_rel_prior_grade_base = sorted(rel_prior_grade_base, reverse=True)
            sort_cost_prior_grade_base = sorted(cost_prior_grade_base, reverse=True)

            # calculate the rank of components according to their reliability and cost
            rank_rel = [sort_rel_prior_grade_base.index(prior) + 1 for prior in rel_prior_grade_base]
            rank_cost = [sort_cost_prior_grade_base.index(prior) + 1 for prior in cost_prior_grade_base]

            if prior_func == 2:
                rel_prior_grade = [(len(rank_rel) + 1.0 - rank) / len(rank_rel) for rank in rank_rel]
                cost_prior_grade = [(len(rank_cost) + 1.0 - rank) / len(rank_cost) for rank in rank_cost]
            elif prior_func == 3:
                rel_prior_grade = [1.0 / rank for rank in rank_rel]
                cost_prior_grade = [1.0 / rank for rank in rank_cost]

        # calculate heuristic information
        self.heuristic = [calc_heur(rel_prior_grade[comp], cost_prior_grade[comp]) for comp in xrange(len(self.comps))]


    def __init__(self, comps, tau0, beta, use_heuristic, heuristic_func, prior_func):
        # hardware and software components
        self.comps = comps
        # parameter denoting the relative importance of the heuristic information versus the pheromone trail
        self.beta = beta

        # amount of pheromone on edges to appropriate components
        self.pheromone = [tau0 for comp in xrange(len(self.comps))]

        # components reliability sum
        self.rel_sum = float(sum([comp.rel for comp in self.comps]))
        # components reverse cost sum
        self.rcost_sum = float(sum([1.0 / comp.cost for comp in self.comps]))

        # calculate heuristic information
        if use_heuristic:
            self.CalculateHeuristic(heuristic_func, prior_func)

        # calculate edge scores and probabilities
        self.UpdateEdges(use_heuristic)

    # update edge scores and probabilities
    def UpdateEdges(self, use_heuristic):
        # calculate edge scores
        if use_heuristic:
            self.edge_score = [self.pheromone[comp] * (self.heuristic[comp] ** self.beta)
                               for comp in xrange(len(self.comps))]
        else:
            self.edge_score = [self.pheromone[comp] for comp in xrange(len(self.comps))]
        # calculate sum of edge scores
        self.score_sum = float(sum(self.edge_score))
        # calculate probability distribution on edges
        self.edge_probability = [self.edge_score[comp] / self.score_sum for comp in xrange(len(self.comps))]

# class for solution representation
class Solution:
    def __init__(self):
        self.choosen_comps = [0 for subsystems in xrange(2 * len(Module.conf.modules))]

    # calculate current solution cost
    def CalculateCost(self, subsystems_tree):
        cost = 0
        for subsystem in xrange(len(subsystems_tree)):
            cost += subsystems_tree[subsystem].comps[self.choosen_comps[subsystem]].cost

        return cost

    # calculate current solution reliability
    def CalculateRel(self, subsystems_tree):
        rel = 1.0
        for subsystem in xrange(len(subsystems_tree)):
            rel *= subsystems_tree[subsystem].comps[self.choosen_comps[subsystem]].rel

        return rel

class EAC(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)

        # tree of all available subsystems
        self.subsystems_tree = []
        # cost constraint
        self.cost_limit = 0
        for cls in System.constraints:
            if cls.__class__.__name__ == "CostConstraints":
                self.cost_limit = cls.limitCost
                break
        # best solution
        self.best_solution = None

    # prepare data for algorithm
    def PrepareData(self):
        # calculate z parameter
        # S - number of subsystems, hardware and software parts counts as two subsystems
        if self.algconf.z_equation == "S/2":
            self.algconf.z = len(Module.conf.modules)
        elif self.algconf.z_equation == "S":
            self.algconf.z = 2 * len(Module.conf.modules)
        else:
            self.algconf.z = 0

        # construct tree of subsystems
        for subsystem_num in xrange(len(Module.conf.modules)):
            self.subsystems_tree.append(SubsystemTree(Module.conf.modules[subsystem_num].sw, self.algconf.tau0,
                                                      self.algconf.beta, self.algconf.use_heuristic,
                                                      self.algconf.heuristic_func, self.algconf.prior_func))
            self.subsystems_tree.append(SubsystemTree(Module.conf.modules[subsystem_num].hw, self.algconf.tau0,
                                                      self.algconf.beta, self.algconf.use_heuristic,
                                                      self.algconf.heuristic_func, self.algconf.prior_func))

    # choose the best component for which the product between the pheromone trail
    # and the heuristic information is maximum
    def ChooseBestComp(self, subsystem):
        return subsystem.edge_score.index(max(subsystem.edge_score))

    # select a component according to the probability distribution
    def SelectCompAccordingProbability(self, subsystem):
        probability_intervals = [sum(subsystem.edge_probability[:index + 1]) for index in xrange(len(subsystem.edge_probability))]
        probability_intervals[-1] = 1.0
        choice = random.random()
        for index in xrange(len(probability_intervals)):
            if choice < probability_intervals[index]:
                return index

    # construct initial solution
    def ConstructSolution(self):
        solution = Solution()
        for subsystem in xrange(len(self.subsystems_tree)):
            if (random.random() < self.algconf.q0):
                # choose the best component for which the product between the pheromone trail
                # and the heuristic information is maximum
                solution.choosen_comps[subsystem] = self.ChooseBestComp(self.subsystems_tree[subsystem])
            else:
                # select a component according to the probability distribution
                solution.choosen_comps[subsystem] = self.SelectCompAccordingProbability(self.subsystems_tree[subsystem])

        return solution

    # if solution is infeasible, make it feasible
    def MakeSolutionFeasible(self, solution):
        while solution.CalculateCost(self.subsystems_tree) > self.cost_limit:
            # choose random subsystem
            choosen_subsystem = random.randint(0, len(self.subsystems_tree) - 1)
            # replace current component with component that has
            # the highest reliability among all of the components which
            # have smaller cost than the current one
            best_rel = -1
            best_component = 0
            for comp in xrange(len(self.subsystems_tree[choosen_subsystem].comps)):
                if (self.subsystems_tree[choosen_subsystem].comps[comp].cost <
                    self.subsystems_tree[choosen_subsystem].comps[solution.choosen_comps[choosen_subsystem]].cost) \
                   and (self.subsystems_tree[choosen_subsystem].comps[comp].rel > best_rel):
                    best_rel = self.subsystems_tree[choosen_subsystem].comps[comp].rel
                    best_component = comp
            if best_rel != -1:
                solution.choosen_comps[choosen_subsystem] = best_component

    # performs local search in order to find a better solution
    def LocalSearch(self, solution):
        step_counter = 0
        while (solution.CalculateCost(self.subsystems_tree) != self.cost_limit):
            # choose random subsystem
            choosen_subsystem = random.randint(0, len(self.subsystems_tree) - 1)
            best_rel = -1
            best_component = 0
            # try to find better component
            for comp in xrange(len(self.subsystems_tree[choosen_subsystem].comps)):
                if (self.subsystems_tree[choosen_subsystem].comps[comp].rel >
                    self.subsystems_tree[choosen_subsystem].comps[solution.choosen_comps[choosen_subsystem]].rel) and \
                   ((self.subsystems_tree[choosen_subsystem].comps[comp].cost -
                     self.subsystems_tree[choosen_subsystem].comps[solution.choosen_comps[choosen_subsystem]].cost)
                    <= (self.cost_limit - solution.CalculateCost(self.subsystems_tree))) and \
                   (self.subsystems_tree[choosen_subsystem].comps[comp].rel > best_rel):
                    best_rel = self.subsystems_tree[choosen_subsystem].comps[comp].rel
                    best_component = comp
            if best_rel != -1:
                solution.choosen_comps[choosen_subsystem] = best_component
            else:
                if step_counter % 2 == 1:
                    break
            step_counter += 1

    # update pheromone trails according to the local updating rule
    def PheromoneLocalUpdate(self, solution):
        for index in xrange(len(solution.choosen_comps)):
            self.subsystems_tree[index].pheromone[solution.choosen_comps[index]] = (1.0 - self.algconf.rho_dash) * \
                                                self.subsystems_tree[index].pheromone[solution.choosen_comps[index]] + \
                                                self.algconf.rho_dash * self.algconf.tau0
            self.subsystems_tree[index].UpdateEdges(self.algconf.use_heuristic)

    # update pheromone trails according to the global updating rule
    def PheromoneGlobalUpdate(self, best_solution):
        update_coef = best_solution.CalculateRel(self.subsystems_tree) / best_solution.CalculateCost(self.subsystems_tree)
        for index in xrange(len(best_solution.choosen_comps)):
            self.subsystems_tree[index].pheromone[best_solution.choosen_comps[index]] = (1.0 - self.algconf.rho) * \
                                            self.subsystems_tree[index].pheromone[best_solution.choosen_comps[index]] + \
                                            self.algconf.rho * self.algconf.z * update_coef
            self.subsystems_tree[index].UpdateEdges(self.algconf.use_heuristic)

    def Step(self):
        # construct solution for each ant in colony
        for ant in xrange(self.algconf.ant_size):
            # construct initial solution, it can be infeasible
            solution = self.ConstructSolution()
            # make constructed solution feasible
            self.MakeSolutionFeasible(solution)
            # perform local search for better solution
            if self.algconf.use_local_search:
                self.LocalSearch(solution)
            # update pheromone trails according to the local updating rule
            self.PheromoneLocalUpdate(solution)
            # choose best solution
            if (self.best_solution == None) or \
               (self.best_solution.CalculateRel(self.subsystems_tree) < solution.CalculateRel(self.subsystems_tree)):
                self.best_solution = copy.deepcopy(solution)
        self.PheromoneGlobalUpdate(self.best_solution)

    def ConstructCurrentSolutionSystem(self):
        self.currentSolution = System()
        for mod_num in range(Module.conf.modNum):
            sol_sw = self.best_solution.choosen_comps[2 * mod_num]
            sol_hw = self.best_solution.choosen_comps[2 * mod_num + 1]
            self.currentSolution.modules.append(NONE(mod_num, [sol_hw], [sol_sw]))
        self.currentSolution.Update()


    def Run(self):
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        Algorithm.time = time.time()

        self.PrepareData()

        for iter in xrange(self.algconf.max_iter):
            self.Step()

            self.ConstructCurrentSolutionSystem()
            print "Iteration: ", iter + 1, "-- Current solution: ", self.currentSolution

        print "--------------------------------------"
        print "Best solution: ", self.currentSolution
        print "--------------------------------------\n"

        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(self.currentSolution, self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))

        self.Clear()

    def Clear(self):
        Algorithm.Clear(self)
        self.subsystems_tree = []
        self.best_solution = None