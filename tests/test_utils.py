import psycopg2
import pytest
from _pytest import monkeypatch

from src.config import config
from src.db_manager import DBManager
from src.utils import create_database, save_data_to_database, analyze_prices

db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'max1313',
    }



# def test_empty_config_file(tmpdir):
#     """Тест для случая, когда конфигурация файла существует, но он пустой"""
#     empty_config_file = tmpdir.join("empty_database.ini")
#     with pytest.raises(Exception) as excinfo:
#         config(empty_config_file, "postgresql")
#     assert "Section postgresql is not found" in str(excinfo.value)


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


def test_analyze_prices(monkeypatch):
    """Тест для анализа данных в БД"""
    db_manager = DBManager('test_db', db_params)

    monkeypatch.setattr('builtins.input', lambda _: '1')
    assert len(analyze_prices(db_manager)) == 3

