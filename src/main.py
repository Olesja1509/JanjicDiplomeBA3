from src.config import config
from src.db_manager import DBManager
from src.utils import analyze_prices, create_database, save_data_to_database

if __name__ == "__main__":
    message = f'Добро пожаловать в программу для прогнозирования цен на рынке'
    print(message)

    params = config()

    # Создание базы данных
    create_database('database_products', params)

    # Сохранение данных в БД
    save_data_to_database('../csv_data.csv', 'database_products', params)

    # Создание класса для работы в БД
    db_manager = DBManager('database_products', params)

    analyze_prices(db_manager)
