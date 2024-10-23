from flask import redirect, request, session, render_template, flash, jsonify
from app import app

@app.route('/base')
def base():
    return render_template('home.html')

@app.route('/home')
def homepage():
    if not session.get('user'):
        return redirect('/login')
    return render_template('home.html')

@app.route('/')
def hello_page():
    return redirect('/base')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog_2')
def blog_2():
    return render_template('blog2.html')

@app.route('/blog_3')
def blog_3():
    return render_template('blog3.html')      
