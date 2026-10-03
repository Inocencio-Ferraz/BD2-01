from database.connection import create_tables, engine


def main() -> None:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    create_tables()
    print("Conexão com MariaDB estabelecida e tabelas criadas/verificadas.")


if __name__ == "__main__":
    main()
