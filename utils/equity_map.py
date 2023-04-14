"""
Equity Map.

Learning a direct map from winning rates against random opponents
to heads-up winning rate.
"""
import pbots_calc as pc
from sim_hands import sim_hands
import time
import numpy as np

ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
suits = ['d','s','h','c']

numRanks = len(ranks)
numSuits = len(suits)

numIters = 200000
numPlayers = 3

startclock = time.clock()
xy_matrix = np.empty([numIters, numPlayers+1])
simulated_hands = sim_hands(numPlayers, numIters)
print 'number of simulated hands: ', numIters
for hand_id, hand in enumerate(simulated_hands):
    if hand_id % 1000 == 1:
        print 'hand_id: ', hand_id
    x = []
    y = []
    rndhands = ""
    for player in range(numPlayers-1):
        rndhands = rndhands + ":xx"
    for player in range(numPlayers):
        r = pc.calc(hand.hands[player]+rndhands, hand.flop, "", 1000)
        x.append(r.ev[0])
    r = pc.calc(":".join(hand.hands), hand.flop, "", 1000)
    y.append(r.ev[0])
    xy_matrix[hand_id,] = np.array(x+y)
np.savetxt("sim3p_equity_4.csv", xy_matrix, delimiter=",") 

endclock = time.clock()
print endclock - startclock


# startclock = time.clock()
# for n in range(numIters):
#     pokerHand = sim_hands(numPlayers)
#     x = []
#     y = []
#     rndhands = ""
#     for player in range(numPlayers-1):
#         rndhands = rndhands + ":xx"
#     for player in range(numPlayers):
#         r = pc.calc(pokerHand[0].hands[player]+rndhands, pokerHand[0].flop, "", 1000)
#         x.append(r.ev[0])
#     r = pc.calc(":".join(pokerHand[0].hands), pokerHand[0].flop, "", 1000)
#     y = r.ev[0]
# 
# endclock = time.clock()
# print endclock - startclock
#    for player in range(numPlayers):
#        print hands[player], x[player]
#    print flop, y

#class Hand:
#    def eval_equity(self):
#        print 'TODO: equity evaluation.'
#        # evaluate unconditional equity
#        opCards = ":xx"
#        if self.numCurrentPlayers == 3:
#            opCards = ":xx:xx"
#        r = pc.calc(self.holeCards[0]+self.holeCards[1]+opCards, "".join(self.boardCards), "", 10000)
#        print r.ev[0]
#        # evaluate zero-order unconditional EV
#        self.equity = r.ev[0]
#        return self.equity
#    def eval_bet(self, p):
#        print 'TODO: unconditional _optimal_ bet according to Kelly Criterion'
#        myStack = self.stackSizes[self.seat-1]
#        print myStack
#        value = (p*self.numCurrentPlayers - 1)/(self.numCurrentPlayers - 1) * myStack
#        return value
#    def eval_call(self, size):
#        print 'TODO: call evaluation'
#        value = self.equity * self.potSize - (1-self.equity) * size
#        return value
##    def eval_raise(self, minRaise, maxRaise):
##        print 'TODO: raise evaluation'
##        p_opFold = 1./3.
##        p_opCall = 1./3.
##        p_opRaise = 1./3.
##        size = minRaise
##        value = p_opFold * self.potSize + \
##                p_opCall * self.equity * (self.potSize + size) -  \
##                p_opRaise * self.equity * (self.potSize + )
##    def eval_bet(self, minBet, maxBet):
##        print 'TODO: bet evaluation'
##        pass
