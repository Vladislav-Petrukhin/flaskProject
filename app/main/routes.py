from bson.json_util import dumps
from flask import render_template, redirect, url_for, request, session, jsonify
from . import main
from app import mongo
from app.neural_networks import preprocess_data, train_model, save_to_db, retrieve_results


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


progress = 0

@main.route('/neural_networks')
def neural_networks():
    return render_template('neural_networks.html')


@main.route('/tasks')
def tasks():
    if 'username' not in session:
        return redirect(url_for('main.home'))
    return render_template('tasks.html')


@main.route('/preprocess_data', methods=['POST'])
def preprocess_and_train():
    global progress
    progress = 0
    data, y = preprocess_data()
    results = train_model(data, y)
    save_to_db(results)
    return dumps(results)


@main.route('/retrieve_results', methods=['POST'])
def retrieve_data():
    results = retrieve_results()
    return jsonify(results)


@main.route('/training_progress', methods=['GET'])
def training_progress():
    global progress
    return jsonify({'progress': progress})
