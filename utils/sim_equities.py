import pbots_calc as pc
from sim_hands import sim_hands
import time
import numpy as np

infilename = 'sim_data/sim_hands_3p_1.csv'
outfilename = 'sim_pf_equities_' + infilename[-8:]
ifh = open(infilename,'r')

numPlayers = 3
numSamples = 100000
startclock = time.clock()
xy_matrix = np.empty([numSamples, numPlayers+1])
i=0
for i in range(numSamples):
    hands = ifh.readline().strip().split(', ')
    if i % 1000 == 1:
        print 'i =', i
    x = []
    rndhands = ""
    for player in range(numPlayers-1):
        rndhands = rndhands + ":xx"
    for player in range(numPlayers):
        #print hands[player]+rndhands
        r = pc.calc(hands[player]+rndhands, "", "", 1000)
        x.append(r.ev[0])
    #print ":".join(hands[:numPlayers])
    r = pc.calc(":".join(hands[:numPlayers]), "", "", 1000)
    x.append(r.ev[0])
    xy_matrix[i,] = np.array(x)
ifh.close()
np.savetxt(outfilename, xy_matrix, fmt = "%.2f", delimiter=",") 

endclock = time.clock()
print 'time elapsed: ', endclock - startclock
