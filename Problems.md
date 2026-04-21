# Problems.md — ICU demo-web-app Analysis

This document catalogues missing best practices, performance issues, and security vulnerabilities found in the project. Findings are grouped by category and include file paths and line numbers where applicable.

---

## CATEGORY 1 — SECURITY

### SEC-01 — Hardcoded Root Credentials Everywhere (Critical)
**Files**: `docker-compose.yml` lines 7, 42–43, 68; `services/items-service/config.py` lines 10–11; `services/reviews-service/src/main/resources/application.properties` lines 2–3; `Makefile` line 44

The MySQL root password `root` is hardcoded in plain text across five files. The root user is used for all application connections — there is no dedicated least-privilege database user.

**Fix**: Use `.env` files or Docker secrets for credentials. Create a restricted `icu_app` user in `init.sql` with only `SELECT`, `INSERT`, `DELETE` on `icu_v1`.

---

### SEC-02 — Debug Ports Exposed on All Network Interfaces (High)
**File**: `docker-compose.yml` lines 49, 72

Both the Python debugpy port `5678` and Java JDWP port `5005` are bound to `0.0.0.0`, exposing them on all host interfaces. Anyone who can reach the host can attach a debugger and execute arbitrary code.

```yaml
- "5678:5678"   # Python debugpy — exposed publicly
- "5005:5005"   # Java JDWP — exposed publicly
```

**Fix**: Bind to localhost only: `"127.0.0.1:5678:5678"` and `"127.0.0.1:5005:5005"`.

---

### SEC-03 — MySQL Port 3306 Unnecessarily Exposed to Host (Medium)
**File**: `docker-compose.yml` line 13

All services communicate over the internal `icu-network`. Exposing `3306` to the host makes the database reachable from outside Docker.

**Fix**: Remove the `ports:` stanza from the `mysql` service.

---

### SEC-04 — No Input Validation on API Endpoints (Medium)
**File**: `services/items-service/app.py` lines 80–103

JSON fields are read with `data.get('field')` without validation. Missing fields silently become `None` and are passed directly to database queries.

**Fix**: Validate required fields and types before executing queries. Consider `pydantic` or `marshmallow`.

---

### SEC-05 — XSS via Unescaped `innerHTML` (Medium)
**Files**: `frontend/public/items.html` lines 105–106; `purchases.html` lines 100–104; `reviews.html` lines 94–98

API data is interpolated directly into HTML template strings and inserted via `innerHTML` without escaping:

```javascript
html += `<td>${item.name}</td>`;  // name from DB, unescaped
```

A malicious string stored in the database (e.g., `<script>alert(1)</script>`) will execute in the browser.

**Fix**: Use `textContent` assignment or an HTML-escaping utility instead of raw `innerHTML` interpolation.

---

### SEC-06 — No CORS Configuration on Backend Services (Medium)
**Files**: `frontend/public/app.js` lines 3–5; `frontend/public/items.html` line 67

The browser makes cross-origin requests directly to `localhost:5001` and `localhost:8081`. Neither the Flask nor Spring Boot service configures CORS headers. This works only by coincidence in local development.

**Fix**: Add `flask-cors` to items-service and a `CorsConfigurationSource` bean to reviews-service. Or proxy all API calls through the Node.js server.

---

### SEC-07 — `FLASK_ENV=development` and `debug=True` in Docker Compose (Medium)
**Files**: `docker-compose.yml` line 45; `services/items-service/config.py` line 19; `services/items-service/app.py` line 247

Flask's debug mode enables the Werkzeug interactive debugger, which allows arbitrary Python code execution via the browser if an exception occurs.

**Fix**: Default `FLASK_ENV` to `production`. Use a production WSGI server (`gunicorn`) instead of `app.run()`.

---

## CATEGORY 2 — BUGS AND FUNCTIONAL CORRECTNESS

### BUG-01 — Port Mismatch: Service on 5001, All Clients Use 5000 (Critical)
**Files**: `docker-compose.yml` lines 46–48, 85; `frontend/public/items.html` line 67; `frontend/public/purchases.html` line 63; `services/items-service/Dockerfile` line 10; `services/items-service/test_items.py` line 6; `.github/workflows/build.yml` lines 43–44

