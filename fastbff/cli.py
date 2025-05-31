import os
import typer
import uvicorn
import yaml
from pathlib import Path
from fastbff.fastbff_app import create_app, load_config
from fastbff.util.helper import generate_config_yaml, get_file_path
from fastbff.util.helper import CONFIGS_DIR

app = typer.Typer()  # create the main app

DEFAULT_CONFIG = "config"


@app.command()
def init(config: str = typer.Argument(DEFAULT_CONFIG, help="Name of the config file")):
    """
    Generate a starter YAML config file inside the 'configs/' directory.
    """
    os.makedirs(CONFIGS_DIR, exist_ok=True)
    # Build full file path, extend to other file type such as json

    config_path = get_file_path(config)

    if config_path.exists():
        typer.secho(
            f"⚠️  '{config_path}' already exists. Aborting.", fg=typer.colors.YELLOW
        )
        raise typer.Exit(code=1)

    generate_config_yaml(config_path, config_name=config)

    typer.secho(
        f"✅ Generated starter '{config_path}' successfully!", fg=typer.colors.GREEN
    )


@app.command()
def validate(
    config: str = typer.Argument(DEFAULT_CONFIG, help="Name of the config file")
):
    config_path = get_file_path(config)

    if not os.path.exists(config_path):
        typer.secho(f"❌ Config file not found: {config_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        typer.secho(f"❌ Invalid YAML: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Check for expected keys in the config
    required_top_keys = {"startup", "routes"}
    missing_keys = required_top_keys - config.keys()

    if missing_keys:
        typer.secho(
            f"❌ Missing required top-level keys: {', '.join(missing_keys)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    required_startup_keys = {"title", "version"}
    startup_keys = config.get("startup", {}).keys()
    missing_keys = required_startup_keys - startup_keys

    if missing_keys:
        typer.secho(
            f"❌ Missing required start up keys: {', '.join(missing_keys)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    # Optionally, validate each route structure
    for i, route in enumerate(config.get("routes", [])):
        if not all(k in route for k in ("path", "method", "source")):
            typer.secho(
                f"❌ Route #{i+1} is missing required fields.", fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

    typer.secho("✅ Config is valid!", fg=typer.colors.GREEN)


@app.command()
def serve(
    config: str = typer.Argument(DEFAULT_CONFIG, help="Name of the config file"),
    env: str = typer.Option("prod", help="Define production or env"),
    watch: bool = typer.Option(False, help="Enable auto-reload"),
):
    config_path = get_file_path(config)
    """Start the FastBFF REST server."""
    if not os.path.exists(config_path):
        typer.secho(
            f"❌ Config file not found: {config_path}, use fastbff init <name> to initialise a config file.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        config = load_config(config_path)
    except Exception as e:
        typer.secho(f"❌ Failed to load config: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    config = load_config(config_path)
    app_instance, host, port, log_level = create_app(config, env)
    uvicorn.run(app_instance, host=host, port=port, log_level=log_level, reload=watch)


if __name__ == "__main__":
    app()
