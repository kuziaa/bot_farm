from bot import Bot


class BotFarm:

    def __init__(self, bot_farm_config: dict) -> None:
        self.bot_farm_config = bot_farm_config
        self.check_bot_farm_config()
        self.bots_configs = self.bot_farm_config['bots']
        self.bots = []
        self.bots_initialization()

    def check_bot_farm_config(self):
        mandatory_keys = ['bots']

        assert isinstance(self.bot_farm_config, dict), f"Incorrect bot_farm config file. Must be dict but now: \
            {type(self.bot_farm_config)}"

        for key in mandatory_keys:
            assert key in self.bot_farm_config.keys(), f"Incorrect bot_farm config file. Key {key} is mandatory"

    def bots_initialization(self):
        for bot_config in self.bots_configs:
            self.bots.append(Bot(bot_config))

    def start(self):
        for bot in self.bots:
            bot.work()
