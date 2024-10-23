from flask import redirect, request, session, render_template, jsonify, flash
from app.model import User
from app.validate import email_validation, check_password
import bcrypt
import json
import os
from app.model import User
from app import app
from app.validate import email_validation, check_password 

usersDB_path = 'app/usersDB.json'

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

        if os.path.exists(usersDB_path):
            with open(usersDB_path, 'r') as file:
                userdb = json.load(file)
        else:
            userdb = []

        if any(user['email'] == email for user in userdb):
            return jsonify({"error": 'Email already exists! Please use a different email.'}), 400

        new_user = User(name, email, password,address, phone,security_question)
        hashed_password = new_user.hash_password()
        new_user.format_data(hashed_password)

        session['user'] = str(new_user.id)
        return jsonify({
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "address": new_user.address,
            "phone": new_user.phone
        }), 201
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users_list = []
        with open(usersDB_path) as file:
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
        with open(usersDB_path, 'r') as file:
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

            with open(usersDB_path, 'r') as file:
                users = json.load(file)

            for user in users:
                if user['email'] == email:
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    user['password'] = hashed_password.decode('utf-8')
                    break

            with open(usersDB_path, 'w') as file:
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/base')