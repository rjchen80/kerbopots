import argparse
import socket
import sys
import random
import math
from hand import Hand

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
                done = False
#                discount = 1
#                for raiseEvent in self.hand.raiseHistory:
                equity = self.hand.eval_equity()
#                print equity
                equity_discounts = self.hand.eval_equity_discount()
                discount = 1.0
                for player in self.hand.playerNames:
                    if not player == self.name:
                        neglogx = - math.log(equity_discounts[self.hand.playerNameToId[player]])
                        neglogx = neglogx - self.discountAdjust[player] * neglogx**2 / 64
                        x = math.exp(-neglogx)
                        discount = discount * x
#                if random.random() < 0.5:
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
            self.players = packet_values[1:4]
            self.starting_stack = int(packet_values[4])
            self.big_blind = int(packet_values[5])
            self.num_of_hands = int(packet_values[6])
            self.timebank = float(packet_values[7])
            self.nameAssigned = False
            self.avgLogDiscount = dict({self.players[0]:0.0, self.players[1]:0.0, self.players[2]:0.0})
            self.discountAdjust = dict({self.players[0]:0.0, self.players[1]:0.0, self.players[2]:0.0})
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
