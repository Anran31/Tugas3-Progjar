import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 21))

commands = ['USER anran\r\n', 'PASS progjarasik\r\n', 'TYPE A\r\n', 'PASV\r\n',
            'STOR Bangkit Re-registration.PNG\r\n', 'QUIT\r\n']
i = 0
while True:
    try:
        if i == len(commands):
            msg = str(s.recv(1024).decode('utf-8'))
            print(msg.strip())
            break

        s.send(commands[i].encode('utf-8'))
        msg = str(s.recv(1024).decode('utf-8'))
        print(msg.strip())

        if "Entering Passive Mode" in msg:
            str_ports = msg.split('\r\n')[0].strip()
            msg = str(s.recv(1024).decode('utf-8'))
            print(msg.strip())

            ports = [int(x) for x in str_ports.strip().split()
                     [-1].strip('()').split(',')[-2:]]

            data_port = ports[0] * 256 + ports[1]
            data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_sock.connect(('localhost', data_port))

            file_name = ' '.join(commands[4].strip('\r\n').split()[1:])
            file_path = os.path.join(os.getcwd(), file_name)

            with open(file_path, 'rb') as file:
                while True:
                    bytes_read = file.read(4096)
                    if not bytes_read:
                        break
                    data_sock.sendall(bytes_read)
                file.close()
            data_sock.close()
            msg = str(s.recv(1024).decode('utf-8'))
            print(msg.strip())

        i += 1

    except socket.error:
        s.close()
        break
