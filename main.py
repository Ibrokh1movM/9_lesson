import requests
from context_managers import DatabaseConnect


def fetch_data():
    url = "https://dummyjson.com/products"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['products']
    else:
        print(f"Error fetching data: {response.status_code}")
        return []


def save_to_database(products):
    db_info = {
        'host': 'localhost',
        'database': 'nt',
        'user': 'postgres',
        'password': 'Muzaffar080403',
        'port': 5432
    }

    with DatabaseConnect(**db_info) as conn:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2),
                    discountPercentage DECIMAL(5, 2),
                    rating DECIMAL(3, 2),
                    stock INT,
                    brand VARCHAR(100) DEFAULT 'Unknown'
                );
                """)
                conn.commit()

                for product in products:
                    brand = product.get('brand', 'Unknown')
                    cur.execute("""
                    INSERT INTO products (title, description, price, discountPercentage, rating, stock, brand)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        product['title'],
                        product['description'],
                        product['price'],
                        product['discountPercentage'],
                        product['rating'],
                        product['stock'],
                        brand
                    ))
                conn.commit()
                print(f"{len(products)} products saved successfully.")


if __name__ == '__main__':
    products = fetch_data()
    if products:
        save_to_database(products)
