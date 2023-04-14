import numpy as np
class PFPlayer:
    def __init__(self):
        hc3p = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,126,683,2082,4346,6612,8583,10040,11568,12845,13733,14195,14492,14593,14173,13952,13583,12803,12180,11911,11820,11116,10550,9756,8832,8005,7066,6184,5427,4838,4202,3647,2777,2191,1480,917,649,514,419,314,357,379,409,357,357,396,345,332,354,391,318,280,330,397,294,213,253,363,359,196,83,17,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype='float')
        chc3p = np.cumsum(hc3p)
        self.rawdens3p = hc3p/chc3p[-1]
        self.rawdist3p = chc3p/chc3p[-1]
        hc2p = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,56,218,595,1327,2199,3321,3973,4706,5061,5768,6000,6157,6501,6334,6512,6226,6697,6642,7203,6789,6881,6791,7185,7016,6852,6826,6896,7195,6783,6596,5913,5381,4744,3979,3249,2991,2440,1915,1192,692,476,330,349,292,302,307,312,363,344,344,389,388,366,344,306,289,327,249,93,20,0,0,0,0,0,0,0,0,0,0,0,0], dtype='float')
        chc2p = np.cumsum(hc2p)
        self.rawdens2p = hc2p/chc2p[-1]
        self.rawdist2p = chc2p/chc2p[-1]
        self.rawdist23 = (self.rawdist2p, self.rawdist3p)
        self.rawdistx = np.linspace(0,1,101)
        self.irsp_3p = [0.4, 1.0, 0.3, 0.37] #p1, p2, k1, k2
        self.irsp_2p = [0.4, 1.0, 0.47, 0.55]
    def pfdist(self, nump, x):
        out = []
        for xx in x:
            if xx<=0:
                pos = 0
            else:
                pos = max(np.where(xx>=self.rawdistx)[0])
            r = (xx - self.rawdistx[pos]) / 0.01
            assert(r>=0 and r<=1)
            if nump == 3:
                out.append((1-r)*self.rawdist3p[pos] + r*self.rawdist3p[min(pos+1,100)])
            else:
                out.append((1-r)*self.rawdist2p[pos] + r*self.rawdist2p[min(pos+1,100)])
        return np.array(out)
    def pfidist(self, nump, y):
        out = []
        for yy in y:
            if yy <=0:
                pos = 0
            else:
                if nump == 3:
                    pos = max(np.where(yy>=self.rawdist3p)[0])
                else:
                    pos = max(np.where(yy>=self.rawdist2p)[0])
            if pos < 100:
                if nump == 3:
                    if self.rawdist3p[pos+1] - self.rawdist3p[pos] > 1e-8:
                        print pos
                        print 'denom:', self.rawdist3p[pos+1] - self.rawdist3p[pos]
                        print 'numer:', yy - self.rawdist3p[pos]
                        r = (yy - self.rawdist3p[pos]) / (self.rawdist3p[pos+1] - self.rawdist3p[pos])
                    else:
                        r = 0
                else:
                    if self.rawdist2p[pos+1] - self.rawdist2p[pos] > 1e-8:
                        print pos
                        print 'denom:', self.rawdist2p[pos+1] - self.rawdist2p[pos]
                        print 'numer:', yy - self.rawdist2p[pos]
                        r = (yy - self.rawdist2p[pos]) / (self.rawdist2p[pos+1] - self.rawdist2p[pos])
                    else:
                        r = 0
            else:
                r = 0
            print 'pfidist: r =',r
            assert(r>=0 and r<=1)
            out.append((1-r)*pos/100 + r*(pos+1)/100)
        return np.array(out)
    # initial raise sampling probability    
    def irsp(self, nump, e):
        if nump == 3:
            p1 = self.irsp_3p[0]
            p2 = self.irsp_3p[1]
            k1 = self.irsp_3p[2]
            k2 = self.irsp_3p[3]
        else:
            p1 = self.irsp_2p[0]
            p2 = self.irsp_2p[1]
            k1 = self.irsp_2p[2]
            k2 = self.irsp_2p[3]
        if e<k1:
            out = p1
        elif e>k2:
            out = p2
        else:
            r = (e-k1) / (k2 - k1)
            out = (1-r)*p1 + r*p2
        return out




