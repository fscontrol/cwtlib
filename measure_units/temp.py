from measure_units.param import Param
class TempP(Param):
    units = dict(
        C=dict(read=lambda x: x, write=lambda x: x),
        F=dict(write=lambda x: (x - 32) * 5 / 9, read=lambda x: x * 9 / 5 + 32),
        K=dict(write=lambda x: x - 273.15, read=lambda x: x + 273.15)
    )
