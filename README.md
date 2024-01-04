### ДИПЛОМНАЯ РАБОТА Модель ценообразования

### Описание

Вы работаете в компании, которая продвигает свой товар на разных рынках, и конечно, у компании есть конкуренты.
Отдел аналитики отдал вам исторические данные по ценам, количеству продаж, затрат на продвижение товара, а также базу данных с ценами конкурентов на аналогичный продукт.
Компания находится на этапе составления прогноза цен на основании этих параметров.

Задача разработчика – создать алгоритм, который будет прогнозировать ценообразование на определенном рынке.

### Требуемый стэк
- python 3.11
- postgresql

### Установка и использование.
1. git clone git@github.com:Olesja1509/JanjicDiplomeBA3.git
2. установить зависимости из pyproject.toml
3. Для работы с базой данных необходимо создать файл database.ini с параметрами доступа к базе данных PostgresSQL. Пример содержимого файла:
[postgresql]
host=localhost
user=postgres
password='password'
port=5432
4. Для начала работы необходимо запустить файл main.py

### Описание работы программы
•	В файле config.py хранятся конфигуграции для подключения к БД
•	В файле utils.py хранится функция для работы с анализом цен на рынке, созданию БД и заполнению БД из файла с данными csv_data.csv
•	В файле db_manager.py хранися класс DBManager для работы с данными БД.
