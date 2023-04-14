import argparse
import socket
import sys
import random
import math
from hand import Hand
from PFPlayer import PFPlayer
from actionHistory import ActionHistory
#import time
"""
Simple and stupid Raisebot, written in python.

This is an example of a bare bones pokerbot. It always raises or bets the minimum amount whenever possible.
If it cannot raise/bet, it seeks to call. If it cannot call, it will check.
Such a stupid pokerbot! But it very often beats Randombot.
"""
class Player:
    def run(self, s):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = s.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            print data

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            self.parse_packet(data)
            word = data.split()[0]
            if word == "GETACTION":                    
                # Currently CHECK on every move. You'll want to change this.
                if self.ah._currentRound == 0:
                    print 'playerFoldActionId', self.ah.playerFoldActionId
                    print self.ah._activePlayers
                    effplayers = []
                    for i in range(3):
                        effplayers.append(self.ah.playerFoldActionId[i]==None and self.ah._activePlayers[i])
                    print effplayers
                    nump = sum(effplayers)
                    equity_nump = self.hand.eval_equity_nump(nump)
                    # if there is bet/raise
                    if self.ah._hasBRThisRound:
                        done = False
                        raisepriors = [[1.0/3], [1.0/4, 1.0/8]] # [[initial raise], [raised raise, raised twice reraise]]
                        minweight = 5
                        # collect player preflop raise data
                        raiselist = []
                        raiseplayers = []
                        for (aid, x) in enumerate(self.ah.handActionHistory):
                            if x[2] == 'RAISE' or x[2] == 'BET':
                                cond = 1
                                if x[0] not in raiseplayers:
                                    raiseplayers.append(x[0])
                                else:
                                    cond = 2
                                raiselist.append(x+[aid, cond])
                                print 'retrieve raise record + [aid, cond]', x, [aid, cond]
                        raiselist[0][-1] = 0
                        i = 1
                        opraiselevel = []
                        while i<3 and i<=len(raiselist):
                            print 'raiselist[], reversed entries', i, raiselist[-i]
                            if raiselist[-i][0] == self.name:
                                break
                            query_name = raiselist[-i][0]
                            if not raiselist[-i][-1] == 2:
                                query_cond = [raiselist[-i][-1]]
                                query_res = self.ah.recentActionAverage(query_name, [0], query_cond, 2, 15, numRetrace=100)
                                print 'query name, condition, response', query_name, query_cond, query_res
                                if sum(query_res) >= minweight:
                                    opraiselevel.append(1 - 1.0*query_res[0]/query_res[1])
                                else:
                                    obsweight = sum(query_res)
                                    priorweight = minweight-obsweight
                                    opraiselevel.append(1 - (query_res[0]+priorweight*raisepriors[query_cond[0]][0])/(query_res[1]+priorweight))
                                print 'op raise quantile', opraiselevel
                            else:
                                query_cond = [1,2]
                                query_res = self.ah.recentActionAverage(query_name,[0],query_cond, 2, 15, numRetrace=1000)
                                print 'query name, condition2, response2', query_name, query_cond, query_res
                                if sum(query_res) >= minweight:
                                    opraiselevel.append(1 - 1.0*query_res[0]/query_res[1])
                                else:
                                    obsweight = sum(query_res)
                                    priorweight = minweight-obsweight
                                    opraiselevel.append(1 - (query_res[0]+priorweight*raisepriors[1][1])/(query_res[1]+priorweight))
                                print 'op raise quantile', opraiselevel
                            i+=1
                        pillar = max(opraiselevel)
                        uppercallbound = pillar + (1-pillar)/2.0
                        lowercallbound = max(0, max(pillar - 0.1, pillar - (1-pillar)/4.0))
                        print 'pillar, uppercallbound, lowercallbound', pillar, uppercallbound, lowercallbound
                        uppereqbound = self.pfp.pfidist(nump, [uppercallbound])
                        lowereqbound = self.pfp.pfidist(nump, [lowercallbound])
                        print 'uppereqbound, lowereqbound', uppereqbound, lowereqbound
                        print 'my equity, number of people', equity_nump, nump
                        if equity_nump >= uppereqbound:
                            print 'Decided to Reraise, above uppereqbound'
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'RAISE' or a[0] == 'BET':
                                    print a
                                    raisemax = int(a[2])
                                    raisemin = int(a[1])
                                    raiseamount = int(round(random.gauss(raisemax-1, 1)))
                                    raiseamount = max(raisemin, min(raiseamount, raisemax))
                                    print a[0]+":"+str(raiseamount)+"\n"
                                    s.send(a[0]+":"+str(raiseamount)+"\n")
                                    done = True
                                    self.hand.bet = int(a[1])
                                    self.hand.pfpState = (1,2)
                                    break
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'CALL' and not done:
                                    print action+"\n"
                                    s.send(action+"\n")
                                    done = True
                                    self.hand.bet = int(a[1])
                                    self.hand.pfpState = (1,1)
                                    break
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'CHECK' and not done:
                                    done = True
                                    s.send("CHECK\n")
                                    self.hand.pfpState = (1,1)
                            if not done:
                                s.send("FOLD\n")
                                self.hand.pfpState = (1,0)
                        elif equity_nump >= lowereqbound:
                            print 'Decided to call, above lowereqbound.'
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'CALL' and not done:
                                    print action+"\n"
                                    s.send(action+"\n")
                                    done = True
                                    self.hand.bet = int(a[1])
                                    self.hand.pfpState = (1,1)
                                    break
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'CHECK' and not done:
                                    done = True
                                    s.send("CHECK\n")
                                    self.hand.pfpState = (1,1)
                            if not done:
                                s.send("FOLD\n")
                                self.hand.pfpState = (1,0)
                        else:
                            print 'Decided to fold, below lowereqbound'
                            s.send("FOLD\n")
                            self.hand.pfpState = (1,0)
                    # if there is no initial raise
                    else:
                        done = False
                        # retrieve opponent statistics: [pf raised raise, pf raised fold, pf init raise]
                        mypriors = [1.0/4, 1.0/3, 1.0/3] # [raised raise, raised fold, init raise]
                        minweight = 8.0
                        opstats = dict()
                        for p in self.players:
                            if (not p == self.name) and effplayers[self.hand.playerNameToId[p]]:
                                if p not in opstats:
                                    opstats[p] = []
                                qres = self.ah.recentActionAverage(p, [0], [1], 2, 20, numRetrace=200)
                                if sum(qres)<minweight:
                                    obsweight = sum(qres)
                                    priorweight = minweight - obsweight
                                else:
                                    priorweight = 0.0
                                opstats[p].append((qres[0]+1.0*priorweight*mypriors[0])/(qres[1]+priorweight))
                                qres = self.ah.recentActionAverage(p, [0], [1], 0, 20, numRetrace=200)
                                if sum(qres)<minweight:
                                    obsweight = sum(qres)
                                    priorweight = minweight - obsweight
                                else:
                                    priorweight = 0.0
                                opstats[p].append((qres[0]+1.0*priorweight*mypriors[1])/(qres[1]+priorweight))
                                qres = self.ah.recentActionAverage(p, [0], [0], 2, 20, numRetrace=200)
                                if sum(qres)<minweight:
                                    obsweight = sum(qres)
                                    priorweight = minweight - obsweight
                                else:
                                    priorweight = 0.0
                                opstats[p].append((qres[0]+1.0*priorweight*mypriors[2])/(qres[1]+priorweight))
                        assert(len(opstats.keys())==nump-1)
                        print 'no initial raise, opstats', opstats
                        # set blind initial raise params
                        ppratio = []
                        rrlevel = []
                        irlevel = []
                        for k in opstats.keys():
                            ppratio.append(opstats[k][1]/(opstats[k][0]+0.00001))
                            rrlevel.append(opstats[k][0])
                            irlevel.append(opstats[k][2])
                        ppratio = max(ppratio)
                        rrlevel = 1 - min(rrlevel)
                        irlevel = 1 - min(irlevel)
                        if ppratio > 2.2:
                            self.pfp.irsp_3p = [0.4, 1.0, 0.25, 0.45]
                            self.pfp.irsp_2p = [0.4, 1.0, 0.38, 0.62]
                        else:
                            k3 = self.pfp.pfidist(3, [rrlevel])
                            self.pfp.irsp_3p = [min((1-k3)/k3, 0.5), 1.0,k3-0.01,k3]
                            k2 = self.pfp.pfidist(2, [rrlevel])
                            self.pfp.irsp_2p = [min((1-k2)/k2, 0.5), 1.0,k2-0.01,k2]
                        # set decide not to blind init raise params
                        self.pfp.noir_3p = [self.pfp.pfidist(3, [irlevel/2.0]), self.pfp.pfidist(3, [irlevel])]
                        self.pfp.noir_2p = [self.pfp.pfidist(2, [irlevel/2.0]), self.pfp.pfidist(2, [irlevel])]
                        
                        p_pfp = self.pfp.irsp(nump, equity_nump)
                        print 'p_pfp', p_pfp
                        # decide to blind initial raise
                        if random.uniform(0,1) < p_pfp:
                            print 'Decided to blind initial raise'
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'RAISE' or a[0] == 'BET':
                                    print a
                                    raisemax = int(a[2])
                                    raisemin = int(a[1])
                                    raiseamount = int(round(random.gauss(raisemax-1, 1)))
                                    raiseamount = max(raisemin, min(raiseamount, raisemax))
                                    print a[0]+":"+str(raiseamount)+"\n"
                                    s.send(a[0]+":"+str(raiseamount)+"\n")
                                    done = True
                                    self.hand.bet = int(a[1])
                                    self.hand.pfpState = (0,2)
                                    break
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'CALL' and not done:
                                    print action+"\n"
                                    s.send(action+"\n")
                                    done = True
                                    self.hand.bet = int(a[1])
                                    self.hand.pfpState = (0,1)
                                    break
                            for action in self.hand.legalActions:
                                a = action.split(':')
                                if a[0] == 'CHECK' and not done:
                                    done = True
                                    s.send("CHECK\n")
                                    self.hand.pfpState = (0,1)
                            if not done:
                                s.send("FOLD\n")
                                self.hand.pfpState = (0,0)
                        # decide not to blind initial raise
                        else:
                            print self.hand.legalActions
                            print done
                            print 'Decided NOT to blind initial raise'
                            if nump == 3:
                                k2 = self.pfp.noir_3p[1]
                                k1 = self.pfp.noir_3p[0]
                            else:
                                k2 = self.pfp.noir_3p[1]
                                k1 = self.pfp.noir_3p[0]
                            if equity_nump >= k2:
                                for action in self.hand.legalActions:
                                    a = action.split(':')
                                    if a[0] == 'RAISE' or a[0] == 'BET':
                                        print a
                                        raisemax = int(a[2])
                                        raisemin = int(a[1])
                                        raiseamount = int(round(random.gauss(raisemax-1, 1)))
                                        raiseamount = max(raisemin, min(raiseamount, raisemax))
                                        print a[0]+":"+str(raiseamount)+"\n"
                                        s.send(a[0]+":"+str(raiseamount)+"\n")
                                        done = True
                                        self.hand.bet = int(a[1])
                                        self.hand.pfpState = (0,2)
                                        break
                                for action in self.hand.legalActions:
                                    a = action.split(':')
                                    if a[0] == 'CALL' and not done:
                                        print action+"\n"
                                        s.send(action+"\n")
                                        done = True
                                        self.hand.bet = int(a[1])
                                        self.hand.pfpState = (0,1)
                                        break
                                for action in self.hand.legalActions:
                                    a = action.split(':')
                                    if a[0] == 'CHECK' and not done:
                                        done = True
                                        s.send("CHECK\n")
                                        self.hand.pfpState = (0,1)
                                if not done:
                                    s.send("FOLD\n")
                                    self.hand.pfpState = (0,0)

                            elif equity_nump >= k1:
                                for action in self.hand.legalActions:
                                    a = action.split(':')
                                    if a[0] == 'CALL' and not done:
                                        print action+"\n"
                                        s.send(action+"\n")
                                        done = True
                                        self.hand.bet = int(a[1])
                                        self.hand.pfpState = (0,1)
                                        break
                                for action in self.hand.legalActions:
                                    a = action.split(':')
                                    if a[0] == 'CHECK' and not done:
                                        done = True
                                        s.send("CHECK\n")
                                        self.hand.pfpState = (0,1)
                                if not done:
                                    s.send("FOLD\n")
                                    self.hand.pfpState = (0,0)
                            else:
                                for action in self.hand.legalActions:
                                    a = action.split(':')
                                    if a[0] == 'CHECK' and not done:
                                        done = True
                                        s.send("CHECK\n")
                                        self.hand.pfpState = (0,1)
                                if not done:
                                    s.send("FOLD\n")
                                    self.hand.pfpState = (0,0)
                else:
                    done = False
