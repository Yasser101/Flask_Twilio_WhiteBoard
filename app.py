import os
from flask_socketio import SocketIO, emit, disconnect
from flask import Flask, request, jsonify, render_template,session
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
async_mode = None
app = Flask(__name__)
fake = Faker()
socket_ = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/token')
def generate_token():
    # get credentials from environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')
    sync_service_sid = os.getenv('TWILIO_SYNC_SERVICE_SID')
    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=username)
    # create a Sync grant and add to token
    sync_grant = SyncGrant(sync_service_sid)
    token.add_grant(sync_grant)
    return jsonify(identity=username, token=token.to_jwt().decode())


@socket_.on('drawingData')
def test_message(message):
    print(message)
  #  session['receive_count'] = session.get('receive_count', 0) + 1
    emit('messagePublished',message,broadcast=True, include_self=False)


app.run(host='0.0.0.0', port=8088)