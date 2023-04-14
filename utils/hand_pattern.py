"""
hand pattern module.

Analyzing hand patterns.

Basic Usage:
### generate hand pattern ###
(ranks,suits,suit_idx) = sort_cards(cards)
(uni_ranks, uni_idx) = np.unique(ranks,return_index=True)
uni_rank_pattern = to_ranks_pattern(uni_ranks)
suit_pattern = to_suits_pattern(suits)
### after which test your hand against patterns ###
flop_raight = test_raight(uni_rank_pattern,uni_idx,ranks)
"""
import re
import numpy as np
from numpy import random as rnd

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

re_two = re.compile('[^0](0)(?=[^0]+)')
re_three = re.compile('[^0](00)(?=[^0]+)')
re_four = re.compile('[^0](000)(?=[^0]+)')
re_connector = re.compile('(1)')
re_suited = re.compile('(0)')
re_straight = re.compile('(1)(?=111)')
re_traight = re.compile('(?:[^1])(1)(?=(?=11(?=[^12]|$))|(?=12(?=[^1]|$))|(?=21(?=[^1]|$)))|(?:\w)(2)(?=11(?=[^1]|$))')
re_raight = re.compile('(?:[^12])(1)(?=1(?=[^123]))|(?:[^1])(1)(?=2(?=[^12]))|(?:\w)(1)(?=3(?=[^1]))|(?:[^1])(2)(?=1(?=[^1]))|(?:\w)(2)(?=2(?=[^1]))|(?:[^1])(3)(?=1(?=[^123]))')
re_flush = re.compile('(0)(?=000)')
re_lush = re.compile('(?:[^0]+)(0)(?=00(?=[^0]|$))')
re_ush = re.compile('(?:[^0]+)(0)(?=0(?=[^0]|$))')


def test_pair(rank_pattern,ranks):
    # test pairs
    pair_loc = []
    for m in re_two.finditer(rank_pattern):
        pair_loc = pair_loc + [m.start()]
    pair_rank = map(lambda x: ranks[x], pair_loc)
    if len(pair_rank) > 0:
        feature = (len(pair_rank), pair_rank[-1]/14.0)
    else:
        feature = (0, 0)
    return feature

def test_three(rank_pattern,ranks):
    # test threes
    three_loc = []
    for m in re_three.finditer(rank_pattern):
        three_loc = three_loc + [m.start()]
    three_rank = map(lambda x: ranks[x], three_loc)
    if len(three_rank) > 0:
        feature = (len(three_rank), three_rank[-1]/14.0)
    else:
        feature = (0, 0)
    return feature

def test_four(rank_pattern,ranks):
    # test fours
    four_loc = []
    for m in re_four.finditer(rank_pattern):
        four_loc = four_loc + [m.start()]
    four_rank = map(lambda x: ranks[x], four_loc)
    if len(four_rank) > 0:
        feature = (1, four_rank[-1]/14.0)
    else:
        feature = (0, 0)
    return feature

def test_straight(uni_rank_pattern,uni_idx,ranks):
    # test straights
    straight_loc = []
    for m in re_straight.finditer(uni_rank_pattern):
        straight_loc = straight_loc + [m.start()-1]
    straight_rank = map(lambda x: (ranks[uni_idx[x]],ranks[uni_idx[x]]+4), straight_loc)
    if len(straight_rank) > 0:
        feature = (1, straight_rank[-1][-1]/14.0)
    else:
        feature = (0, 0)
    return feature

def test_traight(uni_rank_pattern,uni_idx,ranks):
    # test traights
    traight_loc = []
    for m in re_traight.finditer(uni_rank_pattern):
        traight_loc = traight_loc + [m.start()]
    traight_rank = map(lambda x: (ranks[uni_idx[x]],ranks[uni_idx[x+1]],ranks[uni_idx[x+2]],ranks[uni_idx[x+3]]), traight_loc)
    if len(traight_rank) > 0:
        feature = (1, traight_rank[-1][-1]/14.0)
    else:
        feature = (0, 0)
    return feature

def test_raight(uni_rank_pattern,uni_idx,ranks):
    # test raights
    raight_loc = []
    for m in re_raight.finditer(uni_rank_pattern):
        raight_loc = raight_loc + [m.start()]
    raight_rank = map(lambda x: (ranks[uni_idx[x]],ranks[uni_idx[x+1]],ranks[uni_idx[x+2]]), raight_loc)
    if len(raight_rank) > 0:
        feature = (1, raight_rank[-1][-1]/14.0)
    else:
        feature = (0, 0)
    return feature

def test_flush(suit_pattern,suit_idx,cards):
    # test flushes
    flush_loc = []
    for m in re_flush.finditer(suit_pattern):
        flush_loc = flush_loc + [m.start()]
    flush_card = map(lambda x: [cards[2*suit_idx[x-1]],cards[2*suit_idx[x]],cards[2*suit_idx[x+1]],cards[2*suit_idx[x+2]],cards[2*suit_idx[x+3]]], flush_loc)
    flush_rank = map(lambda x: sorted(map(lambda y: rank_map[y], x)), flush_card)
    if len(flush_rank) > 0:
        feature = (1, flush_rank[-1][-1]/14.0)
    else:
        feature = (0,0)
    return feature

def test_lush(suit_pattern,suit_idx,cards):
    # test lushes
    lush_loc = []
    for m in re_lush.finditer(suit_pattern):
        lush_loc = lush_loc + [m.start()+1]
    lush_card = map(lambda x: [cards[2*suit_idx[x-1]],cards[2*suit_idx[x]],cards[2*suit_idx[x+1]],cards[2*suit_idx[x+2]]], lush_loc)
    lush_rank = map(lambda x: sorted(map(lambda y: rank_map[y], x)), lush_card)
    if len(lush_rank) > 0:
        feature = (1, lush_rank[-1][-1]/14.0)
    else:
        feature = (0,0)
    return feature

def test_ush(suit_pattern,suit_idx,cards):
    # test ushes
    ush_loc = []
    for m in re_ush.finditer(suit_pattern):
        ush_loc = ush_loc + [m.start()+1]
    ush_card = map(lambda x: [cards[2*suit_idx[x-1]],cards[2*suit_idx[x]],cards[2*suit_idx[x+1]]], ush_loc)
    ush_rank = map(lambda x: sorted(map(lambda y: rank_map[y], x)), ush_card)
    if len(ush_rank) > 0:
        feature = (1, ush_rank[-1][-1]/14.0)
    else:
        feature = (0,0)
    return feature

def test_suited(suit_pattern):
    # test suited
    if re_suited.search(suit_pattern):
        feature = 1.0
    else:
        feature = 0.0
    return feature

def test_connector(rank_pattern):
    # test connector
    if re_connector.search(rank_pattern):
        feature = 1.0
    else:
        feature = 0.0
    return feature
