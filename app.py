import bcrypt
import uuid
import json
from flask import Flask, redirect, request, session, render_template, flash, url_for, jsonify
from flask_session import Session
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import os

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
verification_codes = {} 

class User:
    def __init__(self, name, email, password, address, phone,security_question):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone
        self.security_question = security_question
        self.id = uuid.uuid4()
        self.wishlist = []  
        self.cart = {}      
        self.orders = []

    def hash_password(self):
        return bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

    def format_data(self, hashed_password):
        users_list = []
        data = {
            "name": self.name,
            "email": self.email,
            "id": str(self.id),
            "password": hashed_password.decode('utf-8'),
            "address": self.address,
            "phone": self.phone,
            "security_question": self.security_question,
            "wishlist": self.wishlist,  
            "cart": self.cart,          
            "orders": self.orders
        }
        try:
            with open('usersDB.json', 'r') as file:
                users_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        users_list.append(data)
        with open("usersDB.json", "w") as file:
            json.dump(users_list, file, indent=4)

    @staticmethod
    def update_user_data(user_id, updated_data):
        try:
            with open('usersDB.json', 'r') as file:
                users_list = json.load(file)

            for user in users_list:
                if user['id'] == user_id:
                    user.update(updated_data)
                    break

            with open("usersDB.json", "w") as file:
                json.dump(users_list, file, indent=4)
        except Exception as e:
            raise Exception("Error updating user data:", str(e))

    def __init__(self, name, email, password,address, phone,security_question):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone
        self.id = uuid.uuid4()
        self.security_question = security_question

    def hash_password(self):
        return bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

    def format_data(self, hashed_password):
        users_list = []
        data = {
            "name": self.name,
            "email": self.email,
            "id": str(self.id),
            "password": hashed_password.decode('utf-8'),
            "address": self.address,
            "phone": self.phone,
            "security_question": self.security_question
        }
        try:
            with open('usersDB.json', 'r') as file:
                users_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        users_list.append(data)
        with open("usersDB.json", "w") as file:
            json.dump(users_list, file, indent=4)

def email_validation(email):
    try:
        email_info = validate_email(email, check_deliverability=False)
        return [True, email_info.normalized]
    except EmailNotValidError as e:
        return [False, str(e)]
def check_password(user_password, hash):
    user_bytes = user_password.encode('utf-8') 
    saved_password = hash.encode('utf-8')
    result = bcrypt.checkpw(user_bytes, saved_password) 
    return result


@app.route('/home')
def homepage():
    if not session.get('user'):
        return redirect('/login')
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        phone = request.form.get('phone')
        security_question = request.form.get('security_question')

        if not email or not password or not name:
            return render_template('signup.html', error='Please enter email, password, and username')

        email_valid = email_validation(email)
        if not email_valid[0]:
            return render_template('signup.html', error=email_valid[1])

        email = email_valid[1]

        userdb_path = 'usersDB.json'
        if os.path.exists(userdb_path):
            with open(userdb_path, 'r') as file:
                userdb = json.load(file)
        else:
            userdb = []

        if any(user['email'] == email for user in userdb):
         return render_template('signup.html', error='Email already exists! Please use a different email.')

        new_user = User(name, email, password,address, phone,security_question)
        hashed_password = new_user.hash_password()
        new_user.format_data(hashed_password)

        session['user'] = str(new_user.id)

        return redirect('/home')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users_list = []
        with open('usersDB.json') as file:
            users_list = json.load(file)

        if not email or not password:
            return render_template('login.html', error='Please enter email and password') 
        
        email_valid = email_validation(email)
        if not email_valid[0]:
            return render_template('login.html', error=email_valid[1])
                
        email = email_valid[1]

        for user in users_list:
            if email == user["email"] and check_password(password, user["password"]):
                session['user'] = user["id"]

                return jsonify({
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "address": user["address"],
                    "phone": user["phone"]
                })

        return render_template('login.html', error='Invalid email or password')
    else:
        if session.get('user'):
            return redirect('/home')

        return render_template('login.html')


@app.route('/pass_page', methods=['GET', 'POST'])
def pass_page():
    if request.method == 'POST':
        return redirect('/pass')
    return render_template('forget.html')

