"""
Hand Analyzer.

Extracting hand features for prediction of heads-up winning rate.
"""
import random as rnd
import numpy as np
#from poker_hand import PokerHand
import re

#class HandAnalyzer:
#    ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
#    rank_map = dict({'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14})
#    suits = ['d','s','h','c']
#    suit_map = dict({'d':1, 's':2, 'h':3, 'c':4})
#    def __init__(self, hand):
#        self.hand = hand
#    def join(self):
#        cards = self.hand.hole
#        if self.hand.flop:
#            cards = cards + self.hand.flop
#        if self.hand.turn:
#            cards = cards + self.hand.turn
#        if self.hand.river:
#            cards = cards + self.hand.river
#        return cards
#    def sort_cards(self, cards=None):
#        if not cards:
#            cards = self.join()
#        numCards = len(cards)/2
#        cardRanks = []
#        cardSuits = []
#        for i in range(numCards):
#            cardRanks = cardRanks + [cards[2*i]]
#            cardSuits = cardSuits + [cards[2*i+1]]
#        rankIds = map(lambda x:self.rank_map[x], cardRanks)
#        suitIds = map(lambda x:self.suit_map[x], cardSuits)
##        print set(sorted(rankIds))
#        print sorted(rankIds), sorted(suitIds)



ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
rank_map = dict({'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14})
suits = ['d','s','h','c']
suit_map = dict({'d':1, 's':2, 'h':3, 'c':4})

def sort_cards(cards):
    numCards = len(cards)/2
    cardRanks = []
    cardSuits = []
    for i in range(numCards):
        cardRanks = cardRanks + [cards[2*i]]
        cardSuits = cardSuits + [cards[2*i+1]]
    rankIds = map(lambda x:rank_map[x], cardRanks)
    suitIds = map(lambda x:suit_map[x], cardSuits)
    #        print set(sorted(rankIds))
    ranks = sorted(rankIds)
    suits = sorted(suitIds)
    suit_idx = sorted(range(len(suitIds)), key=lambda k:suitIds[k])
    if ranks[-1] == 14:
        ranks = [1] + ranks
    return (ranks, suits, suit_idx)


def to_ranks_pattern(ranks):
    pattern_map = dict({-1:'b',0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'t',11:'j',12:'q',13:'k'})
    dranks = np.hstack((-1,np.diff(ranks),-1))
    ps = map(lambda x:pattern_map[x], dranks)
    p = ''.join(ps)
    return p

def to_suits_pattern(suits):
    pattern_map = dict({-1:'b', 0:'0',1:'1',2:'2',3:'3'})
    dsuits = np.hstack((-1,np.diff(suits),-1))
    ps = map(lambda x:pattern_map[x], dsuits)
    p = ''.join(ps)
    return p

#re_two = re.compile('[^0]0[^0]*')
re_two = re.compile('[^0](0)(?=[^0]+)')
re_three = re.compile('[^0](00)(?=[^0]+)')
re_four = re.compile('[^0](000)(?=[^0]+)')

#re_pair = re.compile('^[^0]+(0)[^0]*$')
#re_twopair = re.compile('[^0](0)[^0]+(0)[^0]*$')
#re_threeofakind = re.compile('[^0](00)[^0]*$')
re_connector = re.compile('(1)')
re_suited = re.compile('(0)')
re_straight = re.compile('(1)(?=111)')
re_traight = re.compile('(?:[^1])(1)(?=(?=11(?=[^12]|$))|(?=12(?=[^1]|$))|(?=21(?=[^1]|$)))|(?:\w)(2)(?=11(?=[^1]|$))')
re_raight = re.compile('(?:[^12])(1)(?=1(?=[^123]))|(?:[^1])(1)(?=2(?=[^12]))|(?:\w)(1)(?=3(?=[^1]))|(?:[^1])(2)(?=1(?=[^1]))|(?:\w)(2)(?=2(?=[^1]))|(?:[^1])(3)(?=1(?=[^123]))')
re_flush = re.compile('(0)(?=000)')
re_lush = re.compile('(?:[^0]+)(0)(?=00(?=[^0]|$))')
re_ush = re.compile('(?:[^0]+)(0)(?=0(?=[^0]|$))')
#re_fullhouse = re.compile(')
#re_fourofakind = re.compile('(000)[^0]*$')

#def is_pair(ranks):
#    dranks = np.diff(ranks)
#    max_z = 0
#    tmp_z = 0
#    n_pair = 0
#    for drank in dranks:
#        if drank == 0:
#            tmp_z = tmp_z+1
#            if tmp_z > max_z:
#                max_z = tmp_z
#        else:
#            if tmp_z == 1:
#                n_pair = n_pair+1
#            tmp_z = 0
#    return (max_z==1) and (n_pair==1)
#
#def is_threeOfAKind(ranks):
#    dranks = np.diff(ranks)
#    max_z = 0
#    tmp_z = 0
#    n_pair = 0
#    for drank in dranks:
#        if drank == 0:
#            tmp_z = tmp_z+1
#            if tmp_z > max_z:
#                max_z = tmp_z
#        else:
#            if tmp_z == 1:
#                n_pair = n_pair+1
#            tmp_z = 0
#    return (max_z==2) and (n_pair==0)
#
#def is_fourOfAKind(ranks):
#    dranks = np.diff(ranks)
#    max_z = 0
#    tmp_z = 0
#    for drank in dranks:
#        if drank == 0:
#            tmp_z = tmp_z+1
#            if tmp_z > max_z:
#                max_z = tmp_z
#        else:
#            tmp_z = 0
#    return max_z==3
#
#def is_twoPairs(ranks):
#    dranks = np.diff(ranks)
#    max_z = 0
#    tmp_z = 0
#    n_pair = 0
#    for drank in dranks:
#        if drank == 0:
#            tmp_z = tmp_z+1
#            if tmp_z > max_z:
#                max_z = tmp_z
#        else:
#            if tmp_z == 1:
#                n_pair = n_pair+1
#            tmp_z = 0
#    return (max_z==1) and (n_pair>1)
#
#def is_fullHouse(ranks):
#    dranks = np.diff(ranks)
#    max_z = 0
#    tmp_z = 0
#    n_pair = 0
#    for drank in dranks:
#        if drank == 0:
#            tmp_z = tmp_z+1
#            if tmp_z > max_z:
#                max_z = tmp_z
#        else:
#            if tmp_z == 1:
#                n_pair = n_pair+1
#            tmp_z = 0
#    print max_z, n_pair
#    return (max_z==2) and (n_pair>0)
#
#def is_straight(ranks):
#    if ranks[-1] == 14:
#        ranks = [1] + ranks
#    uranks = np.unique(ranks)
#    l = len(uranks)
#    for i in range(l-4):
#        if uranks[i+4]-uranks[i] == 4:
#            return True
#    return False
#
#def is_flush(suits):
#    dsuits = np.diff(suits)
#    max_z = 0
#    tmp_z = 0
#    for dsuit in dsuits:
#        if dsuit == 0:
#            tmp_z = tmp_z+1
#            if tmp_z > max_z:
#                max_z = tmp_z
#        else:
#            tmp_z = 0
#    return max_z>3
#
#def is_4inStraight(ranks):
#    # [1,3,4,5],[1,2,4,5],[1,2,3,5], [1,2,3,4,5,7], and [1,2,3,4], [11,12,13,14]
#    if ranks[-1] == 14:
#        ranks = [1] + ranks
#    uranks = np.unique(ranks)
#    l = len(uranks)
##    for i in range(l-4)
#
#def is_4outStraight(ranks):
#    # [2,3,4,5],...,[10,11,12,13]
#    pass
#
#def is_3inStraight(ranks):
#    # [1,2,5],[1,3,5],[1,4,5],..., and [1,2,3],[1,2,4],[1,3,4],[12,13,14],[11,13,14],[11,12,14]
#    pass
#
#def is_3outStraight(ranks):
#    # [
#    pass
#
#def is_3inOutStraight(ranks):
#    pass

#hand = PokerHand("KsQd", "9sTs9c", "8s", "Js")
#
#ha = HandAnalyzer(hand)
#ha.sort_cards()