import os
import json
from Bot_farm.bot_farm import BotFarm


def json_files_from_folder(folder: str) -> list:
    """Return all config files in folder"""

    files = []
    for file_name in os.listdir(folder):
        splitted_filename = file_name.split(".")
        if splitted_filename[-1] == "json":
            files.append(file_name)
    return files


def select_config_file(config_files) -> int:
    """Print all files in list as a table for choice"""

    print("Select a config file")
    expected_choice = []  # Save all possible variants to check input
    for num, config_file in enumerate(config_files):
        expected_choice.append(str(num + 1))
        print(f"{num + 1} - {config_file}")
    choice = input()
    assert choice in expected_choice, "Incorrect choice, try again"
    return int(choice)


def choose_config(config_files: list) -> str:
    """Return a config file from a list"""

    if len(config_files) == 0:
        raise Exception("There is no config file in 'config' folder")
    elif len(config_files) == 1:
        return config_files[0]
    else:
        choice = select_config_file(config_files)
    return config_files[choice - 1]


def config_file_address() -> str:
    """Return the address of config file"""

    config_files = json_files_from_folder("config")
    config_file = choose_config(config_files)  # Choice a config file if there is more then 1 in config folder
    return config_file


if __name__ == "__main__":

    #  Load config file
    with open(os.path.join("config", config_file_address())) as f:
        config = json.load(f)

    #  Initialization and startup of bot farm with all bots described in config file
    bot_farm = BotFarm(config)
    bot_farm.start()
