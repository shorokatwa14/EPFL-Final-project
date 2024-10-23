from flask import jsonify, request, session, render_template
import json
from app import app


usersDB_path='app/usersDB.json'
productDB_path = 'app/products.json'



@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/get_wishlist_products', methods=['POST'])
def get_wishlist_products():
    wishlist_ids = request.json.get('wishlist', [])
    try:
        with open(productDB_path, 'r') as file:
            all_products = json.load(file)
        wishlist_products = [product for product in all_products if product['id'] in wishlist_ids]
        return jsonify(wishlist_products)
    except FileNotFoundError:
        return jsonify({"error": "Products file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in products file"}), 500
@app.route('/get_wishlist', methods=['GET'])
def get_wishlist():
    if not session.get('user'):
        return jsonify({"error": "You need to be logged in"}), 403

    user_id = session.get('user')

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        user = next((user for user in users_list if user['id'] == user_id), None)

        if user:
            return jsonify({"success": True, "wishlist": user['wishlist']})
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    if not session.get('user'):
        return jsonify({"error": "You need to be logged in"}), 403

    user_id = session.get('user')
    product_id = request.json.get('product_id')

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['wishlist']:
                    user['wishlist'].remove(product_id)  
                else:
                    user['wishlist'].append(product_id)  
                break

        with open(usersDB_path, "w") as file:
            json.dump(users_list, file, indent=4)

        return jsonify({"success": True, "message": "Wishlist updated!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist():
    if not session.get('user'):
        return jsonify({"error": "You need to be logged in"}), 403

    user_id = session.get('user')
    product_id = request.json.get('product_id')

    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['wishlist']:
                    user['wishlist'].remove(product_id)
                break

        with open(usersDB_path, "w") as file:
            json.dump(users_list, file, indent=4)

        return jsonify({"success": True, "message": "Product removed from wishlist!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500