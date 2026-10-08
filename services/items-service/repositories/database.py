from logging import Logger

import pymysql

from config import Config


class DatabaseConnection:
    def __init__(self, app_logger: Logger):
        self.app_logger = app_logger
        self.connection = self._get_db_connection()

    def _get_db_connection(self):
        """Get database connection"""
        try:
            connection = pymysql.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            self.app_logger.error(f"Database connection error: {e}")
            return None


    def execute_query(self, query, params=None, fetch=True):
        """Execute database query"""
        if not self.connection:
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    result = cursor.fetchall()
                else:
                    self.connection.commit()
                    result = {"affected_rows": cursor.rowcount}
            return result
        except Exception as e:
            self.app_logger.error(f"Query execution error: {e}")
            return None

    def alive(self):
        return self.connection is not None
