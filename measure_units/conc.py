from measure_units.param import Param
from copy import deepcopy
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

    def __init__(self, v=0, unit="meq", ion="cl"):
        super().__init__(unit=unit)
        self._ion = Ion(ion)
        self.set_funcs()
        self.value = v

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
    def __init__(self, unit="ppm", v=0, tds_coeff = 2):
        super().__init__(unit=unit)
        self.tds_coeff = tds_coeff
        self.set_funcs()
        self.value = v


