from copy import deepcopy
class Param:
    units = {}
    def __init__(self, unit=None):
        self._unit = unit

    def set_value(self, value):
        self.value = value
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
        if name != "measure_units" and name in self.units.keys():
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
