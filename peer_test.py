import threading
import json
from peer_test_define import *
import socket
from enum import Enum
from urllib.parse import urlparse
#import requests

class PeerEstablishState(Enum):
    INIT = 1
    LOGIN = 2
    PUBLISH = 3


class PeerState(Enum):
    HANDSHAKE = 1
    INTEREST = 2
    CHOKE = 3
    UNCHOKE = 4
    PIECE_REQUEST = 5

# Tracker information
tracker_host = ""
tracker_port = 0

# Peer information
peer_host = ""
peer_port = 0   # Default: 5000

# Description: get <Host> of the URL
def get_host_url(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

# Description: get <Port> of the URL
def get_port_url(url):
    parsed_url = urlparse(url)
    return parsed_url.port

# Description: Get IP of local machine
def get_host_name():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Description:  The peer send HTTP request to the tracker to establish connection
# Parameter:    + tracker_url: URL of the tracker
#               + metainfo: Send hashed Metainfo string to the tracker
#               + login_data: hashed login information
# Flow          The peer sends login_info to tracker -> The tracker responses "accept/decline"
#               If (tracker_accept):
#                   the peer publishes "metainfo" to the tracker
#               else
#                   the peer must correct username and password and resend login_info
# Why we need the login mechanism: -> The tracker stores "Downloading/Uploading" amount of each peer
def peer_init(tracker_url, metainfo):
    global tracker_host
    global tracker_port
    peer_state = PeerEstablishState.INIT
    # Login
    peer_username = input("Username: ")
    peer_password = input("Password: ")
    # Hash login information
    hashed_login_info = hash(peer_username + peer_password)
    # Get Host/Port from tracker_address
    tracker_host = get_host_url(tracker_url)
    tracker_port = get_port_url(tracker_url)
    # Generate Peer Host/Port
    peer_host = get_host_name()
    peer_port = PEER_DEFAULT_PORT
    peer_socket = socket.socket()
    peer_socket.bind((peer_host, peer_port))
    # Establish connection
    peer_socket.connect((tracker_host, tracker_port))
    # Todo: Send login information (hashed_login_info) to the tracker (via HTTP protocol)

    print(hashed_login_info)
    # print(peer_port)


def get_topic(message):
    return message[TOPIC_KEY]

def get_addr(message):
    return message[HEADER_KEY][PEER_HOST_KEY]


def get_filename(message):
    return message[HEADER_KEY][FILE_NAME_KEY]

# Description: User want to download 1 file from Torrent (event from user)
# Parameter:    + tracker_host
#               + tracker_port
#               + file_info: Information of the file
# Flow          -> Send the file_name.torrent to tracker
#               -> Receive a peer_list from the tracker
#               -> Create a table about progresses of all pieces (see a table in BTL1 pg.2)
#               -> Create multi-threading to process all seeder in the list
#               -> If a piece of a thread is completed -> update the progress table -> Find another "pending" piece in table -> Continue new transaction
#               -> If a seeder is disconnected -> Delete piece file of the seeder from computer -> Change state of the piece to "pending" state
#               |    Piece Number   |       State           |
#               |       Piece 1     |       Completed       |
#               |       Piece 2     |       Processing      |
#               |       Piece 3     |       Pending         |
#               | ..............    |   ................    |
#               * This table is stored in the torrent file `.torrent`. when a file is uncompleted (some pieces are uncompleted), the application will continue leecher process
#
#               -> When all pieces are completed -> Merge all pieces -> State to the tracker
#               -> End the thread
def handle_seeder(tracker_host, tracker_port):


    return 1

# Description:  A peer from another machine who wants to download my file
# Parameters:   + leecher_socket
#               + address
def handle_leecher(leecher_socket, address):
    print(f"Leecher is connecting from {address}")
    # Initial state
    seeder_state = PeerState.HANDSHAKE
    while True:
        leecher_packet = leecher_socket.recv(1024)

        if not leecher_packet:
            break
        # Todo: Response case
        if seeder_state == PeerState.HANDSHAKE:
            # Todo: Handshaking response
            break
        elif seeder_state == PeerState.INTEREST:
            # Todo: Interest from leecher
            break
        elif seeder_state == PeerState.CHOKE:
            # Todo:
            break
















packet = {
    "TOPIC": "DOWLOADING",
    "HEADER": {
        "Source Address": "1:1:1:1",
        "Source Port"
        "FileName": "YourCV.pdf"
    },
    "BODY": {
        "Connection information to FTP server": "abcdef"
    }
}

#peer_init(TRACKER_URL, "a")
