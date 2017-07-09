import socket, select, sys


def chat_conversation():
    if (len(sys.argv) < 3):
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(2)

    try:
        soc.connect((host, port))
    except:
        print 'Connection failed'
        sys.exit()

    prompt()

    while 1:
        socket_list = [sys.stdin, soc]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == soc:
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                msg = sys.stdin.readline()
                soc.send(msg)
                prompt()


def prompt():
    sys.stdout.write('<Me> ')
    sys.stdout.flush()


if __name__ == "__main__":
    chat_conversation()