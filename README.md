# ICU v1.0.0 - Inventory Control Utility

A minimalistic microservices learning project demonstrating modern architecture patterns with multiple technology stacks.

## Overview

ICU (Inventory Control Utility) is a web application for managing inventory items, purchase orders, and inventory reviews. It's designed as a v1.0.0 learning project with intentionally minimal implementation to focus on technology integration rather than production best practices.

## Technology Stack

- **Frontend**: Node.js + Express + Vanilla JavaScript
- **Items Service**: Python 3.11 + Flask
- **Reviews Service**: Java 17 + Spring Boot
- **Database**: MySQL 8.0
- **Mocking**: WireMock
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Port 3000)                  │
│                  Node.js + Express                       │
└────────────┬────────────────────────┬────────────────────┘
             │                        │
     ┌───────▼────────┐      ┌───────▼────────┐
     │ Items Service  │      │Reviews Service │
     │ (Port 5001)    │      │ (Port 8081)    │
     │ Python + Flask │      │ Java + Spring  │
     └────────┬────────┘      └───────┬────────┘
              │                       │
              └───────────┬───────────┘
                          │
                    ┌─────▼──────┐
                    │ MySQL DB   │
                    │(Port 3306) │
                    └────────────┘
                    
    WireMock (Port 8080) - Mocks provider endpoints
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Make (optional, for convenient commands)

### Build and Run

```bash
# Build all services
make build

# Start all services
make up

# View logs
make logs

# Stop services
make down
```

### Access the Application

- **Frontend UI**: http://localhost:3000
- **Items Service API**: http://localhost:5001
- **Reviews Service API**: http://localhost:8081
- **WireMock Admin**: http://localhost:8080/__admin
- **MySQL**: localhost:3306

## Usage

### Using Makefile

```bash
make help               # Show all available commands
make build             # Build Docker images
make up                # Start services
make down              # Stop services
make logs              # View logs from all services
make logs-items        # View Items service logs
make logs-reviews      # View Reviews service logs
make logs-frontend     # View Frontend logs
make logs-mysql        # View MySQL logs
make test              # Run all tests
make shell-mysql       # Open MySQL shell
make clean             # Clean up containers and images
```

### Manual Docker Compose

```bash
docker-compose build
docker-compose up -d
docker-compose logs -f
docker-compose down
```

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

### WireMock Provider Endpoints (Port 8080)

The frontend includes a **Providers** page for testing WireMock provider endpoints:

- `POST /provider/{providerName}` - Test a provider endpoint with items
  - **Available Providers**:
    - `CMOT` - Returns error (test failure scenario)
    - `Throat` - Returns error (test failure scenario)
    - `AirlineA` - Returns success
    - `AirlineB` - Returns success
    - `AirlineC` - Returns success
  - **Request Body**: JSON array of items
  - **Response**: Provider-specific response data

Access the Providers testing page at: **http://localhost:3000/providers.html**

## Data Model

### item
- item_id (INT)
- name (VARCHAR)
- optimal_stock (INT)
- price (DECIMAL)
- volume (DECIMAL)
- weight (DECIMAL)

### purchase_order
- purchase_order_id (INT)
- created_dt (DATETIME)
- delivered_dt (DATETIME)
- status (VARCHAR)
- provider (VARCHAR)

### purchase_order_item
- purchase_order_item_id (INT)
- item_id (INT)
- purchase_order_id (INT)
- price (DECIMAL)
- quantity (INT)

### review
- review_id (INT)
- start_dt (DATETIME)
- end_dt (DATETIME)
- status (VARCHAR)

### review_item
- review_item_id (INT)
- review_id (INT)
- item_id (INT)
- quantity (INT)

**Note**: No PRIMARY KEYS, FOREIGN KEYS, or INDEXES per v1.0.0 design decisions.

## Debugging

### Items Service (Python/Flask)

**Debug port**: 5678

Debug with pdb:
```bash
docker-compose exec items-service python -m pdb app.py
```

### Reviews Service (Java/Spring Boot)

**Debug port**: 5005

Configure IDE for remote debugging:
1. Create a "Remote JVM Debug" configuration
2. Set Host: `localhost`
3. Set Port: `5005`
4. Click Debug

### Frontend (Node.js)

Use browser DevTools (F12):
- Console for errors
- Network tab for API calls
- Elements/Inspector for DOM inspection

