import os
from sqlalchemy import create_engine, text
from models import accounts
from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

DATABASE_URL = "cockroachdb://foodhubadmin:suGuSm6T2jdJVVht2vuC2w@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dwowed-slime-6541"
engine = create_engine(DATABASE_URL)
# create connection to db
conn = engine.connect()

# removes all tables from database (so we can easily clear junk tables)
def remove_all_tables():
    remove_all_query = """
    DROP TABLE IF EXISTS accounts;
    DROP TABLE IF EXISTS accountsdb ;
    DROP TABLE IF EXISTS accounts_db;
    DROP TABLE IF EXISTS products_db;
    """
    # remove all tables first
    conn.execute(text(remove_all_query))

# consumer's POV?
def get_products(zip):
    get_product_query = f"""
    SELECT * FROM products_db WHERE zip_code = {zip}
    """
    return conn.execute(text(get_product_query)).fetchall()

def remove_product(product_name, store_name, product_manufacturer):
    # ASSUMPTION: product_name, store_name, product_manuf. are all unique identifiers. could be source of bugs
    get_product_query = f"""
    SELECT * FROM products_db WHERE product_name = {product_name}
    AND store_name = {store_name} 
    AND product_manufacturer={product_manufacturer}
    """
    quantity = conn.execute(text(get_product_query)).fetchall()[-3]
    if (quantity == 1):
        delete_query = f"""DELETE FROM products_db  WHERE product_name = {product_name}
        AND store_name = {store_name} 
        AND product_manufacturer={product_manufacturer}
    """
        conn.execute(text(delete_query))
    else:
        update_query = f"""UPDATE products_db SET quantity={quantity-1} WHERE product_name = {product_name}
        AND store_name = {store_name} 
        AND product_manufacturer={product_manufacturer};"""
        conn.execute(text(update_query))

def add_product(data):
    product_name, store_name, product_manufacturer = data["product_name"], data["store_name"], data["product_manufacturer"]
    # if no matches then need to add new entry, else increment count
    get_product_query = f"""
    SELECT * FROM products_db WHERE product_name = {product_name}
    AND store_name = {store_name} 
    AND product_manufacturer={product_manufacturer}
    """
    result = conn.execute(text(get_product_query)).fetchall()
    if (len(result) == 0):
        # doesn't exist in db; add new entry
        insert_query = f"""INSERT INTO products_db
        VALUES({str(data.values())[1:-1]})
        """
        conn.execute(text(insert_query))
    else:
        # already exists; increment count
        quantity = result[-3]
        update_query = f"""UPDATE products_db SET quantity={quantity+1} WHERE product_name = {product_name}
        AND store_name = {store_name} 
        AND product_manufacturer={product_manufacturer};"""
        conn.execute(text(update_query))

def get_types():
    get_types_query = "SELECT DISTINCT product_type FROM products_db"
    return conn.execute(text(get_types_query)).fetchall()


# initializes database with tables
def init_db():
    # TODO: do I need unique ID?
    # creates new tables if they don't already exist
    create_products_query = """CREATE TABLE IF NOT EXISTS products_db (
        product_name STRING,
        product_manufacturer STRING,
        product_type STRING,
        expiration_date DATE,
        discounted_price DECIMAL,
        quantity INT,
        store_name STRING,
        zip_code INT
    );"""
    conn.execute(text(create_products_query))
    insert_product = """INSERT INTO products_db
    VALUES('a', 'a', 'a', DATE '2016-03-26', 2.5, 10, 'a', 78705)
    ;"""
    conn.execute(text(insert_product))
    # create accounts db
    create_accounts_query = """
    CREATE TABLE IF NOT EXISTS accounts_db (
        acountType INT,
        email STRING,
        password STRING,
        address STRING
    );
    """
    conn.execute(text(create_accounts_query))

# removes all tables and then adds them back
def reinit_db():
    remove_all_tables()
    init_db()

sqlQuery = """CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance INT8
);"""
#res = conn.execute(text(sqlQuery))

# initialize db
reinit_db()

#conn.execute(text(create_products_query))
res = conn.execute(text("SELECT * FROM products_db;")).fetchall()
#res = conn.execute(text("select * from products_db")).fetchall()
print(res)