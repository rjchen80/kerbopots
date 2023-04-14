"""
Hand Analyzer Test.

.
"""
from hand_analyzer import *
import re
import numpy as np
from numpy import random as rnd
import csv

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

def gen_flopfeature(filename):
#    hand_collection = ['AhAd2s2c', '2h2d2s', '3c3d3h3s', 'AhTsJsKcQd', 'AhTsJsKc', 'AhTsJs', '2h3h7h8hKh', '2h3h7h8h', '2h3h7h', '2h3h']
#    for cards in hand_collection:
#        print '====== new test case ======'
#        print 'cards: ', cards
#        (ranks,suits,suit_idx) = sort_cards(cards)
#        print 'ranks: ', ranks, 'suits: ', suits
#        rank_pattern = to_ranks_pattern(ranks)
#        (uni_ranks, uni_idx) = np.unique(ranks,return_index=True)
#        uni_rank_pattern = to_ranks_pattern(uni_ranks)
#        suit_pattern = to_suits_pattern(suits)
#        print 'rank pattern: ', rank_pattern
#        print 'unique-rank pattern: ', uni_rank_pattern
#        print 'suit pattern: ', suit_pattern
    with open(filename+'.csv') as csv_simulation:
        reader = csv.DictReader(csv_simulation)
        with open(filename+'_flopfeature.csv', 'w') as csv_feature:
