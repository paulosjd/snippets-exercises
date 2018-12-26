import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

local_hostname = socket.gethostname()
local_fqdn = socket.getfqdn()
ip_address = socket.gethostbyname(local_hostname)
server_address = (ip_address, 23456)
sock.connect(server_address)  
print(f'connecting to {local_hostname} ({local_fqdn}) with {ip_address}')

# define example data to be sent to the server
temperature_data = ["15", "22", "21", "26", "25", "19"]  
for entry in temperature_data:  
    print(f'data: {entry}')
    new_data = str(f"temp: {entry}\n").encode("utf-8")
    sock.sendall(new_data)
    time.sleep(2)
    data = sock.recv(1024)
    print(f'Server message: {data}')
    time.sleep(1)
sock.close()

