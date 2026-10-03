import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def _database_url() -> URL:
    required = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME")
    missing = [name for name in required if os.getenv(name) is None]
    if missing:
        raise RuntimeError(
            "Variáveis de ambiente ausentes para conectar ao MariaDB: "
            + ", ".join(missing)
            + ". Configure o arquivo .env a partir de .env.example."
        )

    return URL.create(
        drivername="mariadb+mariadbconnector",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )


engine = create_engine(_database_url(), pool_pre_ping=True)
Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def create_tables() -> None:
    # Importa os modelos para registrar todas as tabelas no metadata.
    import model.cliente  # noqa: F401
    import model.funcionario  # noqa: F401
    import model.itemvenda  # noqa: F401
    import model.produto  # noqa: F401
    import model.venda  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_session():
    """Fornece uma sessão para uso com `with get_session() as session`."""
    return Session()
