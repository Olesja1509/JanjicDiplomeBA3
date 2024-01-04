import warnings

import pandas as pd
import psycopg2
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


# Игнорирование всех предупреждений от scikit-learn
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class DBManager:
    """Класс для работы с данными в БД"""

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()
        self.model = {}
        self.mse_calculation = {}
        self.data = None
        self.number = None
        self.number_forest = None

    def load_data(self):
        """Загрузка данных из базы данных"""
        sql_query = "SELECT price, count, add_cost, company, product FROM products"
        self.cur.execute(sql_query)
        columns = [desc[0] for desc in self.cur.description]
        data = self.cur.fetchall()
        self.data = pd.DataFrame(data, columns=columns)

    def get_average_price_for_produt(self):
        """Вывод средних значений по каждому продукту"""
        unique_products = self.data["product"].unique()
        average_prices = {}
        for product in unique_products:
            # Запрос SQL для получения средней цены для конкретного продукта
            sql_query = f"""
                   SELECT AVG(price) AS average_price
                   FROM products
                   WHERE product = '{product}'
               """
            self.cur.execute(sql_query)
            result = self.cur.fetchone()
            average_price = (
                result[0] if result[0] is not None else 0.0
            )  # Обработка случая, когда среднее значение равно NULL
            average_prices[product] = round(average_price)
        return average_prices

    def train_model(self):
        """Разделение данных по продуктам, линейная регрессия"""
        unique_products = self.data["product"].unique()

        for product in unique_products:
            product_data = self.data[self.data["product"] == product]
            x = product_data[["count", "add_cost"]]
            y = product_data["price"]
            x_train, x_test, y_train, y_test = train_test_split(
                x, y, test_size=0.2, random_state=10
            )
            # Вывод количества точек данных
            self.number = len(x_train)
            model = LinearRegression()
            model.fit(x_train.values, y_train)
            self.model[product] = model
            y_pred = model.predict(x_test)
            mse = mean_squared_error(y_test, y_pred)
            self.mse_calculation[product] = mse

    def train_model_forest(self):
        """Разделение данных по продуктам, нелинейная регрессия"""
        unique_products = self.data["product"].unique()

        for product in unique_products:
            product_data = self.data[self.data["product"] == product]
            x = product_data[["count", "add_cost"]]
            y = product_data["price"]
            x_train, x_test, y_train, y_test = train_test_split(
                x, y, test_size=0.2, random_state=10
            )
            # Вывод количества точек данных
            self.number_forest = len(x_train)
            # n_estimators количество деревьев предсказания, max_depth сложность дерева
            model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=10)
            model.fit(x_train, y_train)
            self.model[product] = model
            y_pred = model.predict(x_test)
            mse = mean_squared_error(y_test, y_pred)
            self.mse_calculation[product] = mse

    def predict_price_for_products(self):
        """Прогнозирование цен для всех продуктов"""
        predictions = {}
        for product in self.model:
            product_data = self.data[self.data["product"] == product].iloc[
                0
            ]  # Берем первую строку
            count = product_data["count"]
            add_cost = product_data["add_cost"]
            model = self.model[product]
            price = model.predict([[count, add_cost]])
            predictions[product] = price[0]
        return predictions
