-- Customers table
CREATE TABLE `customers` (
  `id` INT NOT NULL,
  `name` VARCHAR (255) DEFAULT NULL,
  `gender` ENUM ('Male', 'Female') DEFAULT 'Male',
  `email` VARCHAR (255) DEFAULT NULL,
  `address` VARCHAR (255) DEFAULT NULL,
  `postcode` VARCHAR (255) DEFAULT NULL,
  `county` VARCHAR (255) DEFAULT NULL,
  `phone` VARCHAR (255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
-- Products table
CREATE TABLE `products` (
  `id` INT NOT NULL,
  `name` VARCHAR (255) DEFAULT NULL,
  `category` VARCHAR (255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
INSERT INTO customers (id, `name`, gender, email, phone, address)
SELECT DISTINCT customer_id AS id,
  customer_name AS `name`,
  Gender AS gender,
  email,
  phone_number AS phone,
  address
FROM source_dataset
ORDER BY id;
INSERT INTO products (id, `name`, category)
SELECT DISTINCT product_id AS id,
  product_name AS `name`,
  product_category AS category
FROM source_dataset
ORDER BY id;
-- INSERT INTO orders (id, date, status, customer_id)
-- SELECT DISTINCT order_id AS id, 
--                 order_date AS date, 
--                 order_status AS status,
--                 customer_id
-- FROM source_dataset
-- ORDER BY id;
--
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT order_id,
  product_id,
  quantity,
  unit_price
FROM source_dataset
ORDER BY order_id;
INSERT INTO inventory (
    id,
    order_date,
    stock_quantity,
    remaining_quantity,
    product_id,
    quantity_sold
  )
SELECT inventory_id,
  order_date,
  stock_quantity,
  remaining_quantity,
  product_id,
  quantity_sold
FROM source_dataset
ORDER BY order_id;
INSERT INTO inventory (
    inventory_id,
    order_date,
    order_id,
    stock_quantity,
    remaining_quantity,
    product_id,
    quantity_sold
  )
SELECT inventory_id,
  order_date,
  order_id,
  stock_quantity,
  remaining_stock as remaining_quantity,
  product_id,
  quantity as quantity_sold
FROM source_dataset
ORDER BY order_date;