#                    discount = 1
#                    for raiseEvent in self.hand.raiseHistory:
                    equity = self.hand.eval_equity()
#                    print equity
                    equity_discounts = self.hand.eval_equity_discount()
                    discount = 1.0
                    for player in self.hand.playerNames:
                        if not player == self.name:
                            neglogx = - math.log(equity_discounts[self.hand.playerNameToId[player]])
                            neglogx = neglogx - self.discountAdjust[player] * neglogx**2 / 64
                            x = math.exp(-neglogx)
                            discount = discount * x
#                    if random.random() < 0.5:
                    equity = max(0.0, equity + (1-equity) * discount + math.log(discount)/25)**2 * equity
                    print equity, equity_discounts
                    betvalue = self.hand.eval_bet(equity)
                    for action in self.hand.legalActions:
                        a = action.split(':')
                        if a[0] == 'RAISE':
                            for dummy in self.hand.legalActions:
                                b = dummy.split(':')
                                if b[0] == 'CALL' and betvalue + int(b[1]) >= int(a[1]):
                                    done = True
                                    betvalue = random.gauss(betvalue,1)
                                    totalbet = max(int(a[1]), min(int(betvalue)+int(b[1]),int(a[2])))
                                    s.send("RAISE:"+str(totalbet)+"\n")
                                    self.hand.bet = totalbet
                                    break
                    for action in self.hand.legalActions:
                        a = action.split(':')
                        if a[0] == 'BET' and not done and betvalue >= int(a[1]):
                            done = True
                            if self.hand.isFirstInAction:
                                betvalue = 2
                            else:
                                betvalue = random.gauss(betvalue,1)
                            totalbet = max(int(a[1]), min(int(betvalue),int(a[2])))
                            s.send("BET:"+str(totalbet)+"\n")
                            self.hand.bet = totalbet
                            break
                    for action in self.hand.legalActions:
                        a = action.split(':')
                        if a[0] == 'CALL' and not done:
                            callvalue = self.hand.eval_call(int(a[1])-self.hand.bet, equity)
                            if callvalue >= 0:
                                done = True
                                s.send(action+"\n")
                                self.hand.bet = int(a[1])
                                break
                    for action in self.hand.legalActions:
                        a = action.split(':')
                        if a[0] == 'CHECK' and not done:
                            done = True
                            s.send("CHECK\n")
                    if not done:
                        s.send("FOLD\n")
            elif word == "HANDOVER" and self.hand.activePlayers[self.hand.playerNameToId[self.name]]:
                equity_discounts = self.hand.eval_equity_discount()
                for player in self.hand.playerNames:
                    if not player == self.name:
                        neglogx = - math.log(equity_discounts[self.hand.playerNameToId[player]])
                        neglogx = neglogx - self.discountAdjust[player] * neglogx**2 / 64
                        x = math.exp(-neglogx)
                for player in self.hand.playerNames:
                    avgLogDiscount = self.avgLogDiscount[player]
                    neglogx = - math.log(equity_discounts[self.hand.playerNameToId[player]])
                    neglogx = neglogx - self.discountAdjust[player] * neglogx**2 / 64
                    self.avgLogDiscount[player] = ((min(self.hand.handId,100)-1)*avgLogDiscount - neglogx) / min(self.hand.handId,100)
                    if not player == self.name:
                        self.discountAdjust[player] = self.discountAdjust[player] + (self.avgLogDiscount[self.name]-self.avgLogDiscount[player])*3.0/(self.hand.handId+50)
                print self.avgLogDiscount
                print self.discountAdjust
                    
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        input_socket.close()
    def parse_packet(self, data):
        packet_values = data.split(' ')
        if packet_values[0] == 'NEWGAME':
            self.ah = ActionHistory()
        self.ah.updateActionHistory(packet_values)
        if packet_values[0] == 'NEWGAME':
            self.players = packet_values[1:4]
            self.starting_stack = int(packet_values[4])
            self.big_blind = int(packet_values[5])
            self.num_of_hands = int(packet_values[6])
            self.timebank = float(packet_values[7])
            self.nameAssigned = False
            self.avgLogDiscount = dict({self.players[0]:0.0, self.players[1]:0.0, self.players[2]:0.0})
            self.discountAdjust = dict({self.players[0]:0.0, self.players[1]:0.0, self.players[2]:0.0})
            self.pfp = PFPlayer()
        elif packet_values[0] == 'NEWHAND':
            self.hand = Hand()
            self.hand.bet = 0
            self.hand.numBoardCards = 0
            self.hand.handId = int(packet_values[1])
            self.hand.seat = int(packet_values[2])
            self.hand.holeCards = packet_values[3:5]
            self.hand.stackSizes = [int(packet_values[5]), int(packet_values[6]), int(packet_values[7])]
            self.hand.startingStackSizes = self.hand.stackSizes
            self.hand.playerNames = [packet_values[8], packet_values[9], packet_values[10]]
            self.hand.playerNameToId = dict()
            for i in range(3):
                self.hand.playerNameToId[self.hand.playerNames[i]] = i
            if not self.nameAssigned:
                self.name = self.hand.playerNames[self.hand.seat-1]
                
                self.nameAssigned = True
            else:
                for seat in range(len(self.hand.playerNames)):
                    if self.hand.playerNames[seat] == self.name:
                        self.hand.seat = seat + 1
                        break
            self.hand.numActivePlayers = int(packet_values[11])
            self.hand.activePlayers = map(lambda x: x=='true', packet_values[12:15])
            self.hand.timebank = float(packet_values[15])
            self.hand.actions = []
            self.hand.numCurrentPlayers = self.hand.numActivePlayers
            self.hand.raiseHistory = []
            self.hand.myname = self.name
            self.hand.pfpDecided = False
        elif packet_values[0] == 'GETACTION':
            self.hand.potSize = int(packet_values[1])
            if self.hand.numBoardCards < int(packet_values[2]):
                self.hand.numBoardCards = int(packet_values[2])
                self.hand.bet = 0
            offset = int(packet_values[2]) + 3
            self.hand.boardCards = packet_values[3:offset]
            self.hand.stackSizes = [int(packet_values[offset]), int(packet_values[offset+1]), int(packet_values[offset+2])]
            self.hand.numActivePlayers = int(packet_values[offset+3])
            self.hand.activePlayers = packet_values[offset+4:offset+7]
            self.hand.numLastActions = int(packet_values[offset+7])
            offset = offset+8
            self.hand.lastActions = packet_values[offset:offset+self.hand.numLastActions]
            for action in self.hand.lastActions:
                a = action.split(':')
                if a[0] == 'FOLD':
                    self.hand.numCurrentPlayers = self.hand.numCurrentPlayers - 1
                if a[0] == 'POST' and a[2] == self.name:
                    self.hand.bet = int(a[1])
