"""
Hand class.

Storing relevant information within a hand.
Evaluating equity and expected value of actions.
Making decisions.
"""
import pbots_calc as pc

class Hand:
    def eval_equity(self):
        print 'TODO: equity evaluation.'
        # evaluate unconditional equity
        opCards = ":xx"
        if self.numCurrentPlayers == 3:
            opCards = ":xx:xx"
        r = pc.calc(self.holeCards[0]+self.holeCards[1]+opCards, "".join(self.boardCards), "", 10000)
        print r.ev[0]
        # evaluate zero-order unconditional EV
        self.equity = r.ev[0]
        return self.equity
    def eval_bet(self, p):
        print 'TODO: unconditional _optimal_ bet according to Kelly Criterion'
        myStack = self.stackSizes[self.seat-1]
        print myStack
        value = (p*self.numCurrentPlayers - 1)/(self.numCurrentPlayers - 1) * myStack
        return value
    def eval_call(self, size):
        print 'TODO: call evaluation'
        value = self.equity * self.potSize - (1-self.equity) * size
        return value
#    def eval_raise(self, minRaise, maxRaise):
#        print 'TODO: raise evaluation'
#        p_opFold = 1./3.
#        p_opCall = 1./3.
#        p_opRaise = 1./3.
#        size = minRaise
#        value = p_opFold * self.potSize + \
#                p_opCall * self.equity * (self.potSize + size) -  \
#                p_opRaise * self.equity * (self.potSize + )
#    def eval_bet(self, minBet, maxBet):
#        print 'TODO: bet evaluation'
#        pass
