import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC44ce835f45f88a09f22c987c09f2b76b'
    TWILIO_SYNC_SERVICE_SID = 'IS719dd9fe6ca05a3a1d2b6f87acaf21d6'
    TWILIO_API_KEY = 'SKd063be5ca04948bf3b22afaafa0945e9'
    TWILIO_API_SECRET = 'OJRflYurCnsilJLYmBCEXCCeBto4P5rE'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    data_from_notepad = request.form['text']
    with open('textdata.txt','w') as g:
        g.write(data_from_notepad)
    path_of_textfile = "textdata.txt"

    return send_file(path_of_textfile,as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5000', debug=True)
