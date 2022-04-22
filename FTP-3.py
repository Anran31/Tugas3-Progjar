import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 21))

commands = ['USER anran\r\n', 'PASS progjarasik\r\n',
            'TYPE I\r\n', 'PASV\r\n', 'MLSD\r\n', 'QUIT\r\n']
i = 0
while True:
    try:
        if i == len(commands):
            msg = str(s.recv(4096).decode('utf-8'))
            # print(msg.strip())
            s.close()
            break
        s.send(commands[i].encode('utf-8'))
        i += 1
        msg = str(s.recv(4096).decode('utf-8'))
        # print(msg.strip())

        if "Entering Passive Mode" in msg:

            str_ports = msg.split('\r\n')[0].strip()

            ports = [int(x) for x in str_ports.strip().split()
                     [-1].strip('()').split(',')[-2:]]

            data_port = ports[0] * 256 + ports[1]
            data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_sock.connect(('localhost', data_port))
            s.send(commands[i].encode('utf-8'))
            i += 1
            data = data_sock.recv(4096).decode('utf-8')
            while data:
                list_data = data.split('\r\n')[:-1]
                file_list = [' '.join(x.split()[1:]) for x in list_data]
                print('\n'.join(file_list))
                data = data_sock.recv(4096).decode('utf-8')

    except socket.error:
        s.close()
        break
