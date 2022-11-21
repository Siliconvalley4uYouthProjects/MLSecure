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

@app.route('/script.js')
def script():
    return render_template('script.js')

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
            
            # Check Texts:
            if request.form['submit']=='add_text':
                # extract urls from user's input
                texts = ''
                texts = request.form['search_text']
                print(texts)

                # Retrieve inputs from filters


                # Find the urls:
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                urls = re.findall(regex,texts)     
                print(urls) 
                found_urls = []
                count = 0

                # Matching process --> change to compare the rows instead of columns
                for x in urls:
                    for u in all_urls_docs:
                        if x[0] == u: # & date/other fields match
                            print('found')
                            if x[0] not in found_urls:
                                found_urls.append(x[0])
                                # retrieve all attributes for that url
                                count += 1

                if count == 0:
                    print('not found')
                    return render_template('home.html', i=["There is no malicious URLs found in this email."])

                # if count > 50 -> only send 50 

                else:
                    return render_template('home.html', i=found_urls, x='Found {} malicious URL(s):'.format(count))
                
        return render_template('home.html')
    except Exception as e:
        return f"An error occurred: {e}"

# modify search API
@app.route('/urlsearch', methods = ['GET', 'POST'])
def modifySearch():
    try:
        found_urls = pd.DataFrame()
        count = 0
        if request.method=='POST':           
            # Check Texts:
            if request.form['submit']=='add_text':
                # extract urls from user's input
                texts = ''
                texts = request.form['search_text']
                print(texts)
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                urls = re.findall(regex,texts)  
                print(urls) 
                url_list = list(map(lambda x: x[0], urls))
                print(url_list)

                # Retrieve inputs from filters
                url_status = request.form.get('url_status')
                print(url_status)

                threat = request.form.get('url_threat')
                print(threat)

                tags = request.form.get('url_tags')
                print(tags)

                # Find the urls:
                found_urls = pd.DataFrame(columns=df.columns.values.tolist())

                # Matching process --> change to compare the rows instead of columns
                # if there are urls in user's input
                if len(url_list) > 0:
                    for x in urls:
                        pd.concat([found_urls, df[(df['url'] == x)]])
                        print(found_urls)
                else:
                    # if user does not input any text
                    if texts == '':
                        found_urls = df
                    # if user inputs text but there is no url in the text, return an empty dataframe
                    else:
                        found_urls = pd.DataFrame(columns=df.columns.values.tolist())

                # filter url_status
                if url_status == 'all':
                    found_urls = found_urls
                else:
                    found_urls = found_urls[(found_urls['url_status'] == url_status)]
                
                # filter threat
                if threat == 'all':
                    found_urls = found_urls
                else:
                    found_urls = found_urls[(found_urls['threat'] == threat)]
                
                # filter tags
                if tags == 'all':
                    found_urls = found_urls
                else:
                    found_urls = found_urls[(found_urls['tags'] == tags)]
                
                # print result to terminal
                count = found_urls.shape[0]
                print('found ', count)

                # Return result
                # if there is no URL found
                if count == 0:
                    print('not found')
                    return render_template('search.html', x="There is no malicious URLs found.", data = df, d = found_urls)
                else:
                    # Only return 50 URLs if > 50 URLs found
                    if count > 50: 
                        return render_template('search.html', x='Found {} malicious URL(s):'.format(count), data = df, d = found_urls.iloc[:50], y = 'Showing only 50 URLs')
                    else:
                        return render_template('search.html', x='Found {} malicious URL(s):'.format(count), data = df, d = found_urls.iloc[:50])
                    
        return render_template('search.html', data = df, d = found_urls)
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