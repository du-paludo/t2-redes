import socket

sock = []

id = int(input())
next_node_port = 2638 + id

for i in range(0, 4):
    sock[i] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock[i].bind('localhost', 2637 + i)

# s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s1.bind('localhost', 2637)

# s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s2.bind('localhost', 2638)

# s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s3.bind('localhost', 2639)

# s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s4.bind('localhost', 2640)

def send_receive_message(node_id, next_node_id, previous_node_id):
    # Receive message from previous node
    data, address = node_id.recvfrom(1024)
    print(f"Node {node_id} received: {data.decode()}")

    # Send message to the next node
    next_node_id.sendto(data, ('localhost', next_node_port))
    print(f"Node {node_id} sent: {data.decode()}")

initial_message = b"Initial message"
s[0].sendto(initial_message, ('localhost', next_node_port))
print(f"Node 1 sent: {initial_message.decode()}")

# Enter the communication loop
while True:
    send_receive_message(sock[0], sock[1], sock[2])