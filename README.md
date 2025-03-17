# CWTlib

Библиотека для расчетов в области водоподготовки и водоочистки. Включает в себя расчеты для градирен, обратного осмоса и химического анализа воды.

## Установка

```bash
pip install cwtlib2
```

## Требования

- Python >= 3.8
- numpy
- requests
- cwt-units-converter

## Основные компоненты

### 1. Расчеты воды (water.py)

Класс `Water` для расчета различных индексов насыщения и химических параметров воды:

```python
from cwtlib2.water import Water
from units_converter import TemperatureUnit, TDSUnit, IonConcentration

# Создание объекта воды
water = Water(
    ph=7.5,
    ca=IonConcentration(100, 'ppm', 'Ca'),
    hco3=IonConcentration(200, 'ppm', 'HCO3'),
    temp=TemperatureUnit(25, 'C'),
    tds=TDSUnit(500, 'ppm')
)

# Расчет индексов
lsi = water.lsi()  # Индекс Ланжелье
rzn = water.rzn()  # Индекс Ризнара
```

#### Основные методы:

- `ph_predict()` - предсказание pH
- `phs()` - расчет pHs
- `lsi()` - индекс Ланжелье
- `rzn()` - индекс Ризнара
- `larsen()` - индекс Ларсена
- `po4_si()` - индекс насыщения по фосфатам
- `sio2_si()` - индекс насыщения по кремнезему
- `caso4_si()` - индекс насыщения по сульфату кальция

### 2. Расчеты градирен (tower.py)

Класс `Tower` для расчета параметров градирен:

```python
from cwtlib2.tower import Tower, Air
from units_converter import TemperatureUnit, PressureUnit, VolumeUnit, FlowRateUnit

# Создание объекта воздуха
air = Air(
    tair=TemperatureUnit(26, "c"),
    hair=HumidityUnit(50, "percent"),
    pair=PressureUnit(748, "mmhg")
)

# Создание объекта градирни
tower = Tower(
    rr=FlowRateUnit(2100, "m3_h"),
    vol=VolumeUnit(650, "m3"),
    thot=TemperatureUnit(30, "c"),
    tcold=TemperatureUnit(25, "c"),
    air=air
)

# Расчеты
ev = tower.evaporation()  # Расчет испарения
eff = tower.efficacy()    # Расчет эффективности
```

#### Основные методы:

- `evaporation()` - расчет испарения (методы СНИП и Курита)
- `efficacy()` - расчет эффективности градирни
- `set_cycles()` - установка циклов концентрирования

### 3. Расчеты обратного осмоса (ro_norm.py)

Класс `RONorm` для расчета параметров обратноосмотических установок:

```python
from cwtlib2.ro_norm import RONorm
from units_converter import TemperatureUnit, PressureUnit, FlowRateUnit

ro = RONorm(
    temp=TemperatureUnit(25, "c"),
    pressure=PressureUnit(6, "bar"),
    flow=FlowRateUnit(10, "m3_h")
)

# Расчеты
recovery = ro.recovery()  # Расчет степени извлечения
```

## Тестирование

Для запуска тестов:

```bash
python -m unittest discover tests
```

## Лицензия

MIT License

## Авторы

- Ваше имя (your.email@example.com)

## Поддержка

При возникновении проблем или вопросов, пожалуйста, создавайте issue в репозитории проекта.
