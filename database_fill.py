import sqlite3 as sl

con = sl.connect('deitabeiza.db')
# run this file if u need to refill the base

# drop all tables func
if con:
    with con:
        del_query = con.execute("""SELECT name FROM sqlite_master
      WHERE type='table'; """)
        del_query = [i[0] for i in del_query.fetchall() if i[0] != 'sqlite_sequence']
        print(del_query)
        if del_query:
            print('base is dead now\n')
            for i in del_query:
                con.execute(f"""
                        DROP TABLE IF EXISTS '{i}'
                    """)
        else:
            print('base is dead')

# some lists for filling
programs_list = [["Windows"],
                   ["Winrar"]]
# categories_list = [["Книги"],
#                    ["Сладости"],
#                    ["Электроника"],
#                    ["Бытовая техника"],
#                    ["Смартфоны и гаджеты"],
#                    ["Игры и игрушки"],
#                    ["Наушники и акустика"],
#                    ["Текстиль и ковры"],
#                    ["Одежда"],
#                    ["Обувь"],
#                    ["Канцелярия"],
#                    ["Мебель"],
#                    ["Аксессуары"]]
manuals_list = [("Установка Windows", 1),
               ("Переустановка Windows", 1),
               ("Активация Winrar", 2),
                ("Аналоги Winrar", 2)]
# contractors_list = [
#     ("Иванов Иван", "ООО Рога и Копыта", 79123456789, "Москва, ул. Ленина, д.10", "123456789", "Поставщик"),
#     ("Петров Петр", "ИП Петров", 79234567890, "Санкт-Петербург, пр. Невский, д.20", "234567890", "Покупатель"),
#     ("Сидоров Сидор", "ООО Сидор и Ко", 79345678901, "Екатеринбург, ул. Кирова, д.5", "345678901", "Поставщик"),
#     ("Козлов Константин", "ИП Козлов", 79456789012, "Москва, ул. Арбат, д.15", "456789012", "Покупатель"),
#     ("Николаев Николай", "ОАО Николаев и партнеры", 79567890123,
#      "Санкт-Петербург, ул. Рубинштейна, д.8", "567890123", "Поставщик"),
#     ("Григорьев Григорий", "ИП Григорьев", 79678901234, "Екатеринбург, ул. Малышева, д.50", "678901234",
#      "Покупатель")]
tags_list = [("Установка Windows", 0, 1),
              ("Переустановка Windows", 0, 2),
              ("Активация Winrar", 0, 3),
              ("Аналоги Winrar", 0, 4),
              ("Установка Виндоус", 0, 1),
              ("Установка Виндоус", 0, 2)]
stars_list = [(40, 10, 1),
               (40, 10, 2),
               (40, 10, 3),
                (40, 10, 4)]


# creating the base
with con:
    # Manuals
    con.execute("""
        CREATE TABLE IF NOT EXISTS Manuals(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            manu_name TEXT,
            program_id INTEGER

        )
    """)
    print('Manuals created')

    # Tags
    con.execute('''
                    CREATE TABLE IF NOT EXISTS Tags(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    tag_name TEXT,
                    clicks, 
                    manual_id INTEGER)
                    ''')
    print('Tags created')

    # Stars
    con.execute('''
                    CREATE TABLE IF NOT EXISTS Stars(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    total_num,
                    num,
                    manual_id INTEGER)
                    ''')
    print('Stars created')

    # Programs
    con.execute('''
                    CREATE TABLE IF NOT EXISTS Programs(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT)
                    ''')
    print('Programs created')

    # Admins
    con.execute('''
                    CREATE TABLE IF NOT EXISTS Admins(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    role,
                    tg_id INTEGER)
                    ''')
    print('Admins created')

    # Clients
    con.execute('''
                    CREATE TABLE IF NOT EXISTS Clients(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name,
                    phone INTEGER,
                    chat_type TEXT,
                    chat_id INTEGER)
                    ''')
    print('Clients created')

    # filling the base
    sql_insert = '''INSERT OR IGNORE INTO Programs (name) VALUES (?)'''
    for i in programs_list:
        con.execute(sql_insert, i)
    else:
        print('table Programs ready for duty')

    sql_insert = '''INSERT OR IGNORE INTO Manuals (manu_name, program_id) VALUES (?,?)'''
    for i in manuals_list:
        con.execute(sql_insert, i)
    else:
        print('table Manuals ready for duty')

    sql_insert = '''INSERT OR IGNORE INTO Tags (tag_name, clicks, manual_id)
     VALUES (?,?,?)'''
    for i in tags_list:
        con.execute(sql_insert, i)
    else:
        print('table Tags ready for duty')

    sql_insert = '''INSERT OR IGNORE INTO Stars (total_num, num, manual_id)
     VALUES (?,?,?)'''
    for i in stars_list:
        con.execute(sql_insert, i)
    else:
        print('table Stars ready for duty')



# misc stuff

# import sqlite3
# from sqlite3 import Error
#
# La-li-lu-le-lo
# def create_connection(db_file):
#     """ create a database connection to the SQLite database
#         specified by db_file
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)
#
#     return conn
#
# def create_table(conn, create_table_sql):
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)

