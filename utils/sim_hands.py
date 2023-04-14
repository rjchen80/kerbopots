"""
Hands simulator.

Simulating hands for a given number of players.
"""
import random as rnd

class PokerHand:
    def __init__(self,hands,flop=None,turn=None,river=None):
        self.hands = hands
        self.flop = flop
        self.turn = turn
        self.river = river

def sim_hands(numPlayers, numIters=1):
    ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suits = ['d','s','h','c']

    numRanks = len(ranks)
    numSuits = len(suits)

    # numPlayers = 2
    pokerHands = []
    for n in range(numIters):
        selected = []
        hands = []
        preflop = ""
        flop = ""
        turn = ""
        river = ""
        for player in range(numPlayers):
            hand = ""
            for i in range(2):
                while True:
                    rankId = rnd.randrange(numRanks)
                    suitId = rnd.randrange(numSuits)
                    if (rankId, suitId) not in selected:
                        selected.append((rankId, suitId))
                        hand = hand + ranks[rankId] + suits[suitId]
                        break
            hands.append(hand)
        for i in range(3):
            while True:
                rankId = rnd.randrange(numRanks)
                suitId = rnd.randrange(numSuits)
                if (rankId, suitId) not in selected:
                    selected.append((rankId, suitId))
                    flop = flop + ranks[rankId] + suits[suitId]
                    break
        while True:
            rankId = rnd.randrange(numRanks)
            suitId = rnd.randrange(numSuits)
            if (rankId, suitId) not in selected:
                selected.append((rankId, suitId))
                turn = flop + ranks[rankId] + suits[suitId]
                break
        while True:
            rankId = rnd.randrange(numRanks)
            suitId = rnd.randrange(numSuits)
            if (rankId, suitId) not in selected:
                selected.append((rankId, suitId))
                river = turn + ranks[rankId] + suits[suitId]
                break
        # pokerHands.append(PokerHand(hands,flop,turn,river))
        pokerHands = hands + [river]
    return pokerHands

if __name__ == '__main__':
    numPlayers = 3
    numSim = 200000
    fh = open('sim_hands_3p_3.csv','w')
    for i in range(numSim):
        if i%10000 == 0:
            print i
        h = sim_hands(numPlayers, 1)
        for j in range(numPlayers):
            fh.write(h[j]+', ')
        fh.write(h[-1]+'\n')
    fh.close()
