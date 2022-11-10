import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
import pandas as pd
import re

# Initialize Flask App
app = Flask(__name__, template_folder='templates')

# Load dataset
df = pd.read_csv('./dataset/urlhaus_v2.txt', delimiter=',')
all_urls_docs = df['url']
# print(type(all_urls_docs))
# print(all_urls_docs[0])

@app.route('/', methods = ['GET', 'POST'])
def search():
    try:
        if request.method=='POST':
            # Check URL:
            if request.form['submit']=='add_url':
                url = ''
                url = request.form['url']
                print(url)
                count = 0
                for u in all_urls_docs:
                    if u == url:
                        count += 1
                if count > 0:
                    print('found')
                    return render_template('home.html', f="Found URL in Malicious URLs Dataset:", t=[url])
                if count == 0:
                    print('not found')
                    return render_template('home.html', f="Does not find URL in Malicious URLs Dataset.")
            # Check Email:
            if request.form['submit']=='add_email':
                email = ''
                email = request.form['email_text']
                print(email)
                # Find the urls:
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                urls = re.findall(regex,email)     
                print(urls) 
                found_urls = []
                count = 0
                for x in urls:
                    for u in all_urls_docs:
                        if x[0] == u:
                            print('found')
                            found_urls.append(x[0])
                            count += 1
                if count == 0:
                    print('not found')
                    return render_template('home.html', i=["There is no malicious URLs found in this email."])
                else:
                    return render_template('home.html', i=found_urls, x='Found {} malicious URL(s):'.format(count))

                # return [x[0] for x in url]
                
        return render_template('home.html')
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/urls', methods=['GET'])
def basic():
    try:
        all_urls_docs = df['url']
        print(all_urls_docs[0])
        return render_template('index.html', t=all_urls_docs[0:10])
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == 'main':
    app.run(debug=True, port=5000)  