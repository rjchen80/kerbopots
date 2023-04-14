"""
ActionHistory class.

Records actions and related information of all the players in current hand.
 - handActionHistory: [ [f0, f1, ... , f12 ], ... ]
 - players: {myname, playername1, playername2}
 - myname: myname
 - opHoleCards: {playerName: [xx, xx], ... }
 - handWinner: {playerName: winAmount, ... }

TODO: game statistics.

"""
        #############################################
        # Complete information of players actions
        # 0-2 record action maker, round of play (preflop, flop, turn, river, handover), action name
        # 3-5 record amount of money actually put in by the user, by various measures
        # 6-8 record required amount or range for user to call, bet, raise...
        # 9-12 record player stack size and pot size before and after the action
        # #####################
        # 0 actorName, 1 Round, 2 playerAction,
        # 3 actionAmount = moneyInThisRound, 4 moneyInThisAction, 5 moneyInThisHand
        # 6 callCheckAmount 7 raiseBetMin, 8 raiseBetMax,
        # 9 beforeStack, 10 afterStack, 11 beforePot, 12 afterPot

class ActionHistory:
    def __init__(self):
        self._commonPlayerActions = ['FOLD', 'CHECK', 'BET', 'RAISE', 'POST', 'CALL', 'REFUND']

    def addAction(self, a):
        if a[0] in self._commonPlayerActions:
            if a[0] == 'FOLD' or a[0] == 'CHECK':
                playerSeat = self._playerNameToSeat[a[1]]
                lastActionId = self._lastPlayerActionId[playerSeat]
                f0 = a[1]
                if self.handActionHistory[lastActionId][1] == self._currentRound:
                    f3 = self.handActionHistory[lastActionId][3]
                else:
                    f3 = 0
            elif a[0] == 'BET' or a[0] == 'RAISE' or a[0] == 'POST' or a[0] == 'CALL' or a[0] == 'REFUND':
                playerSeat = self._playerNameToSeat[a[2]]
                lastActionId = self._lastPlayerActionId[playerSeat]
                f0 = a[2]
                if a[0] == 'REFUND':
                    # print '####### REFUND ########'
                    f3 = self.handActionHistory[lastActionId][3] - int(a[1])
                    assert(self.handActionHistory[lastActionId][1] == self._currentRound)
                    assert(f3 > 0)
                else:
                    f3 = int(a[1])
            else:
                 print a[0], ' is not in _commonPlayerActions'
                 assert(False)
            f1 = self._currentRound
            f2 = a[0]
            if self.handActionHistory[lastActionId][1] == self._currentRound:
                f4 = f3 - self.handActionHistory[lastActionId][3]
            else:
                f4 = f3
            f5 = self.handActionHistory[lastActionId][5] + f4
            f6 = self._currentBetThisRound
            f9 = self.handActionHistory[lastActionId][10]
            f10 = f9 - f4
            f11 = self.handActionHistory[-1][12]
            f12 = f11 + f4
            if self._hasBetThisRound:
                f7 = f6 + max(self._currentBetThisRound - self._prevBetThisRound, self.big_blind)
                if self.handActionHistory[lastActionId][1] == self._currentRound:
                    f8 = f6*2 - self.handActionHistory[lastActionId][3] + f11
                else:
                    f8 = f6*2 + f11
            else:
                f7 = self.big_blind
                f8 = f11
            if a[0] == 'POST':
                f7 = f8 = f3
            if a[0] == 'REFUND':
                f7 = f8 = None
        elif a[0] == 'DEAL':
            f0 = 'DEAL'
            f1 = self._currentRound + 1
            f2 = a[1]
            f3 = f4 = f5 = f6 = f7 = f8 = f9 = f10 = None
            f11 = self.handActionHistory[-1][11]
            f12 = self.handActionHistory[-1][12]
        else:
            print a[0], ' is unknown action'
            assert(False)

        self.handActionHistory.append([f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12])

        if a[0] == 'BET' or a[0] == 'RAISE' or a[0] == 'POST':
            self._hasBetThisRound = True
            self._prevBetThisRound = self._currentBetThisRound
            self._currentBetThisRound = f3
        if a[0] == 'FOLD':
            self.playerFoldActionId[playerSeat] = len(self.handActionHistory) - 1
        if a[0] == 'DEAL':
            self._prevBetThisRound = self._currentBetThisRound = 0
            self._hasBetThisRound = False
            self._currentRound += 1
        else:
            self._lastPlayerActionId[playerSeat] = len(self.handActionHistory) - 1
        if a[0] == 'REFUND':
            self._currentBetThisRound += f4

        if a[0] == 'RAISE' or a[0] == 'BET' and self._currentRound == 0:
            self.stat_pf_r[a[2]].append(self.handId)
        if a[0] == 'RAISE' or a[0] == 'BET' and self._currentRound == 1:
            self.stat_f_r[a[2]].append(self.handId)
        if a[0] == 'RAISE' or a[0] == 'BET' and self._currentRound == 2:
            self.stat_t_r[a[2]].append(self.handId)
        if a[0] == 'RAISE' or a[0] == 'BET' and self._currentRound == 3:
            self.stat_r_r[a[2]].append(self.handId)
        if a[0] == 'BET' and f3 <= 2:
            self.stat_BetLt2[a[2]].append(self.handId)
        if a[0] == 'BET' and f3 <= 4:
            self.stat_BetLt4[a[2]].append(self.handId)
        if a[0] == 'FOLD' and self._currentRound == 0:
            self.stat_pf_f[a[1]].append(self.handId)
        if a[0] == 'FOLD' and self._currentRound == 1:
            self.stat_f_f[a[1]].append(self.handId)
        if a[0] == 'FOLD' and self._currentRound == 2:
            self.stat_t_f[a[1]].append(self.handId)
        if a[0] == 'FOLD' and self._currentRound == 3:
            self.stat_r_f[a[1]].append(self.handId)
        '''
        # if reach a round, and if player active + not folded, change None to 0 in statistic variables (initiate count)
        if self._currentRound == 0 and not self._pf_init:
            for player in self.players:
                seat = self._playerNameToSeat[player]
                if self._activePlayers[seat] and self.playerFoldActionId[seat] is None:
                    self.stat_pf_r[player][-1] = 0
                    self.stat_BetLt2[player][-1] = 0
                    self.stat_BetLt4[player][-1] = 0
            self._pf_init = True
        if self._currentRound == 1 and not self._f_init:
            for player in self.players:
                seat = self._playerNameToSeat[player]
                if self._activePlayers[seat] and self.playerFoldActionId[seat] is None:
                    self.stat_f_r[player][-1] = 0
            self._f_init = True
        if self._currentRound == 2 and not self._t_init:
            for player in self.players:
                seat = self._playerNameToSeat[player]
                if self._activePlayers[seat] and self.playerFoldActionId[seat] is None:
                    self.stat_t_r[player][-1] = 0
            self._t_init = True
        if self._currentRound == 3 and not self._r_init:
            for player in self.players:
                seat = self._playerNameToSeat[player]
                if self._activePlayers[seat] and self.playerFoldActionId[seat] is None:
                    self.stat_r_r[player][-1] = 0
            self._r_init = True
        # count
        if a[0] == 'RAISE' and self._currentRound == 0:
            self.stat_pf_r[a[2]][-1] += 1
        if a[0] == 'RAISE' and self._currentRound == 1:
            self.stat_f_r[a[2]][-1] += 1
        if a[0] == 'RAISE' and self._currentRound == 2:
            self.stat_t_r[a[2]][-1] += 1
        if a[0] == 'RAISE' and self._currentRound == 3:
            self.stat_r_r[a[2]][-1] += 1
        if a[0] == 'BET' and f3 <= 2:
            self.stat_BetLt2[a[2]][-1] += 1
        if a[0] == 'BET' and f3 <= 4:
            self.stat_BetLt4[a[2]][-1] += 1
        '''
        '''
        print '*****************************************'
        print [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]
        print 'hasBetThisRound', self._hasBetThisRound
        print 'prevBetThisRound', self._prevBetThisRound
        print 'currentBetThisRound', self._currentBetThisRound
        print 'currentRound', self._currentRound
        print 'handId', self.handId
        print 'STAT Pfr', self.stat_pf_r
        print 'STAT Fr', self.stat_f_r
        print 'STAT Tr', self.stat_t_r
        print 'STAT Rr', self.stat_r_r
        print 'STAT BetLt2', self.stat_BetLt2
        print 'STAT BetLt4', self.stat_BetLt4
        print '*******'
        '''
    def updateActionHistory(self, packet_values):
        if packet_values[0] == 'NEWGAME':
            self.players = packet_values[1:4]
            self.myname = self.players[0]
            print 'myname', self.myname
            self._playerNameToId = dict()
            for i in range(3):
                self._playerNameToId[self.players[i]] = i
            self.big_blind = int(packet_values[5])
            self.winners = []

            ############################
            # Game statistics variables
            ############################
            self.stat_pf_r = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_f_r = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_t_r = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_r_r = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_BetLt2 = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_BetLt4 = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_pf_f = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_f_f = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_t_f = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}
            self.stat_r_f = {self.players[0]:[], self.players[1]:[], self.players[2]:[]}


        if packet_values[0] == 'NEWHAND':
            self.handActionHistory = []
            self.opHoleCards = dict()
            self.handWinner = dict()
            self.handId = int(packet_values[1])
            self.holeCards = packet_values[3:5]
            self._newHandStackSizes = [int(packet_values[5]), int(packet_values[6]), int(packet_values[7])]
            self._playerSeatToName = [packet_values[8], packet_values[9], packet_values[10]]
            self._playerNameToSeat = dict()
            for i in range(3):
                self._playerNameToSeat[self._playerSeatToName[i]] = i
            self._numActivePlayers = int(packet_values[11])
            self._activePlayers = map(lambda x: x=='true', packet_values[12:15])
            self.playerFoldActionId = [None, None, None]
            
            self._previousBetThisRound = 0     # with respect to the current handActionHistory list
            self._currentBetThisRound = 0      # with respect to the current handActionHistory list
            self._currentRound = 0    # 0 preflop, 1 flop, 2 turn, 3 river
            self._hasBetThisRound = False

            # initiate handActionHistory
            self.handActionHistory.append(['DEAL', 0, 'NEWHAND', None, None, None, None, None, None, None, None, 0, 0])
            self._lastPlayerActionId = [None, None, None]
            jj = 0
            for i in range(3):
                if self._activePlayers[i]:
                    jj += 1
                    self.handActionHistory.append([self._playerSeatToName[i], 0, 'INIT_AH', 0, 0, 0, None, None, None, self._newHandStackSizes[i], self._newHandStackSizes[i], 0, 0])
                    self._lastPlayerActionId[i] = jj
            '''
            # extend game statistics with each new hand
            for x in self.stat_pf_r, self.stat_f_r, self.stat_t_r, self.stat_r_r, self.stat_BetLt2, self.stat_BetLt4:
                for key in x:
                    x[key].append(None)
                    assert(len(x[key]) == self.handId)
            # flags for initiating stat vars
            self._pf_init = False
            self._f_init = False
            self._t_init = False
            self._r_init = False
            '''
        if packet_values[0] == 'GETACTION':
            offset = int(packet_values[2]) + 10
            numLastActions = int(packet_values[offset])
            offset = offset + 1
            lastActions = packet_values[offset:offset+numLastActions]
            for action in lastActions:
                a = action.split(':')
                self.addAction(a)

        if packet_values[0] == 'HANDOVER':
            self.winners.append([])
            numBoardCards = int(packet_values[4])
            offset = 5 + numBoardCards
            numLastActions = int(packet_values[offset])
            offset = offset + 1
            lastActions = packet_values[offset:offset+numLastActions]
            # other action names: WIN, SHOW, TIE ...
            for action in lastActions:
                a = action.split(':')
                if a[0] in self._commonPlayerActions + ['DEAL']:
                    self.addAction(a)
                elif a[0] == 'SHOW':
                    self.opHoleCards[a[3]] = [a[1], a[2]]
                elif a[0] == 'WIN' or a[0] == 'TIE':
                    self.handWinner[a[2]] = int(a[1])
                    self.winners[-1].append(a[2])
                else:
                    print a[0], ' is an unknown HANDOVER action'
                    assert(False)
            print '*********************'
            print self.winners
            # print 'opHoleCards', self.opHoleCards
            # print 'handWinner', self.handWinner
            # for x in self.handActionHistory:
            #     print x

