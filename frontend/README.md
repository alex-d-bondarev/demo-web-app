# Frontend Service

A simple web UI for the application.

## Running Locally

### Prerequisites
- Node.js 18+
- npm

### Setup

```bash
# Install dependencies
npm install

# Set environment variables (optional)
export ITEMS_SERVICE_URL=http://localhost:9020
export REVIEWS_SERVICE_URL=http://localhost:9030

# Run application
npm start
```


## Docker

Build image:
```bash
docker build -t frontend .
```

Run container:
```bash
docker run -p 9010:9010 \
  -e ITEMS_SERVICE_URL=http://items-service:9020 \
  -e REVIEWS_SERVICE_URL=http://reviews-service:9030 \
  frontend
```
