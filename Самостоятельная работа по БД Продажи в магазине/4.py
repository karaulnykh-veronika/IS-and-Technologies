# ============================================================
# ПОДКЛЮЧЕНИЕ БИБЛИОТЕК
# ============================================================
# sqlite3 — для работы с базой данных SQLite
import sqlite3
# tkinter — для создания графического интерфейса (окна, кнопки, таблицы)
import tkinter as tk
# ttk — улучшенные виджеты (вкладки, таблицы с прокруткой)
from tkinter import ttk, messagebox
# datetime — для работы с датами (сегодняшняя дата, форматирование)
from datetime import datetime

# ============================================================
# 1. СОЗДАНИЕ БАЗЫ ДАННЫХ И ТАБЛИЦ
# ============================================================
def init_database():
    """
    Создаёт базу данных 'sales.db' и все необходимые таблицы.
    Если таблицы уже существуют — не пересоздаёт.
    Заполняет таблицы тестовыми данными, если они пустые.
    """
    # Подключаемся к файлу базы данных (создаётся автоматически)
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    
    # ===== ТАБЛИЦА 1: Должности (job_titles) =====
    # id — первичный ключ (PRIMARY KEY), уникальный номер
    # name — название должности (Продавец-кассир, Старший кассир, Администратор)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_titles (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL
    );
    """)
    
    # ===== ТАБЛИЦА 2: Сотрудники (employees) =====
    # FOREIGN KEY (id_job_title) — ссылается на таблицу job_titles
    # Это означает: у каждого сотрудника есть должность
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        id_job_title INTEGER NOT NULL,
        FOREIGN KEY (id_job_title) REFERENCES job_titles(id)
    );
    """)
    
    # ===== ТАБЛИЦА 3: Категории товаров (categories) =====
    # Например: Электроника, Продукты питания, Канцелярия, Бытовая химия
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id_category INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name_category TEXT NOT NULL
    );
    """)
    
    # ===== ТАБЛИЦА 4: Товары (products) =====
    # FOREIGN KEY (id_category) — ссылается на категории
    # quantity_at_storage — остаток на складе
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id_product INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name_of_product TEXT NOT NULL,
        price REAL NOT NULL,
        id_category INTEGER NOT NULL,
        quantity_at_storage REAL NOT NULL,
        FOREIGN KEY (id_category) REFERENCES categories(id_category)
    );
    """)
    
    # ===== ТАБЛИЦА 5: Чеки (receipts) =====
    # created_at — дата и время создания чека
    # id_cashier — ссылка на сотрудника (кассира)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        id_check INTEGER PRIMARY KEY NOT NULL UNIQUE,
        created_at TEXT NOT NULL,
        id_cashier INTEGER NOT NULL,
        FOREIGN KEY (id_cashier) REFERENCES employees(id)
    );
    """)
    
    # ===== ТАБЛИЦА 6: Позиции в чеках (sale_items) =====
    # Связывает чеки с товарами: сколько и чего купили
    # FOREIGN KEY (id_check) → receipts, (id_product) → products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        id_sale INTEGER PRIMARY KEY NOT NULL UNIQUE,
        id_check INTEGER NOT NULL,
        id_product INTEGER NOT NULL,
        quantity REAL NOT NULL,
        FOREIGN KEY (id_check) REFERENCES receipts(id_check),
        FOREIGN KEY (id_product) REFERENCES products(id_product)
    );
    """)
    
    # ===== ЗАПОЛНЕНИЕ ДАННЫМИ (если таблицы пустые) =====
    
    # Проверяем, есть ли данные в таблице должностей
    cursor.execute("SELECT COUNT(*) FROM job_titles")
    if cursor.fetchone()[0] == 0:
        # Добавляем должности
        cursor.executemany("INSERT INTO job_titles VALUES (?, ?)", [
            (1, 'Продавец-кассир'),
            (2, 'Старший кассир'),
            (3, 'Администратор')
        ])
        
        # Добавляем сотрудников
        cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", [
            (1, 'Иван', 'Иванов', 1),
            (2, 'Мария', 'Петрова', 2),
            (3, 'Ольга', 'Сидорова', 1),
            (4, 'Алексей', 'Козлов', 3)
        ])
        
        # Добавляем категории товаров
        cursor.executemany("INSERT INTO categories VALUES (?, ?)", [
            (1, 'Электроника'),
            (2, 'Продукты питания'),
            (3, 'Канцелярия'),
            (4, 'Бытовая химия')
        ])
        
        # Добавляем товары
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", [
            (101, 'Ноутбук', 50000, 1, 10),
            (102, 'Мышь', 1500, 1, 50),
            (103, 'Хлеб', 50, 2, 100),
            (104, 'Молоко', 80, 2, 30),
            (105, 'Тетрадь', 30, 3, 200),
            (106, 'Ручка', 20, 3, 500),
            (107, 'Порошок стиральный', 400, 4, 20),
            (108, 'Средство для мытья посуды', 150, 4, 15)
        ])
    
    # Проверяем, есть ли чеки
    cursor.execute("SELECT COUNT(*) FROM receipts")
    if cursor.fetchone()[0] == 0:
        # Добавляем чеки за 2025 и 2026 годы
        cursor.executemany("INSERT INTO receipts VALUES (?, ?, ?)", [
            # Чеки за 2025 год
            (1, '2025-05-25 10:30:00', 1),
            (2, '2025-05-25 11:15:00', 1),
            (3, '2025-05-25 12:00:00', 3),
            (4, '2025-05-26 14:30:00', 1),
            (5, '2025-05-26 16:45:00', 2),
            (6, '2025-05-27 09:00:00', 1),
            (7, '2025-05-27 13:20:00', 3),
            (8, '2025-05-27 18:30:00', 2),
            # Чеки за 2026 год
            (9, '2026-05-25 10:00:00', 1),
            (10, '2026-05-26 12:00:00', 2),
            (11, '2026-05-27 11:00:00', 1),
            (12, '2026-05-27 15:30:00', 3),
            (13, '2026-05-27 18:00:00', 1),
        ])
    
    # Проверяем, есть ли позиции в чеках
    cursor.execute("SELECT COUNT(*) FROM sale_items")
    if cursor.fetchone()[0] == 0:
        # Добавляем позиции (какие товары и в каком количестве купили)
        cursor.executemany("INSERT INTO sale_items VALUES (?, ?, ?, ?)", [
            # 2025-05-25
            (1, 1, 101, 1),   # В чеке 1 купили ноутбук 1 шт
            (2, 1, 102, 2),   # В чеке 1 купили мышь 2 шт
            (3, 2, 103, 3),   # В чеке 2 купили хлеб 3 шт
            (4, 2, 104, 2),   # В чеке 2 купили молоко 2 шт
            (5, 3, 105, 5),   # В чеке 3 купили тетради 5 шт
            (6, 3, 106, 10),  # В чеке 3 купили ручки 10 шт
            # 2025-05-26
            (7, 4, 107, 1),
            (8, 4, 108, 2),
            (9, 5, 101, 1),
            (10, 5, 102, 1),
            # 2025-05-27
            (11, 6, 103, 5),
            (12, 6, 104, 3),
            (13, 7, 106, 20),
            (14, 7, 105, 10),
            (15, 8, 108, 3),
            # 2026-05-25
            (16, 9, 101, 1),
            (17, 9, 102, 2),
            # 2026-05-26
            (18, 10, 103, 5),
            (19, 10, 104, 3),
            # 2026-05-27
            (20, 11, 101, 2),
            (21, 11, 102, 1),
            (22, 12, 107, 2),
            (23, 12, 108, 1),
            (24, 13, 105, 10),
            (25, 13, 106, 15),
        ])
    
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована с данными за 2025 и 2026 годы")

