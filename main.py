import deck as dk
# import package as pk
import socket

# @ = 64
# 0 = 48

id = int(input())
ipAddresses = ["10.254.223.31", "10.254.223.38", "10.254.223.39", "10.254.223.40"];
ports = [2637, 2638, 2639, 2640];

UDP_CURRENT_IP = ipAddresses[id]
UDP_CURRENT_PORT = ports[id]
UDP_TARGET_IP = ipAddresses[(id + 1) % 4]
UDP_TARGET_PORT = ports[(id + 1) % 4]

dealingCards = True
if id == 0:
    deck = dk.createDeck()
    print(deck)
    token = 1
    MESSAGE = dk.dealCards(deck)
else:
    token = 0

print("UDP target IP: %s" % UDP_TARGET_IP)
print("UDP target port: %s" % UDP_TARGET_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_CURRENT_IP, UDP_CURRENT_PORT))

myCards = []

while True:
    if token == 1:
        if not dealingCards:
            print("Enter message: ")
            MESSAGE = input().encode()
        else:
            dealingCards = False
        sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
        token = 0
    else:
        data, addr = sock.recvfrom(1024)
        print("Received message: %s" % data)
        decodedMessage = data.decode()
        print(decodedMessage)
        if decodedMessage[0] == '@' and decodedMessage[-1] == '@':
            origin = decodedMessage[1]
            play = decodedMessage[2]
            if play == '0':
                startIndex = 3 + 20 * id
                endIndex = startIndex + 20
                for card in decodedMessage[startIndex: endIndex]:
                    myCards.append(ord(card) - 48)
            MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()
        token = 1