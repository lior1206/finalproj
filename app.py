from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
from os import environ
from datetime import datetime, timedelta
import logging
from bson import ObjectId
import json

app = Flask(__name__)
app.secret_key = '3f5eed7b6884e653ca2debd0653a92bfe9389a0351dd9589'
load_dotenv()
DB_USERNAME = environ.get('DB_USERNAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST')

# MongoDB connection setup
client = MongoClient(f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:27017/finaldb')
db = client.finaldb
collection = db.users_auth
expenses_collection = db.user_expenses  # New collection for expenses

# Setup logging
logging.basicConfig(level=logging.DEBUG)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


app.json_encoder = JSONEncoder


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        user = collection.find_one({'username': username})
        if user is None:
            logging.debug('The user does not exist')
            return "User does not exist", 401
        else:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['username'] = username
                return redirect(url_for('calc'))
            else:
                return "Incorrect password", 401


@app.route('/calc/', methods=['GET', 'POST'])
def calc():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        date = datetime.now().strftime("%Y-%m-%d")
        expenses = {
            'username': username,
            'date': date,
            'food': float(request.form.get('food')),
            'transportation': float(request.form.get('transportation')),
            'housing': float(request.form.get('housing')),
            'utilities': float(request.form.get('utilities')),
            'entertainment': float(request.form.get('entertainment')),
            'others': float(request.form.get('others')),
            'total': float(request.form.get('food')) + float(request.form.get('transportation')) + float(request.form.get('housing')) + float(request.form.get('utilities')) + float(request.form.get('entertainment')) + float(request.form.get('others'))
        }
        result = expenses_collection.insert_one(expenses)
        logging.debug(f'Inserted expense with id: {result.inserted_id}')

        return jsonify({'status': 'success', 'message': 'Expenses saved successfully', 'id': str(result.inserted_id)}), 200

    username = session['username']
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Fetch user's weekly expenses
    weekly_expenses = list(expenses_collection.find({'username': username, 'date': {'$gte': week_ago, '$lte': today}}))
    weekly_expenses = [{**expense, '_id': str(expense['_id'])} for expense in weekly_expenses]

    # Calculate daily average expenses
    total_expenses = sum(exp['total'] for exp in weekly_expenses)
    average_daily_expenses = total_expenses / 7

    return render_template("calculator.html", average_daily_expenses=average_daily_expenses, weekly_expenses=weekly_expenses)


@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        'username': username,
        'password': hashed_password,
        'email': email
    }
    collection.insert_one(user)

    return redirect(url_for('calc'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=35000)
