from collections import OrderedDict
from copy import deepcopy
class Param:
    def __init__(self, unit=None, value=None):
        self._unit = unit
        self._value = value
        self.to_external_funcs = {}
        self.to_internal_funcs = {}

    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, u):
        if u in self.units:
            self._unit = u
        else:
            raise Exception("Uknown unit")
    def set_unit_list(self, l):
        self.units = l

    def get_unit_list(self):
        return self.units.join("; ")
    def to_internal_list(self, l):
        self.to_internal_funcs = dict(zip(self.units, l))

    def to_external_list(self, l):
        self.to_external_funcs = dict(zip(self.units, l))
    @property
    def value(self):
        if self._value is None:
            raise Exception("Value of param is not set")
        return self.to_external_funcs[self._unit](self._value)
    @value.setter
    def value(self, v):
        try:
            v = float(v)
        except:
            raise Exception("Значение параметра должно быть числом")
        self._value = self.to_internal_funcs[self._unit](v)

    def set_value(self,v):
        self.value = v
        return self
    def set_unit(self, u):
        self.unit= u
        return self

    def __str__(self):
        return f"{self.__class__} {self.value} {self.unit}"

    def additional_check_add_mul_params(self):
        return True

    def __add__(self, other):
        ans = deepcopy(self)
        if (type(other) in [int, float]):
            return (ans.set_value(self.value + other))
        elif type(other) == type(self):
            ans._value = self._value + other._value
            return ans
        else:
            raise Exception("Проблемы со операциями единиц параметров")
        return ans

    def __mul__(self, other):
        ans = deepcopy(self)
        if not (type(other) in [int, float]):
            raise Exception("Умножать можно только на число")
        ans._value *= other
        return ans

    def __sub__(self, other):
        ans = deepcopy(self)
        if (type(other) in [int, float]):
            return (ans.set_value(self.value - other))
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
    def __init__(self, unit="C"):
        super().__init__(unit=unit)
        super().set_unit_list(["C", "F", "K"])
        super().to_internal_list([
            lambda x: x,
            lambda x: (x-32)*5/9,
            lambda x: x-273.15
        ])
        super().to_external_list([
            lambda x: x,
            lambda x: x*9/5+32,
            lambda x: x + 273.15
        ])

class HumidityP(Param):
    def __init__(self, unit="%"):
        super().__init__(unit=unit)
        super().set_unit_list(["%", "u"])
        super().to_internal_list([
            lambda x: x/100,
            lambda x: x
        ])
        super().to_external_list([
            lambda x: x*100,
            lambda x: x
        ])

class PressureP(Param):
    def __init__(self, unit="pa"):
        def to_internal(k):
            def calc(x):
                return k*x
            return calc
        def to_external(k):
            def calc(x):
                return x/k
            return calc
        coeffs = OrderedDict({"pa":1, "kpa": 1000, "bar": 100000, "atm": 101325, "psi": 6894.76, "hg": 133.321995, "water": 9.80638, "heksa": 100})
        super().__init__(unit=unit)
        super().set_unit_list(coeffs.keys())
        for n, k in coeffs.items():
            self.to_internal_funcs[n] = to_internal(k)
            self.to_external_funcs[n] = to_external(k)

class IonException(Exception):
    message = "Ion is not in the list"
    '''ion exception'''
    pass


class Ion:
    IONS = {
            "cl" : [35.5, 1],
            "so4" : [98, 2],
            "alk" : [61, 1],
            "hrd" : [40, 2],
            "ca" : [40, 2],
            "mg" : [24, 2],
            "po4" : [95, 3],
            "fe" : [56, 2],
            "zn" : [65, 2],
            "hco3" : [61, 2],
            "nh4" : [18, 1],
             "sio2": [59, 2]
        }
    def __init__(self, name):
        try:
            self.molar_weight = Ion.IONS[name][0]
            self.charge = Ion.IONS[name][1]
            self.equiv_weight = self.molar_weight/self.charge
            self.name = name
        except:
            raise IonException


class ConcP(Param):
    hardness_list = ["ca", "hrd", "mg"]
    def __init__(self, unit="meq", ion="cl"):
        super().__init__(unit=unit)
        super().set_unit_list(["meq", "ppm", "ppb", "mmol", "caco3", "mol"])
        self._ion = Ion(ion)
        self.set_funcs()

    def set_funcs(self):
        super().to_internal_list([
            lambda x: x,
            lambda x: x/self._ion.equiv_weight,
            lambda x: x/self._ion.equiv_weight/1000,
            lambda x: x*self._ion.molar_weight/self._ion.equiv_weight,
            lambda x: x/50,
            lambda x: x*self._ion.molar_weight/self._ion.equiv_weight*1000
        ])
        super().to_external_list([
            lambda x: x,
            lambda x: x*self._ion.equiv_weight,
            lambda x: x*self._ion.equiv_weight*1000,
            lambda x: x*self._ion.equiv_weight/self._ion.molar_weight,
            lambda x: x*50,
            lambda x: x * self._ion.equiv_weight / self._ion.molar_weight/1000,
        ])

    def set_ion(self, i):
        try:
            self._ion = Ion(i)
            self.set_funcs()
            return self
        except IonException as e:
            raise Exception(e.message)

    @property
    def ion(self):
        return self._ion.name

    @ion.setter
    def ion(self, i):
        try:
            self._ion = Ion(i)
            self.set_funcs()
        except IonException as e:
            raise Exception(e.message)

    def __add__(self, other):
        if type(other)==type(self) and self.ion != other.ion and self.ion in ConcP.hardness_list and other.ion in ConcP.hardness_list:
            ans = super().__add__(other)
            return ans.set_unit("meq").set_ion("hrd")
        else:
            super().__add__(other)

    def __sub__(self, other):
        if type(other)==type(self) and self.ion != other.ion and self.ion in ConcP.hardness_list and other.ion in ConcP.hardness_list:
            ans = super().__sub__(other)
            return ans.set_unit("meq").set_ion("hrd")
        else:
            super().__sub__(other)


    def __str__(self):
        return f"{self.ion} = {self.value} {self.unit}"

class TDSP(Param):
    def set_funcs(self):
        super().to_internal_list([
            lambda x: x,
            lambda x: x * self.tds_coeff,
            lambda x: x * 1000 * self.tds_coeff
        ])
        super().to_external_list([
            lambda x: x,
            lambda x: x / self.tds_coeff,
            lambda x: x / self.tds_coeff / 1000
        ])
    def __init__(self, unit="ppm", tds_coeff = 0.5):
        super().__init__(unit=unit)
        self.tds_coeff = tds_coeff
        super().set_unit_list(["ppm", "usm", "msm"])
        self.set_funcs()


