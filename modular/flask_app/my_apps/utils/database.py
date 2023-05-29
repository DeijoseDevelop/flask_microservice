import sqlite3


conn = sqlite3.connect('example.db')

class ConnectDB(object):

    def __init__(self):
        self.cursor = conn.cursor()

    def create_table(self, table_name: str = None, columns: tuple = None) -> None:
        if table_name is None or columns is None:
            raise ValueError("Table name and columns cannot be empty")

        query = f"CREATE TABLE {table_name} ("

        for column in columns:
            if isinstance(column, str):
                column = r"{}".format(column)
            query += f" {column}, "

        query = f"{query[:-2]})"

        print(query)
        self.cursor.execute(query)
        conn.commit()

    def select(self, table_name: str = None, columns: tuple = "*", condition: str = None) -> list:
        if table_name is None or columns is None:
            raise ValueError("Table name and columns cannot be empty")

        where = f"WHERE {condition}"
        if not condition: where = ''

        self.cursor.execute(f'SELECT {columns} FROM {table_name} {where}')

        return self.cursor.fetchall()

    def insert(self, table_name: str = None, values: tuple = None) -> None:
        if table_name is None or values is None:
            raise ValueError("Table name and values cannot be empty")

        query = self._add_values_to_query(f"INSERT INTO {table_name} VALUES (", values)

        self.cursor.execute(query)
        conn.commit()

    def update(self, table_name: str = None, values: tuple = None, record_id: int = None) -> None:
        if table_name is None or values is None or record_id is None:
            raise ValueError("Table name and values cannot be empty")

        query = f"UPDATE {table_name} SET"

        for value in values:
            print(value)
            query += f" {value[0]} = '{value[1]}', "

        query = f"{query[:-2]}"

        query += f" WHERE id = {record_id}"
        print(query)
        self.cursor.execute(query)
        conn.commit()

    def delete(self, table_name: str = None, record_id: int = None) -> None:
        if table_name is None or record_id is None:
            raise ValueError("Table name and values cannot be empty")

        query = f"DELETE FROM {table_name} WHERE id = {record_id}"

        self.cursor.execute(query)
        conn.commit()

    @classmethod
    def _add_values_to_query(cls, query: str, columns: tuple):
        for column in columns:
            if isinstance(column, str):
                column = r"'{}'".format(column)
            query += f" {column}, "

        return f"{query[:-2]})"

    def close_connection(self):
        conn.close()