The items-service runs on port `5001` at runtime (via `FLASK_PORT`), but every client still points to port `5000`:

- `docker-compose.yml:85` — `ITEMS_SERVICE_URL: http://items-service:5000`
- `items.html:67` and `purchases.html:63` — hardcoded `:5000`
- `Dockerfile:10` — `EXPOSE 5000 5678`
- `test_items.py:6` — `BASE_URL = "http://localhost:5000"`
- `build.yml:43` — `curl -f http://localhost:5000/item`

**Fix**: Align all references. Either set `FLASK_PORT` back to `5000`, or update all client references, the Dockerfile EXPOSE, tests, and CI to use `5001`.

---

### BUG-02 — All Error Responses Return HTTP 200 (High)
**Files**: `services/items-service/app.py` lines 62, 72, 78, 237–238; `services/reviews-service/src/main/java/com/icu/controller/ReviewController.java` lines 141–146

All error conditions — 404, 500, bad request — return `HTTP 200` with a JSON error body:

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error"}), 200  # should be 404
```

This makes failures invisible to HTTP clients, load balancers, monitoring tools, and `curl -f` in CI.

**Fix**: Return `404` for not found, `400` for bad input, `500` for server errors, `201` for resource creation.

---

### BUG-03 — New DB Connection Per Query — No Connection Pooling (High)
**File**: `services/items-service/app.py` lines 11–47

Every call to `execute_query()` opens a new database connection and closes it after the query. Under any load this will exhaust MySQL's connection limit and adds significant per-request latency.

**Fix**: Use `SQLAlchemy` with a connection pool, or `DBUtils.PooledDB`.

---

### BUG-04 — Health Endpoint Returns 200 on Database Failure (Medium)
**File**: `services/items-service/app.py` lines 221–232

```python
# Returns 200 even when DB is down
return jsonify({"status": "error", "message": "Database connection failed"}), 200
```

Docker healthchecks inspect HTTP status codes. A `200` response from a broken service appears healthy.

**Fix**: Return `HTTP 503 Service Unavailable` when the DB connection fails.

---

### BUG-05 — MySQL Healthcheck Missing Credentials (Medium)
**File**: `docker-compose.yml` lines 14–18

```yaml
test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
```

Missing `-u root -proot` flags make this unreliable across MySQL configurations.

**Fix**: `["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-proot"]`

---

### BUG-06 — `time.sleep(2)` at Module Level in Tests (Medium)
**File**: `services/items-service/test_items.py` line 9

A bare `time.sleep(2)` delays every test run unconditionally and doesn't reliably guarantee the service is up.

**Fix**: Poll the `/health` endpoint with a retry loop and a meaningful timeout.

---

### BUG-07 — `viewPurchase()` Fetches ALL Purchases to Find One (Medium)
**File**: `frontend/public/purchases.html` lines 118–121

```javascript
const result = await API.fetchAPI(`${ITEMS_URL}/purchase`);  // fetches entire table
const po = result.data.find(p => p.purchase_order_id === poId);  // filters client-side
```

There is no `GET /purchase/<id>` endpoint, so the entire table is loaded to find a single record.

**Fix**: Add `GET /purchase/<purchase_order_id>` to items-service and use it in the frontend.

---

### BUG-08 — WireMock "FAILS" Providers Return HTTP 200 (Low)
**Files**: `wiremock/mappings/1_cmot.json` line 13; `wiremock/mappings/2_throat.json` line 12; `frontend/public/app.js` lines 136–147

CMOT and Throat are labeled as `FAILS` but return `HTTP 200` with `{"status": "failed"}` in the body. Since `response.ok` is `true` for any `2xx`, the providers page shows `SUCCESS ✓`, contradicting the label.

---

## CATEGORY 3 — DOCKER AND DOCKER COMPOSE

### DOCK-01 — WireMock Uses Unpinned `latest` Tag (Medium)
**File**: `docker-compose.yml` line 24

```yaml
image: wiremock/wiremock:latest
```

All other images are pinned (e.g., `mysql:8.0`, `python:3.11-slim`). Using `latest` makes builds non-reproducible.

**Fix**: Pin to a specific version, e.g., `wiremock/wiremock:3.3.1`.

---

### DOCK-02 — Source Code Mounted as Volume — Image Not Self-Contained (Medium)
**File**: `docker-compose.yml` lines 53–54, 93–95

Volume mounts overwrite the `COPY . .` step in the Dockerfile. The built image only works when the source directory is present. CI-built images behave differently from local dev images.

**Fix**: Move source mounts to `docker-compose.override.yml` for local development only.

---

### DOCK-03 — Containers Run as Root (Medium)
**Files**: `services/items-service/Dockerfile`; `services/reviews-service/Dockerfile`; `frontend/Dockerfile`

No `USER` instruction is present. All processes run as root inside the container.

**Fix**: Add a non-root user to each Dockerfile:
```dockerfile
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

