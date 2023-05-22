import unittest
import params

class TestTempParam(unittest.TestCase):
    def setUp(self):
        self.temp = params.TempP()
        self.temp.C = 100

    def test_set_farenheit(self):
        self.temp.unit = "F"
        self.temp.F = 212
        self.assertEqual(self.temp.C, 100)
        self.assertEqual(self.temp.K, 373.15)

    def test_multiply_5(self):
        self.temp.C = self.temp.F * 5
        self.assertEqual(self.temp.C, 1060)

    def test_sum_diff(self):
        temp2 = params.TempP()
        temp2.C = 100
        temp2 = self.temp + temp2
        self.assertEqual(temp2.C, 200)

    def test_divide(self):
        self.temp.C = 100
        self.temp = self.temp / 2
        self.assertEqual(self.temp.C, 50)

class TestHumidityParam(unittest.TestCase):
    def setUp(self):
        self.hum = params.HumidityP()
        self.hum.proc = 50

    def test_set_ratio(self):
        self.assertEqual(self.hum.ratio, 0.5)

    def test_ratio_to_proc(self):
        self.hum.ratio = 0.5
        self.assertEqual(self.hum.proc, 50)


class TestPressureParam(unittest.TestCase):
    def setUp(self):
        self.press = params.PressureP()
        self.press.kpa = 101.325

    def test_pa(self):
        self.assertAlmostEqual(self.press.pa, 101325, 1)
        self.press.pa = 101325
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

    def test_kpa(self):
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

    def test_atm(self):
        self.assertAlmostEqual(self.press.atm, 1, 1)
        self.press.atm = 1
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

    def test_bar(self):
        self.assertAlmostEqual(self.press.bar, 1.01325, 1)
        self.press.bar = 1.01325
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

    def test_hg(self):
        self.assertAlmostEqual(self.press.hg, 760, 1)
        self.press.hg = 760
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

    def test_water(self):
        self.assertAlmostEqual(self.press.water, 10332.274527, 0)
        self.press.water = 10332.274527
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

    def test_psi(self):
        self.assertAlmostEqual(self.press.psi, 14.695948775513, 1)
        self.press.psi = 14.695948775513
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

    def test_heksa(self):
        self.assertAlmostEqual(self.press.heksa, 1013.25, 1)
        self.press.heksa = 1013.25
        self.assertAlmostEqual(self.press.kpa, 101.325, 1)

class TestIon(unittest.TestCase):
    def setUp(self):
        self.ion = params.Ion("po4")
    def test_ion(self):
        self.assertAlmostEqual(self.ion.molar_weight, 95, 0)
        self.assertAlmostEqual(self.ion.charge, -3, 0)
        self.assertAlmostEqual(self.ion.equiv_weight, 31.6666666666667, 0)

class ConcP(unittest.TestCase):
    def setUp(self):
        self.po4 = params.ConcP(unit="meq", ion="po4")
        self.po4.meq = 1
        self.ca = params.ConcP(unit="meq", ion="ca")
        self.ca.meq = 2
        self.mg = params.ConcP(unit="meq", ion="mg")
        self.mg.meq = 3

    def test_ppm(self):
        self.assertAlmostEqual(self.po4.ppm, 31.6666666666667, 0)
        self.po4.ppm = 31.6666666666667
        self.assertAlmostEqual(self.po4.meq, 1, 0)

    def test_mol(self):
        self.assertAlmostEqual(self.po4.mol, 0.001/3, 3)
        self.po4.mol = 0.001/3
        self.assertAlmostEqual(self.po4.meq, 1, 0)

    def test_mmol(self):
        self.assertAlmostEqual(self.po4.mmol, 1/3, 3)
        self.po4.mmol = 1/3
        self.assertAlmostEqual(self.po4.meq, 1, 0)

    def test_caco3(self):
        self.assertAlmostEqual(self.po4.caco3, 50, 3)
        self.po4.caco3 = 50
        self.assertAlmostEqual(self.po4.meq, 1, 0)

    def test_add_one_ions(self):
        self.po4 = self.po4*2
        self.assertEqual(self.po4.meq, 2)
        self.po4 = self.po4 - 1
        self.assertEqual(self.po4.meq, 1)

    def test_add_two_ions(self):
        self.assertRaises(Exception, lambda: self.po4 + self.ca)
        self.assertRaises(Exception, lambda: self.po4 - self.ca)
        x = self.mg + self.ca
        y = self.mg - self.ca
        self.assertEqual(x.meq, 5)
        self.assertEqual(y.meq, 1)

class TestTDS(unittest.TestCase):
    def setUp(self):
        self.tds = params.TDSP()
        self.tds.ppm = 1000
    def test_us(self):
        self.assertAlmostEqual(self.tds.usm, 2000, 0)
        self.tds.usm = 1000
        self.assertAlmostEqual(self.tds.ppm, 500, 0)



if __name__ == '__main__':
    unittest.main()