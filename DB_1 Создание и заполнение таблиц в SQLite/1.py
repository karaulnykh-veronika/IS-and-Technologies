import sqlite3 # Для работы с SQLite базой данных
import pandas as pd # Для работы с таблицами и CSV файлами
import os # Для работы с путями к файлам и папкам

# 1.Определение папки для базы данных
current_folder = os.path.dirname(os.path.abspath(__file__)) # берёт только папку (обрезает имя файла)
db_path = os.path.join(current_folder, "database.db") # склеивает путь к папке и имя файла database.db

print(f"Папка с кодом: {current_folder}")
print(f"База данных: {db_path}")

conn = sqlite3.connect(db_path) # открывает соединение с БД
cursor = conn.cursor() # создаёт курсор (через него выполняем SQL)

# 2.Создание таблиц (SQL)
# Таблица  "Должности"
cursor.execute("""
CREATE TABLE IF NOT EXISTS Должности (
    Код_должности INTEGER PRIMARY KEY NOT NULL UNIQUE,
    Название TEXT NOT NULL
); 
""") # Создаем таблицу,если её ещё нет/главный ключ(уникальный ID)/Поле не может быть пустым/значения не могут повторяться/текстовое поле-обязательно
# Таблица "Сотрудники"
cursor.execute("""
CREATE TABLE IF NOT EXISTS Сотрудники (
    Код_сотрудника INTEGER PRIMARY KEY NOT NULL UNIQUE,
    Фамилия TEXT NOT NULL,
    Имя TEXT NOT NULL,
    Телефон TEXT,
    Код_должности INTEGER NOT NULL,
    FOREIGN KEY (Код_должности) REFERENCES Должности(Код_должности)
);
""")
# Таблица "Клиенты"
cursor.execute("""
CREATE TABLE IF NOT EXISTS Клиенты (
    Код_клиента INTEGER PRIMARY KEY NOT NULL UNIQUE,
    Организация TEXT NOT NULL,
    Телефон TEXT
);
""")
# Таблица "Заказы"
cursor.execute("""
CREATE TABLE IF NOT EXISTS Заказы (
    Код_заказа INTEGER PRIMARY KEY NOT NULL UNIQUE,
    Код_клиента INTEGER NOT NULL,
    Код_сотрудника INTEGER NOT NULL,
    Сумма REAL NOT NULL,
    Дата_выполнения TEXT,
    Отметка_о_выполнении TEXT,
    FOREIGN KEY (Код_клиента) REFERENCES Клиенты(Код_клиента),
    FOREIGN KEY (Код_сотрудника) REFERENCES Сотрудники(Код_сотрудника)
);
""")

print("Таблицы созданы")

# 3.Заполнение таблиц
# Данные для таблицы "Должности"
должности_data = [
    (1, 'Менеджер'),
    (2, 'Разработчик'),
    (3, 'Аналитик')
]
cursor.executemany("INSERT OR IGNORE INTO Должности VALUES (?, ?)", должности_data) # Выполняет INSERT для всех записей из списка/добавляет запись-если такой ID уже есть-пропускает/Места для подстановки значений (защита от SQL-инъекций)
# Данные для таблицы "Сотрудники"
сотрудники_data = [
    (1, 'Иванов', 'Иван', '89001234567', 1),
    (2, 'Петрова', 'Мария', '89007654321', 2),
    (3, 'Сидоров', 'Алексей', '89005556677', 3)
]
cursor.executemany("INSERT OR IGNORE INTO Сотрудники VALUES (?, ?, ?, ?, ?)", сотрудники_data)
# Данные для таблицы "Клиенты"
клиенты_data = [
    (1, 'ООО "Ромашка"', '84951234567'),
    (2, 'ИП Иванов', '84957654321'),
    (3, 'ЗАО "Весна"', '84959998877')
]
cursor.executemany("INSERT OR IGNORE INTO Клиенты VALUES (?, ?, ?)", клиенты_data)
# Данные для таблицы "Заказы"
заказы_data = [
    (101, 1, 1, 15000.0, '2025-03-01', 'Выполнен'),
    (102, 2, 2, 25000.0, '2025-03-05', 'Выполнен'),
    (103, 1, 3, 10000.0, '2025-03-10', 'В работе'),
    (104, 3, 1, 50000.0, '2025-03-15', 'Выполнен'),
    (105, 2, 2, 8000.0, '2025-03-20', 'Отменён')
]
cursor.executemany("INSERT OR IGNORE INTO Заказы VALUES (?, ?, ?, ?, ?, ?)", заказы_data)

conn.commit()
print("Таблицы заполнены данными")

# 4.Простые запросы
print("\n" + "=" * 60)
print("ПРОСТЫЕ ЗАПРОСЫ")
print("=" * 60)
# 1. Все сотрудники
cursor.execute("SELECT * FROM Сотрудники") # берем все колонки из таблицы "Сотрудники"
print("\n1. Все сотрудники:")
for row in cursor.fetchall(): # проходим по каждой строке и выводим-получаем все строки результата в виде списка
    print(f"   {row}")
