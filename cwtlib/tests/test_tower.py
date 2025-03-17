import unittest
import numpy as np
from units_converter import *
from ..tower import Air
from ..tower import Tower


class TestAir(unittest.TestCase):
    def setUp(self):
        self.air = Air(
            tair=TemperatureUnit(26, "c"),
            hair=HumidityUnit(50, "perc"),
            pair=PressureUnit(748, "mmhg")
        )

    def test_initialization(self):
        """Проверка корректной инициализации объекта Air"""
        self.assertEqual(self.air.tair.c, 26)
        self.assertEqual(self.air.hair.perc, 50)
        self.assertEqual(self.air.pair.mmhg, 748)

    def test_evaporation_snip(self):
        """Проверка расчета коэффициента испарения по СНИП"""
        ev_coeff = self.air.evaporation_snip()
        self.assertIsInstance(ev_coeff, float)
        self.assertTrue(0 < ev_coeff < 1)

    def test_evaporation_kurita(self):
        """Проверка расчета коэффициента испарения по Курите"""
        ev_coeff = self.air.evaporation_kurita()
        self.assertIsInstance(ev_coeff, float)
        self.assertTrue(0 < ev_coeff < 1)

    def test_wet_bulb(self):
        """Проверка расчета температуры мокрого термометра"""
        wb = self.air.wet_bulb()
        self.assertIsInstance(wb, TemperatureUnit)
        self.assertTrue(wb.c < self.air.tair.c)
        self.assertTrue(wb.c > 0)

class TestTower(unittest.TestCase):
    def setUp(self):
        self.air = Air(
            tair=TemperatureUnit(26, "c"),
            hair=HumidityUnit(50, "perc"),
            pair=PressureUnit(748, "mmhg")
        )
        self.tower = Tower(
            rr=FlowRateUnit(2100, "m3_h"),
            vol=VolumeUnit(650, "m3"),
            thot=TemperatureUnit(30, "c"),
            tcold=TemperatureUnit(25, "c"),
            air=self.air
        )

    def test_initialization(self):
        """Проверка корректной инициализации объекта Tower"""
        self.assertEqual(self.tower.rr.m3_h, 2100)
        self.assertEqual(self.tower.vol.m3, 650)
        self.assertEqual(self.tower.thot.c, 30)
        self.assertEqual(self.tower.tcold.c, 25)
        self.assertIsInstance(self.tower.air, Air)

    def test_evaporation_snip(self):
        """Проверка расчета испарения по СНИП"""
        ev = self.tower.evaporation(tip="snip")
        self.assertIsInstance(ev, FlowRateUnit)
        self.assertTrue(ev.m3_h > 0)

    def test_evaporation_kurita(self):
        """Проверка расчета испарения по Курите"""
        ev = self.tower.evaporation(tip="kurita")
        self.assertIsInstance(ev, FlowRateUnit)
        self.assertTrue(ev.m3_h > 0)

    def test_set_cycles(self):
        """Проверка установки циклов концентрирования"""
        cycles = 3
        self.tower.set_cycles(cycles)
        self.assertEqual(self.tower.cycles, cycles)
        self.assertTrue(self.tower.mu.m3_h > 0)
        self.assertTrue(self.tower.bd.m3_h > 0)
        self.assertTrue(self.tower.hti.h > 0)

    def test_efficacy(self):
        """Проверка расчета эффективности градирни"""
        eff = self.tower.efficacy()
        self.assertIsInstance(eff, float)
        self.assertTrue(0 < eff < 1)


    def test_temperature_difference(self):
        """Проверка корректности разницы температур"""
        self.assertTrue(self.tower.thot.c > self.tower.tcold.c)

if __name__ == '__main__':
    unittest.main() 