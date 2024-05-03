from flask import render_template, redirect, url_for, request
from . import main
from app import mongo


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        users = mongo.db.users
        users.insert_one({'username': username, 'email': email, 'password': password})

        return redirect(url_for('main.home'))

    return render_template('register.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/tasks')
def tasks():
    return render_template('tasks.html')
