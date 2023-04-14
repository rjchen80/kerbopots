import csv
import pbots_calc as pc
from sets import Set
import os

##features include: numbers: #fold_before_flop %, 
#fold_before_turn %, #fold_before_river, #fold_before_showdown %, 
#win_at_showdown %, etc. histograms: winning_pot_size, losing_pot_size, comparing betting behavior with other top bots

# read = open('../casino/Casino_Day-2_kerbopots_p1/Casino_Day-2_kerbopots_vs_TheHouse_vs_OGRoomies.txt', 'r')
# write = open('basichistory.csv', 'wb')
# wr = csv.writer(write, quoting=csv.QUOTE_ALL)
CHIPS = 200

AllPlayers = {}

class GameFeatures:
    def __init__(self):
        self.players = Set()
        self.stackSize = 0
        self.toPlay = 0
        self.board = ""
        self.flop = False
        self.turn = False
        self.river = False
        self.showdown = False
        self.rank = 3
    def reset(self):
        self.stackSize = 0
        self.toPlay = 0
        self.board = ""
        self.flop = False
        self.turn = False
        self.river = False
        self.showdown = False

class Guy:
    def __init__(self, name, card1 = None, card2 = None):
        self.name = name
        self.playing = True
        self.card1 = card1
        self.card2 = card2
        self.chips = CHIPS
        self.bet = 0
        self.current = 0
        self.foldBeforeFlop = 0
        self.foldOnFlop = 0
        self.foldOnTurn = 0
        self.foldOnRiver = 0
        self.totalGames = 0
        self.wins = 0
        self.losses = 0

        self.firsts = 0
        self.seconds = 0
        self.thirds = 0
        self.ranked = False

        self.flops = 0
        self.turns = 0
        self.rivers = 0

        self.wins_at_showdown = 0
        self.showdowns = 0
        self.winning_pot_size = []
    def __str__(self):
        return self.name + ", Total Games: " + str(self.totalGames) + ". Win%: " +str(float(self.wins)/self.totalGames) +", Fold% preFlop: " + str(float(self.foldBeforeFlop) / self.totalGames) + \
        ", Fold% On Flop: " + str(float(self.foldOnFlop) / self.flops) + ", Fold% On Turn: " + str(float(self.foldOnTurn) / self.turns) + \
        ", Fold% On River: " + str(float(self.foldOnRiver) / self.rivers) + ". Flops, Turns, Rivers: " + str(self.flops) + ", " + str(self.turns) + ", " + str(self.rivers) + \
        ", Average win pot: " + str(self.getAverageWin()) + ", Max pot won: " + str(max(self.winning_pot_size))
        # return self.name + ": foldBeforeFlop: " + str(self.foldBeforeFlop) + ", foldOnFlop: " + str(self.foldOnFlop) + \
        # ", foldOnTurn: " + str(self.foldOnTurn) + ", foldOnRiver: " + str(self.foldOnRiver) + ", Total Games: " + str(self.totalGames) + \
        # ", Total Wins: " + str(self.wins) + ": " + str(self.winning_pot_size)
    def getAverageWin(self):
        value = float(sum(self.winning_pot_size)) / float(len(self.winning_pot_size))
        return value
    def resetRank(self):
        self.ranked = False

