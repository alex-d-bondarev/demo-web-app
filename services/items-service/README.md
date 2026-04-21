# Items Service

## Overview

Python/Flask microservice for managing items and purchase orders. Implements CRUD operations for items and purchase orders, and integrates with WireMock for testing provider endpoints.

## Technology Stack

- Python 3.11
- Flask 3.0.0
- PyMySQL for database connectivity
- Docker for containerization

## Environment Variables

- `DB_HOST` - MySQL host (default: localhost)
- `DB_PORT` - MySQL port (default: 3306)
- `DB_NAME` - Database name (default: icu_v1)
- `DB_USER` - Database user (default: root)
- `DB_PASSWORD` - Database password (default: root)
- `WIREMOCK_URL` - WireMock base URL (default: http://localhost:8080)
- `FLASK_ENV` - Flask environment (default: development)

## Running Locally

### Prerequisites
- Python 3.11+
- MySQL server running
- Virtual environment (recommended)

### Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=icu_v1
export DB_USER=root
export DB_PASSWORD=root

# Run application
python app.py
```

The service will start on `http://localhost:5000`

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

## Debugging

### With Python debugger (pdb)

```python
# Add breakpoint in code
import pdb; pdb.set_trace()
```

Then run:
```bash
docker-compose exec -it items-service python app.py
```

### With debugpy (remote debugging)

1. Install debugpy: `pip install debugpy`
2. Modify app.py to include:
   ```python
   import debugpy
   debugpy.listen(("0.0.0.0", 5678))
   debugpy.wait_for_client()
   ```
3. Connect IDE debugger to localhost:5678

## Docker

Build image:
```bash
docker build -t items-service .
```

Run container:
```bash
docker run -p 5000:5000 \
  -e DB_HOST=mysql \
  -e DB_NAME=icu_v1 \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  items-service
```

## Database

See `database/README.md` for database schema and operations.

## Notes

- All endpoints return HTTP 200 status code (per v1.0.0 requirements)
- Error handling: Catch all exceptions and return error status in JSON body
- No request validation (minimal implementation for v1.0.0)
