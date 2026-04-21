# WireMock Configuration

## Overview

WireMock is a mock server that simulates HTTP responses for provider endpoints. This allows testing of the Items Service's `purchase-from-provider` functionality without relying on real external providers.

## Port

- **Port**: 8080
- **Admin UI**: http://localhost:8080/__admin

## Architecture

```
Frontend/Services → WireMock (Port 8080) → Mock Responses
```

## Provider Endpoints

### POST /provider/{providerName}

Tests a provider endpoint with a list of items.

**Request**:
```json
[
  {"id": 1, "name": "Widget A", "quantity": 5},
  {"id": 2, "name": "Widget B", "quantity": 3}
]
```

**Available Providers**:

#### Failing Providers
These providers are configured to return error responses:

- **CMOT**
  - Endpoint: `POST /provider/CMOT`
  - Response: `{"status": "failed"}`
  - Use Case: Test failure scenarios

- **Throat**
  - Endpoint: `POST /provider/Throat`
  - Response: `{"status": "failed"}`
  - Use Case: Test failure scenarios

#### Success Providers
These providers are configured to return success responses (catch-all pattern):

- **AirlineA**
  - Endpoint: `POST /provider/AirlineA`
  - Response: `{"status": "success"}`
  - Use Case: Test successful transactions

- **AirlineB**
  - Endpoint: `POST /provider/AirlineB`
  - Response: `{"status": "success"}`
  - Use Case: Test successful transactions

- **AirlineC**
  - Endpoint: `POST /provider/AirlineC`
  - Response: `{"status": "success"}`
  - Use Case: Test successful transactions

## Testing Providers

### Via Frontend UI

Use the Providers page (http://localhost:3000/providers.html) to:
1. View all available providers and their expected behavior
2. Test providers with predefined or custom items
3. View detailed response information including status codes and response times

### Via curl

```bash
# Test CMOT (will fail)
curl -X POST http://localhost:8080/provider/CMOT \
  -H "Content-Type: application/json" \
  -d '[{"id": 1, "name": "Widget A", "quantity": 5}]'

# Expected response: {"status": "failed"}

# Test AirlineA (will succeed)
curl -X POST http://localhost:8080/provider/AirlineA \
  -H "Content-Type: application/json" \
  -d '[{"id": 1, "name": "Widget A", "quantity": 5}]'

# Expected response: {"status": "success"}
```

### Via Items Service

The Items Service has a `purchase-from-provider` endpoint that calls WireMock:

```bash
curl -X POST http://localhost:5001/purchase-from-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "AirlineA", "items": [{"id": 1, "quantity": 5}]}'
```

## Configuration

### Stub Definitions

Stub definitions are located in: `wiremock/mappings/`

Each provider endpoint has its own mapping file:
- `1_cmot.json` - CMOT provider (fails)
- `2_throat.json` - Throat provider (fails)
- `9_catchall.json` - Catch-all pattern for all other providers (succeeds)

Format:
```json
{
  "request": {
    "method": "POST",
    "urlPath": "/provider/{providerName}",
    "bodyPatterns": [{"matchesJsonPath": "$"}]
  },
  "response": {
    "status": 200,
    "jsonBody": {"status": "success|failed"}
  }
}
```

### Matching Rules

- **Specific paths** (files 1_*, 2_*): Exact match for specific providers (loaded first)
- **Pattern matching** (file 9_*): Catch-all `/provider/.*` for any other provider (loaded last)

WireMock matches requests in file load order. Files are loaded alphabetically, so numeric prefixes control priority.

## Response Format

All provider endpoints return HTTP 200 with a JSON response:

```json
{
  "status": "success" | "failed"
}
```

The `status` field indicates whether the provider operation succeeded or failed.

## Adding New Providers

To add a new provider stub:

1. Create a new JSON file in `wiremock/mappings/` with an appropriate numeric prefix
2. Add a request/response mapping
3. Example for a new provider "UPS" (file: `wiremock/mappings/3_ups.json`):

```json
{
  "request": {
    "method": "POST",
    "urlPath": "/provider/UPS",
    "bodyPatterns": [{"matchesJsonPath": "$"}]
  },
  "response": {
    "status": 200,
    "jsonBody": {"status": "success"}
  }
}
```

4. Restart WireMock: `docker compose restart wiremock`

**Note**: Use numeric prefixes (1_, 2_, 3_, etc.) to control matching order. Specific providers should have lower numbers than catch-all patterns.

## Debugging

### View Admin UI

Open http://localhost:8080/__admin to:
- View all registered stubs
- See request history
- Test requests directly

### View Logs

```bash
docker compose logs wiremock
```

### Common Issues

**Provider endpoint returns 404**
- Verify the provider name matches exactly (case-sensitive)
- Check that the request method is POST
- Check that the request body is valid JSON

**Provider endpoint returns unexpected response**
- Verify the stub definition in `provider-stubs.json`
- Check that the stub priority is correct (specific paths before catch-all)
- Use Admin UI to see which stub matched

## Notes

- All responses return HTTP 200 per v1.0.0 requirements
- Response body is always JSON
- No request validation on WireMock side (accepts any JSON body)
- The Items Service wraps WireMock responses and also returns HTTP 200

## References

- WireMock Official Docs: https://wiremock.org/docs/
- Items Service: `services/items-service/README.md`
- Frontend Providers Page: `frontend/README.md`
