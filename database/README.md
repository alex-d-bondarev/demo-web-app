# Database Layer

## Schema Details

See [init.sql](./init.sql)

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
