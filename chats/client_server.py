import json
import socket, select, sys
import requests


base_url = 'http://localhost:5000'


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
    msg = ''
    prompt(msg)

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
                    msg = sys.stdout.write(data)
                    prompt(msg)
            else:
                msg = sys.stdin.readline()
                soc.send(msg)
                prompt(msg)


def prompt(message):
    username = '24680'
    try:
        payload = {'username': username, 'message': message}
        r = requests.post(base_url + '/chat', data=json.dumps(payload))

        if r.text == 'chat saved':
            sys.stdout.write('<Me>')
            sys.stdout.flush()
        else:
            try:
                r = requests.post(base_url + '/chat', data=json.dumps(payload))
                sys.stdout.write('<Me>')
                sys.stdout.flush()
            except:
                sys.stdout.write('<Me>')
                sys.stdout.flush()
    except:
        print('something went wrong')


if __name__ == "__main__":
    chat_conversation()