#            for action in self.hand.lastActions:
#                a = action.split(':')
#                if a[0] == 'BET' and not a[2] == self.name:
#                    
#            for action in self.hand.lastActions:
#                a = action.split(':')
#                if a[0] == 'RAISE' and not a[2] == self.name:
#                    for pid in range(len(self.hand.playerNames)):
#                        if self.hand.playerNames[pid] == a[2]:
#                            stack = self.hand.stackSizes[pid]
#                            break
#                    self.hand.raiseHistory.append([stack, int(a[1])])
            self.hand.actions = self.hand.actions + self.hand.lastActions
            offset = offset+self.hand.numLastActions
            self.hand.numLegalActions = int(packet_values[offset])
            offset = offset + 1
            self.hand.legalActions = packet_values[offset:offset+self.hand.numLegalActions]
            offset = offset+self.hand.numLegalActions
            self.hand.timebank = float(packet_values[offset])
        elif packet_values[0] == 'HANDOVER':
            self.hand.stackSizes = [int(packet_values[1]), int(packet_values[2]), int(packet_values[3])]
            self.hand.numBoardCards = int(packet_values[4])
            self.hand.boardCards = packet_values[5:5+self.hand.numBoardCards]
            offset = 5+self.hand.numBoardCards
            self.hand.numLastActions = int(packet_values[offset])
            offset = offset + 1
            self.hand.lastActions = packet_values[offset:offset+self.hand.numLastActions]
            self.hand.actions = self.hand.actions + self.hand.lastActions
            self.hand.timebank = float(packet_values[offset+self.hand.numLastActions])
        elif packet_values[0] == 'REQUESTKEYVALUES':
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        input_socket = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(input_socket)
