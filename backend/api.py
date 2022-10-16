import json
from flask import Flask, request, send_from_directory, render_template, jsonify
# from db import get_products, remove_product, add_product, get_types
from db import *
app = Flask(__name__, template_folder='../pages', static_folder = '../static')



@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

# Used by everyone. Gets inventory of all items matching store_name, product_name, product_manufacturer, product_type
@app.route("/get_inventory_admin", methods = ['POST'])
def get_inventory_admin():
    data = request.json
    out = get_products(data["zip"])
    if ("store_name" in data):
        out = filter(lambda product: data["store_name"].lower() in product[-2].lower(), out)
    if ("product_name" in data):
        out = filter(lambda product: data["product_name"].lower() in product[0].lower(), out)
    if ("product_manufacturer" in data):
        out = filter(lambda product: data["product_manufacturer"].lower() in product[1].lower(), out)
    if ("product_type" in data):
        out = filter(lambda product: data["product_type"].lower() in product[2].lower(), out)
    return jsonify({'result': [dict(row) for row in out]})
    
@app.route("/add_delete_item", methods = ['DELETE', 'POST'])
def add_delete_item():
    # needs all unique identifiers: store, product name & manuf.
    data = request.json
    if (request.method == 'DELETE'):
        remove_product(data["product_name"].lower(), data["store_name"].lower(), data["product_manufacturer"].lower(), data["zip_code"])
    else:
        add_product(data)
    return "true"

@app.route("/get_types", methods = ['GET'])
def get_product_types():
    # gets types of products
    return get_types()
    
@app.route("/", methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route("/home", methods=['GET'])
def get_home():
    return render_template('index.html')

@app.route("/community", methods=['GET'])
def get_community():
    return render_template('community.html')

@app.route("/products", methods=['GET'])
def get_products_page():
    return render_template('products.html')

@app.route("/search", methods=['GET'])
def get_search():
    return render_template('search.html')

@app.route("/mail", methods=['GET'])
def get_mail():
    return render_template('email.html')

@app.route("/admin", methods=['GET'])
def get_admin():    
    return render_template('admin.html')

@app.route("/login", methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route("/add_to_mail_list", methods=['POST'])
def add_to_mail_list():
    data = request.json
    print(data)
    email = data["email"]
    zipcode = data["zip"]
    store = data["store"].lower()
    food_type = data["food_type"].lower()
    # add to db
    add_to_email_list(email, zipcode, store, food_type)

    #print("made it")
    return "True"

@app.route("/grocery_search", methods=['POST'])
def grocery_search():
    data = request.json
    print(data)
    zipcode = data["zip"]
    out = search_groceries(zipcode)
    if ("store_name" in data):
        out = filter(lambda product: data["store_name"].lower() in product[-2].lower(), out)
    if ("food_type" in data):
        out = filter(lambda product: data["product_type"].lower() in product[2].lower(), out)
    return jsonify({'result': [dict(row) for row in out]})
    print(out)
    return jsonify({'result': [dict(row) for row in out]})

if __name__ == "__main__":

    app.debug = True
    app.run(host='0.0.0.0', port=5003) 