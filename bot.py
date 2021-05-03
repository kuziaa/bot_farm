import math
import time
from sensors import SENSORS


class Bot:
    """Bot - a group of sensors in one place. Measured values correspond to sensors of the bot.

    bot_conf: {email, channel, ..., 'sensors': [sensor_1, ..., sensor_8]}
        Every bot_conf contain all information about sensors in it (temperature, pressure, etc.).
        No more then 8 sensors per bot.

    sensor1_conf: {...}
        Every sensor config contain all information about current sensor behaviour: min, max value,
        growth trend and etc.
    """

    def __init__(self, bot_config: dict) -> None:
        self.bot_config = bot_config
        self._check_bot_config()
        self.email = self.bot_config['email']  # email of account were current bot was created
        self.channel = self.bot_config['channel']  # num of channel in account
        self.api_key = self.bot_config['api_key']  # api_key of account
        self.update_time = self._update_time  # Time between 2 measurement (300s default)
        self.work_time = self._work_time  # How long the bot will work (inf default)
        self.start_time = time.time()
        self.sensors_configs = self.bot_config['sensors']
        self.sensors = []
        self.sensors_initialization()
        print('Bot: ' + self.email + ' ' + self.channel + ' ' + self.api_key)

    def _check_bot_config(self) -> None:
        """Check if config file was created correct"""

        mandatory_keys = ['email', 'channel', 'api_key', 'sensors']
        assert isinstance(self.bot_config, dict), f"Incorrect bot_config. It must be dict, " \
                                                  f"but now {type(self.bot_config)}"
        for key in mandatory_keys:
            if key not in self.bot_config.keys():
                raise Exception(f"Incorrect bot_config. Key {key} is mandatory for all bots but absent.")

        assert isinstance(self.bot_config['sensors'], list), f"Incorrect bot_config. bot_config['sensor'] must be" \
                                                             f"list, but now it's {type(self.bot_config['sensors'])}"

    @property
    def _update_time(self) -> int:
        """If there is no 'update_time' key in config - use default value"""
        return int(self.bot_config['update_time']) if 'update_time' in self.bot_config.keys() else 10

    @property
    def _work_time(self) -> int:
        """If there is no 'work_time' key in config - use default value"""
        return int(self.bot_config['work_time']) if 'work_time' in self.bot_config.keys() else math.inf

    def sensors_initialization(self) -> None:
        """Initialization of all sensors (1-8) for the bot"""
        for sensor_config in self.sensors_configs:
            sensor_name = list(sensor_config.keys())[0]
            sensor = SENSORS[sensor_name]
            self.sensors.append(sensor(sensor_config[sensor_name], self.api_key))

    def measure_all_sensors(self) -> None:
        """Measure values for all sensors"""
        for sensor in self.sensors:
            sensor.measure()

    def send_all_values(self) -> None:
        """Send last measured values to server"""
        for sensor in self.sensors:
            sensor.send_current_value()

    def start(self) -> None:
        """Measure and send all values during working time"""

        self.measure_all_sensors()
        self.send_all_values()

