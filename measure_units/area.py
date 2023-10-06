from cwtlib.measure_units.param import Param

class LengthP(Param):
    units = dict(
        m = dict(read=lambda x: x, write=lambda x: x),
        mm = dict(read=lambda x: x*1000, write=lambda x: x/1000),
        cm = dict(read=lambda x: x*100, write=lambda x: x/100),
        km = dict(read=lambda x: x/1000, write=lambda x: x*1000),
        ft = dict(read=lambda x: x/0.3048, write=lambda x: x*0.3048),
        mile = dict(read=lambda x: x/1609.344, write=lambda x: x*1609.344),
        inch = dict(read=lambda x: x/0.0254, write=lambda x: x*0.0254),
        yard = dict(read=lambda x: x/0.9144, write=lambda x: x*0.9144)
    )

class AreaP(Param):
    units = dict(
        m2 = dict(read=lambda x: x, write=lambda x: x),
        mm2 = dict(read=lambda x: x*1000000, write=lambda x: x/1000000),
        cm2 = dict(read=lambda x: x*10000, write=lambda x: x/10000),
        km2 = dict(read=lambda x: x/1000000, write=lambda x: x*1000000),
        ft2 = dict(read=lambda x: x/0.09290304, write=lambda x: x*0.09290304),
        acre = dict(read=lambda x: x/4046.8564224, write=lambda x: x*4046.8564224),
        ha = dict(read=lambda x: x/10000, write=lambda x: x*10000),
        inch2 = dict(read=lambda x: x/0.00064516, write=lambda x: x*0.00064516),
        yard2 = dict(read=lambda x: x/0.83612736, write=lambda x: x*0.83612736)
    )