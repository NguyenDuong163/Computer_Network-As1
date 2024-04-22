import socket
import tqdm
import os

def send_file(dest_host, dest_port, file_path):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step

    # Receiver IP address
    host = dest_host

    # Receiver port
    port = dest_port

    # the name of file we want to send
    filename = os.path.basename(file_path)  #Send all file types but, not in directory \User (causes error)

    # get the file size
    # filesize = os.path.getsize(file_path)
    filesize = 1
    # create the client socket
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file

    with open(file_path, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
    # close the socket
    s.close()

dest_host = '10.0.244.129'    # 10.0.227.150
dest_port = 5000
file_path = "D:\\Design_Specification_Template.docx"

send_file(dest_host,dest_port,file_path)