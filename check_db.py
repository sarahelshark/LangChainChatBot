import sqlite3

def check_database():
    conn = sqlite3.connect('fakeEcommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, description, price, image_url FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

if __name__ == '__main__':
    products = check_database()
    if products:
        print("Database contents:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Image URL: {product[4]}")
    else:
        print("No products found in the database.")
