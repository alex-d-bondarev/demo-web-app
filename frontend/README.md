# Frontend Service

## Overview

Node.js/Express frontend service providing a simple web UI for the ICU application. Uses vanilla JavaScript to interact with backend services.

## Technology Stack

- Node.js 18
- Express.js 4.18
- HTML5/CSS3
- Vanilla JavaScript
- Docker

## Environment Variables

- `ITEMS_SERVICE_URL` - Items service URL (default: http://localhost:5001)
- `REVIEWS_SERVICE_URL` - Reviews service URL (default: http://localhost:8081)
- `PORT` - Server port (default: 3000)
- `NODE_ENV` - Environment (default: development)

## Running Locally

### Prerequisites
- Node.js 18+
- npm

### Setup

```bash
# Install dependencies
npm install

# Set environment variables (optional)
export ITEMS_SERVICE_URL=http://localhost:5001
export REVIEWS_SERVICE_URL=http://localhost:8081

# Run application
npm start
```

The frontend will start on `http://localhost:3000`

## Pages

### Home (index.html)
- Navigation to all sections
- Overview of ICU application

### Items (items.html)
- **List Items**: View all inventory items
- **View Details**: See complete item information
- **Create Item**: Add new items to inventory
- **Delete Item**: Remove items from inventory

### Purchases (purchases.html)
- **List Purchases**: View all purchase orders
- **Purchase Details**: View items in a purchase order
- **Create Purchase**: Create new purchase orders
- **Add Item to Purchase**: Associate items with purchases

### Reviews (reviews.html)
- **List Reviews**: View all inventory reviews
- **Review Items**: See items counted in a review
- **Create Review**: Create new review records
- **Add Item to Review**: Associate items with reviews

### Providers (providers.html) - WireMock Testing
- **Provider Information**: View all available providers and their expected behavior
- **Test Provider Endpoints**: Test individual providers with custom or predefined items
- **Response Analysis**: See detailed response information including status codes and response times
- **Available Providers**:
  - **CMOT**: Fails (error response)
  - **Throat**: Fails (error response)
  - **AirlineA**: Succeeds
  - **AirlineB**: Succeeds
  - **AirlineC**: Succeeds

## API Integration

Frontend communicates with backend services via HTTP fetch API:

- Items Service: http://items-service:5001
- Reviews Service: http://reviews-service:8081
- WireMock: http://wiremock:8080

All API calls use JSON and always return HTTP 200 status code.

## Features

- Responsive design for mobile and desktop
- Real-time form validation feedback
- Success/error messaging
- Tabular data display
- CRUD operations for all entities

## Docker

Build image:
```bash
docker build -t frontend .
```

Run container:
```bash
docker run -p 3000:3000 \
  -e ITEMS_SERVICE_URL=http://items-service:5001 \
  -e REVIEWS_SERVICE_URL=http://reviews-service:8081 \
  frontend
```

## Debugging

### Browser DevTools
- Open browser DevTools (F12 or Cmd+Opt+I)
- Check Console tab for errors
- Use Network tab to inspect API calls
- Use Elements/Inspector to inspect DOM

### Server Logs
```bash
docker-compose logs frontend
```

## Notes

- Minimal implementation for v1.0.0 learning purposes
- No form validation (minimal scope)
- Simple error handling
- Single-page applications with inline scripts
