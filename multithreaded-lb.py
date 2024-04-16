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
            protocol = url.split(':')[0]
            host = url.split(':')[1][2:]
            port = url.split(':')[2]
        else:
            protocol = "http"
            host = url.split(':')[0]
            port = url.split(':')[1]
        return protocol, host, port
    
    def checkServerHealth(self, protocol, host, port, server_number):
        try:
            res = requests.get(protocol + '://' + host + ':' + str(port) + '/health-check')
            if res.status_code == 200:
                print(f"[HEALTH CHECK] Server {server_number} PASSED")
                return True
        except:
            print(f"[HEALTH CHECK] Server {server_number} FAILED")
            return False
        
    def getActiveServers(self):
        print("\n")
        active_servers = []
        server_number = 1
        for server in init_servers:
            protocol, host, port = self.parseServerUrl(server)
            if self.checkServerHealth(protocol, host, port, server_number) == True:
                active_servers.append(host + ':' + port)
            server_number += 1
        return active_servers

# Class to select backend server for the request forwarding (Uses Round Robin Algorithm)
class ServerSelection:
    def __init__(self, server_list):
        self.servers = server_list
        self.current_index = 0

    def get_next_server(self):
        if len(self.servers) == 1:
            self.current_index = 0
        try:
            server = self.servers[self.current_index]
            server_host = server.split(':')[0]
            server_port = server.split(':')[1]
            self.current_index = (self.current_index + 1) % len(self.servers)
            return server_host, int(server_port)
        except Exception:
            return

be_servers = ServerSelection(server_list=init_servers)
threads = []

# Function to update server list every n seconds
def updateAvailableServers():
    threading.Timer(5.0, updateAvailableServers).start()
    be_servers.servers = BackendServers(init_servers).getActiveServers()

class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def ForwardRequestToBackend(self, request, host, port, client_sock):
        be_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            be_socket.connect((host, port))
            be_socket.send(request.encode())
            while True:
                headers, body = be_socket.recv(4096), be_socket.recv(4096)
                if not body or headers:
                    break

            # print(f"Response from Server: {headers.decode().splitlines()[0]}")
            # print(body.decode())

            response = headers + body
            client_sock.send(response)

            client_sock.close()
        except:
            client_sock.close()
            return

    def createSocket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(100)

        while True:
            client, address = server.accept()
            request = client.recv(4096).decode()
            if not request:
                break
            # print(f"\nReceived request from {address[0]}")
            # print(request)

            # Forward request to backend server
            try:
                host, port = be_servers.get_next_server()
            except:
                continue
            newThread = threading.Thread(target=self.ForwardRequestToBackend, args=(request, host, port, client))
            newThread.start()
            threads.append(newThread)

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    print("Load Balancer running on port 8888")
    updateAvailableServers()
    lb_server = Socket('localhost', 8888)
    lb_server.createSocket()