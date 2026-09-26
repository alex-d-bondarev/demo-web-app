# WireMock for providers

WireMock simulates HTTP responses for provider endpoints in the Items Service.

## API

```bash
# Test CMOT (will fail)
curl -X POST http://localhost:9040/provider/CMOT \
  -H "Content-Type: application/json" \
  -d '[{"id": 1, "name": "Widget A", "quantity": 5}]'

# Expected response: {"status": "failed"}

# Test AirlineA (will succeed)
curl -X POST http://localhost:9040/provider/AirlineA \
  -H "Content-Type: application/json" \
  -d '[{"id": 1, "name": "Widget A", "quantity": 5}]'
```

## Configuration

- `1_cmot.json` - CMOT provider (fails)
- `2_throat.json` - Throat provider (fails)
- `9_catchall.json` - Catch-all pattern for all other providers (succeeds)
