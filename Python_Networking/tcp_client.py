# Simple TCP client

import socket

target_host = "xxx.xxx.xxx.xxx"
target_port = 9998

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

''' 1.
Frst create a socket object -> 
AF_INET -> indicate use of standard IPv4 address or hostname
SOCK_STREAM -> indicate that will be TCP client
'''
# Connect the client
client.connect((target_host, target_port))

''' 2.
Then connect the client to the server 
and send it some data as bytes
'''

# Send some data
client.send(b"GET / HTTP/1.1\r\n\tHost: google.com\r\n\r\n") # Ex
# Recive some data
response = client.recv(4096)

''' 3.
The last step is to recive some data back 
and print out the response..
'''

print(response.decode())
client.close()
''' 4.
..and close the socket..
'''