# ============================================================
# 2. ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ
# ============================================================

def get_revenue_by_date(date):
    """
    Получить выручку за указанную дату.
    date — строка в формате 'ГГГГ-ММ-ДД' (например '2025-05-27')
    Возвращает сумму продаж за этот день (число).
    """
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    # IFNULL — если сумма = NULL, возвращает 0 (чтобы не было ошибки)
    # JOIN — соединяем таблицы: чеки → позиции → товары
    # DATE(r.created_at) — берём только дату из полной даты+время
    cursor.execute("""
        SELECT IFNULL(SUM(si.quantity * p.price), 0) AS revenue
        FROM receipts r
        JOIN sale_items si ON r.id_check = si.id_check
        JOIN products p ON si.id_product = p.id_product
        WHERE DATE(r.created_at) = ?
    """, (date,))
    result = cursor.fetchone()[0]  # Берем первое значение из результата
    conn.close()
    return result

def get_sales_by_date(date):
    """
    Получить список проданных товаров за указанную дату.
    Возвращает список кортежей: (название_товара, количество, сумма)
    """
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    # GROUP BY — группируем по каждому товару
    # SUM — суммируем количество и сумму по каждому товару
    cursor.execute("""
        SELECT 
            p.name_of_product AS Товар,
            SUM(si.quantity) AS Количество,
            SUM(si.quantity * p.price) AS Сумма
        FROM sale_items si
        JOIN products p ON si.id_product = p.id_product
        JOIN receipts r ON si.id_check = r.id_check
        WHERE DATE(r.created_at) = ?
        GROUP BY p.id_product
        ORDER BY Сумма DESC
    """, (date,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_sales_summary():
    """
    Получить сводку по всем продажам (выручка по дням).
    Возвращает список кортежей: (дата, количество_чеков, выручка)
    """
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    # COUNT(DISTINCT) — считаем уникальные чеки (чтобы не дублировать)
    cursor.execute("""
        SELECT 
            DATE(r.created_at) AS Дата,
            COUNT(DISTINCT r.id_check) AS Чеков,
            SUM(si.quantity * p.price) AS Выручка
        FROM receipts r
        JOIN sale_items si ON r.id_check = si.id_check
        JOIN products p ON si.id_product = p.id_product
        GROUP BY DATE(r.created_at)
        ORDER BY Дата DESC
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def get_products_stock():
    """
    Получить остатки товаров на складе.
    Возвращает список кортежей: (название, категория, цена, остаток)
    """
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    # ORDER BY — сортируем по категории, затем по названию
    cursor.execute("""
        SELECT 
            p.name_of_product,
            c.name_category,
            p.price,
            p.quantity_at_storage
        FROM products p
        JOIN categories c ON p.id_category = c.id_category
        ORDER BY c.name_category, p.name_of_product
    """)
    result = cursor.fetchall()
    conn.close()
    return result

# ============================================================
# 3. ГРАФИЧЕСКИЙ ИНТЕРФЕЙС (Tkinter)
# ============================================================

class SalesApp:
    """
    Главный класс приложения. Создаёт окно с тремя вкладками:
    1. Продажи за дату
    2. Сводка по дням
    3. Остатки товаров
    """
    
    def __init__(self, root):
        """
        Конструктор. Вызывается при создании приложения.
        root — главное окно (tk.Tk())
        """
        self.root = root
        self.root.title("Магазин - Система учёта продаж")  # Заголовок окна
        self.root.geometry("850x650")  # Размер окна (ширина x высота)
        self.root.resizable(True, True)  # Можно изменять размер окна
        
        # Создаём виджет "Блокнот" для вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== ВКЛАДКА 1: ПРОДАЖИ ЗА ДАТУ =====
        self.tab_date = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_date, text="📊 Продажи за дату")
        self.setup_tab_date()
        
        # ===== ВКЛАДКА 2: СВОДКА ПО ДНЯМ =====
        self.tab_summary = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_summary, text="📈 Сводка по дням")
        self.setup_tab_summary()
        
        # ===== ВКЛАДКА 3: ОСТАТКИ ТОВАРОВ =====
        self.tab_products = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_products, text="📦 Остатки товаров")
        self.setup_tab_products()
        
        # Загружаем данные для сводки и остатков
        self.refresh_summary()
        self.refresh_products()
    
    # ========== НАСТРОЙКА ВКЛАДКИ "ПРОДАЖИ ЗА ДАТУ" ==========
    def setup_tab_date(self):
        """Создаёт интерфейс для просмотра продаж за выбранную дату"""
        
        # Верхняя панель с выбором даты
        top_frame = tk.Frame(self.tab_date)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Надпись "Выберите дату:"
        tk.Label(top_frame, text="Выберите дату:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        # Поле для ввода даты (по умолчанию 2025-05-27 — там точно есть продажи)
        self.date_var = tk.StringVar(value="2025-05-27")
        self.date_entry = tk.Entry(top_frame, textvariable=self.date_var, width=12, font=("Arial", 12))
        self.date_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопка "Показать" — вызывает функцию show_sales
        self.show_btn = tk.Button(top_frame, text="Показать", command=self.show_sales, 
                                   bg="#4CAF50", fg="white", font=("Arial", 10))
        self.show_btn.pack(side=tk.LEFT, padx=10)
        
        # Кнопка "Сегодня" — подставляет сегодняшнюю дату
        self.today_btn = tk.Button(top_frame, text="Сегодня", command=self.set_today,
                                    bg="#2196F3", fg="white", font=("Arial", 10))
        self.today_btn.pack(side=tk.LEFT, padx=5)
        
        # Подсказка: какие даты есть в базе данных
        hint_label = tk.Label(top_frame, text="(есть данные: 2025-05-25, 2025-05-26, 2025-05-27, 2026-05-25, 2026-05-26, 2026-05-27)", 
                              fg="gray", font=("Arial", 9))
        hint_label.pack(side=tk.LEFT, padx=15)
        
        # Фрейм для отображения выручки (с зелёным фоном)
        revenue_frame = tk.Frame(self.tab_date, bg="#e8f5e9", height=80)
        revenue_frame.pack(fill=tk.X, padx=10, pady=10)
        revenue_frame.pack_propagate(False)  # Фиксируем высоту
        
        self.revenue_label = tk.Label(revenue_frame, text="Выручка: 0 руб.", 
                                       font=("Arial", 18, "bold"), bg="#e8f5e9", fg="#2e7d32")
        self.revenue_label.pack(expand=True)
        
        # Таблица для отображения товаров
        columns = ("Товар", "Количество", "Сумма")
        self.tree = ttk.Treeview(self.tab_date, columns=columns, show="headings", height=15)
        
        # Настройка заголовков таблицы
        self.tree.heading("Товар", text="Товар")
        self.tree.heading("Количество", text="Количество (шт)")
        self.tree.heading("Сумма", text="Сумма (руб)")
        
        # Настройка ширины колонок
        self.tree.column("Товар", width=350)
        self.tree.column("Количество", width=150)
        self.tree.column("Сумма", width=150)
        
        # Полоса прокрутки для таблицы
        scrollbar = ttk.Scrollbar(self.tab_date, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Загружаем данные для даты по умолчанию
        self.show_sales()
    
    def setup_tab_summary(self):
        """Создаёт интерфейс для сводки по продажам по дням"""
        
        # Таблица: Дата, Количество чеков, Выручка
        columns = ("Дата", "Чеков", "Выручка")
        self.summary_tree = ttk.Treeview(self.tab_summary, columns=columns, show="headings", height=20)
        
        self.summary_tree.heading("Дата", text="Дата")
        self.summary_tree.heading("Чеков", text="Количество чеков")
        self.summary_tree.heading("Выручка", text="Выручка (руб)")
        
        self.summary_tree.column("Дата", width=150)
        self.summary_tree.column("Чеков", width=150)
        self.summary_tree.column("Выручка", width=200)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.tab_summary, orient=tk.VERTICAL, command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=scrollbar.set)
        
        self.summary_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Кнопка обновления
        refresh_btn = tk.Button(self.tab_summary, text="🔄 Обновить", command=self.refresh_summary,
                                 bg="#FF9800", fg="white", font=("Arial", 10))
        refresh_btn.pack(pady=5)
    
    def setup_tab_products(self):
        """Создаёт интерфейс для просмотра остатков товаров на складе"""
        
        # Таблица: Товар, Категория, Цена, Остаток
        columns = ("Товар", "Категория", "Цена", "Остаток")
        self.products_tree = ttk.Treeview(self.tab_products, columns=columns, show="headings", height=20)
        
        self.products_tree.heading("Товар", text="Товар")
        self.products_tree.heading("Категория", text="Категория")
        self.products_tree.heading("Цена", text="Цена (руб)")
        self.products_tree.heading("Остаток", text="Остаток на складе")
        
        self.products_tree.column("Товар", width=250)
        self.products_tree.column("Категория", width=150)
        self.products_tree.column("Цена", width=100)
        self.products_tree.column("Остаток", width=150)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.tab_products, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Кнопка обновления
        refresh_btn = tk.Button(self.tab_products, text="🔄 Обновить", command=self.refresh_products,
                                 bg="#FF9800", fg="white", font=("Arial", 10))
        refresh_btn.pack(pady=5)
    
    def set_today(self):
        """Устанавливает сегодняшнюю дату в поле ввода и показывает продажи"""
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.show_sales()
    
    def show_sales(self):
        """Показывает продажи за выбранную дату (выручка + список товаров)"""
        date = self.date_var.get()
        
        # Проверка формата даты (должно быть ГГГГ-ММ-ДД)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД\nНапример: 2025-05-27")
            return
        
        # Получаем выручку из базы данных
        revenue = get_revenue_by_date(date)
        
        # Обновляем текст выручки (красный — если нет продаж)
        if revenue == 0:
            self.revenue_label.config(text=f"Выручка за {date}: 0 руб. (нет продаж)", fg="#d32f2f")
        else:
            self.revenue_label.config(text=f"Выручка за {date}: {revenue:,.2f} руб.", fg="#2e7d32")
        
        # Очищаем таблицу перед загрузкой новых данных
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем список проданных товаров
        sales = get_sales_by_date(date)
        total_quantity = 0
        total_amount = 0
        
        # Заполняем таблицу
        for sale in sales:
            self.tree.insert("", tk.END, values=(sale[0], f"{sale[1]:.0f}", f"{sale[2]:,.2f}"))
            total_quantity += sale[1]
            total_amount += sale[2]
        
        # Добавляем итоговую строку
        if sales:
            self.tree.insert("", tk.END, values=("═════════════════", "═══════════", "═══════════════"))
            self.tree.insert("", tk.END, values=("ИТОГО:", f"{total_quantity:.0f}", f"{total_amount:,.2f}"))
        else:
            self.tree.insert("", tk.END, values=("Нет продаж за выбранную дату", "", ""))
    
    def refresh_summary(self):
        """Обновляет таблицу со сводкой по дням"""
        # Очищаем таблицу
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
        
        # Получаем данные из базы
        data = get_all_sales_summary()
        
        # Заполняем таблицу
        for row in data:
            self.summary_tree.insert("", tk.END, values=(row[0], row[1], f"{row[2]:,.2f}"))
    
    def refresh_products(self):
        """Обновляет таблицу с остатками товаров"""
        # Очищаем таблицу
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Получаем данные из базы
        products = get_products_stock()
        
        # Заполняем таблицу
        for product in products:
            self.products_tree.insert("", tk.END, values=(
                product[0],   # Название товара
                product[1],   # Категория
                f"{product[2]:,.2f}",  # Цена (с двумя знаками)
                f"{product[3]:.0f}"    # Остаток
            ))

# ============================================================
# 4. ЗАПУСК ПРИЛОЖЕНИЯ
# ============================================================

if __name__ == "__main__":
    # Сначала создаём/инициализируем базу данных
    init_database()
    
    # Создаём главное окно Tkinter
    root = tk.Tk()
    # Создаём объект приложения (внутри создаются все вкладки)
    app = SalesApp(root)
    # Запускаем главный цикл обработки событий (окно открывается)
    root.mainloop()