import socket
import threading
import sys
import os

def main():
    def handle_req(client, addr):
        data = client.recv(1024).decode()
        req = data.split('\r\n')
        method, path, _ = req[0].split(" ")
        if method == "POST" and path.startswith("/files/"):
            filename = path.split('/')[-1]
            content_length = 0
            for line in req:
                if line.startswith("Content-Length:"):
                    content_length = int(line.split(":")[1].strip())
                    break
            if content_length > 0:
                body = data.split("\r\n\r\n")[1]
                directory = sys.argv[2]
                file_path = os.path.join(directory, filename)
                try:
                    with open(file_path, "w") as f:
                        f.write(body)
                    response = "HTTP/1.1 201 Created\r\n\r\n".encode()
                except Exception as e:
                    response = "HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 400 Bad Request\r\n\r\n".encode()
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
