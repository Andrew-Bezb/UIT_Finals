import sqlite3 as sl
import json

with open('config.json', 'r') as file:
    content = json.load(file)
    db_path = content['db_path']

connect = sl.connect(db_path, check_same_thread=False)


# req file
class DoubleDragon:
    def __init__(self):
        global connect
        self.con = connect

    def get_instructions_by_program_id(self, id: int) -> list:
        """
        get list of instructions
        :param id: id of certain program
        """
        with self.con as con:
            return con.execute(f'''select * from Manuals where program_id = {id} ''').fetchall()


    def get_columns(self, name: str) -> list:
        """
        get all column names
        :param name: table name as string, as example 'Goods'
        """
        with self.con as con:
            result = con.execute(f'''select * from pragma_table_info('{name}')''').fetchall()
            return [i[1] for i in result]

    def get_table_names(self) -> list:
        """
        gets all table names as strings. except temporal ones.

        :return: table names
        :rtype: list
        """
        with self.con as con:
            names = con.execute("""SELECT name FROM sqlite_master  
          WHERE type='table'; """)
        return [i[0] for i in names.fetchall() if i[0] != 'sqlite_sequence']

    def get_table_by_name(self, name: str, with_id=False) -> list:
        """
        gets all from a table.

        :param name: table name as string, as example 'Goods'
        :param with_id: True if id is needed
        :return: all table contains
        :rtype: list
        """
        with self.con as con:
            if with_id:
                return con.execute(f""" select * from '{name}' """).fetchall()
            table_content = con.execute(f""" select * from '{name}' """).fetchall()
            return [table_content[i][1:] for i in range(len(table_content))]

    def get_items(self, table_name: str, values, by: str) -> list:
        """
        returns list of items searched by value (string or tuple). includes all matches i.e. 'in' not '=' in sqlite

        :param table_name: table name as string, as example 'Goods'
        :param values: tuple (if tuple - at least 2 items) i.e. ('Шоколад','Книга') or string of text i.e. 'Шоколад'
        :param by: string of text by which you filter table content, as example 'id'
        :return: list of matches
        :rtype: list
        """
        with self.con as con:
            if type(values) == str:
                values = "'" + values + "'"
                return con.execute(f""" select * from '{table_name}' where {by} LIKE {values} """).fetchall()
            return con.execute(f""" select * from '{table_name}' where {by} in {values} """).fetchall()

    def del_table_content_by_ids(self, name: str, ids: list):
        """
        delete strings from any table. required name of table and list of ids

        :param name: table name as string, as example 'Goods'
        :param ids: list of id, as example [1, 2, 3] or [4]
        :param id_name: name of the id column in table
        """
        with self.con as con:
            if len(ids) > 1:
                ids = tuple(ids)
                con.execute(f'''DELETE FROM '{name}' WHERE id in {ids}''')
            else:
                ids = ids[0]
                con.execute(f'''DELETE FROM '{name}' WHERE id in ({ids})''')

    def del_table_content_by_ids_concat(self, name: str, ids: list) -> str:
        """
        return string of text with delete statement. required name of table and list of ids

        :param name: table name as string, as example 'Goods'
        :param ids: list of id, as example [1, 2, 3] or [4]
        """
        if len(ids) > 1:
            ids = tuple(ids)
            return f''' DELETE FROM '{name}' WHERE id in {ids}; '''
        else:
            ids = ids[0]
            return f''' DELETE FROM '{name}' WHERE id in ({ids}); '''

    def insert(self, name: str, values: tuple) -> int:
        """
        insert values into table. required name of table and tuple of values. id is not required
        return that last id
        :param name: table name as string, as example 'Goods'
        :param values: tuple of values i.e. ('Книга', 350.0, 1, 1234, 0.5, 'Book_1.json', 1, 0, '2024-06-30', 50, 20, 0))
        """
        with self.con as con:
            result = con.execute(f'''select * from pragma_table_info('{name}')''').fetchall()
            listy = [i[1] for i in result if i[1] != 'id']
            if len(listy) > 1:
                listy = tuple(listy)
                con.execute(f'''insert into '{name}' {listy} values {values}; ''')
            else:
                listy = listy[0]
                values = values[0]
                if isinstance(values, str):
                    con.execute(f'''insert into '{name}' ({listy}) values ('{values}'); ''')
                else:
                    con.execute(f'''insert into '{name}' ({listy}) values ({values}); ''')
        return con.execute(f'''select max(id) from '{name}' ''').fetchall()[0][0]

    def insert_concat(self, name: str, values: tuple) -> str:
        """
        return string with insert values into table statement. required name of table and tuple of values.
        id is not required

        :param name: table name as string, as example 'Goods'
        :param values: tuple of values i.e. ('Книга', 350.0, 1, 1234, 0.5, 'Book_1.json', 1, 0, '2024-06-30', 50, 20, 0))
        """
        with self.con as con:
            result = con.execute(f'''select * from pragma_table_info('{name}')''').fetchall()
            listy = tuple([i[1] for i in result if i[1] != 'id'])
            return f''' insert into '{name}' {listy} values {values}; '''

    def update_cell(self, table: str, id: int, param: str, value: any):
        """
        Sets parameter(param) of item(by id) in table(table) to (value)
        """
        if type(value) == str:
            value = "'" + value + "'"
        with self.con as con:
            con.execute(f'''UPDATE {table}
                            SET '{param}' = {value}
                            WHERE id = {id} ''')

    def get_manual_score(self, id: int) -> float:
        """
        get average score of manual
        """
        with self.con as con:
            result = con.execute(f""" select * from Stars where manual_id = {id} """).fetchall()
            return round(result[0][1]/result[0][2], 1)

    def update_score(self, mark: int, id: int):
        """
        updates score of manual
        :param mark: mark in range 1-5
        :param id: manual_id
        """
        with self.con as con:
            con.execute(
                f''' update Stars set total_num = total_num + {mark}, num = num + 1  WHERE manual_id = '{id}' ''')

    def update_tag_clicks(self, id: int):
        """
        updates weight of tag
        :param id: id - Tags.id
        """
        with self.con as con:
            con.execute(
                f''' update Tags set clicks = clicks + 1  WHERE id = '{id}' ''')

db = DoubleDragon()

# misc shit nothing to see here
"""
        select * from pragma_table_info('tblName')
"""
