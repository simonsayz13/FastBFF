from pathlib import Path
import yaml

CONFIGS_DIR = "configs"


def generate_config_yaml(
    config_path: str = "config.yaml", config_name: str = "ExampleAPI"
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
    with open(config_path, "w") as f:
        yaml.dump(starter_config, f, sort_keys=False)


def get_file_path(config: str = "ExampleAPI"):
    return Path(CONFIGS_DIR) / f"{config}.yaml"
