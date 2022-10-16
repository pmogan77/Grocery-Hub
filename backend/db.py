import os
from sqlalchemy import create_engine, text
from models import accounts
from sqlalchemy import Table, Column, Integer, String, MetaData
from testtwilio import send_message

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
    DROP TABLE IF EXISTS email_list_db;
    """
    # remove all tables first
    conn.execute(text(remove_all_query))

# consumer's POV?
def get_products(zip):
    get_product_query = """
    SELECT * FROM products_db
    """
    if(zip != 0):
        get_product_query += f" WHERE zip_code = {zip}"
    return conn.execute(text(get_product_query)).fetchall()


def remove_product(product_name, store_name, product_manufacturer, zip_code):
    # ASSUMPTION: product_name, store_name, product_manuf. are all unique identifiers. could be source of bugs
    get_product_query = f"""
    SELECT * FROM products_db WHERE product_name = '{product_name}'
    AND store_name = '{store_name}'
    AND product_manufacturer='{product_manufacturer}'
    AND zip_code={zip_code}
    """
    print(product_name)
    print(store_name)
    print(product_manufacturer)
    print(zip_code)
    quantity = conn.execute(text(get_product_query)).fetchall()[0][-3]
    if (quantity == 1):
        delete_query = f"""DELETE FROM products_db  WHERE product_name = '{product_name}'
        AND store_name = '{store_name}'
        AND product_manufacturer='{product_manufacturer}'
    """
        conn.execute(text(delete_query))
    else:
        update_query = f"""UPDATE products_db SET quantity={quantity-1} WHERE product_name = '{product_name}'
        AND store_name = '{store_name}'
        AND product_manufacturer='{product_manufacturer}';"""
        conn.execute(text(update_query))
    return "true"

def add_product(data):
    product_name, store_name, product_manufacturer, product_type, zipcode = data["product_name"].lower(), data["store_name"].lower(), data["product_manufacturer"].lower(), data["product_type"].lower(), data["zip_code"]
    # if no matches then need to add new entry, else increment count
    get_product_query = f"""
    SELECT * FROM products_db WHERE product_name = '{product_name}'
    AND store_name = '{store_name}' 
    AND product_manufacturer='{product_manufacturer}';
    """
    result = conn.execute(text(get_product_query)).fetchall()
    if (len(result) == 0):
        # doesn't exist in db; add new entry
        insert_query = f"""INSERT INTO products_db 
        VALUES('{product_name}', '{product_manufacturer}', '{product_type}', DATE '{data['expiration_date']}', {data['discounted_price']}, {data['quantity']}, '{store_name}', {zipcode})
        """
        conn.execute(text(insert_query))
    else:
        # already exists; increment count
        quantity = result[0][-3]
        update_query = f"""UPDATE products_db SET quantity={quantity+data["quantity"]} WHERE product_name = {product_name}
        AND store_name = {store_name} 
        AND product_manufacturer={product_manufacturer};"""
        conn.execute(text(update_query))
    # Notify all users interested in this item in this zip code that it has been added to the list
    find_users_query = f"""
    SELECT email FROM email_list_db WHERE food_type='{product_type}' AND store_name='{store_name}' AND zipcode={zipcode};
    """
    emails = conn.execute(text(find_users_query)).fetchall()
    for email in emails:
        send_message(email, f"{product_name} you're interested in is available at {store_name}")

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
    insert_product = ["""INSERT INTO products_db
    VALUES('buttermilk', 'betsys', 'dairy', DATE '2016-03-26', 2.5, 10, 'target', 78705)
    ;""",
    """INSERT INTO products_db
    VALUES('yogurt', 'yoplait', 'dairy', DATE '2016-03-26', 2.5, 10, 'target', 78705)
    ;""",
    """INSERT INTO products_db
    VALUES('chicken', 'kirkland', 'poultry', DATE '2016-03-26', 2.5, 10, '7/11', 78704)
    ;""",
     """INSERT INTO products_db
    VALUES('chicken', 'kirkland', 'poultry', DATE '2016-03-26', 2.5, 10, 'heb', 78704)
    ;""",
     """INSERT INTO products_db
    VALUES('cheese', 'kraft', 'poultry', DATE '2018-03-26', 2.5, 10, 'walmart', 78704)
    ;""",
    """INSERT INTO products_db
    VALUES('chicken', 'kirkland', 'poultry', DATE '2016-03-26', 2.5, 10, 'walmart', 78705)
    ;""",
    """INSERT INTO products_db
    VALUES('chicken', 'kirkland', 'poultry', DATE '2043-03-26', 2.5, 10, 'costco', 78704)
    ;""",
    """INSERT INTO products_db
    VALUES('chicken', 'kirkland', 'poultry', DATE '2016-03-26', 2.5, 10, 'costco', 78704)
    ;""",
    """INSERT INTO products_db
    VALUES('candy', 'blue', 'dairy', DATE '2022-10-15', 3.5, 10, 'heb', 78705)
    ;""",
    """INSERT INTO products_db
    VALUES('salmon', 'kroger', 'seafood', DATE '2022-10-20', 9.5, 10, 'kroger', 78703)
    ;""",
    """INSERT INTO products_db
    VALUES('tobasco sauce', 'tobasco', 'hot sauce', DATE '2023-01-26', 2.5, 60, 'heb', 78705)
    ;""",
    """INSERT INTO products_db
    VALUES('daves bread', 'kirkland', 'bakery', DATE '2022-10-18', 5.5, 6, 'costco', 78704)
    ;""",
    """INSERT INTO products_db
    VALUES('garlic gread', 'heb', 'bakery', DATE '2022-10-17', .5, 10, 'heb', 78704)
    ;"""
    ]
    for i in insert_product:
        conn.execute(text(i))
    # create accounts table
    # accountType: 0 = user, 1 = company
    create_accounts_query = """
    CREATE TABLE IF NOT EXISTS accounts_db (
        acountType INT,
        email STRING,
        password STRING,
        name STRING,
        zip INT
    );
    """
    conn.execute(text(create_accounts_query))
    # inserts 1 company account
    add_comp_acct_query = """
    INSERT INTO accounts_db VALUES
    (0, 'TheStoreCompany@rediffmail.com', '$Password1', 'Guadalupe Target', 78705);
    """
    conn.execute(text(add_comp_acct_query))

    # creates email_list_db table - user accounts
    email_list_db = """
    CREATE TABLE IF NOT EXISTS email_list_db (
        email STRING,
        store_name STRING,
        food_type STRING,
        zipcode INT
    );
    """
    conn.execute(text(email_list_db))
    # inserts 1 user account into email list 'beagledeagle123@rediffmail.com'
    praveen_cell = ''
    add_user_acct_query = """
    INSERT INTO email_list_db VALUES
    ('+13463061669', 'HEB', 'Dairy', 78705);
    """
    conn.execute(text(add_user_acct_query))

def add_to_email_list(email, zipcode, store, food_type):
    # TODO: if statement to stop same email from reregistering
    add_to_emails_query = f"""
    INSERT INTO email_list_db VALUES
    ('{email}', '{store}', '{food_type}', {zipcode});
    """
    conn.execute(text(add_to_emails_query))
    print(conn.execute(text("""SELECT * FROM email_list_db""")).fetchall())

def search_groceries(zipcode):
    search_groceries_query = """
    SELECT * FROM products_db
    """
    if(zipcode != 0):
        search_groceries_query += f" WHERE zip_code = '{zipcode}'"
    #  store_name='{store}' AND  AND product_type='{food_type}
    return conn.execute(text(search_groceries_query)).fetchall()

# removes all tables and then adds them back
def reinit_db():
    remove_all_tables()
    init_db()

# initialize db
reinit_db()

# sqlQuery = """CREATE TABLE accounts (
#     id UUID PRIMARY KEY,
#     balance INT8
# );"""
