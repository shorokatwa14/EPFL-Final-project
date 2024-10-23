from flask import redirect, request, session, render_template, flash, jsonify
from datetime import datetime
import bcrypt
import os
import json
from app import app

usersDB_path='app/usersDB.json'
productDB_path = 'app/products.json'


def load_products():
    with open(productDB_path, 'r') as f:
        return json.load(f)
    
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/get_product_details', methods=['POST'])
def get_product_details():
    try:
        product_ids = request.json
        products = load_products()
        product_details = [
            product for product in products 
            if str(product['id']) in product_ids
        ]
        return jsonify(product_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_order', methods=['POST'])
def place_order():
    if not session.get('user'):
        return jsonify({"error": "You need to be logged in"}), 403

    user_id = session.get('user')
    order_data = request.json
    order_data['order_date'] = datetime.now().isoformat()
    order_data['order_id'] = generate_order_id()

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if str(user['id']) == str(user_id):
                if 'orders' not in user:
                    user['orders'] = []
                user['orders'].append(order_data)
                user['cart'] = {}
                break

        with open(usersDB_path, "w") as file:
            json.dump(users_list, file, indent=4)

        return jsonify({"success": True, "message": "Order placed successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

def generate_order_id():
    return f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"

@app.route('/get_orders', methods=['GET'])
def get_orders():
    if not session.get('user'):
        return jsonify({"success": False, "error": "User not logged in"}), 403

    user_id = session.get('user')

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        user = next((user for user in users_list if user['id'] == user_id), None)

        if user:

            return jsonify({"success": True, "orders": user.get('orders', [])})
        else:
            return jsonify({"success": False, "error": "User not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

