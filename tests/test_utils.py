import psycopg2
import pytest

from src.config import config
from src.utils import create_database, save_data_to_database

db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'max1313',
    }


def test_non_existing_file():
    """Тест отсутствия файла"""

    with pytest.raises(Exception):
        config("non_existent.ini", "postgresql")


def test_create_database():
    """Тест создания базы"""

    # Создаем соединение с базой данных postgres
    conn = psycopg2.connect(dbname='postgres', **db_params)
    conn.autocommit = True

    try:
        # Попытка создания базы данных
        create_database('test_db', db_params)
    except psycopg2.errors.DuplicateDatabase:
        pass

    # Проверяем, что база данных существует
    with conn.cursor() as cur:
        cur.execute("SELECT datname FROM pg_database WHERE datname = 'test_db'")
        result = cur.fetchone()

    assert result is not None, "База данных 'test_db' не существует"


def test_save_data_to_database():
    """Тест сохранения данных в БД"""
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="postgres",
        password="max1313"
    )
    save_data_to_database('test_csv_data.csv', 'test_db', db_params)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert result > 0, "No data found in the table"
