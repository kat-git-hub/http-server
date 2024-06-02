import socket
import threading
import sys
import os

def main():
    def handle_req(client, addr):
        data = client.recv(1024).decode()
        req = data.split('\r\n')
        request_line = req[0].split(" ")
        method = request_line[0]
        path = request_line[1]

        if method == "GET":
            if path == "/":
                response = "HTTP/1.1 200 OK\r\n\r\n".encode()  
            elif path.startswith('/echo'):
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
            elif path.startswith("/user-agent"):
                user_agent = req[2].split(": ")[1]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
            elif path.startswith("/files"):
                directory = sys.argv[2]
                filename = path[7:]
                try:
                    with open(os.path.join(directory, filename), "r") as f:
                        body = f.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                except Exception as e:
                    response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        elif method == "POST" and path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[7:]
            content_length = 0
            for line in req:
                if line.startswith("Content-Length"):
                    content_length = int(line.split(": ")[1])
                    break

            body_start = data.index("\r\n\r\n") + 4
            body = data[body_start:body_start+content_length]

            try:
                with open(os.path.join(directory, filename), "w") as f:
                    f.write(body)
                response = "HTTP/1.1 201 Created\r\n\r\n".encode()
            except Exception as e:
                response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
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