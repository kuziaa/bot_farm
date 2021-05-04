import random
import time


TENDS = {
    'fast_decrease',
    'decrease',
    'normal',
    'increase',
    'fast_increase'
}


class Sensor:
    """Sensor measure and send value of air parameter"""

    def __init__(self, sensor_config: dict) -> None:
        self.sensor_config = sensor_config
        self.check_config()
        self.field = self.sensor_config['field']
        self.tend = self._start_tend

    def check_config(self):
        mandatory_keys = ['field']

        assert isinstance(self.sensor_config, dict), f"Incorrect config file. Must be dict, but now:" \
                                                     f" {type(self.sensor_config)}"
        for key in mandatory_keys:
            assert key in mandatory_keys, f"Incorrect config file. Key '{key}' is mandatory"

    @property
    def _start_tend(self):
        self.set_tend_time = time.time()
        return self.sensor_config['tend'] if 'tend' in self.sensor_config.keys() else 'normal'

    def change_tend(self):
        self.tend = random.choice(list(TENDS - {self.tend}))


class TemperatureSensor(Sensor):

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'Temperature'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else -40

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 50

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 25

    @property
    def delta_temperature(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-1, -0.2)

        if self.tend == 'decrease':
            return random.uniform(-0.5, -0.1)

        if self.tend == 'normal':
            return random.uniform(-0.3, 0.3)

        if self.tend == 'increase':
            return random.uniform(0.1, 0.5)

        if self.tend == 'fast_increase':
            return random.uniform(0.2, 1)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_temperature, 2)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class HumiditySensor(Sensor):

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'Humidity'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 100

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 50

    @property
    def delta_humidity(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-1, -0.2)

        if self.tend == 'decrease':
            return random.uniform(-0.5, -0.1)

        if self.tend == 'normal':
            return random.uniform(-0.3, 0.3)

        if self.tend == 'increase':
            return random.uniform(0.1, 0.5)

        if self.tend == 'fast_increase':
            return random.uniform(0.2, 1)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_humidity, 2)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class PressureSensor(Sensor):

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'Pressure'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 90

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 110

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 100

    @property
    def delta_pressure(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.5, -0.1)

        if self.tend == 'decrease':
            return random.uniform(-0.2, -0.05)

        if self.tend == 'normal':
            return random.uniform(-0.1, 0.1)

        if self.tend == 'increase':
            return random.uniform(0.05, 0.2)

        if self.tend == 'fast_increase':
            return random.uniform(0.1, 0.5)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_pressure, 2)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class PM25Sensor(Sensor):
    """MPC = 0.025 mg/m3"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'PM2.5'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 0.5

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 0.01

    @property
    def delta_pm25(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.02, -0.005)

        if self.tend == 'decrease':
            return random.uniform(-0.005, -0.001)

        if self.tend == 'normal':
            return random.uniform(-0.001, 0.001)

        if self.tend == 'increase':
            return random.uniform(0.001, 0.005)

        if self.tend == 'fast_increase':
            return random.uniform(0.005, 0.02)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_pm25, 4)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class PM10Sensor(Sensor):
    """MPC = 0.05 mg/m3"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'PM10'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 1

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 0.01

    @property
    def delta_pm10(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.05, -0.01)

        if self.tend == 'decrease':
            return random.uniform(-0.02, -0.005)

        if self.tend == 'normal':
            return random.uniform(-0.01, 0.01)

        if self.tend == 'increase':
            return random.uniform(0.005, 0.02)

        if self.tend == 'fast_increase':
            return random.uniform(0.01, 0.05)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_pm10, 4)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class COSensor(Sensor):
    """MPC = 17.5 ppm
    1 ppm = 1.16197 mg/m3"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'CO'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 25

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 1

    @property
    def delta_CO(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.5, -0.1)

        if self.tend == 'decrease':
            return random.uniform(-0.2, -0.05)

        if self.tend == 'normal':
            return random.uniform(-0.1, 0.1)

        if self.tend == 'increase':
            return random.uniform(0.05, 0.2)

        if self.tend == 'fast_increase':
            return random.uniform(0.1, 0.5)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_CO, 2)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class SO2Sensor(Sensor):
    """MPC = 3.8 ppm
    1 ppm = 2.65722 mg/m3"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'SO2'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 20

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 0.1

    @property
    def delta_SO2(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.04, -0.02)

        if self.tend == 'decrease':
            return random.uniform(-0.02, -0.01)

        if self.tend == 'normal':
            return random.uniform(-0.01, 0.01)

        if self.tend == 'increase':
            return random.uniform(0.01, 0.02)

        if self.tend == 'fast_increase':
            return random.uniform(0.02, 0.04)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_SO2, 4)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class NO2Sensor(Sensor):
    """MPC = 1.6 ppm
    1 ppm = 1.9085 mg/m3"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'NO2'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 20

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 0.1

    @property
    def delta_NO2(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.04, -0.02)

        if self.tend == 'decrease':
            return random.uniform(-0.02, -0.01)

        if self.tend == 'normal':
            return random.uniform(-0.01, 0.01)

        if self.tend == 'increase':
            return random.uniform(0.01, 0.02)

        if self.tend == 'fast_increase':
            return random.uniform(0.02, 0.04)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_NO2, 4)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class O3Sensor(Sensor):
    """MPC = 0.05 ppm
    1 ppm = 1.99116 mg/m3"""
    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'O3'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 18

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 0.001

    @property
    def delta_O3(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.004, -0.002)

        if self.tend == 'decrease':
            return random.uniform(-0.002, -0.001)

        if self.tend == 'normal':
            return random.uniform(-0.001, 0.001)

        if self.tend == 'increase':
            return random.uniform(0.001, 0.002)

        if self.tend == 'fast_increase':
            return random.uniform(0.002, 0.004)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_O3, 4)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class NH3Sensor(Sensor):
    """MPC = 28.2 ppm"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'NH3'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 50

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 1

    @property
    def delta_NH3(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.4, -0.2)

        if self.tend == 'decrease':
            return random.uniform(-0.2, -0.1)

        if self.tend == 'normal':
            return random.uniform(-0.1, 0.1)

        if self.tend == 'increase':
            return random.uniform(0.1, 0.2)

        if self.tend == 'fast_increase':
            return random.uniform(0.2, 0.4)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_NH3, 2)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class H2SSensor(Sensor):
    """MPC = 7.2 ppm"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'H2S'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 20

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 0.5

    @property
    def delta_H2S(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-0.2, -0.1)

        if self.tend == 'decrease':
            return random.uniform(-0.1, -0.05)

        if self.tend == 'normal':
            return random.uniform(-0.05, 0.05)

        if self.tend == 'increase':
            return random.uniform(0.05, 0.1)

        if self.tend == 'fast_increase':
            return random.uniform(0.1, 0.2)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_H2S, 4)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class CO2Sensor(Sensor):
    """MPC = 5000 ppm"""

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.sensor_name = 'CO2'

    @property
    def _min_value(self):
        return int(self.sensor_config['min_value']) if 'min_value' in self.sensor_config.keys() else 0

    @property
    def _max_value(self):
        return int(self.sensor_config['max_value']) if 'max_value' in self.sensor_config.keys() else 20000

    @property
    def _start_value(self):
        return int(self.sensor_config['start_value']) if 'start_value' in self.sensor_config.keys() else 1000

    @property
    def delta_H2S(self):
        if self.tend == 'fast_decrease':
            return random.uniform(-20, -10)

        if self.tend == 'decrease':
            return random.uniform(-10, -5)

        if self.tend == 'normal':
            return random.uniform(-5, 5)

        if self.tend == 'increase':
            return random.uniform(5, 10)

        if self.tend == 'fast_increase':
            return random.uniform(10, 20)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:  # Change tend every 8h
            self.change_tend()

        new_value = round(self.current_value + self.delta_H2S, 1)
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


SENSORS = {
    'temperature': TemperatureSensor,
    'humidity': HumiditySensor,
    'pressure': PressureSensor,
    'PM2.5': PM25Sensor,
    'PM10': PM10Sensor,
    'CO': COSensor,
    'SO2': SO2Sensor,
    'NO2': NO2Sensor,
    'O3': O3Sensor,
    'NH3': NH3Sensor,
    'H2S': H2SSensor,
    'CO2': CO2Sensor
    }
