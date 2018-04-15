import numpy as np
from math import exp

# from Algorithms.SLGA.SLGA import SLGA

# class AdaptiveMethods(SLGA):
 
def adaptate(candidate, new, old, corrMode, corrPar1 = None, corrPar2 = None):
    
        if corrMode == 0:
            absolute(candidate, new, old, corrPar1)
        elif corrMode == 1:
            relative1(candidate, new, old)
        elif corrMode == 2:
            relativeWF1(candidate, new, old, corrPar1)
        elif corrMode == 3:
            relative2(candidate, new, old)
        elif corrMode == 4:
            relativeWF2(candidate, new, old, corrPar1)
        elif corrMode == 5:
            average(candidate, new, old, corrPar1, corrPar2)
        elif corrMode == 6:
            diversity(candidate, new, old, corrPar1)
        elif corrMode == 7:
            disturbance(candidate, new, old, corrPar1)
        elif corrMode == 8:
            survivor(candidate, new, old, corrPar1)
        elif corrMode == 9:
            improved_percent(candidate, new, old, corrPar1)
        elif corrMode == 10:
            deviation(candidate, new, old, corrPar1, corrPar2)
        else:
            iterationsW(candidate, new, old, corrPar1)
            
        if candidate > 0.9:
            candidate = 0.9
        elif candidate < 0.1:
            candidate = 0.1
        
def absolute(candidate, new, old, corrPar1):
    
        df = new.rel - old.rel
        if df > 0:
            candidate -= corrPar1 
        elif df < 0:
            candidate += corrPar1
            
def relative1(candidate, new, old):
    
        candidate += new.rel - old.rel
    
def relativeWF1(candidate, new, old, corrPar1):
    
        candidate = candidate*corrPar1 + new.rel - old.rel
    
def relative2(candidate, new, old):
    
        if old.rel != 0:
            candidate *= new.rel / old.rel
    
def relativeWF2(candidate, new, old, corrPar1):
    
        if old.rel != 0:
            candidate = candidate * corrPar1 * new.rel / old.rel   

def average(candidate, new, avg_r, max_r, corrPar):
    if avg_r <= new.rel:
        candidate = 0.9 - 0.8 / (1 + exp(corrPar*(2*(new.rel - avg_r)/(max_r - avg_r) - 1)))       
    else:
        candidate = 0.9
 
def count_avg(popul):
    rel_list = np.array([i.rel for i in popul])
    return np.std(rel_list)
 
def diversity(candidate, new, old, corrPar1, corrPar2):
    pass

def disturbance(candidate, new, old, corrPar1, corrPar2):
    pass

def survivor(candidate, new, old, corrPar1, corrPar2):
    pass    
           
def improved_percent(candidate, new, old, corrPar1, corrPar2):
    pass
           
def count_variance(popul):
    rel_list = np.array([i.rel for i in popul])
    return np.std(rel_list) / np.mean(rel_list)
    
def deviation(candidate, new, old, corrPar1, corrPar2):
    candidate *= corrPar1 / corrPar2

def iterationsW(candidate, new, old, corrPar1):
    pass
