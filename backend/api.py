from flask import Flask, request
from db import get_products, remove_product, add_product, get_types
app = Flask(__name__)

# Used by everyone. Gets inventory of all items matching store_name, product_name, product_manufacturer, product_type
@app.route("/get_inventory_admin", methods = ['GET'])
def get_inventory_admin():
    data = request.data
    out = get_products(data["zip"])
    
    if (data.has_key("store_name")):
        out = filter(lambda product: data["store_name"].lower() in product[-2].lower(), out)
    if (data.has_key("product_name")):
        out = filter(lambda product: data["product_name"].lower() in product[0].lower(), out)
    if (data.has_key("product_manufacturer")):
        out = filter(lambda product: data["product_manufacturer"].lower() in product[1].lower(), out)
    if (data.has_key("product_type")):
        out = filter(lambda product: data["product_type"].lower() in product[2].lower(), out)
    
    return out
    
@app.route("/add_delete_item", methods = ['DELETE', 'POST'])
def add_delete_item():
    # needs all unique identifiers: store, product name & manuf.
    data = request.data
    if (request.method == 'DELETE'):
        remove_product(data["product_name"], data["store_name"], data["product_manufacturer"])
    else:
        add_product(data)

@app.route("/get_types", methods = ['GET'])
def get_types():
    # gets types of products
    return get_types
    

if __name__ == "__main__":

    app.debug = True
    app.run(host='0.0.0.0', port=5003) 