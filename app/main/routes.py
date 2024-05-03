from flask import render_template, redirect, url_for, request, session
from . import main
from app import mongo


@main.route('/')
@main.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('main.register'))
    username = session['username']
    return render_template('home.html', username=username)



@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        users = mongo.db.users
        existing_user = users.find_one({'username': username})
        if existing_user:
            return 'Пользователь с таким именем уже зарегистрирован!'

        users.insert_one({'username': username, 'email': email, 'password': password})

        session['username'] = username

        return redirect(url_for('main.home'))

    return render_template('register.html')


@main.route('/logout')
def logout():
    session.pop('username', None)

    return redirect(url_for('main.home'))


@main.route('/tasks')
def tasks():
    if 'username' not in session:
        return redirect(url_for('main.home'))

    return render_template('tasks.html')
