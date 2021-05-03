import requests
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

    def __init__(self, sensor_config):
        self.sensor_config = sensor_config
        self.check_config()
        self.api_key = self.sensor_config['api_key']
        self.field_num = self.sensor_config['field_num']
        self.current_value = 0

    def measure(self):
        raise Exception("Current method must be overridden in child classes ")

    def send_current_value(self):
        print(self._url)
        r = requests.get(self._url)
        print(f'r.status_code = {r.status_code}')
        print("__________________________________________________________________________")

    @property
    def _url(self):
        return f'https://api.thingspeak.com/update?api_key={self.api_key}${self.field_num}={self.current_value}'

    def check_config(self):
        mandatory_keys = ['api_key', 'field_num']

        assert isinstance(self.sensor_config, dict), f"Incorrect config file. Must be dict, but now:" \
                                                     f" {type(self.sensor_config)}"
        for key in mandatory_keys:
            if key not in self.sensor_config.keys():
                raise Exception(f"Incorrect config file. Key {key} is mandatory for all sensors but absent.")


class TemperatureSensor(Sensor):

    def __init__(self, sensor_config):
        super().__init__(sensor_config)
        self.min_value = self._min_value
        self.max_value = self._max_value
        self.current_value = self._start_value
        self.tend = self._start_tend

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
    def _start_tend(self):
        self.set_tend_time = time.time()
        return self.sensor_config['tend'] if 'tend' in self.sensor_config.keys() else 'normal'

    def change_tend(self):
        self.tend = random.choice(list(TENDS - {self.tend, }))

    @property
    def delta_temperature(self):
        if self.tend == 'fast_decrease':
            return round(random.uniform(-2, -0.5), 2)

        if self.tend == 'decrease':
            return round(random.uniform(-1, -0.1), 2)

        if self.tend == 'normal':
            return round(random.uniform(-0.5, 0.5), 2)

        if self.tend == 'increase':
            return round(random.uniform(0.1, 1), 2)

        if self.tend == 'fast_increase':
            return round(random.uniform(0.5, 2), 2)

    def measure(self):
        if time.time() - self.set_tend_time > 28800:
            self.change_tend()

        new_value = self.current_value + self.delta_temperature
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < self.min_value:
            new_value = self.min_value

        self.current_value = new_value


class HumiditySensor(Sensor):
    pass


class PressureSensor(Sensor):
    pass


class PM25Sensor(Sensor):
    pass


class PM10Sensor(Sensor):
    pass


class COSensor(Sensor):
    pass


class SO2Sensor(Sensor):
    pass


class NO2Sensor(Sensor):
    pass


class O3Sensor(Sensor):
    pass


class NH3Sensor(Sensor):
    pass


class H2SSensor(Sensor):
    pass


class CO2Sensor(Sensor):
    pass


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
