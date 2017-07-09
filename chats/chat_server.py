import select
import connection

connections, socket_server, receiver = connection.server_connection()


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
                    data = sock.recv(receiver)
                    if data:
                        broadcast_data(sock, "\r" + '<Friend> ' + data)
                except:
                    broadcast_data(sock, "Friend is offline")
                    sock.close()
                    connections.remove(sock)
                    continue

    socket_server.close()


def broadcast_data(sock, message):
    for socket in connections:
        if socket != socket_server and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                connections.remove(socket)


if __name__ == "__main__":
    chat_conversation()