@app.route('/pass', methods=['POST'])
def forgot_password():
    email = request.form['email']
    security_answer = request.form['security_question']

    try:
        with open('usersDB.json', 'r') as file:
            users = json.load(file)

        for user in users:
            if user['email'] == email and user.get('security_question') == security_answer:
                session['reset_email'] = email
                return redirect('/reset_password')

        flash('Invalid email or security answer. Please try again.', 'error')
        return redirect('/pass_page')

    except json.JSONDecodeError:
        flash('Error reading user database. Please contact support.', 'error')
    except IOError:
        flash('Error accessing user database. Please try again later.', 'error')
    except Exception as e:
        flash(f'An unexpected error occurred: {str(e)}', 'error')

    return redirect('/pass_page')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect('/reset_password')

        try:
            email = session.get('reset_email')

            if not email:
                flash('Session expired. Please try again.', 'error')
                return redirect('/pass_page')

            with open('usersDB.json', 'r') as file:
                users = json.load(file)

            for user in users:
                if user['email'] == email:
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    user['password'] = hashed_password.decode('utf-8')
                    break

            with open('usersDB.json', 'w') as file:
                json.dump(users, file, indent=4)

            flash('Password has been reset successfully!', 'success')
            return redirect('/login')

        except json.JSONDecodeError:
            flash('Error reading user database. Please contact support.', 'error')
        except IOError:
            flash('Error accessing user database. Please try again later.', 'error')
        except Exception as e:
            flash(f'An unexpected error occurred: {str(e)}', 'error')

        return redirect('/reset_password')

    return render_template('reset_password.html')

@app.route('/profile')
def profile():
    if not session.get('user'):
        return redirect('/login')
    
    user_id = session.get('user')
    users_list = []
    
    try:
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return render_template('profile.html', error='User data not found')

    current_user = next((user for user in users_list if user['id'] == user_id), None)
    
    if current_user:
        return render_template('profile.html', user=current_user)
    else:
        return render_template('profile.html', error='User not found')

@app.route('/shop')
def shop():
    category = request.args.get('category')
    return render_template('shop.html', category=category)

@app.route('/get_products')
def get_products():
    category = request.args.get('category')
    try:
        with open('products.json', 'r') as file:
            products = json.load(file)
        if category:
            products = [product for product in products if product['type'] == category]
        return jsonify(products)
    except FileNotFoundError:
        return jsonify({"error": "Products file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in products file"}), 500

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/get_wishlist_products', methods=['POST'])
def get_wishlist_products():
    wishlist_ids = request.json.get('wishlist', [])
    try:
        with open('products.json', 'r') as file:
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
        with open('usersDB.json', 'r') as file:
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['wishlist']:
                    user['wishlist'].remove(product_id)  
                else:
                    user['wishlist'].append(product_id)  
                break

        with open("usersDB.json", "w") as file:
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['wishlist']:
                    user['wishlist'].remove(product_id)
                break

        with open("usersDB.json", "w") as file:
            json.dump(users_list, file, indent=4)

        return jsonify({"success": True, "message": "Product removed from wishlist!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['cart']:
                    user['cart'][product_id] += quantity  
                else:
                    user['cart'][product_id] = quantity  
                break

        with open("usersDB.json", "w") as file:
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['cart']:
                    del user['cart'][product_id]  
                break

        with open("usersDB.json", "w") as file:
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if user['id'] == user_id:
                if product_id in user['cart']:
                    user['cart'][product_id] -= quantity
                    if user['cart'][product_id] <= 0:
                        del user['cart'][product_id]  
                break

        with open("usersDB.json", "w") as file:
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        user = next((user for user in users_list if user['id'] == user_id), None)

        cart_items = user['cart'] if user and 'cart' in user else {}
        
        cart_products = []

        with open('products.json', 'r') as file:
            products = json.load(file)

       
        for product_id, quantity in cart_items.items():
            for product in products:
                if str(product['id']) == str(product_id):
                    product['quantity'] = quantity
                    cart_products.append(product)
                    
       
        return jsonify(cart_products)

        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/base')
def base():
    return render_template('home.html')


def load_products():
    with open('products.json', 'r') as f:
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        for user in users_list:
            if str(user['id']) == str(user_id):
                if 'orders' not in user:
                    user['orders'] = []
                user['orders'].append(order_data)
                user['cart'] = {}
                break

        with open("usersDB.json", "w") as file:
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
        with open('usersDB.json', 'r') as file:
            users_list = json.load(file)

        user = next((user for user in users_list if user['id'] == user_id), None)

        if user:
            return jsonify({"success": True, "orders": user.get('orders', [])})
        else:
            return jsonify({"success": False, "error": "User not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/')
def hello_page():
    return "Hello!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/base')


if __name__ == "__main__":
    app.run(debug=True)