---

### DOCK-04 — Flask Dev Server Used Instead of a Production WSGI Server (Medium)
**File**: `services/items-service/Dockerfile` line 12; `services/items-service/app.py` line 247

```dockerfile
CMD ["python", "app.py"]
```

Flask's built-in server is single-threaded and not suitable for concurrent requests.

**Fix**: Add `gunicorn` to `requirements.txt` and use `CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]`.

---

### DOCK-05 — No `.dockerignore` Files (Low)
**Files**: `services/items-service/`, `services/reviews-service/`, `frontend/`

`COPY . .` copies `__pycache__/`, test files, `target/`, and `node_modules/` into images, bloating size and potentially leaking build artifacts.

**Fix**: Add a `.dockerignore` to each service directory.

---

### DOCK-06 — `npm install` Instead of `npm ci` in Dockerfile (Low)
**File**: `frontend/Dockerfile` line 6

`npm install` can modify `package-lock.json` inside the build. `npm ci` performs a reproducible, lockfile-strict install.

**Fix**: Use `npm ci` and commit `package-lock.json`.

---

## CATEGORY 4 — CI/CD (.github/workflows/build.yml)

### CI-01 — CI Tests the Wrong Port (Critical)
**File**: `.github/workflows/build.yml` lines 43–44

```yaml
curl -f http://localhost:5000/item || exit 1
```

Items-service runs on `5001`. These CI checks are non-functional. (Related to BUG-01.)

---

### CI-02 — `docker-compose` (V1) vs `docker compose` (V2) Inconsistency (Medium)
**File**: `.github/workflows/build.yml` line 21; `Makefile`

The Makefile uses `docker compose` (V2 plugin, correct). The CI workflow uses `docker-compose` (V1, deprecated):
```yaml
run: docker-compose build
```
GitHub Actions runners are dropping V1 support.

**Fix**: Replace all `docker-compose` in `build.yml` with `docker compose`.

---

### CI-03 — `sleep 15` as a Service Readiness Check (Medium)
**File**: `.github/workflows/build.yml` lines 27–32

A hard 15-second sleep adds dead time to every run. Only the items-service readiness is checked; reviews-service and frontend have none.

**Fix**: Poll all service health endpoints with retry loops. Use Docker health status checks.

---

### CI-04 — No Caching for Docker Layers, Maven, or npm (Medium)
**File**: `.github/workflows/build.yml`

Every CI run downloads all Maven and npm dependencies from scratch, adding several minutes per run.

**Fix**: Add `actions/cache@v4` steps for `~/.m2`, `~/.npm`, and Docker layer cache.

---

### CI-05 — Outdated `docker/setup-buildx-action@v2` (Low)
**File**: `.github/workflows/build.yml` line 18

Current version is v3. `actions/checkout` is correctly on v4.

**Fix**: Update to `docker/setup-buildx-action@v3`.

---

### CI-06 — No Log Artifact Upload on Failure (Low)
**File**: `.github/workflows/build.yml`

If tests fail, no `docker compose logs` output is saved. Debugging requires re-running the pipeline.

**Fix**: Add an `if: failure()` step to upload logs as a CI artifact.

---

## CATEGORY 5 — BACKEND: Python/Flask items-service

