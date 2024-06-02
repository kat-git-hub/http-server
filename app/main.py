import socket
import os
import sys

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--directory':
        print("Usage: ./your_server.sh --directory <directory>")
        return

    directory = sys.argv[2]

    server_socket = socket.create_server(("0.0.0.0", 4221))
    #server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()

    while True:
        client, _ = server_socket.accept()
        with client:
            request = client.recv(1024).decode("utf-8")
            lines = request.split("\r\n")
            if not lines:
                continue

            request_line = lines[0]
            parts = request_line.split()
            if len(parts) < 3:
                continue
            method, path, _ = parts


            if method != 'GET':
                response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode()
                client.sendall(response)
                continue


            if path.startswith("/files/"):
                filename = path[len("/files/"):]
                file_path = os.path.join(directory, filename)

                if os.path.isfile(file_path):

                    with open(file_path, 'rb') as file:
                        content = file.read()
                    content_length = len(content)
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/octet-stream\r\n"
                        f"Content-Length: {content_length}\r\n\r\n"
                    ).encode() + content
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

            client.sendall(response)


if __name__ == "__main__":
    main()
