import math
import os
from units_converter import TemperatureUnit, PressureUnit, VolumeUnit,  HumidityUnit, TimeUnit, FlowRateUnit
import numpy as np

class Air:
    def __init__(self, tair=TemperatureUnit(26, "c"),
                 hair=HumidityUnit(50, "perc"),
                 pair=PressureUnit(748, "mmhg")):
        self.tair, self.hair, self.pair = tair, hair, pair
    
    def evaporation_snip(self):
        self.ev_coeff = (0.0009971 + 0.00002357 * (self.tair.c) - 0.0000002143 * (self.tair.c))
        return self.ev_coeff
    
    def evaporation_kurita(self):
        self.ev_coeff = (0.575 + 0.011 * self.tair.c) / 580
        return self.ev_coeff

    def wet_bulb(self):
        wb = self.tair.c * np.arctan(0.151977 * (self.hair.perc + 8.313659) ** 0.5) + \
             np.arctan(self.tair.c + self.hair.perc) - np.arctan(self.hair.perc - 1.676331) + \
             0.00391838 * self.hair.perc ** 1.5 * np.arctan(0.023101 * self.hair.perc) - 4.686035
        return TemperatureUnit(float(wb), "c")
class Tower:
    def __init__(self, rr=FlowRateUnit(2100, "m3_h"),
                 vol=VolumeUnit(650, "m3"),
                 thot=TemperatureUnit(30, "c"),
                 tcold=TemperatureUnit(25, "c"), air=Air()):
        self.air = air
        self.rr = rr
        self.vol = vol
        self.thot = thot
        self.tcold = tcold
    def evaporation(self, tip="snip"):
        if tip == "snip":
            self.ev = self.rr*self.air.evaporation_snip()*(self.thot.c - self.tcold.c)
        else:
            self.ev = self.rr*self.air.evaporation_kurita()*(self.thot.c - self.tcold.c)
        return self.ev
    def set_cycles(self, cycles):
        self.cycles = cycles
        self.evaporation()
        self.mu = self.ev*cycles/(cycles-1)
        self.bd = self.mu/cycles
        self.hti = TimeUnit(self.vol.m3/self.bd.m3_h*math.log(2), "h")

    def efficacy(self):
        wb = self.air.wet_bulb()
        self.eff = (self.thot.c - self.tcold.c)/(self.thot.c - wb.c)
        return float(self.eff)
