import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 21))

commands = ['USER anran\r\n', 'PASS progjarasik\r\n', 'QUIT\r\n']
i = 0
while True:
    try:
        if i == len(commands):
            msg = str(s.recv(1024).decode('utf-8'))
            # print(msg.strip())
            break

        s.send(commands[i].encode('utf-8'))
        msg = str(s.recv(1024).decode('utf-8').split('\r\n')[0])
        if not i:
            ftp_server = msg.split('-')[1]
            print(ftp_server)
        i += 1

    except socket.error:
        s.close()
        break
