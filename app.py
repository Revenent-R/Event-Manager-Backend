import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app)

@app.route('/login', methods=['POST'])
def give_status():

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    data = request.get_json()

    uid = data['uid']
    if uid == "" :
        return

    if data['role'] == 'user':
        auth.set_custom_user_claims(uid, {'admin': False})
    elif data['role'] == 'admin':
        auth.set_custom_user_claims(uid, {'admin': True,'club-name':data['clubName']})
    print(f"{data['role']} role assigned")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
