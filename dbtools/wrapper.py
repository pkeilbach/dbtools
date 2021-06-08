from mysql import connector as mysql
from mysql.connector.cursor import MySQLCursor
import pandas as pd
from typing import Union, List, Generator


class MySqlConnection(object):

    @staticmethod
    def get_select_count_stmt(table: str, column: str, distinct: bool):
        if not column and distinct:
            raise SyntaxError("SQL Syntax error: COUNT DISTINCT only works with a specified column")
        elif column and distinct:
            return f"SELECT COUNT(DISTINCT({column})) FROM {table}"
        elif column and not distinct:
            return f"SELECT COUNT({column}) FROM {table}"
        else:
            return f"SELECT COUNT(*) FROM {table}"

    def __init__(self, *args, **kwargs):
        self.cnx = mysql.connect(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.cnx.commit()
        else:
            self.cnx.rollback()
        self.cnx.close()

    def is_connected(self) -> bool:
        return self.cnx.is_connected()

    def cursor(self, *args, **kwargs) -> MySQLCursor:
        return self.cnx.cursor(*args, **kwargs)

    def create_database(self, name: str, *args, **kwargs):
        stmt = f"CREATE DATABASE IF NOT EXISTS {name} DEFAULT CHARACTER SET utf8mb4"
        return self.execute(stmt, commit=True, *args, **kwargs)

    def drop_database(self, name: str, *args, **kwargs):
        stmt = f"DROP DATABASE IF EXISTS {name}"
        return self.execute(stmt, commit=True, *args, **kwargs)

    def create_tables(self, tables: list, schema: str = '', *args, **kwargs):
        cursor = self.cursor(*args, **kwargs)
        if schema:
            cursor.execute(f"USE {schema}")
        for t in tables:
            cursor.execute(t)
        cursor.close()

    def create_table(self, table: str, schema: str = '', *args, **kwargs):
        cursor = self.cursor(*args, **kwargs)
        if schema:
            cursor.execute(f"USE {schema}")
        self.execute(table)
        cursor.close()

    def drop_table(self, table: str, *args, **kwargs) -> bool:
        stmt = f"DROP TABLE IF EXISTS {table}"
        return self.execute(stmt, commit=True, *args, **kwargs)

    def execute(
            self,
            stmt: str,
            params: Union[dict, tuple] = None,
            lastrowid: bool = False,
            commit: bool = False,
            *args, **kwargs
    ) -> Union[int, bool]:

        cursor = self.cursor(*args, **kwargs)

        if params:
            cursor.execute(stmt, params, *args, **kwargs)
        else:
            cursor.execute(stmt, *args, **kwargs)
        cursor.close()

        if commit:
            self.cnx.commit()

        if lastrowid:
            return cursor.lastrowid

        return True

    def execute_many(self, stmt: str, params: List[Union[dict, tuple]], commit: bool = False, *args, **kwargs) -> bool:
        cursor = self.cursor(*args, **kwargs)
        cursor.executemany(stmt, params)
        cursor.close()
        if commit:
            self.cnx.commit()
        return True

    def insert(
            self,
            stmt: str,
            params: Union[dict, tuple, List[Union[dict, tuple]]],
            commit: bool = True,
            *args, **kwargs
    ) -> int:
        if isinstance(params, list):
            return self.execute_many(stmt=stmt, params=params, commit=commit, *args, **kwargs)
        else:
            return self.execute(stmt=stmt, params=params, lastrowid=True, commit=commit,  *args, **kwargs)

    # def insert_batch(self, stmt: str, params: List[Union[dict, tuple]], commit: bool = False, *args, **kwargs) -> bool:
    #     return self.execute_many(stmt=stmt, params=params, commit=commit, *args, **kwargs)

    def delete_from(self, stmt: str, *args, **kwargs) -> Union[int, bool]:
        try:
            cursor = self.cursor(*args, **kwargs)
            cursor.execute(stmt, *args, **kwargs)
            row_count = cursor.rowcount
            cursor.close()
            return row_count
        except mysql.Error as err:
            print(err)
            return False

    def delete_from_table(self, table: str, *args, **kwargs) -> Union[int, bool]:
        stmt = f"DELETE FROM {table}"
        return self.delete_from(stmt, *args, **kwargs)

    def select_count(
            self,
            table: str,
            column: str = None,
            distinct: bool = False,
            *args, **kwargs
    ) -> Union[tuple, dict, bool]:

        try:
            stmt = self.get_select_count_stmt(table, column, distinct)
            cursor = self.cursor(*args, **kwargs)
            cursor.execute(stmt)
            r = cursor.fetchone()[0]
            cursor.close()
            return r
        except mysql.Error as err:
            print(err)
            return False

    def select(
            self,
            stmt: str,
            params: Union[tuple, dict] = None,
            fetchone: bool = False,
            return_df: bool = False,
            *args, **kwargs
    ) -> Union[pd.DataFrame, list, bool, tuple]:

        try:
            cursor = self.cursor(*args, **kwargs)
            cursor.execute(stmt, params)
            if fetchone:
                data_records = cursor.fetchone()
            else:
                data_records = cursor.fetchall()
            columns = cursor.column_names
            cursor.close()

            if return_df:
                return pd.DataFrame(data_records, columns=columns)
            else:
                return data_records
        except mysql.Error as err:
            print(err)
            return False

    def select_batch(
            self,
            stmt: str,
            params: Union[tuple, dict] = None,
            batch_size: int = 100,
            return_df: bool = False,
            *args, **kwargs
    ) -> Generator[list, pd.DataFrame, bool]:
        try:
            cursor = self.cursor(*args, **kwargs)
            cursor.execute(stmt, params)
            data_records = cursor.fetchmany(batch_size)
            while data_records:
                if return_df:
                    yield pd.DataFrame(data_records, columns=cursor.column_names)
                else:
                    yield data_records
                data_records = cursor.fetchmany(batch_size)
        except mysql.Error as err:
            print(err)
            return False

