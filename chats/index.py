import json

import flask
from flask import Flask
from flask import jsonify
from flask import request
import connection

app = Flask(__name__)


@app.route("/chat",  methods=['GET', 'POST'])
def chats():
    print('here')
    if request.method == 'POST':
        payload = request.get_data()
        data = json.loads(payload)

        validation = validate_payload(data)
        print(validation, '.......')
        if validation == 'valid':
            username = data['username']
            msg = data['message']
        else:
            return validation
        try:
            query = connection.ChatTable.insert().values(
                username=username,
                message=msg
            )
            # result = connection.sql_query_to_insert(query)
            response = "chat saved"
        except:
            response = "chat not saved"

        return response
    else:
        json_data = {"message": 'GET method'}
        return flask.jsonify(**json_data)


# Validate user given parameters
def validate_payload(data):
    try:
        if 'username' in data and 'message' in data:
            if data['username'] is None or data['username'] == '':
                message = 'User name is required.'
                return message

            elif data['message'] is None or data['message'] == '':
                message = 'Message is required.'
                return message
        else:
            message = 'Incorrect values supplied.'
            return message
    except:
        message = 'Something went wrong.'
        return message

    message = 'valid'
    return message


def response(message):
    resp = flask.make_response(json.dumps(message))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run(threaded=True, debug=True, host='0.0.0.0', port=5000)