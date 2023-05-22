import numpy as np
import copy
import pathlib
import importlib.util
from django.conf import settings
from device.cwtlib.params import *
'''spec = importlib.util.spec_from_file_location("params", pathlib.Path.joinpath(settings.BASE_DIR, "device/cwtlib", "params.py"))
params = importlib.util.module_from_spec(spec)
spec.loader.exec_module(params)
ConcP = params.ConcP
TempP = params.TempP
TDSP = params.TDSP'''

class Water:
    def __init__(self, **kwargs):
        for p, v in kwargs.items():
            if type(v).__name__ in [x.__name__ for x in [ConcP, TempP, TDSP]]:
                self.__dict__[p] = v
            elif type(v) in [int, float] and p=="ph":
                self.__dict__[p] = v
            elif type(v) in [str] and p=="ph":
                try:
                    self.__dict__[p] = float(v)
                except:
                    raise Exception("ph incorrect")
            else:
                raise Exception(f"неправильно заданы концентрации {p} {v}")
        if 'ca' in self.__dict__.keys() and 'mg' in self.__dict__.keys() and 'hrd' not in self.__dict__.keys():
            self.hrd = (self.ca + self.mg).set_ion('hrd')
        elif 'ca' in self.__dict__.keys() and 'mg' not in self.__dict__.keys() and 'hrd' in self.__dict__.keys():
            self.mg = (self.hrd - self.ca).set_ion('mg')
        elif 'ca' not in self.__dict__.keys() and 'mg' in self.__dict__.keys() and 'hrd' in self.__dict__.keys():
            self.ca = (self.hrd - self.mg).set_ion('ca')
        elif 'ca' in self.__dict__.keys() and 'mg' not in self.__dict__.keys() and 'hrd' not in self.__dict__.keys():
            self.hrd = (self.ca*4/3).set_ion('hrd')
            self.mg = (self.ca/3).set_ion('mg')
        elif 'ca' not in self.__dict__.keys() and 'mg' not in self.__dict__.keys() and 'hrd' in self.__dict__.keys():
            self.ca = (self.hrd*3/4).set_ion('ca')
            self.mg = (self.hrd*1/4).set_ion('mg')
        elif 'ca' not in self.__dict__.keys() and 'mg' in self.__dict__.keys() and 'hrd' not in self.__dict__.keys():
            self.ca = (self.mg*3).set_ion('ca')
            self.hrd = (self.mg*4).set_ion('hrd')
        else:
            raise Exception("Ca, Mg, Hrd has to be set")
        if 'alk' not in self.__dict__.keys():
            raise Exception("Alk has to be set")
        if 'tds' not in self.__dict__.keys():
            raise Exception("TDS has to be set")
        if 'ph' not in self.__dict__.keys():
            self.ph = self.ph_predict()
        if 'cycles' not in self.__dict__.keys():
            self.cycles = 1

    def set_cycles(self, c):
        c_old = self.cycles
        self.cycles = c
        for k, v in self.__dict__.items():
            if type(v)==ConcP:
                self.__dict__[k] *= c/c_old
        self.ph = self.ph_predict()

    def ph_predict(self):
        return 4.17 + 1.7177 * np.log10(self.alk.set_unit('caco3').value)

    def phs(self):
        return self.pk2() - self.pks() - np.log10(self.ca.set_unit('mol').value) + self.phco3() + 5 * self.pfm()

    def pk2(self):
        self.temp.set_unit('K')
        return 107.8871 + 0.03252849 * self.temp.value - 5151.79 /self.temp.value  - 38.92561 * np.log10(self.temp.value) + 563713.9 / self.temp.value ** 2

    def pks(self):
        self.temp.set_unit('K')
        return 171.9065 + 0.077993 * self.temp.value - 2839.319/self.temp.value- 71.595 * np.log10(self.temp.value)

    def pkw(self):
        self.temp.set_unit('K')
        return 4471/self.temp.value  + 0.01706 * self.temp.value - 6.0875

    def phco3(self):
        ans = self.alk.set_unit('mol').value + 10 ** (self.pfm() - self.ph) - 10 ** (self.ph + self.pfm() - self.pkw())
        ans /= 1 + 0.5 * 10 ** (self.ph - self.pk2())
        return -np.log10(ans)

    def pfm(self):
        self.temp.set_unit('K')
        return 1.82E6 * (self.e_help() * self.temp.value) ** (-1.5) * (self.ionic_strength() ** 0.5 / (1 + self.ionic_strength() ** 0.5) - 0.3 * self.ionic_strength() ** 0.5)

    def e_help(self):
        self.temp.set_unit('K')
        return 60954.0 / (self.temp.value + 116) - 68.937

    def ionic_strength(self):
        return 1.6E-5 * self.tds.set_unit('ppm').value

    def casi(self):
        ca0 = self.ca.value
        if self.phs() >= self.ph:
            return 1
        while self.phs() < self.ph:
            self.ca.value -= 0.01
        ca1 = self.ca.value
        self.ca.value = ca0
        return ca0 / ca1

    def ccsp(self):
        ca0 = self.ca.value
        alk0 = self.alk.value
        if self.phs() > self.ph:
            return 1
        while self.phs() < self.ph:
            self.ca.value = self.ca.value - 0.01
            self.alk.value = self.alk.value - 0.01
        ca1 = self.ca.value
        self.ca.value = ca0
        self.alk.value = alk0
        return ca0/ca1

    def lsi(self):
        return self.ph - self.phs()

    def rzn(self):
        return 2*self.phs() - self.ph

    def larsen(self):
        return 100*(self.cl.set_unit('meq').value + self.so4.set_unit('meq').value)/self.alk.set_unit('meq').value

    def calc_tds(self):
        return self.alk.set_unit('caco3').value + self.hrd.set_unit('caco3').value + self.cl.set_unit('ppm').value + self.so4.set_unit('ppm').value

    def calc_na(self):
        na =self.cl.set_unit('meq').value+ self.so4.set_unit('meq').value + self.alk.set_unit('meq').value - self.hrd.set_unit('meq').value
        if na > 0:
            return na
        else:
            return 0

    def larsen_modified(self, hti):
        '''Уточнить'''
        return (self.cl.set_unit('meq').value + self.so4.set_unit('meq').value + self.calc_na())**0.5/self.alk*self.temp/25*hti/50/24

    def po4_si(self):
        return self.ph - (11.75 - np.log10(self.ca.set_unit('caco3').value) - np.log10(self.po4.set_unit('ppm').value) - 2 * np.log10(self.temp.set_unit('C').value))/0.65

    def sio2_si(self):
        sio2_max = 21.43*self.ph - 4.3
        return self.sio2.set_unit('ppm').value/sio2_max

    def caso4_si(self):
        return self.ca.set_unit('ppm').value*self.so4.set_unit('ppm').value/50000

    def phs_simple(self):
        a = (np.log10(self.tds.set_unit('ppm').value)-1)/10
        b = -13.12*np.log10(self.temp.set_unit('K').value) + 34.55
        c = np.log10(self.ca.set_unit('caco3').value) - 0.4
        d = np.log10(self.alk.set_unit('caco3').value)
        return 9.3 + a + b - c - d

    def lsi_simple(self):
        return self.ph - self.phs_simple()

    def rzn_simple(self):
        return 2*self.phs_simple() - self.ph

