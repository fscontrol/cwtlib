import unittest
import numpy as np
from units_converter import TemperatureUnit, TDSUnit, IonConcentration, Ion, TimeUnit
from ..water import Water

class TestWater(unittest.TestCase):
    def setUp(self):
        # Создаем базовые объекты для тестирования
        self.temp = TemperatureUnit(25, 'c')
        self.tds = TDSUnit(500, 'ppm')
        self.ca = IonConcentration("ca", 100, 'ppm')
        self.hco3 = IonConcentration("hco3", 200, 'ppm')
        self.cl = IonConcentration("cl", 50, 'ppm')
        self.so4 = IonConcentration("so4", 100, 'ppm')
        self.po4 = IonConcentration("po4", 5, 'ppm')
        
        # Создаем объект воды с базовыми параметрами
        self.water = Water(
            ph=7.5,
            ca=self.ca,
            hco3=self.hco3,
            temp=self.temp,
            tds=self.tds,
            cl=self.cl,
            so4=self.so4,
            po4=self.po4,
        )

    def test_initialization(self):
        """Проверка корректной инициализации объекта Water"""
        self.assertEqual(self.water.ph, 7.5)
        self.assertEqual(self.water.ca.caco3, self.ca.caco3)
        self.assertEqual(self.water.hco3.caco3, self.hco3.caco3)
        self.assertEqual(self.water.temp.c, 25)
        self.assertAlmostEqual(self.water.tds.ppm, 500, places=0)

    def test_cycles(self):
        """Проверка работы с циклами концентрирования"""
        initial_ph = self.water.ph
        self.water.cycles = 2
        self.assertEqual(self.water.cycles, 2)
        self.assertNotEqual(self.water.ph, initial_ph)  # pH должен измениться
        self.assertEqual(self.water.ca.caco3, self.ca.caco3 * 2)
        self.assertEqual(self.water.hco3.caco3, self.hco3.caco3 * 2)

    def test_ph_predict(self):
        """Проверка предсказания pH"""
        predicted_ph = self.water.ph_predict()
        self.assertTrue(4.5 <= predicted_ph <= 10)

    def test_phs(self):
        """Проверка расчета pHs"""
        phs = self.water.phs()
        self.assertIsInstance(phs, float)
        self.assertTrue(phs > 0)

    def test_lsi(self):
        """Проверка расчета индекса Ланжелье"""
        lsi = self.water.lsi()
        self.assertIsInstance(lsi, float)

    def test_rzn(self):
        """Проверка расчета индекса Ризнара"""
        rzn = self.water.rzn()
        self.assertIsInstance(rzn, float)

    def test_larsen(self):
        """Проверка расчета индекса Ларсена"""
        larsen = self.water.larsen()
        self.assertIsInstance(larsen, float)
        self.assertTrue(larsen >= 0)

    def test_larsen_modified(self):
        """Проверка расчета модифицированного индекса Ларсена"""
        larsen_mod = self.water.larsen_modified(TimeUnit(24, "h"))  # 24 часа
        self.assertIsInstance(larsen_mod, float)
        self.assertTrue(larsen_mod >= 0)

    def test_po4_si(self):
        """Проверка расчета индекса насыщения по фосфатам"""
        po4_si = self.water.po4_si()
        self.assertIsInstance(po4_si, float)


    def test_caso4_si(self):
        """Проверка расчета индекса насыщения по сульфату кальция"""
        caso4_si = self.water.caso4_si()
        self.assertIsInstance(caso4_si, float)
        self.assertTrue(caso4_si >= 0)

    def test_ionic_strength(self):
        """Проверка расчета ионной силы"""
        ionic_strength = self.water.ionic_strength()
        self.assertIsInstance(ionic_strength, float)
        self.assertTrue(ionic_strength > 0)


if __name__ == '__main__':
    unittest.main() 