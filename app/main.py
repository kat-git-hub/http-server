# Uncomment this to pass the first stage
import socket
import threading


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()

    while True:
        client, _ = server_socket.accept()
        with client:
            request = client.recv(1024).decode("utf-8")
            lines = request.split("\r\n")
            _, path, _ = lines[0].split()
            
            if path == "/":
                response = "HTTP/1.1 200 OK\r\n\r\n"
            elif path.startswith("/echo/"):
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
            elif path.startswith("/user-agent"):
                user_agent = "User-Agent header not found"
                for line in lines:
                    if line.startswith("User-Agent:"):
                        user_agent = line.split(": ", 1)[1]
                        break
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
            
            client.sendall(response.encode())
            client.close()


if __name__ == "__main__":
    main()
