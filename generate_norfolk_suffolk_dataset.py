import pandas as pd
import random
from faker import Faker

fake = Faker('en_GB')
random.seed(42)
Faker.seed(42)

# Simulate councils
councils = ['Norfolk County Council', 'Suffolk County Council']

# Generate synthetic source dataset
rows = []
for i in range(1, 101):
    customer_id = i
    order_id = random.randint(1000, 2000)
    product_id = random.randint(1, 10)
    supplier_id = random.randint(1, 5)
    inventory_id = random.randint(1, 10)
    council = random.choice(councils)

    rows.append({
        'serial_number': i,
        'order_id': order_id,
        'customer_id': customer_id,
        'customer_name': fake.name(),
        'Gender': random.choice(['Male', 'Female']),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'address': f"{fake.street_address()}, {council}, UK",
        'product_id': product_id,
        'product_name': fake.word().capitalize() + " Product",
        'product_category': random.choice(['Electronics', 'Clothing', 'Home', 'Toys']),
        'supplier_id': supplier_id,
        'supplier_name': fake.company(),
        'supplier_phone': fake.phone_number(),
        'supplier_email': fake.company_email(),
        'inventory_id': inventory_id,
        'location': random.choice(['Warehouse A', 'Warehouse B', 'Warehouse C']),
        'stock_quantity': random.randint(20, 100),
        'quantity': random.randint(1, 10),
        'unit_price': round(random.uniform(10, 500), 2),
        'order_date': fake.date_between(start_date='-1y', end_date='today').isoformat(),
        'order_status': random.choice(['Delivered', 'Pending', 'Cancelled']),
        'remaining_stock': random.randint(0, 50),
    })

df = pd.DataFrame(rows)
df.to_csv('source_dataset_norfolk_suffolk.csv', index=False)
print("Source dataset created: source_dataset_norfolk_suffolk.csv")
