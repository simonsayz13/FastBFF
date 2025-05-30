import typer
import uvicorn
from fastbff.fastbff_app import create_app, load_config
import os

app = typer.Typer()  # create the main app


@app.command()
def init():
    """Generate a starter config.yaml file."""


@app.command()
def validate():
    """Check if the config.yaml is valid YAML and follows schema rules."""


@app.command()
def serve(
    config_path: str = typer.Argument("config.yaml", help="Path to config file"),
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
    app_instance, host, port, log_level = create_app(config)
    uvicorn.run(app_instance, host=host, port=port, log_level=log_level, reload=watch)


if __name__ == "__main__":
    app()
