# from firebase_admin import messaging, credentials
# import firebase_admin
# from flask import Flask
#
# app = Flask(__name__)
#
# # Initialize Firebase Admin SDK
# cred = credentials.Certificate('retailershakti-delivery-firebase-adminsdk-2k5kk-200e125f93.json')
# firebase_admin.initialize_app(cred)
#
#
# @app.route('/send_notification', methods=['GET'])
# def send_notification():
#     registration_token = "cblHmrdWSpqt2bQoIuyFw_:APA91bF4i1UWeWBMTGdxVLZYWU_EjFuqxOxvG4zEZaL7IzkG1U0TsCm2ToHrVIw7lceVpVHOolcnl74v2q01rDW1WnbOyFrLuAtkg7c2HsEIaonTIr-fKPw"
#
#     _aps = messaging.Aps(
#         sound="default",
#         badge=1,
#         mutable_content=True,
#         content_available=True
#     )
#     _apsPayload = messaging.APNSPayload(aps=_aps)
#
#     _apns = messaging.APNSConfig(payload=_apsPayload)
#
#     _android = messaging.AndroidConfig(
#         priority='high'
#     )
#
#     message = messaging.Message(
#         data={"title": "Sample Title",
#               "message": "This is the main message body",
#               },
#         # apns=_apns,
#         token=registration_token,
#         android=_android
#     )
#     print(f"Onion_msg--- {message}")
#     # Send the message
#     response = messaging.send(message)
#     print(f"Onion_response---{response} {message}")
#     return 'Notification sent: ' + response
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


import firebase_admin
from firebase_admin import credentials, messaging
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate("retailershakti-6527c-firebase-adminsdk-cdj19-a7f6d3304e.json")
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
