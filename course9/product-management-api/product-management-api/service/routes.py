from flask import jsonify, request
from service import app
from service.models import Product

@app.route("/products", methods=["GET"])
def list_products():
    """List all products or filter by query parameters"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    
    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available:
        available_bool = available.lower() == "true"
        products = Product.find_by_availability(available_bool)
    else:
        products = Product.all()
    
    return jsonify([product.serialize() for product in products])

@app.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    """Get a single product by ID"""
    product = Product.find(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product.serialize())

@app.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a product"""
    product = Product.find(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.get_json()
    product.deserialize(data)
    product.update()
    return jsonify(product.serialize())

@app.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product"""
    product = Product.find(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    product.delete()
    return "", 204