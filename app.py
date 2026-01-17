import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify

app = Flask(__name__)

cred = credentials.Certificate("/etc/secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

@app.route('/login', methods=['POST'])
def give_status():

    data = request.get_json()

    if not data or "uid" not in data or "role" not in data:
        return jsonify({"error": "uid and role required"}), 400

    uid = data["uid"]
    role = data["role"]

    if not uid:
        return jsonify({"error": "uid cannot be empty"}), 400

    if role == "user":
        auth.set_custom_user_claims(uid, {"admin": False})

    elif role == "admin":
        club_name = data.get("club-name", "unknown")
        auth.set_custom_user_claims(uid, {
            "admin": True,
            "club-name": club_name
        })

    else:
        return jsonify({"error": "Invalid role"}), 400

    print(f"{role} role assigned to {uid}")

    return jsonify({
        "success": True,
        "role": role
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
