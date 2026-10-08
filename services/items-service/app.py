from typing import Tuple

import requests
from flask import abort, request, jsonify, Response
from flask_openapi3 import OpenAPI, Tag, Info

from config import Config
from data_objects.items import ItemPath, ItemCreateSchema
from data_objects.purchase_orders import PurchaseOrderPath, PurchaseOrderItemCreateSchema
from data_objects.responses import success_response, error_response
from repositories.database import DatabaseConnection
from repositories.items_repository import ItemsRepository
from repositories.purchase_order_repository import PurchaseOrderRepository

info = Info(title="Items Service API", version="0.1.0")
app = OpenAPI(__name__)
app.config.from_object(Config)

item_tag = Tag(name="item", description="Item Operations")
purchase_tag = Tag(name="Purchase", description="Purchase Order Operations")

database_connection = DatabaseConnection(app.logger)
items_repository = ItemsRepository(app.logger, database_connection)
purchase_order_repository = PurchaseOrderRepository(app.logger, database_connection)


# ============= ITEM ENDPOINTS =============

@app.get('/item', tags=[item_tag])
def get_all_items() -> Tuple[Response, int]:
    result = items_repository.get_all()

    if result is None:
        abort(404, description="No items found in database")

    return jsonify(result), 200


@app.get('/item/<int:item_id>', tags=[item_tag])
def get_item(path: ItemPath) -> Tuple[Response, int]:
    result = items_repository.by_id(path.item_id)

    if result is None:
        abort(404, description="Item {} not found".format(path.item_id))

    return success_response()


@app.post('/item', tags=[item_tag])
def create_item(body: ItemCreateSchema) -> Tuple[Response, int]:
    result = items_repository.create(body)

    if result is None:
        return error_response("Database query failed")

    return success_response("Item created")


@app.delete('/item/<int:item_id>', tags=[item_tag])
def delete_item(path: ItemPath) -> Tuple[Response, int]:
    result = items_repository.delete(path.item_id)

    if result is None:
        return error_response("Database query failed")

    return success_response("deleted")


# ============= PURCHASE ORDER ENDPOINTS =============

@app.get('/purchase', tags=[purchase_tag])
def get_all_purchases() -> Tuple[Response, int]:
    result = purchase_order_repository.get_all()

    if result is None:
        abort(404, description="No purchase orders found in database")

    return jsonify(result), 200


@app.post('/purchase', tags=[purchase_tag])
def create_purchase_order() -> Tuple[Response, int]:
    result = purchase_order_repository.create(request.get_json())

    if result is None:
        return error_response("Database query failed")

    return success_response("created")


@app.post('/purchase/<int:purchase_order_id>/item', tags=[purchase_tag])
def add_purchase_order_item(path: PurchaseOrderPath, body: PurchaseOrderItemCreateSchema) -> Tuple[Response, int]:
    result = purchase_order_repository.add_item(path.purchase_order_id, body)

    if result is None:
        return error_response("Database query failed")

    return success_response("added")


@app.delete('/purchase/<int:purchase_order_id>/item/<int:purchase_order_item_id>', tags=[purchase_tag])
def delete_purchase_order_item(purchase_order_id, purchase_order_item_id) -> Tuple[Response, int]:
    result = purchase_order_repository.delete_item(purchase_order_id, purchase_order_item_id)

    if result is None:
        return error_response("Database query failed")

    return success_response("deleted")


# ============= WIREMOCK INTEGRATION ENDPOINT =============
# Does nothing right now
# TBD: see `Add wiremock logic` in TODO.md

@app.post('/purchase-from-provider', tags=[purchase_tag])
def purchase_from_provider() -> Tuple[Response, int]:
    """POST /purchase-from-provider - Call WireMock provider endpoint"""
    try:
        data = request.get_json()
        provider = data.get('provider')
        items = data.get('items', [])

        if not provider:
            return error_response("provider is required")

        wiremock_url = f"{Config.WIREMOCK_URL}/provider/{provider}"
        response = requests.post(wiremock_url, json=items, timeout=5)

        return success_response()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"WireMock request error: {e}")
        return error_response("Look for 'WireMock request error' in logs")
    except Exception as e:
        app.logger.error(f"Error in purchase_from_provider: {e}")
        abort(500, description="Look for 'Error in purchase_from_provider' in logs")


# ============= HEALTH CHECK =============

@app.get('/health', tags=[])
def health_check() -> Tuple[Response, int]:
    if database_connection.alive():
        return success_response()

    abort(500, description="Database connection failed")


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error) -> Tuple[Response, int]:
    message = getattr(error, 'description', 'Not found')
    return error_response(message, 404)


@app.errorhandler(500)
def internal_error(error) -> Tuple[Response, int]:
    app.logger.error(f"Internal error: {error}")
    message = getattr(error, 'description', 'Internal server error')
    return error_response(message, 500)


# ============= main =============

if __name__ == '__main__':
    port = int(Config.FLASK_PORT) if hasattr(Config, 'FLASK_PORT') and Config.FLASK_PORT else 9020
    app.run(host='0.0.0.0', port=port, debug=True)