### PY-01 — `pytest` Missing from `requirements.txt` (Medium)
**File**: `services/items-service/requirements.txt`

`pytest` is used in `test_items.py` and `make test` but is not listed as a dependency.

**Fix**: Add `pytest` to `requirements.txt` or a separate `requirements-dev.txt`.

---

### PY-02 — DB Errors Silently Treated as Empty Results (Medium)
**File**: `services/items-service/app.py` lines 43–45, 57

```python
except Exception as e:
    app.logger.error(f"Query execution error: {e}")
    return None
# caller:
if items is None: items = []
```

A database error is indistinguishable from a legitimate empty result. The user sees "No data available" on DB failure.

---

### PY-03 — `__pycache__` Directory Committed to Git (Low)
**File**: `services/items-service/__pycache__/config.cpython-311.pyc`

A compiled bytecode file is tracked despite `__pycache__/` being in `.gitignore`. Once tracked, `.gitignore` has no effect.

**Fix**: `git rm -r --cached services/items-service/__pycache__/`

---

## CATEGORY 6 — BACKEND: Java/Spring Boot reviews-service

### JAVA-01 — Spring Boot 3.1.5 is End of Life (Medium)
**File**: `services/reviews-service/pom.xml` line 11

Spring Boot 3.1.x reached end-of-commercial-support in November 2023.

**Fix**: Upgrade to `3.3.x` or `3.4.x`.

---

### JAVA-02 — Tests Require a Live Database — No Test Profile (High)
**File**: `services/reviews-service/src/test/java/com/icu/ReviewsControllerTest.java` line 19

`@SpringBootTest` starts the full application context with a real DB connection. Tests fail entirely when MySQL is not running.

**Fix**: Use `@WebMvcTest` with mocked repositories for controller tests, or configure an H2 in-memory datasource for the `test` Spring profile.

---

### JAVA-03 — `addReviewItem` Ignores Path Variables (Medium)
**File**: `services/reviews-service/src/main/java/com/icu/controller/ReviewController.java` lines 88–101

```java
@PostMapping("/review/{review_id}/item/{review_item_id}")
public ResponseEntity<?> addReviewItem(...) {
    reviewItemRepository.save(reviewItem);  // uses body, path vars ignored
```

Path variables `review_id` and `review_item_id` are accepted but never used. The body values silently override them.

**Fix**: Validate that the body IDs match the path variables, or populate the entity from path variables directly.

---

### JAVA-04 — Field Injection Instead of Constructor Injection (Low)
**File**: `services/reviews-service/src/main/java/com/icu/controller/ReviewController.java` lines 19–23

```java
@Autowired
private ReviewRepository reviewRepository;
```

Field injection is discouraged by the Spring team. It hides required dependencies and makes unit testing without reflection harder.

**Fix**: Use constructor injection with `final` fields.

---

### JAVA-05 — MySQL Connector Version Overrides Spring Boot BOM (Low)
**File**: `services/reviews-service/pom.xml` lines 42–47

An explicit `<version>8.0.33</version>` overrides the BOM-managed version and can cause version mismatches.

**Fix**: Remove the `<version>` tag and let the Spring Boot BOM manage it.

---

### JAVA-06 — `Integer` Instead of `Long` for Entity Primary Keys (Low)
**File**: `services/reviews-service/src/main/java/com/icu/model/Review.java` line 15

`Long` is the conventional type for JPA entity IDs, not `Integer` (max ~2 billion).

---

## CATEGORY 7 — FRONTEND

### FE-01 — Browser Calls Backend Services Directly, Bypassing the Node.js BFF (High)
**Files**: `frontend/public/items.html` line 67; `frontend/public/purchases.html` line 63; `frontend/public/reviews.html` line 59

The Express `server.js` acts as a Backend-for-Frontend but performs zero proxying. HTML pages make direct browser requests to `localhost:5001` and `localhost:8081`:

```javascript
const ITEMS_URL = window.location.protocol + '//' + window.location.hostname + ':5000';
```

This hardcodes internal service hostnames and ports in client-side code, requires CORS on all backends, and prevents deploying to any environment other than `localhost` without rebuilding HTML.

