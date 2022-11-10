import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask App
app = Flask(__name__, template_folder='templates')

# Initialize Firestore DB
cred = credentials.Certificate('ServiceAccountKey_v2.json')
default_app = initialize_app(cred)
db = firestore.client()
url_ref = db.collection('urlhaus')

@app.route('/urls', methods=['GET'])
def basic():
    try:
        all_urls_docs = [doc.to_dict() for doc in url_ref.stream()]
        print(all_urls_docs[0])
        return render_template('templates/index_v2.html', t=all_urls_docs[0:10])
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == 'main':
    app.run(debug=True, port=5000)  