import os
import json
from bot_farm import BotFarm


def json_files_from_folder(folder):
    files = []
    for file_name in os.listdir(folder):
        splitted_filename = file_name.split(".")
        if splitted_filename[-1] == "json":
            files.append(file_name)
    return files


def select_config_file(config_files):
    print("Select a config file")
    expected_choice = []
    for num, config_file in enumerate(config_files):
        expected_choice.append(str(num + 1))
        print(f"{num + 1} - {config_file}")
    choice = input()
    assert choice in expected_choice, "Incorrect choice, try again"
    return int(choice)


def choose_config(config_files: list) -> str:
    if len(config_files) == 0:
        raise Exception("There is no config file in 'config' folder")
    elif len(config_files) == 1:
        return config_files[0]
    else:
        choice = select_config_file(config_files)
    return config_files[choice - 1]


def config_file_address():
    config_files = json_files_from_folder("config")
    print(config_files)
    return choose_config(config_files)


with open(os.path.join("config", config_file_address())) as f:
    config = json.load(f)


bot_farm = BotFarm(config)
bot_farm.start()
