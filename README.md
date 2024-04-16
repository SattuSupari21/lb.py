# lb.py

Implementation of a simple Load Balancer which is created from scratch using Python.

#### Concepts:
___
- Networking
- Threading
- Load Balancing Algorithm

#### Usage:
___
- First start the Load Balancer using the command:
```
python multithreaded-lb.py
```
- Then start the Back-end servers using the command:
```
python be.py 5000
python be.py 5001
python be.py 5002
```
- Now use any client like curl to send requests to the Load Balancer:
```
curl http://localhost:8888
```

#### Features:
- Uses Round Robin Algorithm to select Back-end servers.
- Displays Health of Back-end servers
- Automatically adds online and remove offline servers.
- Multi-threaded for faster response time

#### Files:
- lb.py - Single threaded load balancer
- multithreaded-lb.py - Multithreaded load balancer
- be.py - Simple python backend server created using Flask
