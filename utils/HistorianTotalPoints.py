import csv
import pbots_calc as pc
from sets import Set
import os

##features include: numbers: #fold_before_flop %, 
#fold_before_turn %, #fold_before_river, #fold_before_showdown %, 
#win_at_showdown %, etc. histograms: winning_pot_size, losing_pot_size, comparing betting behavior with other top bots

# read = open('../casino/Casino_Day-2_kerbopots_p1/Casino_Day-2_kerbopots_vs_TheHouse_vs_OGRoomies.txt', 'r')
write2 = open('ExampleHistory.txt', 'wb')
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

        self.bigwins = 0
        self.smallwins = 0

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

        self.bet2 = 0
        self.betupto4 = 0
        self.betupto8 = 0
        self.totalactions = 0
        self.points = 0
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
    arrayOfLines = []
    trackWinner = []
    read = open(filename, 'r')

    gameFeatures = GameFeatures()
    for name, player in AllPlayers.items():
        player.resetRank()

    GG = False
    for i, line in enumerate(read):
        arrayOfLines.append(line)
        trackWinner.append(line)
        if 'Hand #' in line:
            ## New hand
            ## Analyze old results and reset
            arrayOfLines = []
            arrayOfLines.append(line)


            elements = line.split()
            elements[2] = fixName(elements[2])
            elements[4] = fixName(elements[4])
            elements[6] = fixName(elements[6])


            if 'Hand #1,' in line and GG == True:
                [winner, second, loser] = findWinner(trackWinner)
                AllPlayers[winner].points += 100
                if type(second) is list:
                    for player in second:
                        AllPlayers[player].points -= 50
                else:
                    AllPlayers[second].points -= 20
                if loser != None:
                    AllPlayers[loser].points -= 80


            trackWinner = []
            trackWinner.append(line)

            gameFeatures.reset()



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
            name = fixName(elements[0])
            AllPlayers[name].totalactions += 1

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
        elif ' checks' in line:
            elements = line.split()
            name = fixName(elements[0])
            AllPlayers[name].totalactions += 1

        elif ' raises to' in line:
            elements = line.split()
            name = fixName(elements[0])
            AllPlayers[name].totalactions += 1

        elif 'bets ' in line:
            elements = line.split()
            name = fixName(elements[0])
            AllPlayers[name].totalactions += 1
            if int(elements[2]) ==2:
                AllPlayers[name].bet2 += 1
            if int(elements[2]) <= 4:
                AllPlayers[name].betupto4 += 1
            if int(elements[2]) <= 8:
                AllPlayers[name].betupto8 += 1
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
            name = fixName(elements[0])
            gameFeatures.showdown = True
            AllPlayers[name].showdowns += 1

        elif ' wins the pot' in line:
            GG = True
            elements = line.split()
            name = fixName(elements[0])
            stack = int(elements[4][1:-1])

            AllPlayers[name].wins += 1
            AllPlayers[name].winning_pot_size.append(stack)
            if stack > 10:
                AllPlayers[name].bigwins += 1
            else:
                AllPlayers[name].smallwins += 1

            if gameFeatures.showdown == True:
                AllPlayers[name].wins_at_showdown += 1

            if stack > 30:
                for line in arrayOfLines:
                    write2.write(line)
                write2.write("\n")
    
    [winner, second, loser] = findWinner(trackWinner)
    AllPlayers[winner].points += 100
    if type(second) is list:
        for player in second:
            AllPlayers[player].points -= 50
    else:
        AllPlayers[second].points -= 20
    if loser != None:
        AllPlayers[loser].points -= 80


    ## Start writing data    

    array = []
    read.close()
    for results in reversed(list(open(filename, 'r'))):
        if ' wins the pot' in results:
            elements = results.split()
            name = fixName(elements[0])
            money = int(elements[-1][1:-1])
            array.append([name, money])
        elif 'Hand #' in results:
            elements = results.split()
            p1 = fixName(elements[2])
            p2 = fixName(elements[4])
            p3 = fixName(elements[6])

            m1 = int(elements[3][1:-2])
            m2 = int(elements[5][1:-2])
            m3 = int(elements[7][1:-1])

            for [name, money] in array:
                name = fixName(name)
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

def fixName(string):
    if string.startswith('ONEBOT1'):
        return 'ONEBOT1'
    if string.startswith('ONEBOT2'):
        return 'ONEBOT2'
    if string.startswith('ONEBOT3'):
        return 'ONEBOT3'
    if string.startswith('BLUFFBOT1'):
        return 'BLUFFBOT1'
    if string.startswith('BLUFFBOT2'):
        return 'BLUFFBOT2'
    if string.startswith('BLUFFBOT3'):
        return 'BLUFFBOT3'
    if string.startswith('CURRENTBOT1'):
        return 'CURRENTBOT1'
    if string.startswith('CURRENTBOT2'):
        return 'CURRENTBOT2'
    if string.startswith('CURRENTBOT3'):
        return 'CURRENTBOT3'
    return string

