-- Insert normalized data from flattened table (source_dataset)
-- 1. Customers
INSERT INTO customers (id, `name`, gender, email, phone, address)
SELECT DISTINCT customer_id AS id,
  customer_name AS `name`,
  Gender AS gender,
  email,
  phone_number AS phone,
  address
FROM source_dataset;

-- 2. Products
INSERT INTO products (id, name, category)
SELECT DISTINCT product_id AS id,
  product_name AS name,
  product_category AS category
FROM source_dataset;

-- 3. Suppliers
INSERT INTO suppliers (id, name, phone, email)
SELECT DISTINCT supplier_id AS id,
  supplier_name AS name,
  supplier_phone AS phone,
  supplier_email AS email
FROM source_dataset;

-- 4. Inventory
INSERT INTO inventory (id, product_id, location, stock_quantity, remaining_stock)
SELECT DISTINCT inventory_id AS id,
  product_id,
  location,
  stock_quantity,
  remaining_stock
FROM source_dataset;

-- 5. Orders
INSERT INTO orders (id, customer_id, order_date, status)
SELECT DISTINCT order_id AS id,
  customer_id,
  order_date,
  order_status
FROM source_dataset;

-- 6. Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT order_id,
  product_id,
  quantity,
  unit_price
FROM source_dataset;
