import glob
import os
import typer
import uvicorn
import yaml
from pathlib import Path
from fastbff.fastbff_app import create_app, load_config
from fastbff.util.helper import (
    check_existing_config,
    check_valid_type,
    generate_config,
    get_file_path,
)
from fastbff.util.helper import CONFIGS_DIR

app = typer.Typer()  # create the main app

DEFAULT_CONFIG = "config"


@app.command()
def init(
    config: str = typer.Argument(DEFAULT_CONFIG, help="Name of the config"),
    type: str = typer.Option(..., help="Type of config (yaml/json)"),
):
    """
    Generate a starter YAML/JSON config file inside the 'configs/' directory.
    """

    os.makedirs(CONFIGS_DIR, exist_ok=True)

    if check_valid_type(type):
        config_path = get_file_path(config, type)
    else:
        typer.secho("❌ Incorrect file type.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if check_existing_config(config):
        typer.secho(f"⚠️  '{config}' config already exists.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=1)

    try:
        generate_config(
            config_path,
            type,
            config_name=config,
        )
    except Exception as e:
        typer.secho(f"❌  Failed to generate config: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(
        f"✅ Generated starter config in '{config_path}' successfully!",
        fg=typer.colors.GREEN,
    )


@app.command()
def validate(
    config: str = typer.Argument(DEFAULT_CONFIG, help="Name of the config file")
):
    """
    Validates a config file
    """
    typer.secho("Checking config...")

    if not check_existing_config(config):
        typer.secho(f"❌ Config file not found: '{config}'", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    file_paths = glob.glob(os.path.join(CONFIGS_DIR, f"{config}.*"))

    try:
        config = load_config(file_paths[0])
    except Exception as e:
        typer.secho(f"❌ Failed to load '{config}': {e}", fg=typer.colors.RED)
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
    config: str = typer.Argument(DEFAULT_CONFIG, help="Name of the config"),
    env: str = typer.Option(
        ..., help="Define production or dev environment [dev, prod]"
    ),
):
    """Start the FastBFF REST server."""

    validate(config)

    file_paths = glob.glob(os.path.join(CONFIGS_DIR, f"{config}.*"))

    try:
        config = load_config(file_paths[0])
    except Exception as e:
        typer.secho(f"❌ Failed to load config: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    app_instance, host, port, log_level = create_app(config, env)

    try:
        uvicorn.run(app_instance, host=host, port=port, log_level=log_level)
    except Exception as e:
        typer.secho(f"❌ Failed to start server: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
