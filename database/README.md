# Database Layer

## Atlas hints

```shell
cd database
export DB_URL="mysql://root:root@localhost:9050/im_db"
export DEV_DB="docker://mysql/8/dev"

# Test connection to local docker compose
atlas schema inspect --url ${DB_URL} --format "OK"

# Dry run the change
atlas schema apply \
  --url "$DB_URL" \
  --to file://schema/ \
  --dev-url "docker://mysql/8/dev" \
  --dry-run
# OR
atlas schema apply --env local --dry-run

# Apply changes
atlas schema apply --env local

# Clean up
atlas tool docker kill --name my-db
```

## Manual Database Operations

### Connect to MySQL
```bash
docker-compose exec mysql mysql -u root -proot im_db
```

### View all tables
```bash
docker-compose exec mysql mysql -u root -proot im_db -e "SHOW TABLES;"
```

### View table structure
```bash
docker-compose exec mysql mysql -u root -proot im_db -e "DESCRIBE item;"
```

### View all data in a table
```bash
docker-compose exec mysql mysql -u root -proot im_db -e "SELECT * FROM item;"
```

### Reset database
```bash
docker-compose down
docker volume rm demo-web-app_im_db_data
docker-compose up -d mysql
```
