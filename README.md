# Demo Web App

Inventory Management (IM) Demo app that behaves like a very simple app for managing 
inventory items, purchase orders, and inventory reviews/audit.

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

```shell
docker compose build
docker compose up -d
docker compose logs -f
docker compose logs -f <service-name>
docker compose down
docker compose restart <service-name>
docker compose up --build <service-name>
```

##### Rebuild

```shell
docker compose down
cd services/reviews-service
mvn clean package -DskipTests
cd ../..
docker compose up --build
```

#### Make

```shell
make help
```

### Hosts

- **Frontend UI**: http://localhost:9010
- **Items Service API**: http://localhost:9020
- **Items Service API (Swagger UI)**: http://localhost:9020/openapi/
- **Reviews Service API**: http://localhost:9030
- **Reviews Service API (Swagger UI)**: http://localhost:9030/swagger-ui/index.html
- **Reviews Service API (OpenAPI Json)**: http://localhost:9030/v3/api-docs
- **Reviews Service API (Debug)**: http://localhost:9031
- **WireMock Admin**: http://localhost:9040/__admin
- **MySQL**: localhost:9050

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

```shell
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
