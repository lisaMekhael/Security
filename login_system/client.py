import socket

SERVER_IP = 'fe80::5927:1fff:1810:258d%7'
SERVER_PORT = 5678

username = input('Enter your username: ')
password = input('Enter your password: ')
msg = input('If you are trying to sign up enter 1, if you are trying to login enter 2: ')

if msg == "1":
    info = f"{{sign up, {username}, {password}}}"
elif msg == "2":
    info = f"{{login, {username}, {password}}}"
else:
    info = "Invalid input."

print(info)

info_byte = info.encode()


with socket.socket(socket.AF_INET6 , socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))
    data = s.recv(1024)
    print(data)
    s.send(info_byte)
    result = s.recv(1024)
    print(result)




