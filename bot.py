import math
import time
from sensors import SENSORS


class Bot:

    def __init__(self, bot_config):
        self.bot_config = bot_config
        self.check_bot_config()
        self.email = self.bot_config['email']
        self.channel = self.bot_config['channel']
        self.update_time = self._update_time
        self.work_time = self._work_time

        self.start_time = time.time()
        self.sensors_configs = self.bot_config['sensors']
        self.sensors = []
        self.sensors_initialization()

    def sensors_initialization(self):
        for sensor_config in self.sensors_configs:
            sensor_name = list(sensor_config.keys())[0]
            self.sensors.append(SENSORS[sensor_name](sensor_config))

    def work(self, ):
        while time.time() < self.start_time + self.work_time:
            self.measure_all_sensors()
            self.send_all_values()

    @property
    def _update_time(self):
        return int(self.bot_config['update_time']) if 'update_time' in self.bot_config.keys() else 300

    @property
    def _work_time(self):
        return int(self.bot_config['work_time']) if 'work_time' in self.bot_config.keys() else math.inf

    def check_bot_config(self):
        mandatory_keys = ['email', 'channel', 'sensors']

        assert isinstance(self.bot_config, dict), f"Incorrect bot_config. It must be dict, " \
                                                  f"but now {type(self.bot_config)}"

        for key in mandatory_keys:
            if key not in self.bot_config.keys():
                raise Exception(f"Incorrect bot_config. Key {key} is mandatory for all bots but absent.")

        assert isinstance(self.bot_config['sensors'], list), f"Incorrect bot_config. bot_config['sensor'] must be" \
                                                             f"list, but now it's {type(self.bot_config['sensors'])}"

    def measure_all_sensors(self):
        for sensor in self.sensors:
            sensor.measure()

    def send_all_values(self):
        for sensor in self.sensors:
            sensor.send_current_value()
