import threading
import json
from peer_test_define import *
import socket
import bencodepy
from enum import Enum
from urllib.parse import urlparse
#import requests

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peer_id = 0
        self.client_socket = None
        self.file_num = 0
        self.file_list = {}

    ########################## User method (start) ##########################################
    def user_login(self):
        # User login
        peer_username = input("Username: ")
        peer_password = input("Password: ")
        # Hash login information
        peer_id = hash(peer_username + peer_password)
        return peer_id
    ########################## User method (end) ##########################################

    ######################## Protocol method (start) ######################################
    def connect_to_tracker(self, tracker_address):
        # Connect to the tracker server
        self.client_socket.connect(tracker_address)
        print(f'Connected to Tracker{tracker_address}')

    def send_request_tracker(self, info_hash, peer_id, event):
        # Send a request to the tracker
        request = bencodepy.encode({b'info_hash': info_hash, b'peer_id': peer_id, b'event': event})
        self.client_socket.send(request)

    def receive_response_tracker(self):
        # Receive the response from the tracker
        response = self.client_socket.recv(1024)
        # response_dict = bencodepy.decode(response)
        response_dict = response
        print("Response from the tracker")
        print(response_dict)
        return response_dict

    def handle_response_tracker(self, response_dict):
        # Parse the response
        status_field = response_dict[b'status']
        if status_field == b'200':
            print("Login successfully")
            return 1  # TODO: Handle information
        elif status_field == b'404':  # Wrong information of metainfo file
            print(response_dict['message'])
            return 0
        elif status_field == b'101':  # Wrong username or password
            print("Wrong username or password. Please try again")
            return 0
    ######################## Protocol method (end) ######################################

    ######################## Thread method (start) ######################################
    def leecher_check(self):
        # Todo: Một peer khác kết nối với đến máy bạn để tải file từ máy bạn.
        return

    def maintain_connection(self):
        # Todo: Máy bạn duy trì kết nối với tracker -> Cập nhật Metainfo thường xuyên (vì người dùng có thể đưa thêm 1 file torrent mới lên hệ thống)
        return

    def user_download_check(self):
        # Todo: Người dùng muốn tải một file trong các file torrent mà tracker đã cập nhật (nhớ kiểm tra xem file đó có trong self.file_list chưa)
        return

    def user_upload_check(self):
        # Todo: Người dùng tạo mới 1 file torrent từ 1 file sẵn có trong máy, sau đó cập nhật file torrent đó vào Metainfo file và self.file_list (Việc cập nhật lên server sẽ ằm ở thread maintain_connection)
        return

    ######################### Thread method (end) #######################################

    ######################### Flow method (start) #######################################
    def establish_connection(self):
        # TODO: the peer send metainfo to the tracker (Application layer Handshaking with the tracker - DatPhan)
        while True:
            # User login
            self.peer_id = self.user_login()

            # Establish connection with the tracker (send metainfo to the tracker)
            info_hash = b''
            self.send_request_tracker(info_hash, self.peer_id, 'started')
            response_dict = self.receive_response_tracker()
            if self.handle_response_tracker(response_dict) == 1:
                break

    def start(self, tracker_address):
        # Create a socket
        self.client_socket = socket.socket()

        # Bind the socket to address and port
        self.client_socket.bind((self.host, self.port))

        # Establish connection (Transport layer handshake)
        self.connect_to_tracker(tracker_address)

        # Establish connection (Application layer Handshake): The peer send metainfo to the tracker
        self.establish_connection()

        # Create 4 threads  -> leecher_check (another peer want to download your file)
        #                   -> maintain_connection (keep-alive and updating metainfo message with the tracker)
        #                   -> user_download_check: user want to download a new file  -> "start downloading" stage
        #                   -> user_upload_check: user want to upload a new torrent file to tracker
        leecher_check_thread = threading.Thread(target=self.leecher_check())
        leecher_check_thread.start()

        maintain_connection_thread = threading.Thread(target=self.maintain_connection())
        maintain_connection_thread.start()

        user_download_check_thread = threading.Thread(target=self.user_download_check())
        user_download_check_thread.start()

        user_upload_check_thread = threading.Thread(target=self.user_upload_check())
        user_upload_check_thread.start()
    ######################### Flow method (end) #######################################


if __name__ == '__main__':
    peer = Peer('localhost', 5002)
    peer.start(('localhost', 12345))
