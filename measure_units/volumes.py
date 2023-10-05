from measure_units.param import Param
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
        h = dict(read=lambda x: x/3600, write=lambda x: x/3600),
        d = dict(read=lambda x: x/3600/24, write=lambda x: x*3600*24)
    )


class VolumeRate:
    def __init__(self, value, unit):
        self.base_value = self.to_base(value, unit)

    def to_base(self, value, unit):
        volume_unit, time_unit = unit.split('_')
        volume_to_base = VolumeP.units[volume_unit]['read'](value)
        time_to_base = TimeP.units[time_unit]['read'](1)
        return volume_to_base / time_to_base

    def from_base(self, volume_unit, time_unit):
        volume_from_base = VolumeP.units[volume_unit]['write'](self.base_value)
        time_from_base = TimeP.units[time_unit]['write'](1)
        return volume_from_base * time_from_base

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

