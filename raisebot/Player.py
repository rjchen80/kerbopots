import argparse
import socket
import sys
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
                for action in self.hand.legalActions:
                    a = action.split(':')
                    if a[0] == 'RAISE' and not done:
                        done = True
                        s.send("RAISE:"+a[1]+"\n")
                        break
                for action in self.hand.legalActions:
                    a = action.split(':')
                    if a[0] == 'BET' and not done:
                        done = True
                        s.send("BET:"+a[1]+"\n")
                        break
                for action in self.hand.legalActions:
                    a = action.split(':')
                    if a[0] == 'CALL' and not done:
                        done = True
                        s.send(action+"\n")
                if done == False:
                    print self.hand.legalActions
                    s.send("CHECK\n")
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
        elif packet_values[0] == 'NEWHAND':
            self.hand = Hand()
            self.hand.handId = int(packet_values[1])
            self.hand.seat = int(packet_values[2])
            self.hand.holeCards = packet_values[3:5]
            self.hand.stackSizes = [int(packet_values[5]), int(packet_values[6]), int(packet_values[7])]
            self.hand.playerNames = [packet_values[8], packet_values[9], packet_values[10]]
            self.hand.numActivePlayers = int(packet_values[11])
            self.hand.activePlayers = packet_values[12:15]
            self.hand.timebank = float(packet_values[15])
            self.hand.actions = []
        elif packet_values[0] == 'GETACTION':
            self.hand.potSize = int(packet_values[1])
            self.hand.numBoardCards = int(packet_values[2])
            offset = int(packet_values[2]) + 3
            self.hand.boardCards = packet_values[3:offset]
            self.hand.stackSizes = [int(packet_values[offset]), int(packet_values[offset+1]), int(packet_values[offset+2])]
            self.hand.numActivePlayers = int(packet_values[offset+3])
            self.hand.activePlayers = packet_values[offset+4:offset+7]
            self.hand.numLastActions = int(packet_values[offset+7])
            offset = offset+8
            self.hand.lastActions = packet_values[offset:offset+self.hand.numLastActions]
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
