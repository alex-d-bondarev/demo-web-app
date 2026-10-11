# Reviews Service

Manage inventory reviews and review items.
For database see [database README.md](../../database/README.md)

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
export DB_PORT=9050
export DB_NAME=im_db
export DB_USER=root
export DB_PASSWORD=root
export FRONT_END_URL=http://localhost:9010

# Run application
java -jar target/reviews-service-1.0.0.jar
```

The service will start on `http://localhost:9030`

## Docker

Build image:
```bash
docker build -t reviews-service .
```

Run container:
```bash
docker run -p 9030:9030 -p 9031:9031 \
  -e DB_HOST=mysql \
  -e DB_NAME=im_db \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  -e FRONT_END_URL=http://localhost:9010 \
  reviews-service
```

## Testing

### Run tests with Maven

```bash
# Using Docker
docker-compose exec reviews-service mvn test

# Locally
mvn test
```

## Debugging via IntelliJ IDEA:
1. The `docker-compose.yml` already exposes port 9031 for debugging.
2. Go to `Run → Edit Configurations`
3. Create new `Remote JVM Debug` configuration
4. Set Host: `localhost`
5. Set Port: `9031`
6. Click Debug
