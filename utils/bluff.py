"""
Bluff class.

"""
import pbots_calc as pc
import numpy as np
from numpy import random as rnd

class Bluff:
    def __init__(self,t=20):
        self.raises = np.hstack((np.linspace(0.1,0.9,5),1))
        self.pots = self.raises + 1
        self.call_ratios = self.pots/self.raises
        self.expected_equity = self.pots/(self.pots+self.raises)
        self.average_equity = np.copy(self.expected_equity)
        self.t = t
    
    def ratioToBin(self,call_ratio):
        call = 1.0/(call_ratio-1)
        if np.absolute(call-1) < 1e-5:
            return 5
        else:
            return np.around((call-0.1)*5)

    def addEquity(self,equity,call_ratio):
        id = self.ratioToBin(call_ratio)
        self.average_equity[id] = (self.average_equity[id]*(self.t-1)+equity)/self.t

    def tryBluff(self,equity):
        pmf = np.maximum(0, self.average_equity-self.expected_equity)
        p = np.sum(pmf)
        if p*10 < rnd.uniform():
#            print 'avg:', self.average_equity
#            print 'exp:', self.expected_equity
#            print 'p:', p
            return (False, 0.0)
        else:
            pmf = pmf/p
            id = rnd.choice(6,1,p=pmf)
            id = id[0]
            print 'I am going to bluff, raising to ', self.raises[id], 'potsize with equity ', equity
            print 'avg:', self.average_equity
            print 'exp:', self.expected_equity
            return (True, self.raises[id])

