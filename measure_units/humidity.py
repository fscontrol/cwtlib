from cwtlib.measure_units.param import Param
class HumidityP(Param):
    units = dict(
        proc = dict(read=lambda x: x, write=lambda x: x),
        ratio = dict(read=lambda x: x/100, write=lambda x: x*100)
    )