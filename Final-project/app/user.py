from flask import redirect, session, render_template, flash, jsonify
import json
from app.model import User
from app import app

usersDB_path = 'app/usersDB.json'

@app.route('/profile')
def profile():
    if not session.get('user'):
        return redirect('/login')
    
    user_id = session.get('user')
    users_list = []
    
    try:
        with open(usersDB_path, 'r') as file:
            users_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return render_template('profile.html', error='User data not found')

    current_user = next((user for user in users_list if user['id'] == user_id), None)
    
    if current_user:
        return render_template('profile.html', user=current_user)
    else:
        return render_template('profile.html', error='User not found')
    