**Fix**: Add proxy routes to `server.js` using `http-proxy-middleware` so the browser only ever talks to `localhost:3000`.

---

### FE-02 — Dead `API_CONFIG` Leaks Internal Docker Hostnames (Low)
**File**: `frontend/public/app.js` lines 2–6

```javascript
const API_CONFIG = {
    ITEMS_URL: 'http://items-service:5001',   // Docker-internal, never used
    REVIEWS_URL: 'http://reviews-service:8081',
    WIREMOCK_URL: 'http://wiremock:8080'
};
```

This object is defined but never referenced. It leaks internal Docker service names to any user who opens DevTools.

---

### FE-03 — No `package-lock.json` Committed (Medium)
**File**: `frontend/`

Without a lockfile, `npm install` resolves the latest compatible versions, making builds non-reproducible across environments.

**Fix**: Commit `package-lock.json` and switch Dockerfile to `npm ci`.

---

### FE-04 — `window.onload` Assignment Instead of `addEventListener` (Low)
**Files**: `frontend/public/items.html` line 163; `purchases.html` line 191; `reviews.html` line 229

```javascript
window.onload = loadItems;  // overwrites any prior handler
```

`addEventListener('load', ...)` is safer and composable.

---

## CATEGORY 8 — DATABASE

### DB-01 — No Primary Keys on Any Table (High)
**File**: `database/init.sql` lines 5–43

```sql
-- (NO PRIMARY KEYS per requirements)
CREATE TABLE IF NOT EXISTS item (
  item_id INT,   -- no PRIMARY KEY constraint
```

Without primary keys MySQL cannot enforce row uniqueness. Duplicate rows with the same `item_id` are possible. JPA `deleteById()` behavior is undefined without a true primary key.

---

### DB-02 — No Foreign Key Constraints (Medium)
**File**: `database/init.sql`

`purchase_order_item.purchase_order_id` and `review_item.review_id` have no `FOREIGN KEY` constraints. Orphaned rows accumulate silently when parent records are deleted.

---

### DB-03 — No Indexes — Full Table Scans on Every Query (Medium)
**File**: `database/init.sql`

No indexes are defined. Every filtered query performs a full table scan. Performance degrades linearly with data volume.

---

### DB-04 — `status` Columns Are Unconstrained `VARCHAR(255)` (Low)
**File**: `database/init.sql` lines 19, 35

No `CHECK` constraint or `ENUM` type restricts `status` to valid values. Any arbitrary string can be stored.

---

## CATEGORY 9 — WIREMOCK

### WM-01 — No WireMock Dependency or Healthcheck in Compose (Low)
**File**: `docker-compose.yml` lines 22–31

Neither `items-service` nor `reviews-service` declares a `depends_on` for `wiremock`. The WireMock service also has no `healthcheck`. If WireMock hasn't started when items-service first handles a `/purchase-from-provider` request, that call fails.

**Fix**: Add a healthcheck to the `wiremock` service and add it to `items-service.depends_on`.

---

### WM-02 — Any Arbitrary Provider Name Returns Success (Informational)
**File**: `wiremock/mappings/9_catchall.json`

Only CMOT and Throat have explicit mappings. All other URL paths (including any typo or unknown provider) fall through to the catch-all and return `{"status": "success"}`. There is no validation that the provider name is one of the five documented providers.

---

## CATEGORY 10 — MAKEFILE

### MAKE-01 — `clean` Does Not Remove Docker Volumes (Low)
**File**: `Makefile` line 52

```makefile
clean:
    docker compose down
    docker rmi ...
```

`docker compose down` without `-v` leaves the `icu_db_data` volume intact. A true clean requires `docker compose down -v`.

---

### MAKE-02 — MySQL Password Visible in Process List (Low)
**File**: `Makefile` line 44

```makefile
docker compose exec mysql mysql -u root -proot icu_v1
```

The `-proot` flag exposes the password in `ps aux` output on the host.

---

## SUMMARY TABLE

