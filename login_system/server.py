import socket
import secrets
import hashlib
import csv
SERVER_IP = 'fe80::5927:1fff:1810:258d%7'
SERVER_PORT = 5678

hash_dictionary = {}
file_path = 'C:/Users/lilia/Videos/security_database.csv'
auth = False

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn, addr = s.accept()
    print(f'Connection accepted from :{addr}')
    with conn:
        while (True):
            conn.send(b'Welcome')
            data = conn.recv(1024)
            print(data)
            data_str = data.decode()

            msg = data_str.split(',')
            input_password = msg[2].strip('}')
            print(input_password)
            input_username = data_str.split(',')[1].strip()
            print(input_username)
            if (data_str.split(',')[0].strip() == '{sign up'):
                salt = secrets.token_hex(16)
                salted_password = input_password + salt
                hashed_password = hashlib.sha512(str(salted_password).encode("utf-8")).hexdigest()
                data = [input_username ,salt, hashed_password]
                print(data)
                with open(file_path , 'a' , newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)
                print('signed in successfully')
                conn.send(b' signed up successfully')

            elif (data_str.split(',')[0].strip() == '{login'):
                print("log in")
                with open(file_path , 'r') as file:
                    reader = csv.reader(file)
                    for line in reader:
                        csv_username = line[0]
                        if(csv_username == input_username):
                            csv_salt = line[1]
                            salt_password = input_password + csv_salt
                            hashed_password = hashlib.sha512(str(salt_password).encode("utf-8")).hexdigest()
                            if(hashed_password==line[2]):
                                print("true")
                                conn.send(b'authenticated')
                            else:
                                print("false")
                                conn.send(b'not authenticated')

            break