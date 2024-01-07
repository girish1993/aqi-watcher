import yaml
import os

CONFIG_FILE_PATH: str = os.path.join("config", "config.yaml")


def parse_config(config_file_path: str = CONFIG_FILE_PATH) -> dict:
    with open(config_file_path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print("Error parsing the config file")
            print(e)