def analyzeGame(filename):
    read = open(filename, 'r')

    gameFeatures = GameFeatures()
    for name, player in AllPlayers.items():
        player.resetRank()

    for line in read:
        if 'Hand #' in line:
            ## New hand
            ## Analyze old results and reset
            gameFeatures.reset()



            elements = line.split()
            gameFeatures.players.add(elements[2])
            gameFeatures.players.add(elements[4])
            gameFeatures.players.add(elements[6])
            if elements[2] not in AllPlayers:
                AllPlayers[elements[2]] = Guy(elements[2])
            if elements[4] not in AllPlayers:
                AllPlayers[elements[4]] = Guy(elements[4])
            if elements[6] not in AllPlayers:
                AllPlayers[elements[6]] = Guy(elements[6])
            
            # Check whether have any chips left, if so playing this game
            for player in gameFeatures.players:
                AllPlayers[player].playing = True

            if elements[3] == '(0),':
                AllPlayers[elements[2]].playing = False
                if AllPlayers[elements[2]].ranked == False:
                    if gameFeatures.rank == 3:
                        AllPlayers[elements[2]].thirds += 1
                    elif gameFeatures.rank == 2:
                        AllPlayers[elements[2]].seconds += 1
                    gameFeatures.rank -=1
                    AllPlayers[elements[2]].ranked = True
            
            if elements[5] == '(0),':
                AllPlayers[elements[4]].playing = False
                if AllPlayers[elements[4]].ranked == False:
                    if gameFeatures.rank == 3:
                        AllPlayers[elements[4]].thirds += 1
                    elif gameFeatures.rank == 2:
                        AllPlayers[elements[4]].seconds += 1
                    gameFeatures.rank -=1
                    AllPlayers[elements[4]].ranked = True
            if elements[7] == '(0)':
                AllPlayers[elements[6]].playing = False
                if AllPlayers[elements[6]].ranked == False:
                    if gameFeatures.rank == 3:
                        AllPlayers[elements[6]].thirds += 1
                    elif gameFeatures.rank == 2:
                        AllPlayers[elements[6]].seconds += 1
                    gameFeatures.rank -=1
                    AllPlayers[elements[6]].ranked = True

            if AllPlayers[elements[2]].playing:
                AllPlayers[elements[2]].totalGames += 1
            if AllPlayers[elements[4]].playing:
                AllPlayers[elements[4]].totalGames += 1
            if AllPlayers[elements[6]].playing:
                AllPlayers[elements[6]].totalGames += 1

        elif ' folds' in line:
            elements = line.split()
            name = elements[0]
            if gameFeatures.flop == False:
                AllPlayers[name].foldBeforeFlop += 1
            elif gameFeatures.turn == False:
                AllPlayers[name].foldOnFlop += 1
            elif gameFeatures.river == False:
                AllPlayers[name].foldOnTurn += 1
            elif gameFeatures.river == True:
                AllPlayers[name].foldOnRiver += 1
            AllPlayers[name].losses += 1
            AllPlayers[name].playing = False

        elif '*** FLOP ***' in line:
            gameFeatures.flop = True
            for player in gameFeatures.players:
                if AllPlayers[player].playing:
                    AllPlayers[player].flops += 1

        elif '*** TURN ***' in line:
            gameFeatures.turn = True
            for player in gameFeatures.players:
                if AllPlayers[player].playing:
                    AllPlayers[player].turns += 1
        elif '*** RIVER ***' in line:
            gameFeatures.river = True
            for player in gameFeatures.players:
                if AllPlayers[player].playing:
                    AllPlayers[player].rivers += 1
        elif ' shows ' in line:
            elements = line.split()
            name = elements[0]
            gameFeatures.showdown = True
            AllPlayers[name].showdowns += 1

        elif ' wins the pot' in line:
            elements = line.split()
            name = elements[0]
            stack = elements[4][1:-1]

            AllPlayers[name].wins += 1
            AllPlayers[name].winning_pot_size.append(int(stack))

            if gameFeatures.showdown == True:
                AllPlayers[name].wins_at_showdown += 1

    array = []
    read.close()
    for results in reversed(list(open(filename, 'r'))):
        if ' wins the pot' in results:
            elements = results.split()
            name = elements[0]
            money = int(elements[-1][1:-1])
            array.append([name, money])
        elif 'Hand #' in results:
            elements = results.split()
            p1 = elements[2]
            p2 = elements[4]
            p3 = elements[6]

            m1 = int(elements[3][1:-2])
            m2 = int(elements[5][1:-2])
            m3 = int(elements[7][1:-1])

            for [name, money] in array:
                if p1 == name:
                    m1 += money
                elif p2 == name:
                    m2 += money
                elif p3 == name:
                    m3 += money
            
            x = max(m1, m2, m3)
            y = min(m1, m2, m3)
            if x == m1:
                if AllPlayers[p1].ranked == False:
                    AllPlayers[p1].firsts += 1
                    AllPlayers[p1].ranked = True
            if x == m2:
                if AllPlayers[p2].ranked == False:
                    AllPlayers[p2].firsts += 1
                    AllPlayers[p2].ranked = True
            if x == m3:
                if AllPlayers[p3].ranked == False:
                    AllPlayers[p3].firsts += 1
                    AllPlayers[p3].ranked = True

            rank = gameFeatures.rank
            if rank == 3:
                if y == m1:
                    if AllPlayers[p1].ranked == False:
                        AllPlayers[p1].thirds += 1
                        AllPlayers[p1].ranked = True
                if y == m2:
                    if AllPlayers[p2].ranked == False:
                        AllPlayers[p2].thirds += 1
                        AllPlayers[p2].ranked = True
                if y == m3:
                    if AllPlayers[p3].ranked == False:
                        AllPlayers[p3].thirds += 1
                        AllPlayers[p3].ranked = True
            elif rank == 2:
                if y == m1:
                    if AllPlayers[p1].ranked == False:
                        AllPlayers[p1].seconds += 1
                        AllPlayers[p1].ranked = True
                if y == m2:
                    if AllPlayers[p2].ranked == False:
                        AllPlayers[p2].seconds += 1
                        AllPlayers[p2].ranked = True
                if y == m3:
                    if AllPlayers[p3].ranked == False:
                        AllPlayers[p3].seconds += 1
                        AllPlayers[p3].ranked = True


            if (x != m1) and (y != m1):
                if AllPlayers[p1].ranked == False:
                        AllPlayers[p1].seconds += 1
                        AllPlayers[p1].ranked = True
            if (x != m2) and (y != m2):
                if AllPlayers[p2].ranked == False:
                        AllPlayers[p2].seconds += 1
                        AllPlayers[p2].ranked = True
            if (x != m3) and (y != m3):
                if AllPlayers[p3].ranked == False:
                        AllPlayers[p3].seconds += 1
                        AllPlayers[p3].ranked = True

            break


    read.close()

