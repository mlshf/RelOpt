import math

class Penalty:
    def __init__(self):
        #self.type = 1
        #self.power = 1
        pass

    def getPenalty(self, currVal, maxVal):
        if self.type==0: #exp
            return math.exp(float(maxVal - currVal) / maxVal)
        elif self.type==1: #Logarithm
            return (math.log(1 + float(maxVal) / currVal))
        elif self.type==2: #power
            return math.pow(float(maxVal) / currVal, self.power)
        elif self.type==3: #none
            return 1.0
