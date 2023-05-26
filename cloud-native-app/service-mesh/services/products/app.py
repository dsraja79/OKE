from flask import Flask, jsonify
import psycopg2
import json
import os

products_file = os.getenv('PRODUCTS_FILE')
version = os.getenv('VERSION')
pg_host = os.getenv('POSTGRES_HOST')

app = Flask(__name__)


print(f"Products file:{products_file}")  

# Database Configuration
#POSTGRES_HOST = "products-postgres-service"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password"
POSTGRES_DB = "products"
MAX_RETRIES = 3
RETRY_DELAY = 2


def establish_database_connection():
    conn = psycopg2.connect(
        host=pg_host,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )
    return conn

# Call the function to establish the database connection
db = establish_database_connection()

def initialize_database(products_file):
    # Connect to the database
    db = establish_database_connection()
    cursor = db.cursor()

    # Create the Products table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Products (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        version VARCHAR(10),
        price INT,
        description TEXT
    )
    """
    cursor.execute(create_table_query)

    # Load product data from JSON file
    with open(products_file) as file:
        products = json.load(file)

    print("Loading products table...");

    # Insert or update product data into the database
    for product in products:
        # Check if the product with the given id already exists in the database
        cursor.execute("SELECT COUNT(*) FROM Products WHERE id = %s", (product['id'],))
        result = cursor.fetchone()
        if result[0] > 0:
            print("product exist, updating -->");
            # Update the existing record
            update_query = """
            UPDATE Products
            SET name = %s, version = %s, price = %s, description = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (product['name'], product['version'], product['price'], product['description'], product['id']))
        else:
            print("no product exist, inserting -->");
            # Insert a new record
            insert_query = """
            INSERT INTO Products (id, name, version, price, description)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (product['id'], product['name'], product['version'], product['price'], product['description']))

    # Commit the changes
    db.commit()
    
    # Close the database connection
    cursor.close()
    db.close()



@app.route('/')
def hello():
    return 'Products Service started!'


@app.route("/api/products")
def get_products():
    conn = establish_database_connection()
    cursor = conn.cursor()
    print("get all products -->");
     # Check if the product with the given id already exists in the database
    cursor.execute("SELECT * FROM products WHERE version = %s", (version,))    
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    response = [{"id": product[0], "name": product[1], "version": product[2], "price": product[3]} for product in products]
    return jsonify(response)

# Route to get the price of a product by name
@app.route('/api/products/<product_name>', methods=['GET'])
def get_product_price(product_name):
    conn = establish_database_connection()
    cursor = conn.cursor()

    try:
        # Query the database for the product price
        query = "SELECT price FROM products WHERE name = %s"
        cursor.execute(query, (product_name,))
        result = cursor.fetchone()

        if result:
            price = result[0]
            return jsonify({'name': product_name, 'price': price})
        else:
            return jsonify({'error': 'Product not found'})
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)})
    finally:
        cursor.close()
        conn.close()
    
    

if __name__ == '__main__':
    initialize_database(products_file)
    app.run(host='0.0.0.0', port=5000)
