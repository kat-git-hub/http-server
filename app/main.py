import socket
import threading
import sys
import os

def main():
    def handle_req(client, addr):
        data = client.recv(1024).decode()
        req = data.split('\r\n')
        method, path, _ = req[0].split(" ")
        if method == "GET" and path.startswith("/files/"):
            filename = path.split('/')[-1]
            directory = sys.argv[2]
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as f:
                        body = f.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                except Exception as e:
                    response = "HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        client.send(response)
        client.close()

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:    
        client, addr = server_socket.accept()
        threading.Thread(target=handle_req, args=(client, addr)).start()

if __name__ == "__main__":
    main()
