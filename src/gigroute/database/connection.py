import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine


project_path = Path(__file__).resolve().parents[3]
env_path = project_path / ".env"

load_dotenv(env_path)


def get_database_engine():
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    db_port = os.getenv("POSTGRES_PORT")
    db_host = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

    if not all([
        db_user,
        db_password,
        db_name,
        db_port,
    ]):
        raise ValueError(
            "Database configuration is incomplete"
        )

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_password,
        host=db_host,
        port=int(db_port),
        database=db_name,
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )