import pytest
import requests
import json
import time

BASE_URL = "http://127.0.0.1:9020"

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
        assert response.json() == {"status": "Item created"}
    
    def test_get_item_by_id_returns_200(self):
        response = requests.get(f"{BASE_URL}/item/1")
        assert response.status_code == 200
    
    def test_delete_item_returns_deleted_status(self):
        response = requests.delete(f"{BASE_URL}/item/1")
        assert response.status_code == 200
        assert response.json() == {"status": "deleted"}
