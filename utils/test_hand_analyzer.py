"""
Hand Analyzer Test.

.
"""
from hand_analyzer import *
import re

hand_collection = ['AhAdAh2s2c', '2h2d2s', '3c3d3h3s', 'Ah2s3s4c5d6s7d', '8hQsJsKc9h', 'AhTsJs', '2h3h7h8hKhJh', '2h3h7h8h', '2h3h7h', 'Ah3h']
for cards in hand_collection:
    print '====== new test case ======'
    print 'cards: ', cards
    (ranks,suits,suit_idx) = sort_cards(cards)
    print 'ranks: ', ranks, 'suits: ', suits
    rank_pattern = to_ranks_pattern(ranks)
    (uni_ranks, uni_idx) = np.unique(ranks,return_index=True)
    uni_rank_pattern = to_ranks_pattern(uni_ranks)
    suit_pattern = to_suits_pattern(suits)
    print 'rank pattern: ', rank_pattern
    print 'unique-rank pattern: ', uni_rank_pattern
    print 'suit pattern: ', suit_pattern
    # test pairs
    pair_loc = []
    for m in re_two.finditer(rank_pattern):
        pair_loc = pair_loc + [m.start()]
    pair_rank = map(lambda x: ranks[x], pair_loc)
    print 'pairs: ', pair_rank
    # test threes
    three_loc = []
    for m in re_three.finditer(rank_pattern):
        three_loc = three_loc + [m.start()]
    three_rank = map(lambda x: ranks[x], three_loc)
    print 'threes: ', three_rank
    # test fours
    four_loc = []
    for m in re_four.finditer(rank_pattern):
        four_loc = four_loc + [m.start()]
    four_rank = map(lambda x: ranks[x], four_loc)
    print 'fours: ', four_rank
    # test straights
    straight_loc = []
    for m in re_straight.finditer(uni_rank_pattern):
        straight_loc = straight_loc + [m.start()-1]
    straight_rank = map(lambda x: (ranks[uni_idx[x]],ranks[uni_idx[x]]+4), straight_loc)
    print 'straights: ', straight_rank
    # test traights
    traight_loc = []
    for m in re_traight.finditer(uni_rank_pattern):
        traight_loc = traight_loc + [m.start()]
    traight_rank = map(lambda x: (ranks[uni_idx[x]],ranks[uni_idx[x+1]],ranks[uni_idx[x+2]],ranks[uni_idx[x+3]]), traight_loc)
    print 'traights: ', traight_rank
    # test raights
    raight_loc = []
    for m in re_raight.finditer(uni_rank_pattern):
        raight_loc = raight_loc + [m.start()]
    raight_rank = map(lambda x: (ranks[uni_idx[x]],ranks[uni_idx[x+1]],ranks[uni_idx[x+2]]), raight_loc)
    print 'raights: ', raight_rank
    # test flushes
    flush_loc = []
    for m in re_flush.finditer(suit_pattern):
        flush_loc = flush_loc + [m.start()]
    flush_card = map(lambda x: [cards[2*suit_idx[x-1]],cards[2*suit_idx[x]],cards[2*suit_idx[x+1]],cards[2*suit_idx[x+2]],cards[2*suit_idx[x+3]]], flush_loc)
    print 'flushes: ', map(lambda x: sorted(map(lambda y: rank_map[y], x)), flush_card)
    # test lushes
    lush_loc = []
    for m in re_lush.finditer(suit_pattern):
        lush_loc = lush_loc + [m.start()+1]
    lush_card = map(lambda x: [cards[2*suit_idx[x-1]],cards[2*suit_idx[x]],cards[2*suit_idx[x+1]],cards[2*suit_idx[x+2]]], lush_loc)
    print 'lushes: ', map(lambda x: sorted(map(lambda y: rank_map[y], x)), lush_card)
    # test ushes
    ush_loc = []
    for m in re_ush.finditer(suit_pattern):
        ush_loc = ush_loc + [m.start()+1]
    ush_card = map(lambda x: [cards[2*suit_idx[x-1]],cards[2*suit_idx[x]],cards[2*suit_idx[x+1]]], ush_loc)
    print 'ushes: ', map(lambda x: sorted(map(lambda y: rank_map[y], x)), ush_card)
    # test suited
    if len(cards) == 4:
        if re_connector.search(rank_pattern):
            print 'connector: ', ranks
        if re_suited.search(suit_pattern):
            print 'suited: ', suits


