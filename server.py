import socket, threading

host = '127.0.0.1'
port = 7973

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f'Server started listening on localhost:{port}')
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left!'.encode('ascii'))
            print(f'{nickname} disconnected')
            nicknames.remove(nickname)
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            client.send('NICKNAME'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)
            print(f'{nickname} connected with {address}')      
            broadcast(f'{nickname} joined!'.encode('ascii'))
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            server.close()

receive()