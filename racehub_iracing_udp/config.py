import os
import json

racehub_directory = os.path.join(os.path.expanduser("~"), "Documents", "RaceHub")

default_config = {
    "frequency": 60,
    "address": "127.0.0.1",
    "port": 20900,
}

config_filepath = os.path.join(racehub_directory, "iracing_config.json")

if not os.path.exists(config_filepath):
    # if not found, create it with default values
    config = default_config

    # create directory if it doesn't exist
    os.makedirs(os.path.dirname(config_filepath), exist_ok=True)

    # save config
    with open(config_filepath, "w") as f:
        json.dump(config, f, indent=4)

else:
    # if found, load it
    with open(config_filepath, "r") as f:
        config = json.load(f)

    # if found, check for missing values and add them
    for key in default_config:
        if key not in config:
            config[key] = default_config[key]

    # save config
    with open(config_filepath, "w") as f:
        json.dump(config, f, indent=4)
