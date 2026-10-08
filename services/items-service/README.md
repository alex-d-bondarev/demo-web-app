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

## Testing

### Run tests with pytest

```bash
# Using Docker
docker-compose exec items-service python -m pytest test_items.py -v
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

## Debugging

1. Start Mysql server from project root
   ```shell
   docker compose up --build mysql
   ```
2. In IDE:
   ```
   # Environment variables:
   DB_HOST=localhost
   DB_PORT=9055
   DB_NAME=im_db
   DB_USER=root
   DB_PASSWORD=root
   WIREMOCK_URL=http://localhost:9040
   FLASK_ENV=development
   FLASK_PORT=9020
   
   # Script parameters:
   --host=0.0.0.0 --no-reload
   ```
