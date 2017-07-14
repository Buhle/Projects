import json
import select

import requests

import connection

connections, socket_server, receiver = connection.server_connection()
base_url = 'http://localhost:5000'


def chat_conversation():
    while 1:
        read_sockets, write_sockets, error_sockets = select.select(connections, [], [])

        for sock in read_sockets:
            if sock == socket_server:
                sockfd, addr = socket_server.accept()
                connections.append(sockfd)

                broadcast_data(sockfd, "Friend is online\n")
            else:
                try:
                    sock_id = sock.getpeername()[1]
                    message = sock.recv(receiver)
                    if message:
                        broadcast_data(sock, "\r" + '<' + str(sock_id) + '> ' + message)
                except:
                    broadcast_data(sock, "Friend is offline\n")
                    sock.close()
                    connections.remove(sock)
                    continue

    socket_server.close()


def broadcast_data(sock, message):
    username = '12345'
    for socket in connections:
        if socket != socket_server and socket != sock:
            try:
                payload = {'username': username, 'message': message}
                r = requests.post(base_url + '/chat', data=json.dumps(payload))

                if r.text == 'chat saved':
                    socket.send(message)
                else:
                    try:
                        r = requests.post(base_url + '/chat', data=json.dumps(payload))
                        socket.send(message)
                    except:
                        socket.send(message)
            except:
                socket.close()
                connections.remove(socket)


if __name__ == "__main__":
    chat_conversation()
