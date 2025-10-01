import click
import subprocess
import os
import sys
from pathlib import Path
from utils.timezone import utcnow

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
SRC_DIR = PROJECT_ROOT / "src"
MIGRATIONS_DIR = SRC_DIR / "infrastructure" / "persistence" / "migrations"


@click.group()
def cli() -> None:
    """Custom commands for your FastAPI project"""
    pass


@cli.command()
@click.option("-m", "--message", required=True, help="Migration message")
def makemigrations(message: str) -> None:
    """Creates Alembic revision with autogenerate"""
    message = f"{utcnow().strftime('%Y%m%d_%H%M%S')}_{message}".replace(" ", "_")
    command = ["alembic", "revision", "--autogenerate", "-m", message]

    click.echo(f"🚧 Creating migration: '{message}'")
    click.echo(f"📂 Working directory: {MIGRATIONS_DIR}")

    # Add src to PYTHONPATH so imports work
    env = os.environ.copy()
    env['PYTHONPATH'] = str(SRC_DIR)

    result = subprocess.run(command, cwd=MIGRATIONS_DIR, env=env)

    if result.returncode == 0:
        click.echo("✅ Migration created successfully!")
    else:
        click.echo("❌ Migration creation failed!", err=True)
        sys.exit(1)


@cli.command()
def migrate() -> None:
    """Applies all Alembic migrations"""
    command = ["alembic", "upgrade", "head"]

    click.echo("🚀 Applying migrations...")
    click.echo(f"📂 Working directory: {MIGRATIONS_DIR}")

    # Add src to PYTHONPATH so imports work
    env = os.environ.copy()
    env['PYTHONPATH'] = str(SRC_DIR)

    result = subprocess.run(command, cwd=MIGRATIONS_DIR, env=env)

    if result.returncode == 0:
        click.echo("✅ Migrations applied successfully!")
    else:
        click.echo("❌ Migration failed!", err=True)
        sys.exit(1)


@cli.command()
def runserver() -> None:
    """Runs the FastAPI development server"""
    command = ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

    click.echo("🚀 Starting FastAPI server...")
    click.echo(f"📂 Working directory: {SRC_DIR}")

    result = subprocess.run(command, cwd=SRC_DIR)

    if result.returncode == 0:
        click.echo("✅ Server stopped.")
    else:
        click.echo("❌ Server stopped with errors!", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()