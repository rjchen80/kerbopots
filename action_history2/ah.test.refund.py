from actionHistory import ActionHistory
ah = ActionHistory()

p0 = 'NEWHAND 38 1 7c Ad 371 15 214 ONEBOTPLUS P1 P2 3 true true true 4.557170'.split()
p1 = 'GETACTION 3 0 371 14 212 3 true true true 2 POST:1:P1 POST:2:P2 3 CALL:2 FOLD RAISE:4:7 4.557170493999999'.split()
p2 = 'GETACTION 58 0 364 3 175 3 true true true 3 RAISE:7:ONEBOTPLUS RAISE:12:P1 RAISE:39:P2 3 FOLD CALL:39 RAISE:66:129 4.453688830999999'.split()
p3 = 'HANDOVER 364 37 199 5 Kh 9d Js 3h Ts 9 FOLD:ONEBOTPLUS CALL:15:P1 REFUND:24:P2 DEAL:FLOP DEAL:TURN DEAL:RIVER SHOW:Qh:Qd:P1 SHOW:5c:Ac:P2 WIN:37:P1 4.349404685999999'.split()


ah.updateActionHistory(p0)
ah.updateActionHistory(p1)
ah.updateActionHistory(p2)
ah.updateActionHistory(p3)

