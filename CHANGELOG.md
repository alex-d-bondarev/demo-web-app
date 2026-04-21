# Changelog

## [1.0.0] - 2026-04-21

Initial release of ICU (Inventory Control Utility).

### Added

- **Frontend** — Node.js/Express server serving four HTML pages: Items, Purchases, Reviews, and Providers
- **Items Service** — Python/Flask REST API for managing items and purchase orders, backed by MySQL
- **Reviews Service** — Java/Spring Boot REST API for managing stock reviews, backed by MySQL
- **WireMock** — Mocked provider endpoints; CMOT and Throat return `{"status":"failed"}`, all other providers return `{"status":"success"}`
- **MySQL** — Database with tables for `item`, `purchase_order`, `purchase_order_item`, `review`, and `review_item`
- **Docker Compose** — Single-command local environment bringing up all five services
- **Makefile** — Convenience targets for building, starting, stopping, testing, and accessing service shells
- **GitHub Actions** — CI pipeline that builds all Docker images and runs the items-service test suite
