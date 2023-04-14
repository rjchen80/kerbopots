from actionHistory import ActionHistory

file = 'Casino_Day-8_kerbopots_vs_CJK_vs_kfosmoe_p1.dump'

fh = open(file, 'r')

legal_packet_keywords = ['NEWGAME', 'NEWHAND', 'GETACTION', 'HANDOVER']
while True:
    line = fh.readline().split()
    if len(line) == 0:
        fh.close()
        break
    if line[0] == 'NEWGAME':
        ah = ActionHistory()
    if line[0] in legal_packet_keywords:
        ah.updateActionHistory(line)
