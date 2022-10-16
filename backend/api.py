import json
from flask import Flask, request, send_from_directory, render_template, jsonify
from db import get_products, remove_product, add_product, get_types
app = Flask(__name__, template_folder='../pages', static_folder = '../static')



@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

# Used by everyone. Gets inventory of all items matching store_name, product_name, product_manufacturer, product_type
@app.route("/get_inventory_admin/<data>", methods = ['GET'])
def get_inventory_admin(data):
    data = json.loads(data)
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
    data = request.data
    if (request.method == 'DELETE'):
        remove_product(data["product_name"], data["store_name"], data["product_manufacturer"])
    else:
        add_product(data)

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
    print("reached")
    print(request.json)
    #email = data['email']
    #zipcode = data["zip"]
    #store = data["store"]
    #food = data["food_type"]
    #print("made it")
    return "True"

if __name__ == "__main__":

    app.debug = True
    app.run(host='0.0.0.0', port=5003) 