import firebase_admin
from firebase_admin import credentials, messaging
from flask import Flask, request, jsonify

from creds import retailerShakti_json

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate(retailerShakti_json)
firebase_admin.initialize_app(cred)


@app.route('/send_notification', methods=['POST'])
def send_notification():
    try:
        data = request.json

        token = data.get('token')
        title = data.get('title')
        body = data.get('body')

        _android = messaging.AndroidConfig(
            priority='high'
        )

        message = messaging.Message(
            data={"title": title,
                  "message": body,
                  },

            token=token,
            android=_android
        )

        response = messaging.send(message)
        return jsonify({'success': True, 'response': response}), 200


    except messaging.UnregisteredError:
        return jsonify({'success': False, 'error': 'Unregistered token. Please refresh your FCM token.'}), 400

    except Exception as e:

        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return "<h1>HUIII</h1>"


if __name__ == '__main__':
    app.run(debug=True)
