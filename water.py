import numpy as np
from cwtlib.measure_units.temp import TempP
from cwtlib.measure_units.conc import ConcP, TDSP
from cwtlib.measure_units.param import Param

class Water:
    def __init__(self, **kwargs):
        flag = 1
        prod = dict(ca=2, mg=3, hrd=5, alk=7, tds=11, temp=19, ph=13, cycles=17)
        for p, v in kwargs.items():
            if issubclass(type(v), Param):
                setattr(self, p, v)
                if p in prod.keys():
                    flag *= prod[p]
            elif  type(v) in [int, float, str] and p in ["ph", "cycles"]:
                setattr(self, p, float(v))
                if p in prod.keys():
                    flag *= prod[p]
            else:
                raise Exception(f"неправильно заданы концентрации {p} {v}")
        if flag % (2*3*5) == 0:
            pass
        elif flag % (2*3) == 0:
            self.hrd = self.ca + self.mg
        elif flag % (2*5) == 0:
            self.mg = self.hrd - self.ca
        elif flag % (3*5) == 0:
            self.ca = self.hrd - self.mg
        elif flag % 2 == 0:
            self.hrd = self.ca*4/3
            self.mg = self.ca/3
        elif flag % 3 == 0:
            self.ca = self.hrd*3/4
            self.mg = self.hrd*1/4
        elif flag % 5 == 0:
            self.ca = self.mg*3
            self.hrd = self.mg*4
        else:
            raise Exception("Ca, Mg, Hrd has to be set")
        if (flag % 7) + (flag % 11) + (flag % 19) != 0:
            raise Exception("Alk and TDS and Temp has to be set")
        if flag % 13 != 0:
            self.ph = self.ph_predict()
        if flag % 17 != 0:
            self.cycles = 1

    def set_cycles(self, c):
        c_old = self.cycles
        self.cycles = c
        for k, v in self.__dict__.items():
            if isinstance(v, ConcP) or isinstance(v, TDSP):
                self.__dict__[k] *= c/c_old
        self.ph = self.ph_predict()

    def ph_predict(self):
        return 4.17 + 1.7177 * np.log10(self.alk.caco3)

    def phs(self):
        return self.pk2() - self.pks() - np.log10(self.ca.mol) + self.phco3() + 5 * self.pfm()

    def pk2(self):
        return 107.8871 + 0.03252849 * self.temp.K - 5151.79 /self.temp.K  - 38.92561 * np.log10(self.temp.K) + 563713.9 / self.temp.K ** 2

    def pks(self):
        return 171.9065 + 0.077993 * self.temp.K - 2839.319/self.temp.K- 71.595 * np.log10(self.temp.K)

    def pkw(self):
        return 4471/self.temp.K  + 0.01706 * self.temp.K - 6.0875

    def phco3(self):
        ans = self.alk.mol + 10 ** (self.pfm() - self.ph) - 10 ** (self.ph + self.pfm() - self.pkw())
        ans /= 1 + 0.5 * 10 ** (self.ph - self.pk2())
        return -np.log10(ans)

    def pfm(self):
        return 1.82E6 * (self.e_help() * self.temp.K) ** (-1.5) * (self.ionic_strength() ** 0.5 / (1 + self.ionic_strength() ** 0.5) - 0.3 * self.ionic_strength() ** 0.5)

    def e_help(self):
        return 60954.0 / (self.temp.K + 116) - 68.937

    def ionic_strength(self):
        return 1.6E-5 * self.tds.ppm

    def casi(self):
        ca0 = self.ca.ppm
        if self.phs() >= self.ph:
            return 1
        while self.phs() < self.ph:
            self.ca.ppm -= 0.01
        ca1 = self.ca.ppm
        self.ca.ppm = ca0
        return ca0 / ca1

    def ccsp(self):
        ca0 = self.ca.ppm
        alk0 = self.alk.ppm
        if self.phs() > self.ph:
            return 1
        while self.phs() < self.ph:
            self.ca.ppm = self.ca.ppm - 0.01
            self.alk.ppm = self.alk.ppm - 0.01
        ca1 = self.ca.ppm
        self.ca.ppm = ca0
        self.alk.ppm = alk0
        return ca0/ca1

    def lsi(self):
        return self.ph - self.phs()

    def rzn(self):
        return 2*self.phs() - self.ph

    def larsen(self):
        return 100*(self.cl.meq + self.so4.meq)/self.alk.meq

    def calc_tds(self):
        tds = 0
        for k, v in self.__dict__.items():
            if isinstance(v, ConcP):
                tds += v.ppm
        return tds

    def calc_na(self):
        na =self.cl.meq + self.so4.meq + self.alk.meq - self.hrd.meq
        if na > 0:
            return na
        else:
            return 0

    def larsen_modified(self, hti):
        '''Уточнить'''
        return (self.cl.meq + self.so4.meq + self.calc_na())**0.5/self.alk.meq*self.temp.C/25*hti/50/24

    def po4_si(self):
        return self.ph - (11.75 - np.log10(self.ca.caco3) - np.log10(self.po4.ppm) - 2 * np.log10(self.temp.C))/0.65

    def sio2_si(self):
        sio2_max = 21.43*self.ph - 4.3
        return self.sio2.ppm/sio2_max

    def caso4_si(self):
        return self.ca.ppm*self.so4.ppm/50000

    def phs_simple(self):
        a = (np.log10(self.tds.ppm)-1)/10
        b = -13.12*np.log10(self.temp.K) + 34.55
        c = np.log10(self.ca.caco3) - 0.4
        d = np.log10(self.alk.caco3)
        return 9.3 + a + b - c - d

    def lsi_simple(self):
        return self.ph - self.phs_simple()

    def rzn_simple(self):
        return 2*self.phs_simple() - self.ph

    def calc_ions(self):
        balance = 0
        for k, v in self.__dict__.items():
            if isinstance(v, ConcP):
                balance += v.meq*v._ion.charge
        return balance

    @property
    def cations(self):
        balance = 0
        for k, v in self.__dict__.items():
            if isinstance(v, ConcP):
                if v._ion.charge > 0:
                    balance += v.meq*v._ion.charge
        return balance

    @property
    def anions(self):
        balance = 0
        for k, v in self.__dict__.items():
            if isinstance(v, ConcP):
                if v._ion.charge < 0:
                    balance += v.meq*v._ion.charge
        return -balance

