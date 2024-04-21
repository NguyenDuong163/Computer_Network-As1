
import socket
import threading
import bencodepy
import time
import pandas as pd

class Tracker:
    def __init__(self, port, host):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.torrents = {}

    def start(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_address = (self.host, self.port)
        self.server_socket.bind(server_address)

        # Listen for incoming connections
        self.server_socket.listen(5)
        print('Server is listening on {}:{}'.format(*server_address))

        while True:
            # Accept a client connection
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            print('New connection from {}:{}'.format(*client_address))

            # Create a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        data = client_socket.recv(1024)
        if data:
            # Decode the data
            request = bencodepy.decode(data)
            info_hash = request[b'info_hash']
            peer_id = request[b'peer_id']
            port = request.get(b'port', client_address[1])  # Use the client's port if not provided
            event = request.get(b'event', b'').decode()  # Default to an empty string if not provided

            peer_info = {'peer_id': peer_id, 'ip': client_address[0], 'port': port}

            # Create new element (for current info_hash)
            if info_hash not in self.torrents:
                self.torrents[info_hash] = []

            if event == 'init':
                # Todo: The peer send metainfo to the tracker
                return 0
            elif event == 'started':
                # Todo: The peer send info_hash of a torrent file to the tracker
                # send list of peers in this torrent
                if info_hash in self.torrents:
                    status = b'200'
                    response_dict = {b'status': status, b'peers': self.torrents[info_hash]}
                    response = bencodepy.encode(response_dict)
                    client_socket.send(response)
                else:
                    status = b'404'
                    response_dict = {b'status': status, 'message': 'No peers found for this torrent'}
                    response = bencodepy.encode(response_dict)
                    client_socket.send(response)
            elif event == 'completed':
                self.torrents[info_hash].append(peer_info)
            elif event == 'stopped':
                if info_hash in self.torrents and peer_info in self.torrents[info_hash]:
                    self.torrents[info_hash].remove(peer_info)