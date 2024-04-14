import socket
import threading
import requests

init_servers = ["http://localhost:5000", "http://localhost:5001", "http://localhost:5002"]

# Class to manage backend servers
class BackendServers:
    def __init__(self, server_list):
        self.server_list = server_list

    # Function to extract host and port from the server url
    def parseServerUrl(self, url):
        host = ""
        if url.split(':')[0] == "http" or url.split(':')[0] == "https":
            host = url.split(':')[1][2:]
            port = url.split(':')[2]
        else:
            host = url.split(':')[0]
            port = url.split(':')[1]
        return host, port
    
    def checkServerHealth(self, host, port):
        # print(f"Checking health of server : {host + ':' + str(port)}")
        res = requests.get('http://' + host + ':' + str(port))
        if res.status_code == 200:
            return True
        else:
            return False
        
    def getActiveServers(self):
        active_servers = []
        for server in init_servers:
            host, port = self.parseServerUrl(server)
            if self.checkServerHealth(host, port) == True:
                active_servers.append(host + ':' + port)
        return active_servers
        # return [5000, 5001, 5002]

# Class to select backend server for the request forwarding (Uses Round Robin Algorithm)
class ServerSelection:
    def __init__(self, server_list):
        self.servers = server_list
        self.current_index = 0

    def get_next_server(self):
        server = self.servers[self.current_index]
        server_host = server.split(':')[0]
        server_port = server.split(':')[1]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server_host, int(server_port)

available_servers = BackendServers(init_servers)
be_servers = ServerSelection(available_servers.getActiveServers())
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
            host, port = be_servers.get_next_server()
            newThread = threading.Thread(target=self.ForwardRequestToBackend, args=(request, host, port, client))
            newThread.start()
            threads.append(newThread)

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    print("Load Balancer running on port 8888")
    lb_server = Socket('localhost', 8888)
    lb_server.createSocket()