import click
import subprocess
import os
from utils.timezone import utcnow

@click.group()
def cli() -> None:
    """Custom commands for your FastAPI project"""
    pass


@cli.command()
@click.option("-m", "--message", required=True, help="Migration message")
def makemigrations(message: str) -> None:
    """Creates Alembic revision with autogenerate"""
    migrations_path = os.path.join("infrastructure/persistence/migrations")
    message = f"{utcnow().strftime('%Y%m%d_%H%M%S')}_{message}".replace(" ", "_")
    command = ["alembic", "revision", "--autogenerate", "-m", message]

    click.echo(f"🚧 Creating migration: '{message}'")

    subprocess.run(command, cwd=migrations_path)

    click.echo("✅ Migration created successfully!")


@cli.command()
def migrate() -> None:
    """Applies all Alembic migrations"""
    migrations_path = os.path.join("infrastructure/persistence/migrations")
    command = ["alembic", "upgrade", "head"]

    click.echo("🚀 Applying migrations...")

    subprocess.run(command, cwd=migrations_path)

    click.echo("✅ Migrations applied successfully!")

if __name__ == "__main__":
    cli()