import pymysql
import json
import requests
from flask import Flask, request, jsonify
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
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
        app.logger.error(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch=True):
    """Execute database query"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                connection.commit()
                result = {"affected_rows": cursor.rowcount}
        return result
    except Exception as e:
        app.logger.error(f"Query execution error: {e}")
        return None
    finally:
        connection.close()

# ============= ITEM ENDPOINTS =============

@app.route('/item', methods=['GET'])
def get_all_items():
    """GET /item - List all items"""
    try:
        query = "SELECT item_id, name FROM item"
        items = execute_query(query, fetch=True)
        if items is None:
            items = []
        return jsonify(items), 200
    except Exception as e:
        app.logger.error(f"Error in get_all_items: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """GET /item/<item_id> - Get item details"""
    try:
        query = "SELECT * FROM item WHERE item_id = %s"
        result = execute_query(query, (item_id,), fetch=True)
        
        if not result:
            return jsonify({"status": "not_found"}), 200
        
        item = result[0]
        return jsonify(item), 200
    except Exception as e:
        app.logger.error(f"Error in get_item: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route('/item', methods=['POST'])
def create_item():
    """POST /item - Create new item"""
    try:
        data = request.get_json()
        
        query = """
            INSERT INTO item (item_id, name, optimal_stock, price, volume, weight)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('item_id'),
            data.get('name'),
            data.get('optimal_stock'),
            data.get('price'),
            data.get('volume'),
            data.get('weight')
        )
        
        execute_query(query, params, fetch=False)
        return jsonify({"status": "created"}), 200
    except Exception as e:
        app.logger.error(f"Error in create_item: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """DELETE /item/<item_id> - Delete item"""
    try:
        query = "DELETE FROM item WHERE item_id = %s"
        execute_query(query, (item_id,), fetch=False)
        return jsonify({"status": "deleted"}), 200
    except Exception as e:
        app.logger.error(f"Error in delete_item: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

# ============= PURCHASE ORDER ENDPOINTS =============

@app.route('/purchase', methods=['GET'])
def get_all_purchases():
    """GET /purchase - List all purchases"""
    try:
        query = "SELECT * FROM purchase_order"
        purchases = execute_query(query, fetch=True)
        if purchases is None:
            purchases = []
        return jsonify(purchases), 200
    except Exception as e:
        app.logger.error(f"Error in get_all_purchases: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route('/purchase', methods=['POST'])
def create_purchase():
    """POST /purchase - Create new purchase"""
    try:
        data = request.get_json()
        
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
        
        execute_query(query, params, fetch=False)
        return jsonify({"status": "created"}), 200
    except Exception as e:
        app.logger.error(f"Error in create_purchase: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route('/purchase/<int:purchase_order_id>/item', methods=['POST'])
def add_purchase_item(purchase_order_id):
    """POST /purchase/<purchase_order_id>/item - Add item to purchase"""
    try:
        data = request.get_json()
        
        query = """
            INSERT INTO purchase_order_item 
            (purchase_order_item_id, item_id, purchase_order_id, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data.get('purchase_order_item_id'),
            data.get('item_id'),
            data.get('purchase_order_id'),
            data.get('price'),
            data.get('quantity')
        )
        
        execute_query(query, params, fetch=False)
        return jsonify({"status": "added"}), 200
    except Exception as e:
        app.logger.error(f"Error in add_purchase_item: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

@app.route('/purchase/<int:purchase_order_id>/item/<int:purchase_order_item_id>', methods=['DELETE'])
def delete_purchase_item(purchase_order_id, purchase_order_item_id):
    """DELETE /purchase/<purchase_order_id>/item/<purchase_order_item_id> - Delete purchase item"""
    try:
        query = """
            DELETE FROM purchase_order_item 
            WHERE purchase_order_id = %s AND purchase_order_item_id = %s
        """
        execute_query(query, (purchase_order_id, purchase_order_item_id), fetch=False)
        return jsonify({"status": "deleted"}), 200
    except Exception as e:
        app.logger.error(f"Error in delete_purchase_item: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

# ============= WIREMOCK INTEGRATION ENDPOINT =============

@app.route('/purchase-from-provider', methods=['POST'])
def purchase_from_provider():
    """POST /purchase-from-provider - Call WireMock provider endpoint"""
    try:
        data = request.get_json()
        provider = data.get('provider')
        items = data.get('items', [])
        
        if not provider:
            return jsonify({"status": "error", "message": "provider is required"}), 200
        
        # Call WireMock
        wiremock_url = f"{Config.WIREMOCK_URL}/provider/{provider}"
        response = requests.post(wiremock_url, json=items, timeout=5)
        
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        app.logger.error(f"WireMock request error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200
    except Exception as e:
        app.logger.error(f"Error in purchase_from_provider: {e}")
        return jsonify({"status": "error", "message": str(e)}), 200

# ============= HEALTH CHECK =============

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        connection = get_db_connection()
        if connection:
            connection.close()
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": "Database connection failed"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Not found"}), 200

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {error}")
    return jsonify({"status": "error", "message": "Internal server error"}), 200

if __name__ == '__main__':
    port = int(Config.FLASK_PORT) if hasattr(Config, 'FLASK_PORT') and Config.FLASK_PORT else 5001
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
