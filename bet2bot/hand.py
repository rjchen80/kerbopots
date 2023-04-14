"""
Hand class.

Storing relevant information within a hand.
Evaluating equity and expected value of actions.
Making decisions.
"""
import pbots_calc as pc
import math

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
    def eval_call(self, size, equity):
        print 'TODO: call evaluation'
        value = equity * self.potSize - (1-equity) * size
        return value
    def eval_equity_discount(self):
        stackSizes = list(self.startingStackSizes)
        myId = self.playerNameToId[self.myname]
        potSize = 3
        bets = [0.0, 0.0, 0.0]
        equity_discounts = [1,1,1]
        self.isFirstInAction = False
        for action in self.actions:
            a = action.split(":")
            if a[0] == "DEAL":
                bets = [0.0, 0.0, 0.0]
                self.isFirstInAction = True
            if a[0] == "POST":
                id = self.playerNameToId[a[2]]
                bets[id] = bets[id] + float(a[1])
                stackSizes[id] = stackSizes[id] - bets[id]
                lastbet = 2.0
            if a[0] == "CHECK":
                id = self.playerNameToId[a[1]]
                equity_discounts[id] = equity_discounts[id]*1.05
            if a[0] == "CALL":
                id = self.playerNameToId[a[2]]
                callvalue = float(a[1])-bets[id]
                try:
                    callratio = callvalue/stackSizes[id]
                except ValueError:
                    print self.actions
                stackSizes[id] = stackSizes[id] - callvalue
                potSize = potSize + callvalue
                discount = 1 / (1+math.log(callvalue+1) * callratio)
                bets[id] = float(a[1])
                equity_discounts[id] = equity_discounts[id]*discount
            if a[0] == "RAISE":
                id = self.playerNameToId[a[2]]
                callvalue = lastbet-bets[id]
                raisevalue = float(a[1])-bets[id]
                if stackSizes[id]-callvalue == 0 or stackSizes[id] == 0:
                    print self.actions
                    print self.startingStackSizes
                    print stackSizes
                try:
                    raiseratio = (raisevalue-callvalue)/(stackSizes[id]-callvalue+1e-5)*2 + callvalue/stackSizes[id] + (raisevalue-callvalue)/potSize + (raisevalue-callvalue)*2/(stackSizes[myId]+1e-5)
                except ValueError:
                    print self.actions
                stackSizes[id] = stackSizes[id] - raisevalue
                potSize = potSize + raisevalue
                discount = 1 / (1+math.log(raisevalue)  * raiseratio)
                bets[id] = float(a[1])
                equity_discounts[id] = equity_discounts[id]*discount
                lastbet = bets[id]
            if a[0] == "BET":
                id = self.playerNameToId[a[2]]
                betvalue = float(a[1])
                if stackSizes[id] == 0:
                    print self.actions
                    print self.startingStackSizes
                    print stackSizes
                try:
                    betratio = betvalue / stackSizes[id] + betvalue / potSize + betvalue*2 / (stackSizes[myId]+1e-5)
                except ValueError:
                    print self.actions
                stackSizes[id] = stackSizes[id] - betvalue
                potSize = potSize + betvalue
                discount = 1 / (1+math.log(betvalue) * betratio)
                equity_discounts[id] = equity_discounts[id]*discount
                bets[id] = float(a[1])
                lastbet = bets[id]
                self.isFirstInAction = False
            if a[0] == "FOLD":
                id = self.playerNameToId[a[1]]
                equity_discounts[id] = 1.0
        return equity_discounts


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