def findWinner(trackWinner):
    hand_number = trackWinner[0]
    winner = None
    loser = None
    second = None
    num_players = 3

    print hand_number

    elements = hand_number.split()
    p1 = fixName(elements[2])
    p2 = fixName(elements[4])
    p3 = fixName(elements[6])
    alive_players = [p1, p2, p3]

    m1 = int(elements[3][1:-2])
    m2 = int(elements[5][1:-2])
    m3 = int(elements[7][1:-1])

    if m1 == 0:
        loser = p1
        num_players -= 1
        alive_players = [p2, p3]
    elif m2 == 0:
        loser = p2
        num_players -= 1
        alive_players = [p1, p3]
    elif m3 == 0:
        loser = p3
        num_players -= 1
        alive_players = [p1, p2]



    if 'Hand #1000,' not in hand_number:
        # Game finished, can tell winner from last line
        for line in reversed(trackWinner):
            if 'wins the pot' in line:
                winner = fixName(line.split()[0])
            elif line != "\n":
                name = fixName(line.split()[0])
                if name!=winner and winner != None:
                    if loser != None:
                        second = name
                        break
                    else:
                        ## both second
                        if winner == p1:
                            second = [p2, p3]
                            break
                        elif winner == p2:
                            second = [p1, p3]
                            break
                        elif winner == p3:
                            second = [p1, p2]
                            break
                        else:
                            assert(False)
    else:
        for line in reversed(trackWinner):
            if 'wins the pot' in line:
                name = fixName(line.split()[0])
                money = int(line.split()[-1][1:-1])
                if name == p1:
                    m1 += money / float(num_players)
                    if p2 in alive_players:
                        m2 -= money / float(num_players)
                    if p3 in alive_players:
                        m3 -= money / float(num_players)
                if name == p2:
                    m2 += money / float(num_players)
                    if p1 in alive_players:
                        m1 -= money / float(num_players)
                    if p3 in alive_players:
                        m3 -= money / float(num_players)
                if name == p3:
                    m3 += money / float(num_players)
                    if p1 in alive_players:
                        m1 -= money / float(num_players)
                    if p2 in alive_players:
                        m2 -= money / float(num_players)
                winner_money = max(m1, m2, m3)
                loser_money = min(m1, m2, m3)
                if winner_money == m1:
                    winner = p1
                elif winner_money == m2:
                    winner = p2
                else:
                    winner = p3
                if loser != None:
                    if p1 != winner and p1 != loser:
                        second = p1
                    elif p2 != winner and p2 != loser:
                        second = p2
                    else:
                        second = p3
                else:
                    if loser_money == m1:
                        loser = p1
                    elif loser_money == m2:
                        loser = p2
                    else:
                        loser = p3
                    if p1 != winner and p1 != loser:
                        second = p1
                    elif p2 != winner and p2 != loser:
                        second = p2
                    else:
                        second = p3
    return [winner, second, loser]


def writeResults(filename):
    write = open(filename, 'wb')

    wr = csv.writer(write, quoting = csv.QUOTE_ALL)
    headers = 'Name,Total Games,Win%,Fold% PreFlop,Fold% On Flop,Fold% On Turn,Fold% On River,Win% On Showdown,AVERAGE Stack Won,MAX pot won, Total #1s, Total #2s, Total #3s, Wins > 10, Wins < 10,bet ==2 percentage, bet 2 games, bet <= 4 percentage, bet <= 4 games, <=8, games, Total Points\n'
    
    write.write(headers)

    for keys, players in AllPlayers.items():
        # print players
        stats = [players.name, players.totalGames, float(players.wins)/players.totalGames, players.foldBeforeFlop/float(players.totalGames),
            players.foldOnFlop / float(players.flops), players.foldOnTurn / float(players.turns), 
            players.foldOnRiver / float(players.rivers), players.wins_at_showdown / float(players.showdowns), 
            players.getAverageWin(), max(players.winning_pot_size), players.firsts, players.seconds, players.thirds, players.bigwins, players.smallwins,
            float(players.bet2) / players.totalactions, players.bet2, float(players.betupto4) / players.totalactions, players.betupto4, 
            float(players.betupto8) / players.totalactions, players.betupto8, players.points]
        wr.writerow(stats)
    write.close()


files = open('files.txt', 'r')
root = '../history/'


#directory = 'mini-Tournament/'

for file in os.listdir(root):
    file = file.strip()
    if file.endswith('.txt'):
        analyzeGame(root + file)


# directory2 = 'self-data/handhistory'
# analyzeGame(root + directory2 + '.txt')

# for i in [2, 3, 4, 5, 6]:
#     analyzeGame(root + directory2 + str(i) + '.txt')
# reader = open(root + 'Casino_Day-2_kerbopots_vs_TheHouse_vs_OGRoomies.txt', 'r')
# analyzeGame('../casino/Casino_Day-2_kerbopots_p1/Casino_Day-2_kerbopots_vs_TheHouse_vs_OGRoomies.txt')

writeResults('Example.csv')
write2.close()
