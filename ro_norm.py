from measure_units import *
class Flow:
    def __init__(self, temp: TempUnit=None, pressure: PressureUnit=None,
                 tds: TDSUnit=None, flow:VolumeRateUnit=None):
        self.temp = temp
        self.pressure = pressure
        self.tds = tds
        self.flow = flow
    def __repr__(self):
        return f"Flow(temp={self.temp.c}, pressure={self.pressure.bar}, tds={self.tds.to_ppm()}, flow={self.flow.mph})"
    def __str__(self):
        return f"Flow(temp={self.temp.c}, pressure={self.pressure.bar}, tds={self.tds.to_ppm()}, flow={self.flow.mph})"

class ROUnit:
    def __init__(self, feed:Flow, concentrate:Flow, permeate:Flow, area:AreaUnit):
        self.feed = feed
        self.concentrate = concentrate
        self.permeate = permeate
        self.area = area
    @property
    def rejection(self):
        salts_out = self.permeate.tds.to_ppm() * self.permeate.flow.mph
        salts_in = self.feed.tds.to_ppm() * self.feed.flow.mph
        return (salts_in - salts_out)/salts_in
    @property
    def recovery(self):
        return self.permeate.flow.mph/self.feed.flow.mph
    @property
    def conc_polarisation_factor(self):
        return np.exp(0.75 * 2 * self.recovery / 100 / (2 - self.recovery / 100))**(1 / 8)
    @property
    def temperature_correction_factor(self):
        if self.feed.temp.c > 25:
            return np.exp(2640 * (1 / 298-1 / self.feed.temp.k))
        else:
            return np.exp(3020 * (1 / 298-1 / self.feed.temp.k))
    @property
    def avg_feed_concentrate_concentration_factor(self):
        return np.log(1/(1-(self.recovery/100)))/(self.recovery/100)
    @property
    def avg_feed_concentrate_concentration(self):
        return self.feed.tds.to_ppm()*self.avg_feed_concentrate_concentration_factor*self.conc_polarisation_factor
    @property
    def avg_osmotic_feed_concentrate_pressure(self):
        return 0.0385 * self.avg_feed_concentrate_concentration * \
            self.feed.temp.k / (1000 - (self.avg_feed_concentrate_concentration / 1000)) / 14.5038
    @property
    def osmotic_permeate_pressure(self):
        return 0.0385 * self.permeate.tds.to_ppm() * \
            self.feed.temp.k / (1000 - (self.permeate.tds.to_ppm()/ 1000)) / 14.5038
    @property
    def pressure_drop(self):
        return self.feed.pressure.bar - self.concentrate.pressure.bar
    @property
    def net_driving_pressure(self):
        return self.feed.pressure.bar - self.pressure_drop/2 - self.avg_osmotic_feed_concentrate_pressure + \
        self.osmotic_permeate_pressure - self.permeate.pressure.bar

    @property
    def water_mass_transport_coefficient(self):
        return self.permeate.flow.mps/self.area.m2/self.temperature_correction_factor/self.net_driving_pressure
    @property
    def salt_mass_transport_coefficient(self):
        return self.permeate.tds.to_ppm()*self.permeate.flow.mps/self.area.m2/self.avg_feed_concentrate_concentration/self.temperature_correction_factor

    @property
    def a_lmhbar(self):
        return self.water_mass_transport_coefficient*1000*3600
    @property
    def b_lmh(self):
        return self.salt_mass_transport_coefficient*1000*3600
    def __str__(self):
        return f"ROUnit(feed={self.feed}, concentrate={self.concentrate}, permeate={self.permeate}, area={self.area.m2})"
