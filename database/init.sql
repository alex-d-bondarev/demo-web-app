-- Create database
CREATE DATABASE IF NOT EXISTS im_db;
USE im_db;

-- Create tables (NO PRIMARY KEYS per requirements)
CREATE TABLE IF NOT EXISTS item (
  item_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  optimal_stock INT,
  volume DECIMAL(10, 2),
  weight DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS purchase_order (
  purchase_order_id INT AUTO_INCREMENT PRIMARY KEY,
  created_dt DATETIME,
  delivered_dt DATETIME,
  status VARCHAR(255),
  provider VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS purchase_order_item (
  purchase_order_item_id INT AUTO_INCREMENT PRIMARY KEY,
  item_id INT,
  purchase_order_id INT,
  price DECIMAL(10, 2),
  quantity INT
);

CREATE TABLE IF NOT EXISTS review (
  review_id INT AUTO_INCREMENT PRIMARY KEY,
  start_dt DATETIME,
  end_dt DATETIME,
  status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS review_item (
  review_item_id INT AUTO_INCREMENT PRIMARY KEY,
  review_id INT,
  item_id INT,
  quantity INT
);

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;
