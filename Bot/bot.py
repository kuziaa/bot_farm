import time
from Sensors.sensors import SENSORS
import requests


def check_sensor_config(sensor_config):
    assert isinstance(sensor_config, dict), f"Incorrect sensor_config. Must be dict, but now: {type(sensor_config)}"
    keys = list(sensor_config.keys())
    assert len(keys) == 1, f"Incorrect sensor_config. Only 1 key expected, but got: {keys}"
    key = keys[0]
    assert key in SENSORS, f"Incorrect sensor_config. Unknown sensor: {key}"


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
        self.bot_name = self.bot_config['bot_name']
        self.api_key = self.bot_config['api_key']  # api_key of account
        self.update_time = self._update_time  # Time between measurements
        self.start_time = time.time()
        self.next_send_time = 0
        self.sensors_configs = self.bot_config['sensors']
        self.sensors = []
        self.sensors_initialization()
        # print('Bot: ' + self.email + ' ' + self.channel + ' ' + self.api_key)

    def _check_bot_config(self) -> None:
        """Check if config file was created correct"""

        mandatory_keys = ['email', 'channel', 'bot_name', 'api_key', 'sensors']
        assert isinstance(self.bot_config, dict), f"Incorrect bot_config. It must be dict, " \
                                                  f"but now {type(self.bot_config)}"
        for key in mandatory_keys:
            if key not in self.bot_config.keys():
                raise Exception(f"Incorrect bot_config. Key {key} is mandatory for all bots but absent.")

    @property
    def _update_time(self) -> int:
        """If there is no 'update_time' key in config - use default value"""
        return int(self.bot_config['update_time']) if 'update_time' in self.bot_config.keys() else 300

    def sensors_initialization(self) -> None:
        """Initialization of all sensors (1-8) for the bot"""
        assert isinstance(self.sensors_configs, list), f"Incorrect bot_config. bot_config['sensor'] must be" \
                                                       f"list, but now it's {type(self.sensors_configs)}"

        for sensor_config in self.sensors_configs:
            check_sensor_config(sensor_config)

            sensor_name = list(sensor_config.keys())[0]
            sensor = SENSORS[sensor_name]
            self.sensors.append(sensor(sensor_config[sensor_name]))

    def measure_all_sensors(self) -> None:
        """Measure values for all sensors"""
        for sensor in self.sensors:
            sensor.measure()
            print(f"{sensor.sensor_name}: {sensor.current_value}")

    def send_all_values(self) -> None:
        """Send last measured values to server"""
        values = ''
        for num, sensor in enumerate(self.sensors):
            values += f'&field{num+1}={sensor.current_value}'
        url = f'https://api.thingspeak.com/update?api_key={self.api_key}{values}'
        while True:
            attemp = 0
            time.sleep(attemp)
            attemp += 1
            try:
                requests.get(url)
            except Exception:
                print(f'Failed request, try again.')
            else:
                break
        self.next_send_time = time.time() + self.update_time
        print(f"{self.bot_name} - update all values")
        print(time.asctime())
        print('____________________________________________________________')

    def start(self) -> None:
        """Measure and send all values"""

        self.measure_all_sensors()
        self.send_all_values()
