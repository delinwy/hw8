import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS countries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL
                )''')

countries_data = [('Kyrgyzstan',), ('China',), ('Japan',)]
cursor.executemany('INSERT INTO countries (title) VALUES (?)', countries_data)

cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    area FLOAT DEFAULT 0,
                    country_id INTEGER,
                    FOREIGN KEY (country_id) REFERENCES countries (id)
                )''')

cities_data = [
    ('Bishkek', 126.71, 1), ('Beijing', 16410.54, 2), ('Osh', 186.94, 1),
    ('Tokyo', 2194.23, 3), ('Kyoto', 827.8, 3), ('Chongqing', 82339.26, 2), ('Shenzhen', 1986.12, 2)
]

cursor.executemany('INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)', cities_data)

cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    city_id INTEGER,
                    FOREIGN KEY (city_id) REFERENCES cities (id)
                )''')

employees_data = [
    ('Ivan', 'Petrov', 2), ('Peter', 'Ivanov', 6), ('Anna', 'Romanova', 1), ('Elena', 'Sidorova', 3),
    ('Julia', 'Ivanova', 3), ('Ainura', 'Mamateminova', 1), ('Saito', 'Tanaka', 5), ('Mikasa', 'Ackerman', 4),
    ('Jackson', 'Wang', 2), ('Xiao', 'Zhang', 7), ('Bektur', 'Aytmatov', 3), ('Sana', 'Minatozaki', 5),
    ('Momo', 'Hirai', 4), ('Nayeon', 'Im', 6), ('Yuqi', 'Song', 7)
]
cursor.executemany('INSERT INTO employees (first_name, last_name, city_id) VALUES (?, ?, ?)', employees_data)

conn.commit()
conn.close()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT id, title FROM cities')
cities = cursor.fetchall()


while True:
    cursor.execute('SELECT id, title FROM cities')
    cities = cursor.fetchall()

    print("Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, для выхода введите 0:")
    for city in cities:
        print(f'{city[0]}. {city[1]}')

    selected_city_id = int(input('Введите id города (для выхода введите 0): '))

    if selected_city_id == 0:
        break

    cursor.execute('''SELECT employees.first_name, employees.last_name, 
                      countries.title AS country, cities.title AS city, cities.area 
                      FROM employees
                      JOIN cities ON employees.city_id = cities.id
                      JOIN countries ON cities.country_id = countries.id
                      WHERE cities.id = ?''', (selected_city_id,))
    employees = cursor.fetchall()

    if employees:
        print(f'Сотрудники, проживающие в выбранном городе:')
        for employee in employees:
            print(f'Имя: {employee[0]}, Фамилия: {employee[1]}, Страна: {employee[2]}, Город: {employee[3]}, Площадь города: {employee[4]}')
    else:
        print('В выбранном городе нет сотрудников.')

conn.close()
