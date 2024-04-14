import socket
import threading

server_list = [5000, 5001, 5002]

class RoundRobin:
    def __init__(self, server_list):
        self.servers = server_list
        self.current_index = 0

    def get_next_server(self):
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server

roundRobin = RoundRobin(server_list)
threads = []

class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def ForwardRequestToBackend(self, request, host, port, client_sock):
        be_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            be_socket.connect((host, port))
        except:
            client_sock.close()
            return
        be_socket.send(request.encode())
        while True:
            headers, body = be_socket.recv(4096), be_socket.recv(4096)
            if not body or headers:
                break

        print(f"Response from Server: {headers.decode().splitlines()[0]}")
        print(body.decode())

        response = headers + body
        client_sock.send(response)

        client_sock.close()

    def createSocket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)

        while True:
            client, address = server.accept()
            request = client.recv(4096).decode()
            if not request:
                break
            print(f"\nReceived request from {address[0]}")
            print(request)

            # Forward request to backend server
            newThread = threading.Thread(target=self.ForwardRequestToBackend, args=(request, 'localhost', roundRobin.get_next_server(), client))
            newThread.start()
            threads.append(newThread)

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    print("Load Balancer running on port 8888")
    lb_server = Socket('localhost', 8888)
    lb_server.createSocket()