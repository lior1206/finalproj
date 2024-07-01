from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
from os import environ


app = Flask(__name__)
app.secret_key = '3f5eed7b6884e653ca2debd0653a92bfe9389a0351dd9589'
load_dotenv()
DB_USERNAME= environ.get('DB_USERNAME')
DB_PASSWORD= environ.get('DB_PASSWORD')
DB_HOST=environ.get('DB_HOST')
# MongoDB connection setup
client = MongoClient(f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:27017/finaldb')
db = client.finaldb
collection = db.users_auth 



    
@app.route('/', methods=['GET', 'POST'])
def logine():
    
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username =request.form.get("username")
        password =  request.form.get("password")
        
        user = collection.find_one({'username': username })
        if user is None:
           print ('the user does not exist')
        else:  
              if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                return redirect(url_for('calc'))
              else:
                return "Incorrect password", 401  
             
            
    return redirect(url_for('login'))    

        


@app.route('/calc/', methods=['GET', 'POST'])
def calc():
    return render_template("calculator.html")

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
    

    result = collection.insert_one(user)

    # Handle successful signup redirection or error handling
    return redirect(url_for('calc'))
    


  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=35000)