def writeResults(filename):
    write = open(filename, 'wb')

    wr = csv.writer(write, quoting = csv.QUOTE_ALL)
    headers = 'Name,Total Games,Win%,Fold% PreFlop,Fold% On Flop,Fold% On Turn,Fold% On River,Win% On Showdown,AVERAGE Stack Won,MAX pot won, Total #1s, Total #2s, Total #3s\n'
    
    write.write(headers)

    for keys, players in AllPlayers.items():
        # print players
        stats = [players.name, players.totalGames, float(players.wins)/players.totalGames, players.foldBeforeFlop/float(players.totalGames),
            players.foldOnFlop / float(players.flops), players.foldOnTurn / float(players.turns), 
            players.foldOnRiver / float(players.rivers), players.wins_at_showdown / float(players.showdowns), 
            players.getAverageWin(), max(players.winning_pot_size), players.firsts, players.seconds, players.thirds]
        wr.writerow(stats)
    write.close()


files = open('files.txt', 'r')
root = '../casino/'


for day in [8]:
    directory = 'Casino_Day-' + str(day) + '/hand_history/'
    for position in [5, 6]:
        seat = 'Casino_Day-' + str(day) + '_kerbopots_p' + str(position) + '/'

        for file in os.listdir(root + directory + seat):
            file = file.strip()
            analyzeGame(root + directory + seat + file)


# directory2 = 'self-data/handhistory'
# analyzeGame(root + directory2 + '.txt')

# for i in [2, 3, 4, 5, 6]:
#     analyzeGame(root + directory2 + str(i) + '.txt')
# reader = open(root + 'Casino_Day-2_kerbopots_vs_TheHouse_vs_OGRoomies.txt', 'r')
# analyzeGame('../casino/Casino_Day-2_kerbopots_p1/Casino_Day-2_kerbopots_vs_TheHouse_vs_OGRoomies.txt')

writeResults('basichistoryDay7CheckBot.csv')







# class Game:
#     def __init__(self):
#         self.players = []
#         self.stackSize = 0
#         self.toPlay = 0
#         self.board = ""
#         self.flop = False
#         self.turn = False
#         self.river = False
#     def setPlayer(self, name, position, game, card1 = None, card2 = None):
#         self.players.append(Guy(name, position, game, card1, card2))
#     def getPlayers(self):
#         return self.players
#     def getNumPlayers(self):
#         return len(self.players)
#     def increaseStack(self, num):
#         self.stackSize += num
#     def getToPlay(self):
#         return self.toPlay
#     def setToPlay(self, num):
#         self.toPlay = num
#     def getBoard(self):
#         return self.board
#     def setBoard(self, string):
#         self.board += string
#     def reset(self):
#         self.board = ""
#         self.flop = False
#         self.turn = False
#         self.river = False
#         self.toPlay = 0
#         self.stackSize = 0
#         for player in self.getPlayers():
#             player.reset()

# game = Game()

