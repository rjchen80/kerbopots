import csv
import pbots_calc as pc

read = open('../casino/Casino_Day-2_kerbopots_p1/Casino_Day-2_kerbopots_vs_OGRoomies_vs_NSASurveillanceB.txt', 'r')
write = open('analysis.csv', 'wb')
wr = csv.writer(write, quoting=csv.QUOTE_ALL)

class Guy:
     def __init__(self, name, card1, card2):
        self.name = name
        self.card1 = card1
        self.card2 = card2


playerHands = []
numPlayers = 3

for line in read:
    # print line
    

    if 'Hand #' in line:
        playerHands = []
        numPlayers = 3

        write.write("\n")
        elements = line.split()
        elements[1] = elements[1][:-1]
        elements[3] = elements[3][1:-2]
        elements[5] = elements[5][1:-2]
        elements[7] = elements[7][1:-1]
        part1 = elements[:2]
        part2 = elements[2:]
        wr.writerow(part1)
        wr.writerow(part2)
        # print elements
    elif 'Dealt to' in line:
        elements = line.split()
        name = elements[2]
        card1 = elements[3][1:]
        card2 = elements[4][:-1]
        array = [name, card1, card2]
        p = Guy(name, card1, card2)
        playerHands.append(p)

        rndhands = ""
        for ps in range(numPlayers-1):
            rndhands = rndhands + ":xx"
        r = pc.calc(p.card1+p.card2+rndhands, "", "", 1000)
        # print playerHands
        # print name, card1, card2
        array.append(r.ev[0])
        wr.writerow(array)
    elif '*** FLOP ***' in line:
        elements = line[-10:-2].split()
        elements.insert(0, "FLOP")
        # print elements
        # print playerHands
        wr.writerow(elements)
        results = []
        for player in playerHands:
            # print player 
            rndhands = ""
            for ps in range(numPlayers-1):
                rndhands = rndhands + ":xx"

            # print player.card1+player.card2+rndhands
            r = pc.calc(player.card1+player.card2+rndhands, line[-10:-2].replace(" ", ""), "", 1000)
            results.append(r.ev[0])
        wr.writerow(results)

    elif '*** TURN ***' in line:
        elements = line[-15:-1].split()
        elements[2] = elements[2][:-1]
        elements[3] = elements[3][1:-1]
        elements.insert(0, "TURN")
        string = elements[1] + elements[2] + elements[3] + elements[4]
        # print elements
        wr.writerow(elements)
        results = []

        for player in playerHands:
            # print player 
            rndhands = ""
            for ps in range(numPlayers-1):
                rndhands = rndhands + ":xx"

            # print player.card1+player.card2+rndhands
            r = pc.calc(player.card1+player.card2+rndhands, string, "", 1000)
            results.append(r.ev[0])
        wr.writerow(results)

    elif '*** RIVER ***' in line:
        elements = line[-18:-1].split()
        elements[4] = elements[4][1:-1]
        elements[3] = elements[3][:-1]
        elements.insert(0, "RIVER")
        # print elements
        results = []

        wr.writerow(elements)

        string = elements[1] + elements[2] + elements[3] + elements[4] + elements[5]
        for player in playerHands:
            # print player 
            rndhands = ""
            for ps in range(numPlayers-1):
                rndhands = rndhands + ":xx"

            # print player.card1+player.card2+rndhands
            r = pc.calc(player.card1+player.card2+rndhands, string, "", 1000)
            results.append(r.ev[0])

        wr.writerow(results)

    elif 'wins the pot' in line:
        elements = line.split()
        array = ["Winner", elements[0], elements[4][1:-1]]
        wr.writerow(array)   
        # print array
    elif 'ties for the pot' in line:
        elements = line.split()
        array = ["Winner", elements[0], elements[-1][1:-1]]
        wr.writerow(array)
    else:
        write.write(line)

write.close()
read.close()