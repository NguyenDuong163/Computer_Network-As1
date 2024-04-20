import socket
import bencodepy # type: ignore
import json

def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the tracker server
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    print('Connected to {}:{}'.format(*server_address))

    # Send a request to the tracker
    info_hash = b'a\t\xc6\xb4LV\x04\x8a\x83\xaeM\x06W\\\x8d:\x87{i\xeb'
    peer_id = b'\xd5\xb4\xf3\xdf\x1e){\xb0C*r\xe7\xfe\xdc\xbd\xb6J\xc0\x96\x1b'
    event = b'started'  # Add the event field

    request = bencodepy.encode({b'info_hash': info_hash, b'peer_id': peer_id, b'event': event})
    client_socket.send(request)

    # Receive the response from the tracker
    response = client_socket.recv(1024)
    response_dict = bencodepy.decode(response)
    
    if response_dict[b'status'] == b'200':
        print('Received list of peers from tracker:', response_dict[b'peers'])
    else:
        print('Error:', response_dict[b'message'])

if __name__ == '__main__':
    main()