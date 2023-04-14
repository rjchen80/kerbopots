import glob
import os
from subprocess import call

try:
    cookie = 'Cookie: session=eyJjc3JmIjp7IiBiIjoiWkRCbE5tVXhZV1U1TnpFeE9UYzBNall3TURFMlpEazJNakUzTURjNU9UUXhNVGc1WW1Vek5BPT0ifSwidXNlcm5hbWUiOiJyamNoZW4ifQ.B6Xsow.k3FEsA5mLAWHaImyUOSPCMj7YLE'
    dirs = glob.glob('*')
    if not dirs[1][0:10] == 'Casino_Day':
        print 'Are you in the right directory?'
        assert(False)
    for d in dirs:
        call(['mkdir', 'day9'+d+'_dump')
        place = d[-3:]
        files = glob.glob(d+'/*')
        for f in files:
            f = os.path.basename(f)[:-4]
            dump_name = f + '.txt'
            dump_url = 'mitpokerbots.com/hh/' + dump_name
            cookie = 
            wget_dump(dump_name)