# class Guy:
#     def __init__(self, name, position, game, card1 = None, card2 = None):
#         self.name = name
#         self.card1 = card1
#         self.card2 = card2
#         self.position = position
#         self.chips = CHIPS
#         self.bet = 0
#         self.game = game
#         self.current = 0
#         self.foldBeforeFlop = 0
#         self.foldOnFlop = 0
#         self.foldOnTurn = 0
#         self.foldOnRiver = 0
#     def setCards(self, card1, card2):
#         self.card1 = card1
#         self.card2 = card2
#     def getEquity(self, num_players, board):
#         rndhands = ""
#         for ps in range(num_players-1):
#             rndhands = rndhands + ":xx"
#         return pc.calc(self.card1+self.card2+rndhands, board, "", 1000).ev[0]
#     def bets(self, num):
#         self.bet += num
#         self.chips -= num
#         self.game.increaseStack(num)
#     def reasonable(self):
#         # print self.getEquity(self.game.getNumPlayers(), self.game.getBoard()), self.bet / self.game.stackSize
#         equity = float(self.getEquity(self.game.getNumPlayers(), self.game.getBoard()))

#         # Expectation negative
#         expectation = equity * self.game.stackSize - (1.0 - equity) * self.bet
#         # print equity, expectation
#         if expectation < 0:
#         # board = float(self.bet) / float(self.game.stackSize)
#         # if (equity < board):
#             print equity, expectation, self.bet, self.game.stackSize
#             print self.name + " made an irrational decision by zerobot standards"
#         return
#     def reset(self):
#         self.card1 = None
#         self.card2 = None
#         self.bet = 0
#         self.current = 0
#     def __str__(self):
#         return self.name+ ": " + self.card1 + self.card2 + str(self.position)



# playerHands = []
# numPlayers = 3
# position = 0
# current = 0


# game = Game()
    

# for line in read:
#     # print line

#     if 'Hand #' in line:
#         game.reset()
#         position = 0
#         for player in game.getPlayers():
#             player.current = 0

#         playerHands = []
#         numPlayers = 3

#         write.write("\n")
#         elements = line.split()
#         elements[1] = elements[1][:-1]
#         elements[3] = elements[3][1:-2]
#         elements[5] = elements[5][1:-2]
#         elements[7] = elements[7][1:-1]
#         part1 = elements[:2]
#         part2 = elements[2:]
#         wr.writerow(part1)
#         wr.writerow(part2)
#         # print elements
#     elif 'Dealt to' in line:
#         elements = line.split()
#         name = elements[2]
#         card1 = elements[3][1:]
#         card2 = elements[4][:-1]
#         array = [name, card1, card2]

#         ## See whether we've initialized the player, if so just add cards
#         found = False
#         index = -1
#         for i in range(len(game.getPlayers())):
#             if game.getPlayers()[i].name == name:
#                 game.getPlayers()[i].setCards(card1, card2)
#                 found = True
#                 index = i
#                 break


#         p = Guy(name, position, game, card1, card2)
#         playerHands.append(p)
        
#         ## This is the case where the player has not been initialized
#         if not found:
#             game.setPlayer(name, position, game, card1, card2)
#             position += 1
        
#         equity = game.players[index].getEquity(3, "")
#         # print name, equity

#         rndhands = ""
#         for ps in range(numPlayers-1):
#             rndhands = rndhands + ":xx"
#         r = pc.calc(p.card1+p.card2+rndhands, "", "", 1000)
#         # print playerHands
#         # print name, card1, card2
#         array.append(r.ev[0])
#         wr.writerow(array)
#     elif 'posts the blind of ' in line:
#         elements = line.split()
#         game.setPlayer(elements[0], position, game)
#         value = int(elements[-1])

#         game.getPlayers()[-1].bets(value)
#         game.getPlayers()[-1].current = value
#         game.setToPlay(max(game.getToPlay(), value))
#         write.write(line)
#     elif ' folds' in line:
#         elements = line.split()
#         for i in range(len(game.getPlayers())):
#             if elements[0] == game.getPlayers()[i].name:
#                 del game.players[i]
#                 break
#         write.write(line)
#     elif (' bets' in line) or (' calls' in line) or (' checks' in line):
#         elements = line.split()
#         if 'checks' in elements:
#             name = elements[0]

