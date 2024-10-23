from flask import jsonify, request, session, render_template
import json
from app import app


usersDB_path='app/usersDB.json'
productDB_path = 'app/products.json'

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not session.get('user'):
        return jsonify({"error": "You need to be logged in"}), 403

    user_id = session.get('user')
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['cart']:
                    user['cart'][product_id] += quantity  
                else:
                    user['cart'][product_id] = quantity  
                break

        with open(usersDB_path, "w") as file:
            json.dump(users_list, file, indent=4)

        return jsonify({"success": True, "message": "Product added to cart!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if not session.get('user'):
        return jsonify({"error": "You need to be logged in"}), 403

    user_id = session.get('user')
    product_id = request.json.get('product_id')

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['cart']:
                    del user['cart'][product_id]  
                break

        with open(usersDB_path, "w") as file:
            json.dump(users_list, file, indent=4)

        return jsonify({"success": True, "message": "Product removed from cart!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/remove_quantity_from_cart', methods=['POST'])
def remove_quantity_from_cart():
    if not session.get('user'):
        return jsonify({"error": "You need to be logged in"}), 403

    user_id = session.get('user')
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['cart']:
                    user['cart'][product_id] -= quantity
                    if user['cart'][product_id] <= 0:
                        del user['cart'][product_id]  
                break

        with open(usersDB_path, "w") as file:
            json.dump(users_list, file, indent=4)

        return jsonify({"success": True, "message": "Quantity updated!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_cart_items', methods=['GET'])
def get_cart_items():
    if not session.get('user'):
        return jsonify({"error": "User not logged in"}), 403

    user_id = session.get('user')
    
    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        user = next((user for user in users_list if user['id'] == user_id), None)

        cart_items = user['cart'] if user and 'cart' in user else {}
        
        cart_products = []

        with open(productDB_path, 'r') as file:
            products = json.load(file)

       
        for product_id, quantity in cart_items.items():
            for product in products:
                if str(product['id']) == str(product_id):
                    product['quantity'] = quantity
                    cart_products.append(product)
                    
       
        return jsonify(cart_products)

        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
