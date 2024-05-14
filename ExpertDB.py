import sqlite3

class DrivingMetricsDatabase:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_tables(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Создаем таблицу параметров
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parameters (
                parameter_id INTEGER PRIMARY KEY,
                parameter_name TEXT
            )
        ''')

        # Создаем таблицу оценок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                expert_id INTEGER,
                parameter_id INTEGER,
                rating INTEGER,
                min_value REAL,
                max_value REAL,
                FOREIGN KEY (parameter_id) REFERENCES parameters(parameter_id)
            )
        ''')

        # Создаем таблицу параметров расчета
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculation_parameters (
                calculation_parameter_id INTEGER PRIMARY KEY,
                parameter_id INTEGER,
                FOREIGN KEY (parameter_id) REFERENCES parameters(parameter_id)
            )
        ''')

        # Создаем таблицу связей между параметрами и экспертами
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expert_parameter_relations (
                expert_id INTEGER,
                calculation_parameter_id INTEGER,
                PRIMARY KEY (expert_id, calculation_parameter_id),
                FOREIGN KEY (expert_id) REFERENCES ratings(expert_id),
                FOREIGN KEY (calculation_parameter_id) REFERENCES calculation_parameters(calculation_parameter_id)
            )
        ''')

        connection.commit()
        connection.close()

    def insert_example_data(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Заполняем таблицу параметров
        cursor.execute('''
            INSERT INTO parameters (parameter_id, parameter_name)
            VALUES (1, 'Amplitude of Steering'),
                    (2, 'Amplitude of Acceleration'),
                    (3, 'Depal Counter'),
                    (4, 'Calc LDV'),
                    (5, 'Calc Mean Velocity')
        ''')

        # Заполняем таблицы оценок для каждого параметра
        cursor.execute('''
        INSERT INTO ratings (expert_id, parameter_id, rating, min_value, max_value)
        VALUES 
            -- Данные для первого эксперта
            (1, 1, 1, 0.0, 5.0),
            (1, 1, 2, 5.0, 10.0),
            (1, 1, 3, 10.0, 12.0),
            (1, 2, 1, 0.0, 6.0),
            (1, 2, 2, 6.0, 10.0),
            (1, 2, 3, 10.0, 15.0),
            (1, 3, 1, 0.0, 7.0),
            (1, 3, 2, 7.0, 12.0),
            (1, 3, 3, 12.0, 20.0),
            (1, 4, 1, 0.0, 2.0),
            (1, 4, 2, 2.0, 5.0),
            (1, 4, 3, 5.0, 10.0),
            (1, 5, 1, 0.0, 10.0),
            (1, 5, 2, 10.0, 15.0),
            (1, 5, 3, 15.0, 25.0),
            -- Данные для второго эксперта
            (2, 1, 1, 0.0, 7.0),
            (2, 1, 2, 7.0, 10.0),
            (2, 1, 3, 10.0, 14.0),
            (2, 2, 1, 0.0, 8.0),
            (2, 2, 2, 8.0, 10.0),
            (2, 2, 3, 10.0, 13.0),
            (2, 3, 1, 0.0, 6.0),
            (2, 3, 2, 6.0, 13.0),
            (2, 3, 3, 13.0, 20.0),
            (2, 4, 1, 0.0, 2.0),
            (2, 4, 2, 2.0, 6.0),
            (2, 4, 3, 6.0, 10.0),
            (2, 5, 1, 0.0, 12.0),
            (2, 5, 2, 12.0, 15.0),
            (2, 5, 3, 15.0, 25.0),
            -- Данные для третьего эксперта эксперта
            (3, 1, 1, 0.0, 7.0),
            (3, 1, 2, 7.0, 12.0),
            (3, 1, 3, 12.0, 18.0),
            (3, 2, 1, 0.0, 8.0),
            (3, 2, 2, 8.0, 9.0),
            (3, 2, 3, 9.0, 17.0),
            (3, 3, 1, 0.0, 5.0),
            (3, 3, 2, 5.0, 11.0),
            (3, 3, 3, 11.0, 20.0),
            (3, 4, 1, 0.0, 2.0),
            (3, 4, 2, 2.0, 4.0),
            (3, 4, 3, 4.0, 12.0),
            (3, 5, 1, 0.0, 11.0),
            (3, 5, 2, 11.0, 15.0),
            (3, 5, 3, 15.0, 30.0)
    ''')

        connection.commit()
        connection.close()


    def query_example_data(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Выполняем запрос для вывода информации о параметрах
        cursor.execute('''
            SELECT p.parameter_name, r.rating, r.min_value, r.max_value
            FROM parameters p
            JOIN ratings r ON p.parameter_id = r.parameter_id
        ''')

        data = cursor.fetchall()
        connection.close()
        return data


    def query_experts_by_parameter_value(self, rate, parameter_id, value):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Выполняем запрос для вывода информации об экспертах по выбранному параметру и значению
        cursor.execute('''
            SELECT e.expert_id
            FROM ratings e
            WHERE e.rating = ? AND e.parameter_id = ? AND ? BETWEEN e.min_value AND e.max_value
        ''', (rate, parameter_id, value))

        data = cursor.fetchall()
        connection.close()
        return data
    
    def query_values_by_parameter(self, rate, parameter_id, expert):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Выполняем запрос для вывода информации об экспертах
        cursor.execute('''
            SELECT *
            FROM ratings e
            WHERE e.parameter_id = ? AND e.expert_id = ? AND e.rating = ?
        ''', (parameter_id, expert,rate))

        data = cursor.fetchall()
        connection.close()
        return data
    


