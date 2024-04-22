import socket
import tqdm
import os

class Server:
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096  # receive 4096 bytes each time

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket()  # TCP socket
        self.server_socket.bind((self.host, self.port))

    def start(self):
        self.server_socket.listen(5)  # enable the server to accept connections
        print(f"[*] Listening as {self.host}:{self.port}")
        self.client_socket, self.address = self.server_socket.accept()  # accept connection if there is any
        print(f"[+] {self.address} is connected.")

    def receive_file(self):
        received = self.client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        filename = os.path.basename(filename)  # remove absolute path if there is
        filesize = int(filesize)  # convert to integer

        with open(filename, "wb") as f:
            while True:
                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                if not bytes_read:    
                    break  # file transmitting is done
                f.write(bytes_read)  # write to the file the bytes we just received

    def close_connection(self):
        self.client_socket.close()
        self.server_socket.close()

# usage
server = Server("10.0.244.129", 5000)
server.start()
server.receive_file()
server.close_connection()