| ID | Severity | Category | Title |
|---|---|---|---|
| SEC-01 | Critical | Security | Hardcoded root credentials everywhere |
| BUG-01 | Critical | Bug | Port mismatch — service on 5001, all clients use 5000 |
| CI-01 | Critical | CI/CD | CI tests wrong port (5000 vs 5001) |
| SEC-02 | High | Security | Debug ports exposed on all network interfaces |
| BUG-02 | High | Bug | All errors return HTTP 200 |
| BUG-03 | High | Bug | New DB connection per query — no connection pooling |
| FE-01 | High | Frontend | Browser calls services directly, bypassing BFF |
| JAVA-02 | High | Java | Tests require live DB, no test profile |
| DB-01 | High | Database | No primary keys on any table |
| SEC-03 | Medium | Security | MySQL port 3306 unnecessarily exposed to host |
| SEC-04 | Medium | Security | No input validation — silent None insertions |
| SEC-05 | Medium | Security | XSS via unescaped innerHTML |
| SEC-06 | Medium | Security | No CORS configuration on backend services |
| SEC-07 | Medium | Security | Flask debug mode enabled in compose |
| BUG-04 | Medium | Bug | Health endpoint returns 200 on DB failure |
| BUG-05 | Medium | Bug | MySQL healthcheck missing credentials |
| BUG-06 | Medium | Bug | `time.sleep(2)` at module level in tests |
| BUG-07 | Medium | Bug | viewPurchase fetches all records to find one |
| DOCK-01 | Medium | Docker | WireMock uses unpinned `latest` tag |
| DOCK-02 | Medium | Docker | Source code mounted as volume — image not self-contained |
| DOCK-03 | Medium | Docker | Containers run as root |
| DOCK-04 | Medium | Docker | Flask dev server used in container |
| CI-02 | Medium | CI/CD | `docker-compose` (V1) vs `docker compose` (V2) inconsistency |
| CI-03 | Medium | CI/CD | Hardcoded `sleep 15` + incomplete readiness check |
| CI-04 | Medium | CI/CD | No caching for Docker/Maven/npm layers |
| PY-01 | Medium | Python | `pytest` missing from requirements.txt |
| PY-02 | Medium | Python | DB errors silently treated as empty results |
| JAVA-01 | Medium | Java | Spring Boot 3.1.5 is end of life |
| JAVA-03 | Medium | Java | `addReviewItem` ignores path variables |
| FE-03 | Medium | Frontend | No `package-lock.json` committed |
| DB-02 | Medium | Database | No foreign key constraints |
| DB-03 | Medium | Database | No indexes — full table scans |
| DOCK-05 | Low | Docker | No `.dockerignore` files |
| DOCK-06 | Low | Docker | `npm install` instead of `npm ci` |
| CI-05 | Low | CI/CD | Outdated `setup-buildx-action@v2` |
| CI-06 | Low | CI/CD | No log artifact upload on failure |
| PY-03 | Low | Python | `__pycache__` committed to git |
| JAVA-04 | Low | Java | Field injection instead of constructor injection |
| JAVA-05 | Low | Java | MySQL connector version overrides Spring Boot BOM |
| JAVA-06 | Low | Java | `Integer` instead of `Long` for entity IDs |
| FE-02 | Low | Frontend | Dead `API_CONFIG` leaks internal Docker hostnames |
| FE-04 | Low | Frontend | `window.onload` assignment instead of addEventListener |
| DB-04 | Low | Database | Unconstrained status VARCHAR |
| WM-01 | Low | WireMock | No healthcheck or depends_on for WireMock |
| WM-02 | Info | WireMock | Any arbitrary provider name returns success |
| BUG-08 | Low | Bug | WireMock "FAILS" providers actually return HTTP 200 |
| MAKE-01 | Low | Makefile | `clean` doesn't remove Docker volumes |
| MAKE-02 | Low | Makefile | MySQL password visible in process list |

**Total: 47 findings** across 10 categories.

**Top 3 priorities:**
1. **BUG-01 / CI-01** — Port mismatch breaks all browser→service communication and all CI endpoint checks
2. **SEC-01** — Hardcoded root credentials committed to version control
3. **SEC-02** — Debug ports publicly accessible on all network interfaces
