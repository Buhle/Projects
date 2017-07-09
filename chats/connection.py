import socket
import sqlalchemy as sql
from sqlalchemy import exc

# SQL Connections
engine = sql.create_engine('mysql+pymysql://chat:246B883af{@^31@c0b2479@127.0.0.1:3306/chat', echo=False)
conn = engine.connect()
metadata = sql.MetaData()


def server_connection():
    connections = []
    receiver = 4096
    port = 8080

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind(("0.0.0.0", port))
    socket_server.listen(10)

    connections.append(socket_server)

    return connections, socket_server, receiver

# Create Database
# conn.execute("CREATE DATABASE IF NOT EXISTS chat")
# conn.execute("Use chat")

# Table for saving chats
ChatTable = sql.Table('chat', metadata,
                    sql.Column('id', sql.Integer, primary_key=True),
                    sql.Column('creationdate', sql.DateTime),
                    sql.Column('username', sql.String(250)),
                    sql.Column('message', sql.String(250)),
                  )

metadata.create_all(engine)


# Method for inserting to chat table
def sql_query_to_insert(query):
    try:
        conn = engine.connect()
        conn.execute(query)
        conn.close()
    except:
        return 'Data was not saved'

    return 'Ok'


# Get all chats for specified user
def sql_query_get_chat(query):
    try:
        conn = engine.connect()
        result = conn.execute(query).fetchall()
        conn.close()
    except exc.DBAPIError as e:
        # an exception is raised, Connection is invalidated.
        if e.connection_invalidated:
            print("Connection was invalidated!")

    # after the invalidate event, a new connection start
    # starts with a new Pool
    conn = engine.connect()
    result = conn.execute(query).fetchall()

    return result

