import json
import flask
from flask import Flask
from sqlalchemy.sql import and_
from flask import request
import connection
import sqlalchemy as sql
from time import gmtime, strftime

app = Flask(__name__)


@app.route("/chat",  methods=['GET', 'POST', 'PUT'])
def chats():
    if request.method == 'POST':
        payload = request.get_data()
        data = json.loads(payload)

        validation = validate_payload(data)

        if validation == 'valid':
            username = data['username']
            msg = data['message']
            msg_to = data['messageto']
        else:
            return validation
        try:
            query = connection.ChatTable.insert().values(
                username=username,
                message=msg,
                messageto=msg_to,
                creationdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
            )
            result = connection.sql_query_to_insert(query)
            response = "chat saved"
        except:
            response = "chat not saved"

        return response

    elif request.method == 'PUT':
        payload = request.get_data()
        print('payload', payload)
        data = json.loads(payload)

        validation = validate_payload(data)

        if validation == 'valid':
            username = data['username']
            message = data['message']
            _id = data['id']
        else:
            return validation

        select_query = sql.select([connection.ChatTable.c.creationdate, connection.ChatTable.c.username,
                            connection.ChatTable.c.message, connection.ChatTable.c.messageto]), and_(
            connection.ChatTable.c.username == username, connection.ChatTable.c.id == _id)
        result = connection.sql_query_get_one_chat(select_query)

        if len(result) > 0:

            query = connection.ChatTable.update().values(
                message=message
            ).where(connection.ChatTable.c.username == username, connection.ChatTable.c.id == id)
            result = connection.sql_query_to_insert(query)

            return 'message updated'
        else:
            return 'user is not allowed to update this record'

    elif request.method == 'GET':
        payload = request.get_data()
        data = json.loads(payload)

        user1 = data['user1']
        user2 = data['user2']

        if user1 and user2 != '' or None:
            # query = sql.select([connection.ChatTable.c.creationdate, connection.ChatTable.c.username,
            #                     connection.ChatTable.c.message, connection.ChatTable.c.messageto]).where(
            #     connection.ChatTable.c.username in (user1, user2) and connection.ChatTable.c.messageto in
            #     (user1, user2)).order_by(sql.desc(connection.ChatTable.c.creationdate))
            query = """SELECT * FROM chat.chat where username in ('{}','{}') and messageto in
             ('{}','{}') order by creationdate desc""".format(user1,user2,user1,user2)
            result = connection.sql_query_get_all_chat(query)

            #get the last 6 chats
            if len(result) > 6:
                data = result[:6]
                last_chat = sorted(data, key=lambda x: x[1])
            elif len(result) == 0:
                last_chat = result
            else:
                last_chat = sorted(result, key=lambda x: x[1])

            return str(last_chat)
        else:
            return 'provide two chat users'


# Validate user given parameters
def validate_payload(data):
    try:
        if 'username' in data and 'message' in data and 'messageto' in data:
            if data['username'] is None or data['username'] == '':
                message = 'User name is required.'
                return message

            elif data['message'] is None or data['message'] == '':
                message = 'Message is required.'
                return message
            elif data['messageto'] is None or data['messageto'] == '':
                message = 'Message to is required.'
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