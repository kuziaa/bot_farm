from bot import Bot
import time


class BotFarm:
    """A bot farm simulates Air Quality Monitoring system.
    Bot farm contain from bots (tne number according to config file.

    bot_farm_config : {'bots': [bot1_conf, ..., bot32_conf, ...]}
        config contain all information about bots to create

    bot1_conf: {..., 'sensors': [sensor_1, ..., sensor_8]}
        Every bot_conf contain all information about sensors in it (temperature, pressure, etc.).
        No more then 8 sensors per bot.

    sensor1_conf: {...}
        Every sensor config contain all information about current sensor behaviour: min, max value,
        growth trend and etc.
    """

    def __init__(self, bot_farm_config: dict) -> None:
        self.bot_farm_config = bot_farm_config
        self._check_bot_farm_config()
        self.bots_configs = self.bot_farm_config['bots']
        self.bots = []
        self._bots_initialization()

    def _check_bot_farm_config(self) -> None:
        """Check if config file was created correct"""

        mandatory_keys = ['bots']
        assert isinstance(self.bot_farm_config, dict), f"Incorrect bot_farm config file. Must be dict but now: \
            {type(self.bot_farm_config)}"

        for key in mandatory_keys:
            assert key in self.bot_farm_config.keys(), f"Incorrect bot_farm config file. Key {key} is mandatory"

    def _bots_initialization(self) -> None:
        """Initialization all bots with their configs"""

        for bot_config in self.bots_configs:
            self.bots.append(Bot(bot_config))

    def start(self) -> None:
        """Turn on all bots in farm. Start to measure parameters and send on server"""
        while True:

            for bot in self.bots:
                bot.start()
            time.sleep(20)
