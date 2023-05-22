from collections import OrderedDict
from copy import deepcopy
class Param:
    units = {}
    def __init__(self, unit=None, value=None):
        self._unit = unit
        self._value = value

    def set_value(self, value):
        self._value = value
        return self

    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, u):
        if u in self.units:
            self._unit = u
        else:
            raise Exception("Uknown unit")

    @property
    def value(self):
        if self._value is None:
            raise Exception("Value of param is not set")
        return self.units[self._unit]["read"](self._value)
    @value.setter
    def value(self, v):
        try:
            v = float(v)
        except:
            raise Exception("Значение параметра должно быть числом")
        self._value = self.units[self._unit]["write"](v)

    def __setattr__(self, name, value):
        if name != "units" and name in self.units.keys():
            self.unit = name
            self.value = value
            return
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        if  name in self.units.keys():
            self.unit = name
            return self.value
        else:
            return getattr(super(), name)

    def __str__(self):
        return f"{self.__class__} {self.value} {self.unit}"

    def additional_check_add_mul_params(self):
        return True

    def __add__(self, other):
        ans = deepcopy(self)
        if (type(other) in [int, float]):
            ans._value = self._value + other
            return ans
        elif type(other) == type(self):
            ans._value = self._value + other._value
            return ans
        else:
            raise Exception("Проблемы со операциями единиц параметров")

    def __mul__(self, other):
        ans = deepcopy(self)
        if not (type(other) in [int, float]):
            raise Exception("Умножать можно только на число")
        ans._value *= other
        return ans

    def __sub__(self, other):
        ans = deepcopy(self)
        if (type(other) in [int, float]):
            ans._value = self._value - other
            return ans
        elif type(other) == type(self):
            ans._value = self._value - other._value
            return ans
        else:
            raise Exception("Проблемы со операциями единиц параметров")
        return ans

    def __truediv__(self, other):
        ans = deepcopy(self)
        if not (type(other) in [int, float]):
            raise Exception("Делить можно только на число")
        ans._value /= other
        return ans

class TempP(Param):
    units = dict(
        C=dict(read=lambda x: x, write=lambda x: x),
        F=dict(write=lambda x: (x - 32) * 5 / 9, read=lambda x: x * 9 / 5 + 32),
        K=dict(write=lambda x: x - 273.15, read=lambda x: x + 273.15)
    )

class HumidityP(Param):
    units = dict(
        proc = dict(read=lambda x: x, write=lambda x: x),
        ratio = dict(read=lambda x: x/100, write=lambda x: x*100)
    )

class PressureP(Param):
    units = dict(
        pa = dict(read=lambda x: x, write=lambda x: x),
        kpa = dict(read=lambda x: x/1000, write=lambda x: x*1000),
        bar = dict(read=lambda x: x/100000, write=lambda x: x*100000),
        atm = dict(read=lambda x: x/101325, write=lambda x: x*101325),
        psi = dict(read=lambda x: x/6894.76, write=lambda x: x*6894.76),
        hg = dict(read=lambda x: x/133.321995, write=lambda x: x*133.321995),
        water = dict(read=lambda x: x/9.80638, write=lambda x: x*9.80638),
        heksa = dict(read=lambda x: x/100, write=lambda x: x*100)
    )

class Ion:
    IONS = {
            "cl" : [35.5, 1, -1],
            "so4" : [98, 2, -1],
            "alk" : [61, 1, -1],
            "hrd" : [40, 2, 1],
            "ca" : [40, 2, 1],
            "mg" : [24, 2, 1],
            "po4" : [95, 3, -1],
            "fe" : [56, 2, 1],
            "zn" : [65, 2, 1],
            "hco3" : [61, 2, -1],
            "nh4" : [18, 1, 1],
             "sio2": [59, 2, -1]
        }
    def __init__(self, name):
        try:
            self.molar_weight = Ion.IONS[name][0]
            self.charge = Ion.IONS[name][1]
            self.equiv_weight = self.molar_weight/self.charge
            self.charge = self.charge * Ion.IONS[name][2]
            self.name = name
        except:
            raise Exception("Unknown ion")

class ConcP(Param):
    hardness_list = ["ca", "hrd", "mg"]
    def __init__(self, unit="meq", ion="cl"):
        super().__init__(unit=unit)
        self._ion = Ion(ion)
        self.set_funcs()

    def set_funcs(self):
        self.units = dict(
            meq = dict(read=lambda x: x, write=lambda x: x),
            ppm = dict(read=lambda x: x*self._ion.equiv_weight, write=lambda x: x/self._ion.equiv_weight),
            ppb = dict(read=lambda x: x*self._ion.equiv_weight*1000, write=lambda x: x/self._ion.equiv_weight/1000),
            mmol = dict(read=lambda x: x/self._ion.molar_weight*self._ion.equiv_weight, write=lambda x: x/self._ion.equiv_weight*self._ion.molar_weight),
            caco3 = dict(read=lambda x: x*50, write=lambda x: x/50),
            mol = dict(read=lambda x: x/self._ion.molar_weight*self._ion.equiv_weight/1000, write=lambda x: x / self._ion.equiv_weight * self._ion.molar_weight*1000)
        )


    @property
    def ion(self):
        return self._ion.name

    @ion.setter
    def ion(self, i):
        self._ion = Ion(i)
        self.set_funcs()

    def __add__(self, other):
        if type(other) in [float, int, type(self)]:
            if type(other) in [float, int]:
                ans = deepcopy(self)
                ans._value += other
                return ans
            elif type(other) == type(self):
                if self.ion == other.ion:
                    ans = deepcopy(self)
                    ans._value += other.value
                    return ans
                elif self.ion in ConcP.hardness_list and other.ion in ConcP.hardness_list:
                    ans = deepcopy(self)
                    ans._value += other.value
                    ans.ion = "hrd"
                    return ans
                else:
                    raise Exception("Нельзя складывать разные ионы")

    def __sub__(self, other):
        if type(other) in [float, int, type(self)]:
            if type(other) in [float, int]:
                ans = deepcopy(self)
                ans._value -= other
                return ans
            elif type(other) == type(self):
                if self.ion == other.ion:
                    ans = deepcopy(self)
                    ans._value -= other.value
                    return ans
                elif self.ion in ConcP.hardness_list and other.ion in ConcP.hardness_list:
                    ans = deepcopy(self)
                    ans._value -= other.value
                    ans.ion = "hrd"
                    return ans
                else:
                    raise Exception("Нельзя вычитать разные ионы")
    def __str__(self):
        return f"{self.ion} = {self.value} {self.unit}"

class TDSP(Param):
    def set_funcs(self):
        self.units = dict(
            ppm = dict(read=lambda x: x, write=lambda x: x),
            usm = dict(read=lambda x: x*self.tds_coeff, write=lambda x: x/self.tds_coeff),
        )
    def __init__(self, unit="ppm", tds_coeff = 2):
        super().__init__(unit=unit)
        self.tds_coeff = tds_coeff
        self.set_funcs()


