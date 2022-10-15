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
    # TODO: idk how to do this normally
    remove_all_query = """
    DROP TABLE IF EXISTS accounts;
    DROP TABLE IF EXISTS accountsdb ;
    DROP TABLE IF EXISTS products_db;
    """
    # remove all tables first
    conn.execute(text(remove_all_query))

# initializes database with tables
def init_db():
    # creates new tables if they don't already exist
    create_products_query = """CREATE TABLE IF NOT EXISTS products_db (
        product_name STRING,
        product_manufacturer STRING,
        product_type STRING,
        expiration_date DATE,
        quantity INT,
        store_name STRING,
        store_location STRING
    );"""
    # accounts for grocery stores
    conn.execute(text(create_products_query))


sqlQuery = """CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance INT8
);"""
#res = conn.execute(text(sqlQuery))

# initialize db
# remove_all_tables()
init_db()

#conn.execute(text(create_products_query))
res = conn.execute(text("show tables;")).fetchall()
#res = conn.execute(text("select * from products_db")).fetchall()
print(res)