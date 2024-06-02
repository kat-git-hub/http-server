import socket
import os
import sys

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--directory':
        print("Usage: ./your_server.sh --directory <directory>")
        return

    directory = sys.argv[2]

    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()

    while True:
        client, _ = server_socket.accept()
        with client:
            request = client.recv(1024).decode("utf-8")
            lines = request.split("\r\n")
            if not lines:
                continue
            _, path, _ = lines[0].split()

            if path.startswith("/files/"):
                filename = path[len("/files/"):]
                file_path = os.path.join(directory, filename)

                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        content = file.read()
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/octet-stream\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                    ).encode() + content
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

            client.sendall(response)
            client.close()

if __name__ == "__main__":
    main()
