from cwtlib.water import Water
from units_converter import Ion, TDSUnit, TemperatureUnit,IonConcentration

ca = IonConcentration("ca", 100, 'ppm')
hco3 = IonConcentration("hco3", 100, 'ppm')
cl = IonConcentration("cl", 100, 'ppm')
so4 = IonConcentration("so4", 100, 'ppm')
temp = TemperatureUnit(25, 'c')
tds = TDSUnit(1000, 'ppm')
ph = 7
water = Water(ph=ph, ca=ca, hco3=hco3, temp=temp, tds=tds, cl=cl, so4=so4)

print(water.phs())
print(water.phs_simple())

