import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import pandas as pd
import csv 

cred = credentials.Certificate('./ServiceAccountKey.json')
app = firebase_admin.initialize_app(cred)

store = firestore.client()

file_path = "./top-1m.csv"
collection_name = "top1websitesalexa"

def batch_data(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

data = []
headers = []

with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            for header in row:
                headers.append(header)
            line_count += 1
        else:
            obj = {}
            for idx, item in enumerate(row):
                obj[headers[idx]] = item
            data.append(obj)
            line_count += 1
    print(f'Processed {line_count} lines.')


for batched_data in batch_data(data, 499):
    batch = store.batch()
    for data_item in batched_data:
        doc_ref = store.collection(collection_name).document()
        batch.set(doc_ref, data_item)
    batch.commit()

# doc_ref = store.collection(u'test')
# doc_ref.add({u'name': u'test', u'added': u'just now'})

# try: 
#     docs = doc_ref.get()
#     for doc in docs:
#         print(u'Doc Data:{}'.format(doc.to_dict()))

# except google.cloud.exceptions.NotFound:
#     print(u'Missing data')

# df = pd.read_csv('top-1m.csv')
# print(df.head())