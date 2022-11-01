import pyrebase
# from collections.abc import MutableMapping

config = {
    "apiKey": "AIzaSyBpPT7IQZxyOMhxoiQpLI4Ho4Opr9Z0MPk",
    "authDomain": "test-e8881.firebaseapp.com",
    "databaseURL": "https://test-e8881-default-rtdb.firebaseio.com",
    "projectId": "test-e8881",
    "storageBucket": "test-e8881.appspot.com",
    "messagingSenderId": "796926947188",
    "appId": "1:796926947188:web:7b04439a740a44ef910621"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

from flask import *

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