View logs:
```bash
make logs-frontend
```

## Database Access

### Open MySQL Shell

```bash
make shell-mysql
```

### Common Commands

```bash
# List tables
SHOW TABLES;

# View table structure
DESCRIBE item;

# View data
SELECT * FROM item;

# Reset database
docker volume rm demo-web-app_icu_db_data
```

## Testing

### Run All Tests

```bash
make test
```

### Items Service Tests

```bash
docker-compose exec items-service python -m pytest test_items.py -v
```

### Reviews Service Tests

```bash
docker-compose exec reviews-service mvn test
```

## Project Structure

```
demo-web-app/
├── frontend/                 # Node.js frontend service
│   ├── server.js            # Express server
│   ├── package.json         # Dependencies
│   ├── Dockerfile           # Container definition
│   ├── public/              # Static files (HTML, CSS, JS)
│   │   ├── index.html       # Home page
│   │   ├── items.html       # Items management page
│   │   ├── purchases.html   # Purchases management page
│   │   ├── reviews.html     # Reviews management page
│   │   ├── providers.html   # Provider testing page (NEW)
│   │   ├── app.js           # Shared API utilities
│   │   ├── providers.js     # Provider page logic (NEW)
│   │   ├── style.css        # Styling
│   └── README.md            # Frontend documentation
├── services/
│   ├── items-service/       # Python/Flask service
│   │   ├── app.py           # Flask application
│   │   ├── config.py        # Configuration
│   │   ├── requirements.txt # Python dependencies
│   │   ├── test_items.py   # Tests
│   │   ├── Dockerfile       # Container definition
│   │   └── README.md        # Service documentation
│   └── reviews-service/     # Java/Spring Boot service
│       ├── src/             # Java source code
│       ├── pom.xml          # Maven configuration
│       ├── Dockerfile       # Container definition
│       └── README.md        # Service documentation
├── database/                # Database layer
│   ├── init.sql            # Schema initialization
│   └── README.md           # Database documentation
├── wiremock/               # WireMock configuration
│   ├── mappings/           # Stub definitions
│   └── __files/            # Mock response files
├── .github/workflows/      # GitHub Actions CI/CD
│   └── build.yml          # Build pipeline
├── Makefile               # Build commands
├── docker-compose.yml     # Container orchestration
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── Plan_v1.0.0.md        # Implementation plan
```

## Service Communication

- **Frontend to Services**: Via HTTP requests to service URLs
- **Service to Database**: Direct JDBC/PyMySQL connections
- **Service to WireMock**: HTTP calls to mock provider endpoints
- **Services to Each Other**: Frontend orchestrates (no direct service-to-service calls)

## Data Persistence

All data is persisted in the `icu_db_data` Docker volume:
- Data survives container restarts
- To reset: `docker volume rm demo-web-app_icu_db_data`

## Development Workflow

1. **Start services**: `make up`
2. **Monitor logs**: `make logs`
3. **Make changes**: Edit code in services
4. **Services auto-reload** (Python) or require restart (Java)
5. **Test changes**: Use frontend UI or curl
6. **Run tests**: `make test`
7. **Stop services**: `make down`

## Known Limitations (Intentional v1.0.0 Decisions)

- ✗ No input validation
- ✗ No authentication/authorization
- ✗ No request logging
- ✗ No database indexes or primary keys
- ✗ No error recovery mechanisms
- ✗ Minimal error handling
- ✗ All endpoints return HTTP 200
- ✗ No rate limiting
- ✗ No caching

These will be addressed in future versions.

## CI/CD Pipeline

GitHub Actions automatically builds and tests on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

See `.github/workflows/build.yml` for details.

## Support & Documentation

- **Plan v1.0.0**: See `Plan_v1.0.0.md` for detailed implementation plan
- **Plan v1.0.1**: See `Plan_v1.0.1.md` for Provider testing feature plan
- **Requirements**: See `Requirements_v1.0.0.md` for specifications
- **Items Service**: See `services/items-service/README.md`
- **Reviews Service**: See `services/reviews-service/README.md`
- **Frontend**: See `frontend/README.md`
- **Database**: See `database/README.md`

## License

ISC

## Notes

This is a learning project (v1.0.0) designed to demonstrate microservices architecture and technology integration. It is not intended for production use. Future versions will implement best practices for stability, scalability, and security.
