import yaml


def generate_config_yaml():
    config_path = "config.yaml"

    starter_config = {
        "startup": {
            "title": "ExampleAPI",
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
