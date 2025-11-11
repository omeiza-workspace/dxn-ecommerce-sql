# ===============================================
# Synthetic E-commerce Database Data Generator
# ===============================================
# Author: [Your Student ID, not your name]
# Module: MSc Data Science and Artificial Intelligence
# Assignment: Introduction to Programming and Data Management
# ===============================================

from faker import Faker
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Initialize Faker and random seeds for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Output directory
output_dir = Path('synthetic_ecommerce')
output_dir.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------
# PARAMETERS
# -----------------------------------------------
TARGET_ROWS = 2000       # Total number of order_items (flattened rows)
NUM_SUPPLIERS = 50
NUM_PRODUCTS = 300
NUM_CUSTOMERS = 400
NUM_ORDERS = 650         # Will produce ~2000 order item rows

# Date range for the last 6 months
today = datetime.now().date()
start_date = today - timedelta(days=180)
date_range_days = (today - start_date).days

# -----------------------------------------------
# 1. SUPPLIERS TABLE
# -----------------------------------------------
suppliers = []
for i in range(1, NUM_SUPPLIERS + 1):
    suppliers.append({
        'supplier_id': i,
        'supplier_name': fake.company(),
        'supplier_phone': fake.phone_number(),
        'supplier_email': fake.company_email()
    })
suppliers_df = pd.DataFrame(suppliers)

# -----------------------------------------------
# 2. PRODUCTS TABLE
# -----------------------------------------------
categories = ['Electronics', 'Home', 'Garden', 'Clothing', 'Toys', 'Sports', 'Beauty', 'Grocery']
products = []
for i in range(1, NUM_PRODUCTS + 1):
    supplier = random.choice(suppliers)
    products.append({
        'product_id': i,
        'product_name': fake.unique.word().capitalize() + ' ' + fake.word().capitalize(),
        'product_category': random.choice(categories),
        'supplier_id': supplier['supplier_id'],
        'unit_price': round(random.uniform(5.0, 500.0), 2)
    })
products_df = pd.DataFrame(products)

# -----------------------------------------------
# 3. INVENTORY TABLE
# -----------------------------------------------
inventory = []
for i, p in enumerate(products, start=1):
    stock = random.randint(0, 500)
    remaining = stock
    inventory.append({
        'inventory_id': i,
        'product_id': p['product_id'],
        'location': random.choice(['Warehouse A', 'Warehouse B', 'Store 1', 'Store 2']),
        'stock_quantity': stock,
        'remaining_stock': remaining
    })
inventory_df = pd.DataFrame(inventory)

# -----------------------------------------------
# 4. CUSTOMERS TABLE
# -----------------------------------------------
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    gender = random.choice(['Male', 'Female', 'Other'])
    customers.append({
        'customer_id': i,
        'customer_name': fake.name(),
        'gender': gender,
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'address': fake.address().replace('\n', ', ')
    })
customers_df = pd.DataFrame(customers)

# -----------------------------------------------
# 5. ORDERS TABLE
# -----------------------------------------------
orders = []
for i in range(1, NUM_ORDERS + 1):
    customer = random.choice(customers)
    rand_days = random.randint(0, date_range_days)
    order_date = start_date + timedelta(days=rand_days)
    order_status = random.choices(['Pending', 'Shipped', 'Delivered', 'Cancelled'],
                                  weights=[0.05, 0.3, 0.6, 0.05])[0]
    orders.append({
        'order_id': i,
        'customer_id': customer['customer_id'],
        'order_date': order_date,
        'order_status': order_status
    })

# Some customers make repeated orders
extra_order_id = NUM_ORDERS + 1
repeat_customers = random.sample(customers, 50)
for cust in repeat_customers:
    rand_days = random.randint(0, date_range_days)
    order_date = start_date + timedelta(days=rand_days)
    orders.append({
        'order_id': extra_order_id,
        'customer_id': cust['customer_id'],
        'order_date': order_date,
        'order_status': random.choice(['Pending', 'Shipped', 'Delivered'])
    })
    extra_order_id += 1

