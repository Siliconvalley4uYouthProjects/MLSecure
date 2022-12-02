# MLSecure - ITSS 4395 Capstone Project for SwatCloud

## Project Description

This project is to create a web application to check whether an URL is malicious and provide user with information about malicious URLs based on their inputs (status, threats, tags, etc.). In the future, we want to extend the datasets to security events, domains, IP addresses, file hash, etc. and add more features to the application, for example, file scanner to check if there is any security threat in a file.

## Stacks

This application is built using Flask API as back-end and HTML, CSS, and Javascript as front-end. We also use Bootstrap as a CSS framework for design templates. In the future, we want to connect Firebase as a cloud database for the application.

## Firebase

A Firebase project is created for this application. You can find the Key to connect to the Firestore Database in **/mal_url_detect_app/ServiceAccountKey_v2.json** file.

## Folder Description

### to-do_app

This is a test application that we created in the beginning phase of the project to test the Flask API request and Firebase connection. It is a to-do app that will keep track of to-do list items and user can add, update, and delete a to-do item. The database for this app is Firebase Real Time Database and it gets updated with user's action in real time.

### mal_url_detect_app

This is the directory for Malicious URL Detector app.

#### client

This folder is the environment for developing a web app in ReactJS. The app is set up to communicate with the Flask API in app.py, but has yet to be developed fully. This is for future developers moving forward with the project and want to use a more robust, efficient, and user-responsive web developmemnt framework.

#### dataset

This folder is the dataset that we used for the Malicious URL Detector app. It is from URLHaus, a project operated by abuse.ch to collect, track, and share malware URLs, helping network administrators and security analysts to protect their network and customers from cyber threats. The dataset can be downloaded here: https://urlhaus.abuse.ch/api/#csv in Database Dump (CSV) section. The CSV gets generated every 5 minutes. The dataset we have is last updated on 2022-11-01 15:41:14 (UTC).

#### static/styles

This folder is where the web app front-end's CSS and Javascript file resides.

#### templates

This folder is where the web app front-end's HTML file resides. **file.html** is for the file scanner page, and **search.html** is for the url search page.

#### app.py

This is the app.py file for creating Flask app and runnning Flask server. The commented sections are for testing connection to Firebase. Due to the limited quota for free plan, we have to comment it out so it does not read data every time, which will easily make it go over the limit.

#### main.py

This is the code we used to upload the dataset to Firestore Cloud Database. It basically reads each row of the dataset and insert it to Firestore collection named "urlhaus." However, due to the limit, we were only able to upload about 23K rows from the dataset.

## Instruction to compile

### Prerequisite

Make sure you have already installed all of the following programs:

- Python 3.10.7 or later (https://www.python.org/getit/)
- pip (https://pip.pypa.io/en/stable/installing/)

### Installation

1. Clone this repository
2. Go to the root directory of this repository on your local machine, then go to /mal_url_detect_app folder:

`cd MLSecure/mal_url_detect_app`

3. Create virtual environment

`pip install virtualenv`

`virtualenv venv -python=python3`

`source venv/bin/activate`

4. Install required packages:

`pip install -r requirements.txt`

5. Start the app:

Type the following command in your terminal:

`python -m flask run`
