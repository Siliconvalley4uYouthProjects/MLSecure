import pyrebase
# from collections.abc import MutableMapping
from flask import *
from firebase_admin import credentials, initialize_app

config = {
    "apiKey": "AIzaSyAKa4D-Wf2lT9C8KHq03UJNDw3fkJ3kuL0",
    "authDomain": "mlv2-5433c.firebaseapp.com",
    "projectId": "mlv2-5433c",
    "storageBucket": "mlv2-5433c.appspot.com",
    "messagingSenderId": "102375590557",
    "appId": "1:102375590557:web:ecfdc34f084f8e5d1f6274"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def basic():
    if request.method=='POST':
        if request.form['submit']=='add':
            name = request.form['name']
            db.child("todo").push(name)
            todo = db.child("todo").get()
            to = todo.val()
            return render_template('index.html', t=to.values())
        elif request.form['submit'] == 'delete':
            db.child("todo").remove()
    return render_template('index.html')

if __name__ == 'main':
    app.run(debug=True, port=5000)  