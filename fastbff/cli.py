import typer
import uvicorn
import yaml
from fastbff.fastbff_app import create_app, load_config
from fastbff.util.helper import generate_config_yaml
import os

app = typer.Typer()  # create the main app
CONFIG_FILE = "config.yaml"


@app.command()
def init():
    """Generate a starter config.yaml file."""

    config_path = CONFIG_FILE

    if os.path.exists(config_path):
        typer.secho(
            f"⚠️  '{config_path}' already exists. Aborting.", fg=typer.colors.YELLOW
        )
        raise typer.Exit(code=1)

    generate_config_yaml()

    typer.secho(
        f"✅ Generated starter '{config_path}' successfully!", fg=typer.colors.GREEN
    )


@app.command()
def validate(config_path: str = CONFIG_FILE):
    """Check if the config file is valid YAML and follows expected structure."""
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
    config_path: str = typer.Argument(CONFIG_FILE, help="Path to config file"),
    env: str = typer.Option("prod", help="Define production or env"),
    watch: bool = typer.Option(False, help="Enable auto-reload"),
):
    """Start the FastBFF REST server."""
    if not os.path.exists(config_path):
        typer.secho(
            f"❌ Config file not found: {config_path}", fg=typer.colors.RED, err=True
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
