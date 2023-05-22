import math
import requests
import os
from params import TempP, HumidityP, PressureP
import numpy as np
from copy import deepcopy
try:
    TOKEN = os.environ["OpenWeatherMap"]
except:
    TOKEN = None

class Air:
    def __init__(self, tair=TempP("C").set_value(25), hair=HumidityP("proc").set_value(50), pair=PressureP("hg").set_value(748)):
        self.tair, self.hair, self.pair = tair, hair, pair

    def load_weather_conditions(self, loc):
        if TOKEN:
            weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={loc}&APPID={TOKEN}&units=metric").json()
            self.tair.C = weather["main"]["temp"]
            self.hair.proc = weather["main"]["humidity"]
            self.pair.heksa = weather["main"]["pressure"]*100
        else:
            raise Exception("PLEASE set openweathermap API  token as an environmental variable OpenWeatherMap")

    def evaporation_snip(self):
        self.ev_coeff = (0.0009971 + 0.00002357 * (self.tair.C) - 0.0000002143 * (self.tair.C))
        return self.ev_coeff

    def evaporation_kurita(self):
        self.ev_coeff = (0.575 + 0.011 * self.tair.C) / 580
        return self.ev_coeff

    def wet_bulb(self):
        wb = self.tair.C * np.arctan(0.151977 * (self.hair.proc + 8.313659) ** 0.5) + \
             np.arctan(self.tair.C + self.hair.proc) - np.arctan(self.hair.proc - 1.676331) + \
             0.00391838 * self.hair.proc ** 1.5 * np.arctan(0.023101 * self.hair.proc) - 4.686035
        return TempP("C").set_value(wb)

class Tower:
    def __init__(self, rr=2100, vol=650, thot=TempP("C").set_value(30), tcold=TempP("C").set_value(25), air=Air()):
        self.air = air
        self.rr = rr
        self.vol = vol
        self.thot = thot
        self.tcold = tcold

    def evaporation(self, tip="snip"):
        if tip == "snip":
            self.ev = self.air.evaporation_snip()*(self.thot.C - self.tcold.C)*self.rr
        else:
            self.ev = self.air.evaporation_kurita() * (self.thot.C - self.tcold.C) * self.rr
        return self.ev

    def set_cycles(self, cycles):
        self.cycles = cycles
        self.evaporation()
        self.mu = self.ev*cycles/(cycles-1)
        self.bd = self.mu/cycles
        self.hti = self.vol/self.bd*math.log(2)

    def efficacy(self):
        wb = self.air.wet_bulb()
        self.eff = (self.thot.C - self.tcold.C)/(self.thot.C - wb.C)
        return self.eff

