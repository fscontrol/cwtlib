from cwtlib.units.unit import Unit

class PowerUnit(Unit):
    units = dict(
        default = dict(a=1, b=0),
        W = dict(a=1, b=0),
        kW = dict(a=1e3, b=0),
        MW = dict(a=1e6, b=0),
        GW = dict(a=1e9, b=0),
        hp = dict(a=745.7, b=0),
        BTU_h = dict(a=0.293071, b=0),
        BTU_min = dict(a=17.5843, b=0),
        BTU_s = dict(a=1055.06, b=0),
        kcal_h = dict(a=1.163, b=0),
        kcal_min = dict(a=69.78, b=0),
        kcal_s = dict(a=4186.8, b=0),
        cal_h = dict(a=0.001163, b=0),
        cal_min = dict(a=0.06978, b=0),
        cal_s = dict(a=4.1868, b=0),
        ft_lb_s = dict(a=1.35582, b=0),
        ft_lb_min = dict(a=81.349, b=0),
        ft_lb_h = dict(a=4880.94, b=0),
        ft_pound_s = dict(a=1.35582, b=0),
        ft_pound_min = dict(a=81.349, b=0),
        ft_pound_h = dict(a=4880.94, b=0),
        kgf_m_s = dict(a=9.80665, b=0),
        kgf_m_min = dict(a=588.399, b=0),
        kgf_m_h = dict(a=35303.9, b=0),
        kgf_meter_s = dict(a=9.80665, b=0),
        kgf_meter_min = dict(a=588.399, b=0),
        kgf_meter_h = dict(a=35303.9, b=0),
        kgf_cm_s = dict(a=0.0980665, b=0),
        kgf_cm_min = dict(a=5.88399, b=0),
        kgf_cm_h = dict(a=353.039, b=0),
    )