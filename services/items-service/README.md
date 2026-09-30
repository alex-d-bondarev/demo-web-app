# Items Service

Manage items and purchase orders. 
Providers are mocked, see [wiremock README.md](../../wiremock/README.md).
For database see [database README.md](../../database/README.md)

### Setup

```bash
uv sync

# Set environment variables (optional)
export DB_HOST=localhost
export DB_PORT=9050
export DB_NAME=im_db
export DB_USER=root
export DB_PASSWORD=root
export FLASK_PORT=9020

# Run application
uv run flask run --host=0.0.0.0 --port=9020
```

The service will start on `http://localhost:9020`

## Update

```shell
uv add "<dependency>==<version>"
uv remove "<dependency>"

# or update pyproject.toml and run:
uv sync
```

## API Endpoints

### Items

- `GET /item` - List all items
- `GET /item/<item_id>` - Get item details
- `POST /item` - Create item
- `DELETE /item/<item_id>` - Delete item

### Purchase Orders

- `GET /purchase` - List all purchases
- `POST /purchase` - Create purchase
- `POST /purchase/<purchase_order_id>/item` - Add item to purchase
- `DELETE /purchase/<purchase_order_id>/item/<purchase_order_item_id>` - Delete purchase item

### WireMock Integration

- `POST /purchase-from-provider` - Call WireMock provider endpoint

### Health

- `GET /health` - Health check

## Testing

### Run tests with pytest

```bash
# Using Docker
docker-compose exec items-service python -m pytest test_items.py -v

# Locally
pip install pytest requests
pytest test_items.py -v
```

## Docker

Build image:
```bash
docker build -t items-service .
```

Run container:
```bash
docker run -p 9020:9020 \
  -e DB_HOST=mysql \
  -e DB_NAME=im_db \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  -e FLASK_PORT=9020 \
  items-service
```
