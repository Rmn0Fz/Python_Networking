# Standard multythreaded TCP server

import socket
import threading

IP = "0.0.0.0"
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))  
    '''1.
    We pass the IP address and port we want server to listen on..
    '''
    server.listen(5)  
    '''2.
    We tell server to start listening, with max back log of connection set to 5
    '''
    print(f'[*] Listening on {IP}:{PORT}')

    '''3.
    Server is is in main loop, waiting for an incoming connection.
    We recive a client socket in the CLIENT VARIABLE and remote connection details
    in the ADDRESS variable. We then create a new thread object that points to our 
    HANDLE_CLIENT function, and we pass a client socket as argument.
    '''
    while True:
        client, addres = server.accept() 
        print(f"[*] Accepted connection from {addres[0]}:{addres[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start() #START
        '''4.
        We then #STARTthe thread to handle the client connection,
        and at that point server is ready to handle another incoming connection. 
        '''

def handle_client(client_socket):
    '''5.
    The HANDLE_CLIENT function preforms the recv() and sends 
    a simple mesage back to the client..
    '''
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Recived: {request.decode('utf-8')}")
        sock.send(b"ACK")

if __name__=='__main__':
    main()

