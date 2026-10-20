from typing import Tuple

import requests
from flask import abort, request, jsonify, Response
from flask_openapi3 import OpenAPI, Tag, Info
from flask_cors import CORS

from config import Config
from data_objects.items import ItemPath, ItemSchema
from data_objects.responses import success_response, error_response
from repositories.database import DatabaseConnection
from repositories.items_repository import ItemsRepository

info = Info(title="Items Service API", version="0.1.0")
app = OpenAPI(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "http://localhost:9010"}}, supports_credentials=True)

item_tag = Tag(name="item", description="Item Operations")
purchase_tag = Tag(name="Purchase", description="Purchase Order Operations")

database_connection = DatabaseConnection(app.logger)
items_repository = ItemsRepository(app.logger, database_connection)


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

    return jsonify(result[0]), 200


@app.post('/item', tags=[item_tag])
def create_item(body: ItemSchema) -> Tuple[Response, int]:
    result = items_repository.create(body)

    if result is None:
        return error_response("Database query failed")

    return success_response("Item created")


@app.put('/item/<int:item_id>', tags=[item_tag])
def update_item(path: ItemPath, body: ItemSchema) -> Tuple[Response, int]:
    result = items_repository.update(path.item_id, body)

    if result is None:
        abort(500, description="Database query failed")

    return success_response("Item updated")


@app.delete('/item/<int:item_id>', tags=[item_tag])
def delete_item(path: ItemPath) -> Tuple[Response, int]:
    result = items_repository.delete(path.item_id)

    if result is None:
        return error_response("Database query failed")

    return success_response("deleted")


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
