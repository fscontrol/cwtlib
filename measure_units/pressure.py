from measure_units.param import Param
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
