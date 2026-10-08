from flask import abort
from logging import Logger
from typing import Optional

from data_objects.items import ItemCreateSchema
from repositories.database import DatabaseConnection


class ItemsRepository:
    def __init__(self, app_logger: Logger, database_connection: DatabaseConnection):
        self.app_logger = app_logger
        self.database_connection = database_connection

    def by_id(self, item_id: int) -> Optional[dict]:
        """GET /item/<item_id> - Get item details"""
        try:
            query = "SELECT * FROM item WHERE item_id = %s"
            return self.database_connection.execute_query(query, (item_id,), fetch=True)

        except Exception as e:
            self.app_logger.fatal(f"Error in get_item: {e}")
            abort(500, description="Look for 'Error in get_item' in logs")

    def create(self, body: ItemCreateSchema):
        try:
            query = """
                INSERT INTO item (name, optimal_stock, volume, weight)
                VALUES (%s, %s, %s, %s)
            """
            params = (
                body.name,
                body.optimal_stock,
                body.volume,
                body.weight
            )

            return self.database_connection.execute_query(query, params, fetch=False)

        except Exception as e:
            self.app_logger.fatal(f"Error in create_item: {e}")
            abort(500, description="Look for 'Error in create_item' in logs")

    def delete(self, item_id: int):
        try:
            query = "DELETE FROM item WHERE item_id = %s"
            return self.database_connection.execute_query(query, (item_id,), fetch=False)
        except Exception as e:
            self.app_logger.fatal(f"Error in delete_item: {e}")
            abort(500, description="Look for 'Error in delete_item' in logs")

    def get_all(self) -> Optional[dict]:
        try:
            query = "SELECT item_id, name FROM item;"
            return self.database_connection.execute_query(query, fetch=True)

        except Exception as e:
            self.app_logger.fatal(f"Error in get_all_items: {e}")
            abort(500, description="Look for 'Error in get_all_items' in logs")
