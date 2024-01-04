import psycopg2


def analyze_prices(db_manager):
    """Функция для работы с анализом цен на рынке"""

    while True:
        user_input = input('Пожалуйста, выберите команду: \n'
                           '1. Вывести среднюю цену на каждый продукт.\n'
                           '2. Прогнозирование цен линейной регрессией.\n'
                           '3. Прогнозирование цен методом случайных деревьев.\n'
                           '4. Выйти из программы.\n')

        if user_input == '1':
            db_manager.load_data()
            average_price = db_manager.get_average_price_for_product()
            if average_price == {}:
                print('Отсутствуют данные для отображения')
            print('Средние цены:')
            for key, value in average_price.items():
                print(f'{key}:{value}')

        elif user_input == '2':
            db_manager.load_data()
            db_manager.train_model()
            all_predict = db_manager.predict_price_for_products()
            if all_predict == {}:
                print('Отсутствуют данные для отображения')
            print('Прогноз цен с помощью линейной регрессии:')
            for key, value in all_predict.items():
                mse = db_manager.mse_calculation.get(key, None) / db_manager.number
                print(f'Прогнозируемая цена для {key}: {round(value)},'
                      f'среднее отклонение {round((mse / value) * 100, 2)} процентов')

        elif user_input == '3':
            db_manager.load_data()
            db_manager.train_model_forest()
            all_predict = db_manager.predict_price_for_products()
            if all_predict == {}:
                print('Отсутствуют данные для отображения')
            print('Прогноз цен с помощью случайных деревьев:')
            for key, value in all_predict.items():
                mse = db_manager.mse_calculation.get(key, None) / db_manager.number_forest
                print(f'Прогнозируемая цена для {key}: {round(value)},'
                      f'среднее отклонение {round((mse / value) * 100, 2)} процентов')

        elif user_input == '4':
            print("Работа завершена. Спасибо за использование программы")
            break


def create_database(database_name: str, params: dict):
    """Создание БД"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE products (
                    price INTEGER,
                    count INTEGER,
                    add_cost INTEGER,
                    company VARCHAR(50),
                    product VARCHAR(50)
                )
            """)

    conn.commit()
    conn.close()


def save_data_to_database(file_name, database_name: str, params: dict) -> None:
    """Сохранение данных в БД"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with open(file_name, "r") as f:
        cur = conn.cursor()
        cur.copy_expert(
            "COPY products(price, count, add_cost, company, product) FROM STDIN WITH CSV HEADER",
            f,
        )
    conn.commit()

    conn.close()
