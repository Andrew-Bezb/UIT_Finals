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
                   ["Winrar"],
                   ["Косынка"],
                   ["Сладости"],
                   ["Электроника"],
                   ["Бытовая техника"],
                   ["Смартфоны и гаджеты"],
                   ["Игры и игрушки"],
                   ["Наушники и акустика"],
                   ["Текстиль и ковры"],
                   ["Одежда"],
                   ["Обувь"],
                   ["Канцелярия"],
                   ["Мебель"],
                   ["Аксессуары"]]
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
                ("Аналоги Winrar", 2),
                ("Косынка без смс и регистрации", 3),
                ("Одежда", 3),
                ("Бытовая техника", 3),
                ("Одежда", 3),
                ("Обувь", 3),
                ("Канцелярия", 3),
                ("Мебель", 3),
                ("Аксессуары", 3)]
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
              ("Переустановка Виндоус", 0, 2),
             ("Установка операционной системы Windows.", 5, 1),
             ("Процесс установки Windows.", 6, 1),
             ("Установка Windows на компьютер.", 7, 1),
             ("Подготовка к установке Windows.", 1, 1),
             ("Параметры установки Windows.", 8, 1),
             ("Процедура установки Windows.", 8, 1),
             ("Инструкция по установке Windows.", 10, 1),
             ("Шаги установки Windows.", 10, 1),
             ("Установка операционной системы от Microsoft.", 3, 1),
             ("Как установить Windows на ПК.", 6, 1),
             ("Обновление операционной системы Windows.", 9, 2),
             ("Процесс переустановки Windows.", 5, 2),
             ("Переустановка ОС Windows.", 8, 2),
             ("Установка Windows заново.", 7, 2),
             ("Переустановка операционной системы от Microsoft.", 5, 2),
             ("Обновление Windows на компьютере.", 4, 2),
             ("Процедура переустановки Windows.", 3, 2),
             ("Восстановление Windows на ПК.", 8, 2),
             ("Переустановка ОС от Microsoft.", 7, 2),
             ("Обновление программного обеспечения Windows.", 5, 2),
             ("Без необходимости отправки сообщений и регистрации доступно приложение Косынка.", 0, 5),
             ("Приложение Косынка без СМС и регистрации.", 0, 5),
             ("Косынка доступна без отправки сообщений и регистрации.", 0, 5),
             ("Играй в Косынку, не требуя SMS и регистрации.", 0, 5),
             ("Без необходимости регистрироваться и отправлять SMS - Косынка.", 0, 5)]
"""
tags_list = [("Установка Windows", 0, 1),
              ("Переустановка Windows", 0, 2),
              ("Активация Winrar", 0, 3),
              ("Аналоги Winrar", 0, 4),
              ("Установка Виндоус", 0, 1),
              ("Переустановка Виндоус", 0, 2),
             ("Установка операционной системы Windows.", 0, 1),
             ("Процесс установки Windows.", 0, 1),
             ("Установка Windows на компьютер.", 0, 1),
             ("Подготовка к установке Windows.", 0, 1),
             ("Параметры установки Windows.", 0, 1),
             ("Процедура установки Windows.", 0, 1),
             ("Инструкция по установке Windows.", 0, 1),
             ("Шаги установки Windows.", 0, 1),
             ("Установка операционной системы от Microsoft.", 0, 1),
             ("Как установить Windows на ПК.", 0, 1),
             ("Обновление операционной системы Windows.", 0, 2),
             ("Процесс переустановки Windows.", 0, 2),
             ("Переустановка ОС Windows.", 0, 2),
             ("Установка Windows заново.", 0, 2),
             ("Переустановка операционной системы от Microsoft.", 0, 2),
             ("Обновление Windows на компьютере.", 0, 2),
             ("Процедура переустановки Windows.", 0, 2),
             ("Восстановление Windows на ПК.", 0, 2),
             ("Переустановка ОС от Microsoft.", 0, 2),
             ("Обновление программного обеспечения Windows.", 0, 2),             
             ("Без необходимости отправки сообщений и регистрации доступно приложение Косынка.", 0, 5),
             ("Приложение Косынка без СМС и регистрации.", 0, 5),
             ("Косынка доступна без отправки сообщений и регистрации.", 0, 5),
             ("Играй в Косынку, не требуя SMS и регистрации.", 0, 5),
             ("Без необходимости регистрироваться и отправлять SMS - Косынка.", 0, 5)]
"""
stars_list = [(40, 10, 1),
               (40, 10, 2),
               (40, 10, 3),
              (40, 10, 4),
              (40, 10, 5)]

