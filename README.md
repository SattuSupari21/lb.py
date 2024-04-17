# lb.py

Implementation of a simple Load Balancer which is created from scratch using Python.

### Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Concepts](#concepts)
- [Usage](#usage)

### Features:
- Uses Round Robin Algorithm to select Back-end servers.
- Displays Health of Back-end servers
- Automatically adds online and remove offline servers.
- Multi-threaded for faster response time

### Demo:
![Demo](https://github.com/SattuSupari21/lb.py/blob/main/demo/lb-py-demo.gif)

### Concepts:
- Networking
- Threading
- Load Balancing Algorithm

### Usage:
- First start the Load Balancer using the command:
```
python multithreaded-lb.py
```
- The Load Balancer will start on port 8888 by default.
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