# 2. Все должности
cursor.execute("SELECT * FROM Должности")
print("\n2. Все должности:")
for row in cursor.fetchall():
    print(f"   {row}")
# 3. Все клиенты
cursor.execute("SELECT * FROM Клиенты")
print("\n3. Все клиенты:")
for row in cursor.fetchall():
    print(f"   {row}")
# 4. Все заказы
cursor.execute("SELECT * FROM Заказы")
print("\n4. Все заказы:")
for row in cursor.fetchall():
    print(f"   {row}")
# 5. Сотрудники с телефонами
cursor.execute("SELECT Фамилия, Имя, Телефон FROM Сотрудники")
print("\n5. Контакты сотрудников:")
for row in cursor.fetchall():
    print(f"   {row[0]} {row[1]}: {row[2]}")

# 5.Запросы с агрегацией
print("\n" + "=" * 60)
print("ЗАПРОСЫ С АГРЕГАЦИЕЙ")
print("=" * 60)
# COUNT-количество заказов
cursor.execute("SELECT COUNT(*) FROM Заказы")
print(f"\n1. Всего заказов: {cursor.fetchone()[0]}")
# SUM-общая сумма всех заказов
cursor.execute("SELECT SUM(Сумма) FROM Заказы")
print(f"2. Общая сумма всех заказов: {cursor.fetchone()[0]} руб.")
#AVG-средняя сумма заказа
cursor.execute("SELECT AVG(Сумма) FROM Заказы")
print(f"3. Средняя сумма заказа: {round(cursor.fetchone()[0], 2)} руб.")

# 6.Запросы с объединением (JOIN)
# Берём две таблицы(например Сотрудники и Должности)/соединяем их по условию(Код_должности совпадает)/В результате получаем:фамилия,имя из первой + название должности из второй
print("\n" + "=" * 60)
print("ЗАПРОСЫ С ОБЪЕДИНЕНИЕМ И УСЛОВИЯМИ")
print("=" * 60)
# Сотрудники+их должности
cursor.execute("""
    SELECT Сотрудники.Фамилия, Сотрудники.Имя, Должности.Название
    FROM Сотрудники
    JOIN Должности ON Сотрудники.Код_должности = Должности.Код_должности
""")
print("\n1. Сотрудники и их должности:")
for row in cursor.fetchall():
    print(f"   {row[0]} {row[1]} - {row[2]}")

# Заказы+клиенты+сотрудники
cursor.execute("""
    SELECT Заказы.Код_заказа, Клиенты.Организация, Сотрудники.Фамилия, Заказы.Сумма, Заказы.Отметка_о_выполнении
    FROM Заказы
    JOIN Клиенты ON Заказы.Код_клиента = Клиенты.Код_клиента
    JOIN Сотрудники ON Заказы.Код_сотрудника = Сотрудники.Код_сотрудника
    WHERE Заказы.Отметка_о_выполнении = 'Выполнен'
""")
print("\n2. Выполненные заказы с информацией:")
for row in cursor.fetchall():
    print(f"   Заказ {row[0]}: {row[1]} → сотрудник {row[2]}, сумма {row[3]} руб.")

# Сумма заказов по каждому сотруднику
cursor.execute("""
    SELECT Сотрудники.Фамилия, Сотрудники.Имя, SUM(Заказы.Сумма) as Общая_сумма
    FROM Заказы
    JOIN Сотрудники ON Заказы.Код_сотрудника = Сотрудники.Код_сотрудника
    GROUP BY Сотрудники.Код_сотрудника
""")
print("\n3. Общая сумма заказов по сотрудникам:")
for row in cursor.fetchall():
    print(f"   {row[0]} {row[1]}: {row[2]} руб.")

# 7. ЭКСПОРТ И ИМПОРТ ИЗ CSV
print("\n" + "=" * 60)
print("ИМПОРТ/ЭКСПОРТ CSV")
print("=" * 60)
# Экспорт таблиц в CSV
pd.read_sql_query("SELECT * FROM Сотрудники", conn).to_csv(os.path.join(current_folder, "Сотрудники.csv"), index=False)
pd.read_sql_query("SELECT * FROM Должности", conn).to_csv(os.path.join(current_folder, "Должности.csv"), index=False)
pd.read_sql_query("SELECT * FROM Клиенты", conn).to_csv(os.path.join(current_folder, "Клиенты.csv"), index=False)
pd.read_sql_query("SELECT * FROM Заказы", conn).to_csv(os.path.join(current_folder, "Заказы.csv"), index=False)

print("Таблицы экспортированы в CSV файлы")

# Импорт из CSV в новые таблицы (для демонстрации)
сотрудники_df = pd.read_csv(os.path.join(current_folder, "Сотрудники.csv"))
сотрудники_df.to_sql('csv_Сотрудники', conn, if_exists='replace', index=False)

print("Импорт из CSV выполнен)")

# 8. ЗАКРЫТИЕ
conn.commit() # сохранение изменений
conn.close() # закрытие соединения

print("\n" + "=" * 60)
print(f"База данных: {db_path}")
print("=" * 60)