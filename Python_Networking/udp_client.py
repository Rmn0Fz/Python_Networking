# Simple UDP client

import socket

target_host = "xxx.xxx.xxx.xxx"
target_port = 9997

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

''' 1.
We just change socket type -> SOCK_DGRAM..
Same as the TCP.
'''

# Send some datat
client.sendto(b"AAABBBCCC", (target_host, target_port))

''' 2.
Passing in the data and server you want to send data to.
UDP -> conectionless protocol..
'''

# Recive some data
data, addr = client.recvfrom(4096)

''' 3.
Recive UDP data back..
Returns -> the data and details of the remote host and port..
'''

print(data.decode())
client.close()
