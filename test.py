import socket

# sock = []

id = int(input())
ipAddresses = ["10.254.223.29", "10.254.223.30", "10.254.223.31", "10.254.223.32"];
ports = [2637, 2638, 2639, 2640];

UDP_IP = ipAddresses[id]
UDP_PORT = ports[id]

if id == 0:
    token = 1
else:
    token = 0

print("DP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    if token == 1:
        print("Enter message: ")
        MESSAGE = input()
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        token = 0
    else:
        data, addr = sock.recvfrom(1024)
        print("Received message: %s" % data)
        token = 1


# for i in range(0, 4):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind(('localhost', 2637 + i))
#     sock.append(s);

# s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s1.bind('localhost', 2637)

# s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s2.bind('localhost', 2638)

# s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s3.bind('localhost', 2639)

# s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s4.bind('localhost', 2640)

# def send_receive_message(node_id, next_node_id, previous_node_id):
#     # Receive message from previous node
#     data, address = node_id.recvfrom(1024)
#     print(f"Node {node_id} received: {data.decode()}")

#     # Send message to the next node
#     next_node_id.sendto(data, ('localhost', next_node_port))
#     print(f"Node {node_id} sent: {data.decode()}")

# initial_message = b"Initial message"
# sock[0].sendto(initial_message, ('localhost', next_node_port))
# print(f"Node 1 sent: {initial_message.decode()}")

# Enter the communication loop
# while True:
#     send_receive_message(sock[0], sock[1], sock[2])