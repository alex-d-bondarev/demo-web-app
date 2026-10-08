from flask import abort
from logging import Logger

from data_objects.purchase_orders import PurchaseOrderItemCreateSchema
from repositories.database import DatabaseConnection


class PurchaseOrderRepository:
    def __init__(self, app_logger: Logger, database_connection: DatabaseConnection):
        self.app_logger = app_logger
        self.database_connection = database_connection

    def add_item(self, purchase_order_id: int, body: PurchaseOrderItemCreateSchema):
        try:
            query = """
                INSERT INTO purchase_order_item 
                (purchase_order_id, item_id, price, quantity)
                VALUES (%s, %s, %s, %s)
            """

            params = (
                purchase_order_id,
                body.item_id,
                body.price,
                body.quantity
            )

            return self.database_connection.execute_query(query, params, fetch=False)

        except Exception as e:
            self.app_logger.fatal(f"Error in add_purchase_item: {e}")
            abort(500, description="Look for 'Error in add_purchase_item' in logs")

    def create(self, data: dict):
        try:
            query = """
                INSERT INTO purchase_order (purchase_order_id, created_dt, delivered_dt, status, provider)
                VALUES (%s, %s, %s, %s, %s)
            """

            params = (
                data.get('purchase_order_id'),
                data.get('created_dt'),
                data.get('delivered_dt'),
                data.get('status'),
                data.get('provider')
            )

            return self.database_connection.execute_query(query, params, fetch=False)

        except Exception as e:
            self.app_logger.fatal(f"Error in create_purchase: {e}")
            abort(500, description="Look for 'Error in create_purchase' in logs")

    def delete_item(self, purchase_order_id: int, item_id: int):
        try:
            query = """
                DELETE FROM purchase_order_item 
                WHERE purchase_order_id = %s AND purchase_order_item_id = %s
            """

            return self.database_connection.execute_query(query, (purchase_order_id, item_id), fetch=False)

        except Exception as e:
            self.app_logger.fatal(f"Error in delete_purchase_item: {e}")
            abort(500, description="Look for 'Error in delete_purchase_item' in logs")

    def get_all(self):
        try:
            query = "SELECT * FROM purchase_order"
            return self.database_connection.execute_query(query, fetch=True)

        except Exception as e:
            self.app_logger.fatal(f"Error in get_all_purchases: {e}")
            abort(500, description="Look for 'Error in get_all_purchases' in logs")
