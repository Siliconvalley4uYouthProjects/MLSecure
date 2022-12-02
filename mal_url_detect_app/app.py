import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
import pandas as pd
import re
from flask_cors import CORS

# Initialize Flask App
app = Flask(__name__, template_folder='templates')
CORS(app)

# Initialize Firestore DB (just for testing) (Commented out because it will exceed Firebase Quota Limit)
# cred = credentials.Certificate('ServiceAccountKey_v2.json')
# default_app = initialize_app(cred)
# db = firestore.client()
# url_ref = db.collection('urlhaus')
# query = url_ref.limit_to_last(10).order_by("url")  # Order by the URL column and only retrieve the first 10 rows
# results = query.get()

# Test Connection with Firestore DB (Commented out because it will exceed Firebase Quota Limit)
# @app.route('/urls', methods=['GET'])
# def connect_fb():
#     try:
#         all_urls_docs = [doc.to_dict() for doc in results]  # change to make it faster
#         print(all_urls_docs[0])
#         return render_template('index.html', t=all_urls_docs)
#     except Exception as e:
#         return f"An error occurred: {e}"

# Load dataset
df = pd.read_csv('./dataset/urlhaus_v2.txt', delimiter=',')
all_urls_docs = df['url']
print(df.shape)
df.drop('id', axis=1, inplace=True)


# url search API
@app.route('/urlsearch', methods=['GET', 'POST'])
def modifySearch():
    try:
        found_urls = pd.DataFrame()
        count = 0

        # process the tags column and add all unique values to tags_set for display in drop-down list
        tags = df.tags.str.split(',')
        tags_list = []
        for t in tags:
            for e in t:
                if e == '':
                    continue
                else:
                    tags_list.append(e)
        tags_set = sorted(set(tags_list))

        # handle POST request
        if request.method == 'POST':
            # Check Texts:
            if request.form['submit'] == 'add_text':
                # extract urls from user's input
                texts = ''
                texts = request.form['search_text']
                print(texts)
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                urls = re.findall(regex, texts)
                print(urls)
                url_list = list(map(lambda x: x[0], urls))
                print(url_list)

                # make the list into a set for unique urls
                url_set = set(url_list)
                print(url_set)

                # Retrieve inputs from filters
                url_status = request.form.get('url_status')
                print(url_status)

                threat = request.form.get('url_threat')
                print(threat)

                tags = request.form.get('url_tags')
                print(tags)

                # Find the urls:
                found_urls = pd.DataFrame(columns=df.columns.values.tolist())

                # Matching process
                # if there are urls in user's input, return the dataframe containing the URLs matched in dataset
                if len(url_set) > 0:
                    for x in url_set:
                        found_urls = pd.concat(
                            [found_urls, df[(df['url'] == x)]], axis=0)
                else:
                    # if user does not input any text, return the whole dataset
                    if texts == '':
                        found_urls = df
                    # if user inputs text but there is no url in the text, return an empty dataframe
                    else:
                        found_urls = pd.DataFrame(
                            columns=df.columns.values.tolist())

                # filter url_status
                if url_status == 'all':
                    found_urls = found_urls
                else:
                    found_urls = found_urls[(
                        found_urls['url_status'] == url_status)]

                # filter threat
                if threat == 'all':
                    found_urls = found_urls
                else:
                    found_urls = found_urls[(found_urls['threat'] == threat)]

                # filter tags
                if tags == 'all':
                    found_urls = found_urls
                else:
                    found_urls = found_urls[(found_urls['tags'].isin(
                        [t for t in found_urls['tags'] if tags in t]))]

                # print result to terminal
                count = found_urls.shape[0]
                print('found ', count)

                # Render HTML template with results found
                # if there is no URL found
                if count == 0:
                    print('not found')
                    return render_template(
                        'search.html',
                        x="There is no malicious URLs found.",
                        data=df,
                        d=found_urls,
                        url_tags=tags_set)
                else:
                    # Only return 50 URLs if > 50 URLs found
                    if count > 50:
                        return render_template(
                            'search.html',
                            x='Found {} malicious URL(s):'.format(count),
                            data=df,
                            d=found_urls.iloc[:50].reset_index(drop=True),
                            y='Showing only 50 URLs',
                            url_tags=tags_set)
                    else:
                        return render_template(
                            'search.html',
                            x='Found {} malicious URL(s):'.format(count),
                            data=df,
                            d=found_urls.iloc[:50].reset_index(drop=True),
                            url_tags=tags_set)

        return render_template('search.html',
                               data=df,
                               d=found_urls,
                               url_tags=tags_set)
    except Exception as e:
        return f"An error occurred: {e}"


# file scanner API
@app.route('/fileupload', methods=['GET'])
def file_scan():
    try:
        print("Upload File API called")
        return render_template('file.html')
    except Exception as e:
        return f"An error occurred: {e}"


# just a test
@app.route("/test", methods=["GET"])
def test():
    return "1"


if __name__ == 'main':
    app.run(debug=True, port=5000)
