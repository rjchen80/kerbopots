"""
Hand Analyzer Test.

.
"""
from hand_analyzer import *
import re
import numpy as np
from numpy import random as rnd
import csv

def normalize_features(filename):
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
    with open(filename+'.csv') as csv_feature:
        reader = csv.DictReader(csv_feature)
        cnt = 0
        fieldnames = ['hole_paired','hole_suited','hole_connected','hole_high','hole_low','flop_pair','flop_pairhigh','flop_three','flop_threehigh','flop_raight','flop_raighthigh','flop_ush','flop_ushhigh','flop_high','flop_low','fhand_pair','fhand_pairhigh','fhand_three','fhand_threehigh','fhand_four','fhand_fourhigh','fhand_fullhouse','fhand_fullhigh','fhand_househigh','fhand_twopair','fhand_twopairhigh','fhand_straight','fhand_straighthigh','fhand_traight','fhand_traighthigh','fhand_raight','fhand_raighthigh','fhand_flush','fhand_flushhigh','fhand_lush','fhand_lushhigh','fhand_ush','fhand_ushhigh','hole_in_fhandhigh','hole_in_fhandlow','def2','ef1','ef2','efv0','efv1','efv2','efv3','efv4','efv5','efv6','efv7','efv8','efv9','turn_infogain']
        means = dict()
        stds = dict()
        for field in fieldnames:
            means[field] = 0
            stds[field] = 0
        for row in reader:
            for field in fieldnames:
                means[field] = means[field] + float(row[field])
                stds[field] = stds[field] + float(row[field])**2
            cnt = cnt + 1
        for field in fieldnames:
            means[field] = means[field]/cnt
            stds[field] = stds[field]/cnt
            stds[field] = np.sqrt(stds[field] - means[field]**2)
    with open(filename+'_transform.csv', 'w') as csv_transform:
        writer = csv.DictWriter(csv_transform, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(means)
        writer.writerow(stds)
    with open(filename+'.csv') as csv_feature:
        reader = csv.DictReader(csv_feature)
        with open(filename+'_output.csv', 'w') as csv_output:
#            fieldnames = ['hole1','hole2','flop','turn','river','epf1','epf2','epfv','ef1','ef2','efv','et1','et2','etv','er1','er2','erv']
            writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                for field in fieldnames:
                    val = float(row[field])
                    row[field] = '{:.4}'.format((val-means[field])/(stds[field]+1e-4))
                writer.writerow(row)


normalize_features('sim100_flopfeature')