#            fieldnames = ['hole1','hole2','flop','turn','river','epf1','epf2','epfv','ef1','ef2','efv','et1','et2','etv','er1','er2','erv']
            fieldnames = ['hole_paired','hole_suited','hole_connected','hole_high','hole_low','flop_pair','flop_pairhigh','flop_three','flop_threehigh','flop_raight','flop_raighthigh','flop_ush','flop_ushhigh','flop_high','flop_low','fhand_pair','fhand_pairhigh','fhand_three','fhand_threehigh','fhand_four','fhand_fourhigh','fhand_fullhouse','fhand_fullhigh','fhand_househigh','fhand_twopair','fhand_twopairhigh','fhand_straight','fhand_straighthigh','fhand_traight','fhand_traighthigh','fhand_raight','fhand_raighthigh','fhand_flush','fhand_flushhigh','fhand_lush','fhand_lushhigh','fhand_ush','fhand_ushhigh','hole_in_fhandhigh','hole_in_fhandlow','def2','ef1','ef2','efv0','efv1','efv2','efv3','efv4','efv5','efv6','efv7','efv8','efv9','turn_infogain']
            writer = csv.DictWriter(csv_feature, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                hole = row['hole1']
                flop = row['flop']
                fhand = hole + flop
                f = dict()
                # hole features
                (ranks,suits,suit_idx) = sort_cards(hole)
                rank_pattern = to_ranks_pattern(ranks)
                suit_pattern = to_suits_pattern(suits)
                hole_paired = test_pair(rank_pattern,ranks)
                f['hole_paired'] = hole_paired[0]
                f['hole_suited'] = test_suited(suit_pattern)
                f['hole_connected'] = test_connector(rank_pattern)
                f['hole_high'] = ranks[-1]/14.0
                f['hole_low'] = ranks[-2]/14.0
                # flop features
                (ranks,suits,suit_idx) = sort_cards(flop)
                (uni_ranks, uni_idx) = np.unique(ranks,return_index=True)
                uni_rank_pattern = to_ranks_pattern(uni_ranks)
                suit_pattern = to_suits_pattern(suits)
                flop_pair = test_pair(rank_pattern,ranks)
                f['flop_pair'] = flop_pair[0]
                f['flop_pairhigh'] = flop_pair[1]
                flop_three = test_three(rank_pattern,ranks)
                f['flop_three'] = flop_three[0]
                f['flop_threehigh'] = flop_three[1]
                flop_raight = test_raight(uni_rank_pattern,uni_idx,ranks)
                f['flop_raight'] = flop_raight[0]
                f['flop_raighthigh'] = flop_raight[1]
                flop_ush = test_ush(suit_pattern,suit_idx,flop)
                f['flop_ush'] = flop_ush[0]
                f['flop_ushhigh'] = flop_ush[1]
                f['flop_high'] = ranks[-1]/14.0
                f['flop_low'] = ranks[-3]/14.0
                # fhand features
                (ranks,suits,suit_idx) = sort_cards(fhand)
                (uni_ranks, uni_idx) = np.unique(ranks,return_index=True)
                uni_rank_pattern = to_ranks_pattern(uni_ranks)
                suit_pattern = to_suits_pattern(suits)
                fhand_pair = test_pair(rank_pattern,ranks)
                fhand_three = test_three(rank_pattern,ranks)
                if fhand_pair[0] == 1 and fhand_three[0] == 0:
                    f['fhand_pair'] = fhand_pair[0]
                    f['fhand_pairhigh'] = fhand_pair[1]
                else:
                    f['fhand_pair'] = 0
                    f['fhand_pairhigh'] = 0
                if fhand_three[0] == 1 and fhand_pair[0] == 0:
                    f['fhand_three'] = fhand_three[0]
                    f['fhand_threehigh'] = fhand_three[1]
                else:
                    f['fhand_three'] = 0
                    f['fhand_threehigh'] = 0
                if fhand_pair[0] > 1:
                    f['fhand_twopair'] = fhand_pair[0]
                    f['fhand_twopairhigh'] = fhand_pair[1]
                else:
                    f['fhand_twopair'] = 0
                    f['fhand_twopairhigh'] = 0
                if fhand_pair[0] > 0 and fhand_three[0] > 0:
                    f['fhand_fullhouse'] = 1
                    f['fhand_fullhigh'] = fhand_three[1]
                    f['fhand_househigh'] = fhand_pair[1]
                else:
                    f['fhand_fullhouse'] = 0
                    f['fhand_fullhigh'] = 0
                    f['fhand_househigh'] = 0
                fhand_four = test_four(rank_pattern,ranks)
                f['fhand_four'] = fhand_four[0]
                f['fhand_fourhigh'] = fhand_four[1]
                fhand_raight = test_raight(uni_rank_pattern,uni_idx,ranks)
                f['fhand_raight'] = fhand_raight[0]
                f['fhand_raighthigh'] = fhand_raight[1]
                fhand_ush = test_ush(suit_pattern,suit_idx,fhand)
                f['fhand_ush'] = fhand_ush[0]
                f['fhand_ushhigh'] = fhand_ush[1]
                fhand_straight = test_straight(uni_rank_pattern,uni_idx,ranks)
                f['fhand_straight'] = fhand_straight[0]
                f['fhand_straighthigh'] = fhand_straight[1]
                fhand_traight = test_traight(uni_rank_pattern,uni_idx,ranks)
                f['fhand_traight'] = fhand_traight[0]
                f['fhand_traighthigh'] = fhand_traight[1]
                fhand_lush = test_lush(suit_pattern,suit_idx,fhand)
                f['fhand_lush'] = fhand_lush[0]
                f['fhand_lushhigh'] = fhand_lush[1]
                fhand_flush = test_flush(suit_pattern,suit_idx,fhand)
                f['fhand_flush'] = fhand_flush[0]
                f['fhand_flushhigh'] = fhand_flush[1]
                f['hole_in_fhandhigh'] = f['hole_high']/(f['hole_high']+f['flop_high'])
                f['hole_in_fhandlow'] = f['hole_low']/(f['hole_low']+f['flop_high'])
                epf2 = float(row['epf2'])
                ef2 = float(row['ef2'])-1e-4
                ef1 = float(row['ef1'])-1e-4
                efv = float(row['efv'])*(1-1e-4) + 5e-5
                f['def2'] = rnd.normal(np.log(ef2/(1-ef2))-np.log(epf2/(1-epf2)), 1)
                pf = ef1
                f['ef1'] = np.log(ef1/(1-ef1))
                f['ef2'] = rnd.normal(np.log(ef2/(1-ef2)), 1)
                bins = [1.0/8, 1.0/5, 1.0/3, 1.0/2, 1.0, 2.0, 3.0, 5.0, 8.0]
                bin_id = np.nonzero(np.array(bins) > efv/(1-efv))
                if len(bin_id[0]) > 0:
                    bin_id = str(bin_id[0][0])
                else:
                    bin_id = '9'
                for i in range(10):
                    f['efv'+str(i)] = 0
                f['efv'+bin_id] = 1
                pt = float(row['et1'])
                ent_f = -pf*np.log(pf) - (1-pf)*np.log(1-pf+1e-10)
                ent_t = -pt*np.log(pt) - (1-pt)*np.log(1-pt+1e-10)
                f['turn_infogain'] = ent_f - ent_t
                for key in f.keys():
                    f[key] = '{:.4}'.format(float(f[key]))
                writer.writerow(f)


gen_flopfeature('sim100')






