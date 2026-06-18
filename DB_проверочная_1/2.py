import sqlite3 # sqlite3-позволяет Python работать с базами данных SQLite
import pandas as pd # pandas (pd)-помогает читать/писать CSV файлы и работать с таблицами
import os # os-нужен для работы с путями к файлам (чтобы найти папку, где лежит программа)

current_folder = os.path.dirname(os.path.abspath(__file__))
if current_folder == "":
    current_folder = os.getcwd()  

print(f"ВСЕ ФАЙЛЫ БУДУТ СОХРАНЕНЫ В:")
print(f"   {current_folder}")
print("=" * 60)
# Создаём данные для таблицы "Категории"
# pd.DataFrame() — создаёт таблицу в памяти Python
categories_data = pd.DataFrame([
    {"Код_категории": 1, "Название": "Электроника"},
    {"Код_категории": 2, "Название": "Одежда"},
    {"Код_категории": 3, "Название": "Книги"}
])
categories_path = os.path.join(current_folder, "категории.csv")
categories_data.to_csv(categories_path, index=False, encoding="utf-8-sig")
print(f"✅ создан: {categories_path}")

# таблица "Товары"
products_data = pd.DataFrame([
    {"Код_товара": 101, "Название": "Ноутбук", "Код_категории": 1, "Цена": 50000},
    {"Код_товара": 102, "Название": "Мышь", "Код_категории": 1, "Цена": 1500},
    {"Код_товара": 103, "Название": "Футболка", "Код_категории": 2, "Цена": 1200},
    {"Код_товара": 104, "Название": "Учебник Python", "Код_категории": 3, "Цена": 800},
    {"Код_товара": 105, "Название": "Наушники", "Код_категории": 1, "Цена": 3000}
])
products_path = os.path.join(current_folder, "товары.csv")
products_data.to_csv(products_path, index=False, encoding="utf-8-sig")
print(f"✅ создан: {products_path}")

#таблица "Продажи"
sales_data = pd.DataFrame([
    {"Код_продажи": 1, "Код_товара": 101, "Дата": "2025-01-10", "Количество": 2},
    {"Код_продажи": 2, "Код_товара": 102, "Дата": "2025-01-15", "Количество": 5},
    {"Код_продажи": 3, "Код_товара": 103, "Дата": "2025-01-20", "Количество": 3},
    {"Код_продажи": 4, "Код_товара": 104, "Дата": "2025-01-25", "Количество": 4},
    {"Код_продажи": 5, "Код_товара": 105, "Дата": "2025-02-01", "Количество": 2},
    {"Код_продажи": 6, "Код_товара": 101, "Дата": "2025-01-05", "Количество": 1}
])
sales_path = os.path.join(current_folder, "продажи.csv")
sales_data.to_csv(sales_path, index=False, encoding="utf-8-sig")
print(f"✅ создан: {sales_path}")

# Собираем полный путь к файлу базы данных
db_path = os.path.join(current_folder, "database.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"\nБаза данных создана: {db_path}")


# 4. ИМПОРТ ДАННЫХ ИЗ CSV В SQLite
# 4.Импорт данных из CVS в SQLite
# pd.read_csv()-читает CSV файл и превращает его в DataFrame (таблицу в памяти)
categories = pd.read_csv(categories_path)
products = pd.read_csv(products_path)
sales = pd.read_csv(sales_path)

# to_sql()-сохраняет DataFrame в базу данных SQLite
# conn — соединение с БД
# if_exists="replace"-если таблица уже есть, заменить её новой
# index=False-не сохранять номера строк
categories.to_sql("Категории", conn, if_exists="replace", index=False)
products.to_sql("Товары", conn, if_exists="replace", index=False)
sales.to_sql("Продажи", conn, if_exists="replace", index=False)

print("✅ Данные импортированы в SQLite")

# 5. SQL запрос
print("\n" + "=" * 60)
print("ЗАПРОС: Сумма продаж электроники за январь 2025")
print("=" * 60)

# Это SQL запрос на русском языке
# Он:
# 1. Берёт таблицы: Продажи, Товары, Категории
# 2. Соединяет их (JOIN) по кодам товаров и категорий
# 3. Фильтрует (WHERE) только электронику и январь 2025
# 4. Считает сумму (SUM) = цена * количество
query = """
SELECT SUM(Товары.Цена * Продажи.Количество) AS Сумма_продаж
FROM Продажи
JOIN Товары ON Продажи.Код_товара = Товары.Код_товара
JOIN Категории ON Товары.Код_категории = Категории.Код_категории
WHERE Категории.Название = 'Электроника'
  AND Продажи.Дата BETWEEN '2025-01-01' AND '2025-01-31'
"""

# pd.read_sql() — выполняет SQL запрос и возвращает результат в виде DataFrame
result = pd.read_sql(query, conn)
print("\n📊 РЕЗУЛЬТАТ:")
print(result)

# Сохраняем результат в CSV файл
result_path = os.path.join(current_folder, "результат_запроса.csv")
result.to_csv(result_path, index=False)
print(f"\n✅ Результат сохранён: {result_path}")

# ============================================================
# 6. ВЫВОД ВСЕХ ТАБЛИЦ (для проверки и для отчёта)
# ============================================================
print("\n" + "=" * 60)
print("ТАБЛИЦЫ ДЛЯ ОТЧЁТА")
print("=" * 60)

# Читаем и выводим таблицу "Категории"
print("\n📌 Категории:")
print(pd.read_sql("SELECT * FROM Категории", conn))

# Читаем и выводим таблицу "Товары"
print("\n📌 Товары:")
print(pd.read_sql("SELECT * FROM Товары", conn))

# Читаем и выводим таблицу "Продажи"
print("\n📌 Продажи:")
print(pd.read_sql("SELECT * FROM Продажи", conn))

# ============================================================
# 7. ЗАКРЫТИЕ СОЕДИНЕНИЯ С БАЗОЙ ДАННЫХ
# ============================================================
# conn.close() — закрывает соединение. ОЧЕНЬ ВАЖНО!
# Если не закрыть, файл БД может повредиться или данные не сохранятся
conn.close()

print("\n" + "=" * 60)
print("✅ ВСЕ ФАЙЛЫ СОЗДАНЫ В ПАПКЕ:")
print(f"   {current_folder}")
print("=" * 60)