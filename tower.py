import math
import requests
import os
from .params import TempP, HumidityP, PressureP
import numpy as np
from copy import deepcopy
try:
    TOKEN = os.environ["OpenWeatherMap"]
except:
    TOKEN = None

class Air:
    def __init__(self, tair=TempP("C").set_value(25), hair=HumidityP("%").set_value(50), pair=PressureP("hg").set_value(748)):
        self.tair, self.hair, self.pair = tair, hair, pair

    def load_weather_conditions(self, loc):
        if TOKEN:
            weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={loc}&APPID={TOKEN}&units=metric").json()
            self.tair = weather["main"]["temp"]
            self.hair = weather["main"]["humidity"]/100
            self.pair = weather["main"]["pressure"]*100
        else:
            raise Exception("PLEASE set openweathermap API  token as an environmental variable OpenWeatherMap")

    def evaporation_snip(self):
        self.ev_coeff = (0.0009971 + 0.00002357 * (self.tair.set_unit("C").value) - 0.0000002143 * (self.tair.set_unit("C").value))
        return self.ev_coeff

    def evaporation_kurita(self):
        self.ev_coeff = (0.575 + 0.011 * self.tair.set_unit("C").value) / 580
        return self.ev_coeff

    def pressure_of_saturated_vapor(self):
        return math.exp((1500.3+23.5*self.tair.set_unit("C").value)/(234 + self.tair.set_unit("C").value))

    def pressure_of_vapor(self):
        return self.hair.set_unit("u").value*self.pressure_of_saturated_vapor()

    def content_of_water(self):
        return 622*self.pressure_of_vapor()/(self.pair.set_unit("pa").value - self.pressure_of_vapor())

    def heat_of_evaporasation(self):
        return (-2.362*self.tair.set_unit("C").value + 2501)

    def enthalpy_wet_air(self):
        return (1.006*self.tair.set_unit("C").value + (self.heat_of_evaporasation() + 1.86*self.tair.set_unit("C").value)*self.content_of_water()/1000)

    def wet_bulb_temp(self):
        ent = self.enthalpy_wet_air()
        self.wb = TempP("C").set_value((-6.14+0.651*ent)/(1+0.0097*ent - 0.00000312 * ent**2))
        return self.wb

    def wet_bulb(self):
        wb = self.tair.set_unit("C").value * np.arctan(0.151977 * (self.hair.set_unit("%").value + 8.313659) ** 0.5) + \
             np.arctan(self.tair.set_unit("C").value + self.hair.set_unit("%").value) - np.arctan(self.hair.set_unit("%").value - 1.676331) + \
             0.00391838 * self.hair.set_unit("%").value ** 1.5 * np.arctan(0.023101 * self.hair.set_unit("%").value) - 4.686035
        return TempP("C").set_value(wb)

    def dew_temp(self):
        a = np.log(self.hair.set_unit("%").value) + 17.62 * self.tair.set_unit("C").value / (243.12 + self.tair.set_unit("C").value)
        dt = 243.12 * a / (17.62 - a)
        return TempP("C").set_value(dt)


class Tower:

    def __init__(self, rr=2100, vol=650, thot=TempP("C").set_value(30), tcold=TempP("C").set_value(25), air=Air()):
        self.air = air
        self.rr = rr
        self.vol = vol
        self.thot = thot
        self.tcold = tcold

    def lg_ratio(self):
        delta_enthalpy_of_water = 4.18 * (self.thot.set_unit("C").value - self.tcold.set_unit("C").value)
        enthalpy_cold_air = self.air.enthalpy_wet_air()
        hair = deepcopy(self.air.hair)
        tair = deepcopy(self.air.tair)
        self.air.hair = HumidityP("%").set_value(100)
        self.air.tair = self.thot
        enthalpy_hot_air = self.air.enthalpy_wet_air()
        self.air.hair = hair
        self.air.tair = tair
        return (enthalpy_hot_air - enthalpy_cold_air) / delta_enthalpy_of_water

    def evaporation_thermo(self):
        x = self.lg_ratio()
        was_water = self.air.content_of_water()
        hair = self.air.hair
        tair = self.air.tair
        self.air.hair = HumidityP("%").set_value(100)
        self.air.tair = self.thot
        became_water = self.air.content_of_water()
        self.air.hair = hair
        self.air.tair = tair
        self.ev = (became_water - was_water) / x / 1000*self.rr
        return self.ev

    def evaporation(self, tip="snip"):
        if tip == "snip":
            self.ev = self.air.evaporation_snip()*(self.thot.set_unit("C").value - self.tcold.set_unit("C").value)*self.rr
        elif tip == "kurita":
            self.ev = self.air.evaporation_kurita() * (self.thot.set_unit("C").value - self.tcold.set_unit("C").value) * self.rr
        else:
            self.ev = self.evaporation_thermo()
        return self.ev

    def set_cycles(self, cycles):
        self.cycles = cycles
        self.evaporation()
        self.mu = self.ev*cycles/(cycles-1)
        self.bd = self.mu/cycles
        self.hti = self.vol/self.bd*math.log(2)

    def efficacy(self):
        wb = self.air.wet_bulb_temp()
        self.eff = (self.thot.set_unit("C").value - self.tcold.set_unit("C").value)/(self.thot.set_unit("C").value - wb.set_unit("C").value)
        return self.eff

