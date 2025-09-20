import psycopg2
from psycopg2 import sql

# Conexão inicial (servidor principal, sem banco alvo ainda)
DATABASE_URL = "postgresql://postgres:1234@localhost/postgres"

# Nome do banco, schema e tabela alvo
TARGET_DATABASE = "api_db"
SCHEMA_NAME = "api"
TABLE_NAME = "users"


def create_database_if_not_exists():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        [TARGET_DATABASE]
    )
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TARGET_DATABASE))
        )
        print(f"Banco '{TARGET_DATABASE}' criado!")
    else:
        print(f"Banco '{TARGET_DATABASE}' já existe.")

    cursor.close()
    conn.close()


def create_schema_if_not_exists():
    conn = psycopg2.connect(
        f"postgresql://u_grupo06:grupo06@200.144.245.12:45432/{TARGET_DATABASE}"
    )
    cursor = conn.cursor()

    cursor.execute(
        sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(SCHEMA_NAME))
    )
    conn.commit()
    print(f"Schema '{SCHEMA_NAME}' ok.")

    cursor.close()
    conn.close()


def create_users_table():
    conn = psycopg2.connect(
        f"postgresql://u_grupo06:grupo06@200.144.245.12:45432/{TARGET_DATABASE}"
    )
    cursor = conn.cursor()

    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}.{} (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """).format(sql.Identifier(SCHEMA_NAME), sql.Identifier(TABLE_NAME))

    cursor.execute(create_table_query)
    conn.commit()
    print(f"Tabela '{SCHEMA_NAME}.{TABLE_NAME}' pronta.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database_if_not_exists()
    create_schema_if_not_exists()
    create_users_table()