#             # for player in game.getPlayers():
#                 # if player.name == name:
#                     # player.reasonable()
#             #         print game.getToPlay(), player.bet, game.stackSize
#             #         player.bets(game.getToPlay() - player.bet)
#             #         print line, game.getToPlay(), player.bet, game.stackSize
#             #         break
#         elif 'calls' in elements:
#             name = elements[0]
#             value = int(elements[2])
#             for player in game.getPlayers():
#                 if player.name == name:
#                     # amount = value - player.bet
#                     player.bets(value - player.current)
#                     player.current = value
#                     game.setToPlay(max(player.bet, game.getToPlay()))
#                     player.reasonable()
#                     # print line, player.bet, game.stackSize
#                     break
#         elif 'bets' in elements:
#             name = elements[0]
#             value = int(elements[2])
#             for player in game.getPlayers():
#                 if player.name == name:
#                     player.bets(value - player.current)
#                     player.current = value
#                     game.setToPlay(max(player.bet, game.getToPlay()))
#                     player.reasonable()
                        
#                     # print line, player.bet, game.stackSize
#                     break
#         write.write(line)
#     elif ' raise' in line:
#         elements = line.split()
#         name = elements[0]
#         amount = int(elements[3])
#         for player in game.getPlayers():
#             if player.name == name:
#                 player.bets(amount - player.current)
#                 player.current = amount
#                 game.setToPlay(max(player.bet, game.getToPlay()))
#                 player.reasonable()
#                 # print line, player.bet, game.stackSize
#                 break
#         write.write(line)
#     elif '*** FLOP ***' in line:
#         for player in game.getPlayers():
#             player.current = 0

#         game.setBoard(line[-10:-2].replace(" ", ""))

#         elements = line[-10:-2].split()
#         elements.insert(0, "FLOP")
#         # print elements
#         # print playerHands
#         wr.writerow(elements)
#         results = []
#         for player in playerHands:
#             # print player 
#             rndhands = ""
#             for ps in range(numPlayers-1):
#                 rndhands = rndhands + ":xx"

#             # print player.card1+player.card2+rndhands
#             r = pc.calc(player.card1+player.card2+rndhands, game.getBoard(), "", 1000)
#             results.append(r.ev[0])
#         wr.writerow(results)

#     elif '*** TURN ***' in line:
#         for player in game.getPlayers():
#             player.current = 0

#         elements = line[-15:-1].split()
#         elements[2] = elements[2][:-1]
#         elements[3] = elements[3][1:-1]
#         elements.insert(0, "TURN")
#         string = elements[1] + elements[2] + elements[3] + elements[4]


#         game.setBoard(elements[4])

#         # print elements
#         wr.writerow(elements)
#         results = []

#         for player in playerHands:
#             # print player 
#             rndhands = ""
#             for ps in range(numPlayers-1):
#                 rndhands = rndhands + ":xx"

#             # print player.card1+player.card2+rndhands
#             r = pc.calc(player.card1+player.card2+rndhands, game.getBoard(), "", 1000)
#             results.append(r.ev[0])
#         wr.writerow(results)

#     elif '*** RIVER ***' in line:
#         for player in game.getPlayers():
#             player.current = 0

#         elements = line[-18:-1].split()
#         elements[4] = elements[4][1:-1]
#         elements[3] = elements[3][:-1]
#         elements.insert(0, "RIVER")
#         # print elements
#         results = []

#         wr.writerow(elements)

#         string = elements[1] + elements[2] + elements[3] + elements[4] + elements[5]
#         game.setBoard(elements[5])

#         for player in playerHands:
#             # print player 
#             rndhands = ""
#             for ps in range(numPlayers-1):
#                 rndhands = rndhands + ":xx"

#             # print player.card1+player.card2+rndhands
#             r = pc.calc(player.card1+player.card2+rndhands, game.getBoard(), "", 1000)
#             results.append(r.ev[0])

#         wr.writerow(results)

#     elif 'wins the pot' in line:
#         elements = line.split()
#         array = ["Winner", elements[0], elements[4][1:-1], game.stackSize]
#         # if int(elements[4][1:-1]) != game.stackSize:
#         #     print "SHITTTTTTTTTTTT"
#         wr.writerow(array)
#         # print array
#     elif 'ties for the pot' in line:
#         elements = line.split()
#         array = ["Winner", elements[0], elements[-1][1:-1], game.stackSize]
#         # if int(elements[-1][1:-1]) != game.stackSize / num_winners:
#         #      print "SHITTTTTTTTTTTT TIE BROKE"
#         wr.writerow(array)
#     else:
#         write.write(line)

# write.close()
# read.close()