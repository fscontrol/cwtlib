import numpy as np
from units_converter import TemperatureUnit, TDSUnit,  IonConcentration, Ion

class Water:
    def __init__(self, ph, ca, hco3, temp, tds, **kwargs):
        self.ph = ph
        if not isinstance(ca, IonConcentration):
            raise ValueError('ca must be an instance of IonConcentration')
        if not isinstance(hco3, IonConcentration):
            raise ValueError('alk must be an instance of IonConcentration')
        if not isinstance(temp, TemperatureUnit):
            raise ValueError('temp must be an instance of TemperatureUnit')
        if not isinstance(tds, TDSUnit):
            raise ValueError('tds must be an instance of TDSUnit')
        self.ca = ca
        self.hco3 = hco3
        self.temp = temp
        self.tds = tds
        self._cycles = 1
        for arg in kwargs:
            if isinstance(kwargs[arg], IonConcentration):
                setattr(self, arg, kwargs[arg])
            if isinstance(kwargs[arg], TDSUnit):
                self.tds = kwargs[arg]
            if isinstance(kwargs[arg], TemperatureUnit):
                self.temp = kwargs[arg]
    @property
    def cycles(self):
        return self._cycles
    @cycles.setter
    def cycles(self, c):
        c_old = self._cycles
        self._cycles = c
        for k, v in self.__dict__.items():
            if isinstance(v, IonConcentration) or isinstance(v, TDSUnit):
                self.__dict__[k] *= c/c_old
        self.ph = self.ph_predict()
    def ph_predict(self):
        ans = 4.17 + 1.7177 * np.log10(self.hco3.caco3 + 0.001)
        if ans < 4.5:
            ans = 4.5
        elif ans > 10:
            ans = 10
        return ans

    def phs(self):
        return self.pk2() - self.pks() - np.log10(self.ca.caco3/100000) + self.phco3() + 5*self.pfm()
    def pk2(self):
        return 107.8871 + 0.03252849 * self.temp.k- 5151.79 /self.temp.k  - 38.92561 * np.log10(self.temp.k) + 563713.9 / self.temp.k ** 2
    def pks(self):
        return 171.9065 + 0.077993 * self.temp.k - 2839.319/self.temp.k- 71.595 * np.log10(self.temp.k)
    def pkw(self):
        return 4471/self.temp.k  + 0.01706 * self.temp.k - 6.0875
    def phco3(self):
        ans = self.hco3.meq/1000 + 10 ** (self.pfm() - self.ph) - 10 ** (self.ph + self.pfm() - self.pkw())
        ans /= 1 + 0.5 * 10 ** (self.ph - self.pk2())
        return -np.log10(ans)
    def pfm(self):
        return 1.82E6 * (self.e_help() * self.temp.k) ** (-1.5) * (self.ionic_strength() ** 0.5 / (1 + self.ionic_strength() ** 0.5) - 0.3 * self.ionic_strength() ** 0.5)
    def e_help(self):
        return 60954.0 / (self.temp.k + 116) - 68.937
    def ionic_strength(self):
        return self.tds._calculate_ionic_strength(self.tds.ppm)
        # return 1.6E-5 * self.tds.ppm

    def ccsp(self):
        if self.phs() > self.ph_predict():
            return -1
        else:
            cycles = self.cycles
            while self.phs() < self.ph_predict() and self.cycles >0:
                self.cycles -= 0.01
            cycles_fin = self.cycles
            self.cycles = cycles
            return cycles_fin/cycles
    def lsi(self):
        return self.ph - self.phs()
    def rzn(self):
        return 2*self.phs() - self.ph
    def larsen(self):
        return 100*(self.cl.meq + self.so4.meq)/self.hco3.meq
    def calc_tds(self):
        return sum([v.caco3 for k, v in self.__dict__.items() if isinstance(v, Ion)])
    def calc_na(self):
        return self.calc_ions()
    def larsen_modified(self, hti):
        return (self.cl.meq + self.so4.meq + self.calc_ions())**0.5/self.hco3.meq*self.temp.c/25*hti.h/50/24
    def po4_si(self):
        return self.ph - (11.75 - np.log10(self.ca.caco3) - np.log10(self.po4.caco3) - 2 * np.log10(self.temp.c))/0.65
    def sio2_si(self):
        sio2_max = 21.43*self.ph - 4.3
        return self.sio2.ppm/sio2_max
    def caso4_si(self):
        return self.ca.ppm*self.so4.ppm/50000
    def phs_simple(self):
        a = (np.log10(self.tds.ppm)-1)/10
        b = -13.12*np.log10(self.temp.k) + 34.55
        c = np.log10(self.ca.caco3) - 0.4
        d = np.log10(self.hco3.caco3)
        return 9.3 + a + b - c - d
    def lsi_simple(self):
        return self.ph - self.phs_simple()
    def rzn_simple(self):
        return 2*self.phs_simple() - self.ph
    def calc_ions(self):
        return self.cations - self.anions
    @property
    def cations(self):
        try:
            return sum([v.caco3 for k, v in self.__dict__.items() if (isinstance(v, Ion) and v.charge > 0)])
        except:
            return 0
    @property
    def anions(self):
        try:
            return sum([v.caco3 for k, v in self.__dict__.items() if (isinstance(v, Ion) and v.charge < 0)])
        except:
            return 0
