import pytest
import warnings

from src.db_manager import DBManager
from src.utils import create_database, save_data_to_database

db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'max1313',
    }


@pytest.fixture(scope="module")
def create_test_db():
    # Создание временной базы данных для тестов
    create_database('my_test_db', db_params)
    save_data_to_database('test_csv_data.csv', 'my_test_db', db_params)


def test_get_average_price_for_product(create_test_db):
    warnings.filterwarnings("ignore", category=UserWarning)
    db_manager = DBManager('my_test_db', db_params)

    db_manager.load_data()
    average_price = db_manager.get_average_price_for_product()
    assert len(average_price) == 3


def test_train_model(create_test_db):
    warnings.filterwarnings("ignore", category=UserWarning)
    db_manager = DBManager('my_test_db', db_params)

    db_manager.load_data()
    db_manager.train_model()
    all_predict = db_manager.predict_price_for_products()
    assert len(all_predict) == 3


def test_train_model_forest(create_test_db):
    warnings.filterwarnings("ignore", category=UserWarning)
    db_manager = DBManager('my_test_db', db_params)

    db_manager.load_data()
    db_manager.train_model_forest()
    all_predict = db_manager.predict_price_for_products()
    assert len(all_predict) == 3



