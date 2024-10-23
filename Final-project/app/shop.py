from flask import jsonify, request, session, render_template
import json
from app import app


usersDB_path='app/usersDB.json'
productDB_path = 'app/products.json'

@app.route('/shop')
def shop():
    category = request.args.get('category')
    return render_template('shop.html', category=category)

@app.route('/get_products')
def get_products():
    category = request.args.get('category')
    try:
        with open(productDB_path, 'r') as file:
            products = json.load(file)
        if category:
            products = [product for product in products if product['type'] == category]
        return jsonify(products)
    except FileNotFoundError:
        return jsonify({"error": "Products file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in products file"}), 500

        
