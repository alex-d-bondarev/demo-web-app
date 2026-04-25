import pytest
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5001"

# Wait for service to be ready
time.sleep(2)

class TestItemEndpoints:
    """Test item endpoints"""
    
    def test_get_all_items_returns_200(self):
        response = requests.get(f"{BASE_URL}/item")
        assert response.status_code == 200
    
    def test_post_item_returns_created_status(self):
        payload = {
            "item_id": 1,
            "name": "Test Item",
            "optimal_stock": 100,
            "price": 25.50,
            "volume": 0.5,
            "weight": 2.3
        }
        response = requests.post(f"{BASE_URL}/item", json=payload)
        assert response.status_code == 200
        assert response.json() == {"status": "created"}
    
    def test_get_item_by_id_returns_200(self):
        response = requests.get(f"{BASE_URL}/item/1")
        assert response.status_code == 200
    
    def test_delete_item_returns_deleted_status(self):
        response = requests.delete(f"{BASE_URL}/item/1")
        assert response.status_code == 200
        assert response.json() == {"status": "deleted"}


class TestPurchaseEndpoints:
    """Test purchase order endpoints"""
    
    def test_get_all_purchases_returns_200(self):
        response = requests.get(f"{BASE_URL}/purchase")
        assert response.status_code == 200
    
    def test_post_purchase_returns_created_status(self):
        payload = {
            "purchase_order_id": 1,
            "created_dt": "2024-01-01 10:00:00",
            "delivered_dt": "2024-01-05 15:30:00",
            "status": "delivered",
            "provider": "Supplier A"
        }
        response = requests.post(f"{BASE_URL}/purchase", json=payload)
        assert response.status_code == 200
        assert response.json() == {"status": "created"}
    
    def test_post_purchase_item_returns_added_status(self):
        payload = {
            "purchase_order_item_id": 1,
            "item_id": 1,
            "purchase_order_id": 1,
            "price": 25.50,
            "quantity": 50
        }
        response = requests.post(f"{BASE_URL}/purchase/1/item", json=payload)
        assert response.status_code == 200
        assert response.json() == {"status": "added"}
    
    def test_delete_purchase_item_returns_deleted_status(self):
        response = requests.delete(f"{BASE_URL}/purchase/1/item/1")
        assert response.status_code == 200
        assert response.json() == {"status": "deleted"}
