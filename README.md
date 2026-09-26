# Demo Web App

A demo web app that behaves like a very simple app for managing 
inventory items, purchase orders, and inventory reviews.

## Technology Stack

- **Frontend**: Node.js + Express + Vanilla JavaScript
- **Items Service**: Python 3.11 + Flask
- **Reviews Service**: Java 17 + Spring Boot
- **Database**: MySQL 8.0
- **Mocking**: WireMock
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Make

### Build and Run

#### Docker Compose

```bash
docker compose build
docker compose up -d
docker compose logs -f
docker compose logs -f <container>
docker compose down
docker compose restart <container>
```

#### Make

```bash
make help
```

### Hosts

- **Frontend UI**: http://localhost:9010
- **Items Service API**: http://localhost:9020
- **Reviews Service API**: http://localhost:9030
- **Reviews Service API (Debug)**: http://localhost:9031
- **WireMock Admin**: http://localhost:9040/__admin
- **MySQL**: localhost:9050

## API Endpoints

### Items Service (Python/Flask)

- `GET /item` - List all items
- `GET /item/<item_id>` - Get item details
- `POST /item` - Create item
- `DELETE /item/<item_id>` - Delete item
- `GET /purchase` - List all purchases
- `POST /purchase` - Create purchase
- `POST /purchase/<purchase_order_id>/item` - Add item to purchase
- `DELETE /purchase/<purchase_order_id>/item/<purchase_order_item_id>` - Delete purchase item
- `POST /purchase-from-provider` - Call WireMock provider (test endpoint)
- `GET /health` - Health check

### Reviews Service (Java/Spring Boot)

- `GET /review` - List all reviews
- `POST /review` - Create review
- `DELETE /review/<review_id>` - Delete review
- `GET /review/<review_id>/item` - List review items
- `POST /review/<review_id>/item/<review_item_id>` - Add item to review
- `DELETE /review/<review_id>/item/<review_item_id>` - Delete review item
- `GET /health` - Health check

All endpoints return HTTP 200 status code per v1.0.0 requirements.

### WireMock Provider Endpoints (Port 9040)

The frontend includes a **Providers** page for testing WireMock provider endpoints:

- `POST /provider/{providerName}` - Test a provider endpoint with items
  - **Available Providers**:
    - `CMOT` - Returns error (test failure scenario)
    - `Throat` - Returns error (test failure scenario)
    - `<Any Other String>` - Returns success
  - **Request Body**: JSON array of items
  - **Response**: Provider-specific response data

## Testing

```bash
make test
```

## Development Workflow

1. **Start services**: `make up`
2. **Monitor logs**: `make logs`
6. **Run tests**: `make test`
7. **Stop services**: `make down`

## CI/CD Pipeline

See [.github/workflows/build.yml](.github/workflows/build.yml)

## License

MIT
