from cwtlib.measure_units.param import Param
class VolumeP(Param):
    units = dict(
        l = dict(read=lambda x: x, write=lambda x: x),
        ml = dict(read=lambda x: x*1000, write=lambda x: x/1000),
        m3 = dict(read=lambda x: x/1000, write=lambda x: x*1000),
        gallon = dict(read=lambda x: x/3.78, write=lambda x: x*3.78),
        barrel = dict(read=lambda x: x/158.987, write=lambda x: x*158.987)
    )
class TimeP(Param):
    units = dict(
        s = dict(read=lambda x: x, write=lambda x: x),
        m = dict(read=lambda x: x/60, write=lambda x: x*60),
        h = dict(read=lambda x: x/3600, write=lambda x: x*3600),
        d = dict(read=lambda x: x/3600/24, write=lambda x: x*3600*24)
    )


class VolumeRate:
    def __init__(self, value, unit):
        self.base_value = self.to_base(value, unit)

    def to_base(self, value, unit):
        volume_unit, time_unit = unit.split('_')
        vol = VolumeP(volume_unit).set_value(value)
        time = TimeP(time_unit).set_value(1)
        return vol.l/time.s

    def from_base(self, volume_unit, time_unit):
        vol = VolumeP("l").set_value(self.base_value)
        vol.unit = volume_unit
        time = TimeP("s").set_value(1)
        time.unit = time_unit
        return vol.value/time.value

    def __getattr__(self, name):
        if "_" in name:
            volume_unit, time_unit = name.split('_')
            if volume_unit in VolumeP.units and time_unit in TimeP.units:
                return self.from_base(volume_unit, time_unit)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == "base_value":
            super().__setattr__(name, value)
        else:
            if "_" in name:
                volume_unit, time_unit = name.split('_')
                if volume_unit in VolumeP.units and time_unit in TimeP.units:
                    self.base_value = self.to_base(value, name)
                    return
            super().__setattr__(name, value)

