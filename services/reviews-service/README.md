# Reviews Service

## Overview

Java/Spring Boot microservice for managing inventory reviews and review items. Implements CRUD operations for reviews and their associated items.

## Technology Stack

- Java 17
- Spring Boot 3.1.5
- Spring Data JPA
- MySQL 8.0
- Maven
- Docker

## Environment Variables

- `DB_HOST` - MySQL host (default: localhost)
- `DB_PORT` - MySQL port (default: 3306)
- `DB_NAME` - Database name (default: icu_v1)
- `DB_USER` - Database user (default: root)
- `DB_PASSWORD` - Database password (default: root)

## Running Locally

### Prerequisites
- Java 17+
- Maven 3.9+
- MySQL server running

### Setup

```bash
# Build project
mvn clean package

# Set environment variables (optional)
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=icu_v1
export DB_USER=root
export DB_PASSWORD=root

# Run application
java -jar target/reviews-service-1.0.0.jar
```

The service will start on `http://localhost:8081`

## API Endpoints

### Reviews

- `GET /review` - List all reviews
- `POST /review` - Create review
- `DELETE /review/<review_id>` - Delete review

### Review Items

- `GET /review/<review_id>/item` - List review items for a review
- `POST /review/<review_id>/item/<review_item_id>` - Add item to review
- `DELETE /review/<review_id>/item/<review_item_id>` - Delete review item

### Health

- `GET /health` - Health check

## Testing

### Run tests with Maven

```bash
# Using Docker
docker-compose exec reviews-service mvn test

# Locally
mvn test
```

## Debugging

### Remote Debugging with JDWP

The service supports remote debugging on port 5005.

#### Setup in IDE (IntelliJ IDEA):
1. Go to `Run → Edit Configurations`
2. Create new `Remote JVM Debug` configuration
3. Set Host: `localhost`
4. Set Port: `5005`
5. Click Debug

#### Or via Docker Compose:
The `docker-compose.yml` already exposes port 5005 for debugging.

### Enable in Dockerfile:
The JDWP agent is configured via JAVA_OPTS:
```
JAVA_OPTS: "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"
```

## Docker

Build image:
```bash
docker build -t reviews-service .
```

Run container:
```bash
docker run -p 8081:8081 -p 5005:5005 \
  -e DB_HOST=mysql \
  -e DB_NAME=icu_v1 \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  reviews-service
```

## Database

See `database/README.md` for database schema and operations.

## Project Structure

```
src/main/java/com/icu/
├── ReviewsApplication.java      # Spring Boot entry point
├── controller/
│   └── ReviewController.java    # REST endpoints
├── model/
│   ├── Review.java             # Review entity
│   └── ReviewItem.java         # ReviewItem entity
└── repository/
    ├── ReviewRepository.java   # Review data access
    └── ReviewItemRepository.java # ReviewItem data access
```

## Notes

- All endpoints return HTTP 200 status code (per v1.0.0 requirements)
- Error handling: Catch all exceptions and return error status in JSON body
- No request validation (minimal implementation for v1.0.0)
- JPA entities use `@Id` annotation but no `@GeneratedValue` (IDs provided by client)
