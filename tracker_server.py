import socket
import threading
import bencodepy # type: ignore
import time
class TrackerServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.torrents = {}
        self.send_lock = threading.Lock()
        self.recv_lock = threading.Lock()   
        self.data_check = False

    def start(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_address = (self.host, self.port)
        self.server_socket.bind(server_address)

        # Listen for incoming connections
        self.server_socket.listen(5)
        print('Server is listening on {}:{}'.format(*server_address))

        # Start the client checking thread
        check_thread = threading.Thread(target=self.check_clients)
        check_thread.start()

        while True:
            # Accept a client connection
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            #DEBUG
            print(self.clients)
            #
            print('New connection from {}:{}'.format(*client_address))

            # Create a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def check_clients(self):
        while True:
            time.sleep(5)
            print(self.clients)
            for client in self.clients:
                try:
                    status = b'505'
                    response_dict = {b'status': status}
                    response = bencodepy.encode(response_dict)
                    with self.send_lock:
                        client.send(response)
                    if self.data_check == True:
                        print('Client is alive')
                    self.data_check = False
                except OSError:  # Socket is closed
                    print("Client has disconnected")
                    self.clients.remove(client)
                    continue
                # Here you can perform additional checks or operations on the client if needed

            
                    
    def handle_client(self, client_socket, client_address):
        while True:
            try:
                # Receive data from the client
                with self.recv_lock:
                    data = client_socket.recv(1024)
                if data:
                    # Decode the data
                    request = bencodepy.decode(data)
                    info_hash = request[b'info_hash']
                    peer_id = request[b'peer_id']
                    port = request.get(b'port', client_address[1])  # Use the client's port if not provided
                    event = request.get(b'event', b'').decode()  # Default to an empty string if not provided
                    if event == 'check_response':
                        self.data_check = True
                    else:
                        peer_info = {'peer_id': peer_id, 'ip': client_address[0], 'port': port}

                        if info_hash not in self.torrents:
                            self.torrents[info_hash] = []

                        if event == 'started':
                            # send list of peers in this torrent
                            if info_hash in self.torrents:
                                status = b'200'
                                response_dict = {b'status': status, b'peers': self.torrents[info_hash]}
                                response = bencodepy.encode(response_dict)
                                with self.send_lock:
                                    client_socket.send(response)
                            else:
                                status = b'404'
                                response_dict = {b'status': status, 'message': 'No peers found for this torrent'}
                                response = bencodepy.encode(response_dict)
                                with self.send_lock:
                                    client_socket.send(response)

                        if event == 'completed':
                            self.torrents[info_hash].append(peer_info)

                        if event == 'stopped':
                            if info_hash in self.torrents and peer_info in self.torrents[info_hash]:
                                self.torrents[info_hash].remove(peer_info)

            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                client_socket.close()
                self.clients.remove(client_socket)
                break

    def stop(self):
        if self.server_socket:
            self.server_socket.close()
            print('Server stopped.')

if __name__ == '__main__':
    server = TrackerServer('localhost', 12345)
    server.start()

