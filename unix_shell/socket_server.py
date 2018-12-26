import socket

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

local_hostname = socket.gethostname()
ip_address = socket.gethostbyname(local_hostname)
print(f"working on {local_hostname} ({socket.getfqdn()}) with {ip_address}")
server_address = (ip_address, 23456)
print(f'starting up on {server_address} port 23456')
sock.bind(server_address)
# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print ('connection from', client_address)
        while True:
            data = connection.recv(64)
            if data:
                print(f'Data: {data}')
                # send on the connected socket, not the listening socket
                connection.send('Thanks client, server received'.encode('utf-8'))
            else:
                print("no more data.")
                break
    finally:
        connection.close()