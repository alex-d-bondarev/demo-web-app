# Database Layer

## Overview

This directory contains the MySQL database initialization scripts for ICU v1.0.0.

## Schema Details

### Tables

#### `item`
Stores inventory items with their properties.

**Fields**:
- `item_id` (INT): Unique identifier for the item
- `name` (VARCHAR): Item name
- `optimal_stock` (INT): Optimal stock level
- `price` (DECIMAL): Unit price
- `volume` (DECIMAL): Item volume
- `weight` (DECIMAL): Item weight

#### `purchase_order`
Stores purchase orders from suppliers.

**Fields**:
- `purchase_order_id` (INT): Unique identifier for the purchase order
- `created_dt` (DATETIME): Order creation date/time
- `delivered_dt` (DATETIME): Delivery date/time
- `status` (VARCHAR): Order status (e.g., pending, delivered)
- `provider` (VARCHAR): Supplier name

#### `purchase_order_item`
Links items to purchase orders with quantities and prices.

**Fields**:
- `purchase_order_item_id` (INT): Unique identifier
- `item_id` (INT): Reference to item
- `purchase_order_id` (INT): Reference to purchase_order
- `price` (DECIMAL): Unit price at time of purchase
- `quantity` (INT): Quantity ordered

#### `review`
Stores inventory reviews/audits.

**Fields**:
- `review_id` (INT): Unique identifier for the review
- `start_dt` (DATETIME): Review start date/time
- `end_dt` (DATETIME): Review end date/time
- `status` (VARCHAR): Review status (e.g., completed, in-progress)

#### `review_item`
Links items to reviews with quantities counted during review.

**Fields**:
- `review_item_id` (INT): Unique identifier
- `review_id` (INT): Reference to review
- `item_id` (INT): Reference to item
- `quantity` (INT): Quantity counted during review

## Data Persistence

- MySQL container uses named volume `icu_db_data`
- Volume mounted to `/var/lib/mysql` in container
- Data persists between container restarts

## Initialization

- The `init.sql` script is automatically executed when the MySQL container starts for the first time
- Script is copied to `/docker-entrypoint-initdb.d/` in the container
- Database and tables are created automatically

## Manual Database Operations

### Connect to MySQL
```bash
docker-compose exec mysql mysql -u root -proot icu_v1
```

### View all tables
```bash
docker-compose exec mysql mysql -u root -proot icu_v1 -e "SHOW TABLES;"
```

### View table structure
```bash
docker-compose exec mysql mysql -u root -proot icu_v1 -e "DESCRIBE item;"
```

### View all data in a table
```bash
docker-compose exec mysql mysql -u root -proot icu_v1 -e "SELECT * FROM item;"
```

### Reset database
```bash
docker volume rm demo-web-app_icu_db_data
docker-compose up -d mysql
```

## Important Notes

- **No PRIMARY KEYS**: Per v1.0.0 requirements, no primary key constraints
- **No FOREIGN KEYS**: No referential integrity constraints
- **No INDEXES**: No performance indexes
- **All fields nullable**: Minimal schema for v1.0.0 learning purposes

These constraints are intentionally set for the learning phase and will be improved in future versions.