orders_df = pd.DataFrame(orders)

# -----------------------------------------------
# 6. ORDER ITEMS TABLE
# -----------------------------------------------
order_items = []
order_item_id = 1
all_order_ids = orders_df['order_id'].tolist()

for oid in all_order_ids:
    num_items = random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
    for _ in range(num_items):
        prod = random.choice(products)
        qty = max(1, int(np.random.poisson(2)))
        unit_price = prod['unit_price'] * (1 + random.choice([0, 0, 0.05, -0.05]))
        order_items.append({
            'order_item_id': order_item_id,
            'order_id': oid,
            'product_id': prod['product_id'],
            'quantity': qty,
            'unit_price': round(unit_price, 2)
        })
        order_item_id += 1
    if len(order_items) >= TARGET_ROWS:
        break

# Fill up to 2000 rows if needed
while len(order_items) < TARGET_ROWS:
    oid = random.choice(all_order_ids)
    prod = random.choice(products)
    qty = max(1, int(np.random.poisson(2)))
    order_items.append({
        'order_item_id': order_item_id,
        'order_id': oid,
        'product_id': prod['product_id'],
        'quantity': qty,
        'unit_price': prod['unit_price']
    })
    order_item_id += 1

order_items_df = pd.DataFrame(order_items).iloc[:TARGET_ROWS].copy()

# -----------------------------------------------
# 7. FLATTENED SOURCE DATASET (for testing)
# -----------------------------------------------
merged = order_items_df.merge(orders_df, on='order_id', how='left')
merged = merged.merge(customers_df, on='customer_id', how='left')
products_df_renamed = products_df.rename(columns={'unit_price': 'product_unit_price'})
merged = merged.merge(products_df_renamed, on='product_id', how='left')
merged = merged.merge(suppliers_df, on='supplier_id', how='left')
merged = merged.merge(inventory_df[['product_id', 'inventory_id', 'location',
                                    'stock_quantity', 'remaining_stock']],
                      on='product_id', how='left')

flattened = pd.DataFrame({
    'serial_number': range(1, len(merged) + 1),
    'order_id': merged['order_id'],
    'customer_id': merged['customer_id'],
    'customer_name': merged['customer_name'],
    'Gender': merged['gender'],
    'email': merged['email'],
    'phone_number': merged['phone_number'],
    'address': merged['address'],
    'product_id': merged['product_id'],
    'product_name': merged['product_name'],
    'product_category': merged['product_category'],
    'supplier_id': merged['supplier_id'],
    'supplier_name': merged['supplier_name'],
    'supplier_phone': merged['supplier_phone'],
    'supplier_email': merged['supplier_email'],
    'inventory_id': merged['inventory_id'],
    'location': merged['location'],
    'stock_quantity': merged['stock_quantity'],
    'quantity': merged['quantity'],
    'unit_price': merged['unit_price'],
    'order_date': merged['order_date'].astype(str),
    'order_status': merged['order_status'],
    'remaining_stock': merged['remaining_stock']
})

# -----------------------------------------------
# 8. SAVE FILES
# -----------------------------------------------
customers_df.to_csv(output_dir / 'customers.csv', index=False)
suppliers_df.to_csv(output_dir / 'suppliers.csv', index=False)
products_df.to_csv(output_dir / 'products.csv', index=False)
inventory_df.to_csv(output_dir / 'inventory.csv', index=False)
orders_df.to_csv(output_dir / 'orders.csv', index=False)
order_items_df.to_csv(output_dir / 'order_items.csv', index=False)
flattened.to_csv(output_dir / 'source_dataset_flattened.csv', index=False)

print(f"✅ Synthetic dataset generated successfully in folder: {output_dir}")
print(f"📦 Total records in flattened dataset: {len(flattened)}")
print(f"👥 Customers: {len(customers_df)}, Orders: {len(orders_df)}, Products: {len(products_df)}")