texts_list = [["1. Установка Windows начинается с загрузки компьютера с установочного носителя. Для этого необходимо настроить BIOS или UEFI так, чтобы загрузка происходила с CD/DVD или USB-накопителя.", 1],
                   ["2. После загрузки с установочного носителя компьютер начнет загрузку файлов установщика Windows. Пользователю будет предложено выбрать язык установки, формат времени и клавиатуры.", 1],
                   ["3. Затем необходимо выбрать тип установки Windows: обновление существующей операционной системы или чистая установка. Важно следовать инструкциям на экране и выбирать правильные опции.", 1],
                   ["4. После выбора типа установки необходимо указать раздел на жестком диске, куда будет устанавливаться Windows. Можно создать новый раздел или выбрать существующий для установки.", 1],
                   ["5. После выбора раздела начнется процесс установки Windows, который может занять некоторое время. После завершения установки компьютер перезагрузится и пользователю будет предложено выполнить начальную настройку операционной системы.", 1],
                  ["6. В процессе начальной настройки Windows пользователю будет предложено создать учетную запись, выбрать пароль, настроить сетевое подключение и выполнить другие необходимые шаги для полноценной работы системы.", 1],
                  ["7. После завершения всех шагов установки Windows можно начать использовать операционную систему для работы с компьютером. Важно следовать рекомендациям по обновлению и настройке системы для безопасной и эффективной работы.", 1],
                  ["1. Для переустановки Windows необходимо подготовить установочный носитель с соответствующей версией операционной системы. Загрузите компьютер с этого носителя, настроив BIOS или UEFI для загрузки с CD/DVD или USB.", 2],
                    ["2. При загрузке с установочного носителя выберите язык установки, формат времени и клавиатуры. Затем следует выбрать опцию 'Установка Windows' и приступить к процессу переустановки.", 2],
                    ["3. При выборе раздела для установки Windows можно оставить старый раздел и переустановить операционную систему поверх существующей, либо создать новый раздел. Важно быть осторожным, чтобы не потерять важные данные.", 2],
                    ["4. После выбора раздела начнется процесс переустановки Windows, который может занять некоторое время. После завершения переустановки компьютер перезагрузится, и вы сможете начать начальную настройку системы.", 2],
                    ["5. В процессе начальной настройки Windows вам предложат создать новую учетную запись, настроить сетевое подключение и выполнить другие шаги для полноценной работы системы.", 2],
                    ["6. После завершения всех этапов переустановки Windows можно начать использовать операционную систему для работы с компьютером. Не забудьте обновить систему и настроить ее по своим потребностям для комфортной и безопасной работы.", 2],
                    ["1. Для активации WinRAR необходимо приобрести лицензионный ключ на официальном сайте разработчика или у авторизованных партнеров. После получения ключа можно приступить к активации программы.", 3],
                    ["""2. Запустите WinRAR и откройте меню "Help" (Справка). В этом меню выберите опцию "Enter registration key" (Ввести регистрационный ключ) или аналогичную.""", 3],
                    ["""3. В появившемся окне введите лицензионный ключ, который вы приобрели, и нажмите "OK". После этого WinRAR будет активирован и вы сможете пользоваться всеми функциями программы без ограничений.""", 3],
                    ["""4. При необходимости можно проверить статус активации в меню "Help" (Справка) -> "About WinRAR" (О программе WinRAR). Там будет указана информация о лицензии и активации.""", 3],
                    ["""5. Помните, что использование пиратских версий программы незаконно и может нарушить законы о защите авторских прав. Лучше всегда покупать лицензионные ключи для программ и поддерживать разработчиков.""", 3],
                    ["""6. После успешной активации WinRAR вы сможете продолжать использовать программу для архивации и распаковки файлов с уверенностью в ее работоспособности и безопасности.""", 3],
                    ["""1. Для активации аналогов WinRAR необходимо сначала выбрать подходящий архиватор, который соответствует вашим потребностям и требованиям. Существует множество альтернативных программ, таких как 7-Zip, PeaZip, Bandizip, и другие.""", 4],
                  ["""2. После установки выбранного архиватора, необходимо изучить инструкцию по активации на официальном сайте разработчика или в документации к программе.""", 4],
                  ["""3. В случае с 7-Zip, например, активация не требуется, поскольку программа бесплатна и распространяется под лицензией GNU LGPL. Просто установите программу и начинайте использовать ее для работы с архивами.""", 4],
                  ["""4. Другие аналоги WinRAR могут иметь свои собственные процедуры активации, включая лицензионные ключи или регистрацию через интернет. Проверьте информацию на сайте разработчика или в документации к программе.""", 4],
                  ["""5. Важно помнить, что использование лицензионных версий программ является законным и поддерживает разработчиков в их труде. Пиратские версии могут быть незаконными и нести риски для безопасности вашего компьютера.""", 4],
                  ["""6. После успешной установки и активации аналога WinRAR вы сможете использовать его для создания и распаковки архивов с уверенностью в его функциональности и надежности.""", 4],
                  ["""1. Косынка без смс и регистрации - это удобный и быстрый способ играть в популярную карточную игру без необходимости проходить долгие процедуры регистрации и получения кодов подтверждения. Просто откройте сайт или приложение, выберите количество игроков и начните игру!""", 5],
                  ["""2. Благодаря отсутствию смс и регистрации вы экономите свое время и сразу погружаетесь в игровой процесс. Никаких лишних шагов или препятствий - просто наслаждайтесь игрой и развивайте свои стратегические навыки в игре "Косынка".""", 5],
                  ["""3. Многие игровые платформы предлагают возможность играть в "Косынку" без смс и регистрации как на компьютере, так и на мобильных устройствах. Это удобно для тех, кто хочет быстро и легко насладиться игрой в любое время.""", 5],
                  ["""4. Отсутствие необходимости вводить личные данные или получать коды подтверждения делает процесс начала игры еще более простым и удобным. Просто выберите нужное количество игроков и начинайте игру!""", 5],
                  ["""5. Игра в "Косынку" без смс и регистрации доступна для всех, кто хочет провести время с пользой и удовольствием. Не тратьте время на лишние формальности - присоединяйтесь к игре и наслаждайтесь процессом!""", 5]]


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

    # Texts
    con.execute('''
                    CREATE TABLE IF NOT EXISTS Texts(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    manual_id INTEGER)
                    ''')
    print('Texts created')

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

    sql_insert = '''INSERT OR IGNORE INTO Texts (text, manual_id)
     VALUES (?,?)'''
    for i in texts_list:
        con.execute(sql_insert, i)
    else:
        print('table Texts ready for duty')



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

