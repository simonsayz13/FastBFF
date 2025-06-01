import glob
import json
import os
from pathlib import Path
import yaml

CONFIGS_DIR = "configs"
FILE_FORMATS = ["json", "yaml"]


def check_valid_type(type: str) -> bool:
    return type in FILE_FORMATS


def check_existing_config(config: str) -> bool:
    pattern = os.path.join(CONFIGS_DIR, f"{config}.*")
    matches = glob.glob(pattern)
    return len(matches) > 0


def generate_config(
    config_path: str,
    type: str,
    config_name: str = "ExampleAPI",
):
    starter_config = {
        "startup": {
            "title": config_name,
            "version": "1.0.0",
            "port": 8000,
        },
        "routes": [
            {
                "path": "/hello",
                "method": "GET",
                "source": {
                    "type": "static",
                    "data": [{"message": "Welcome to FastBFF!"}],
                },
            }
        ],
    }

    try:
        with open(config_path, "w") as f:
            if type == "yaml":
                yaml.dump(starter_config, f, sort_keys=False)
            elif type == "json":
                json.dump(starter_config, f, sort_keys=False)
    except Exception as e:
        raise ValueError(e)


def get_file_path(config: str = "ExampleAPI", type: str = "yaml"):
    if type == "yaml":
        file_path = Path(CONFIGS_DIR) / f"{config}.yaml"
    elif type == "json":
        file_path = Path(CONFIGS_DIR) / f"{config}.json"
    return file_path
