
import sys
import socket
import threading
from urllib import request

'''1.
We create a HEX_FILTER string that contains ASCII printable caracters of lenght = 3,
if one exsist, or (.) if such a representation dose't exist.'''

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        '''2.
        First we create a function HEX_DUMP. And first we make sure we have a string, 
        decodeing byes if bytes string was passed in.
        '''
        src = src.decode()
    
    results = list()
    for i in range(0, len(src), length):
        '''3.
        Then we grab a pice of a string to dump and put it into a WORD variable.
        We use the TRANSLATE built-in function '''
        word = str(src[i:i+length])

        '''4.
        We use the TRANSLATE built-in function to substtitute the string representation of each character
        for coresponding character in the raw string (PRINTABLE).'''

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join(f'{ord(c):02X}' for c in word)
        hexwidth = length*3
        '''5.
        We substitute the hex representation of the integer value o
        f every character in the raw string (HEXA). Finally, we create a new arraz to hold the strings,
        RESULT, that contains the hex value of the index of the first byte in the word, 
        the hex value of the word and its printable representation.cd'''
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

    if show:
        for line in results:
            print(line)
    
    else:
        return results

def receive_from(connection):
    buffer = b""
    '''1.
    For reciveing local and remote data, we pass inn the socket object.
    Create an empty byte string, BUFFER,  that will accumulate responses from the socket.
    '''
    connection.settimeout(5)    # by defoult 5 sec time-out, incraes as necessary
    try:
        while True:
            '''2.
            We set up a loop to read response data into the buffer until there's no more data or we time-out
            '''
            data = connection.recv(4096)
            if not data:
                break
            buffer += data

    except Exception as e:
        pass
    return buffer   #Finnaly we return the BUFFER byte string to the caller, which could be either the local or remote machine
    
def request_handler(buffer):
    # Perform packet modification
    return buffer

def response_handler(buffer):
    # Perform packet modification
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes from localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to local host.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closeing connections.")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    '''1.
    The SERVER_LOOP function create a socket'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        '''2.
        And then binds to the local host and listen'''
        server.bind((local_host, local_port))
    except Exception as e:
        print('problem on bind: %r' % e)

        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)

    '''3.
    When fresh connection request comes in, we hand it off to the PROXY_HANDLER in new thred, 
    which dose all of the sending and reciveing of bits to either side of data stream.'''
    while True:
        client_socket, addr = server.accept()
        # print out local connection information 
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        # start a thred to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py[localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py xxx.xxx.xxx.xxx 9000 xxx.xxx.xxx.xxx 9000 True") # Replace x-es with IP addresses
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()






    

