import socket
import classes
import deck as dk
import game
import package
import random

# @ = 64
# 0 = 48

def checkConfirmation(code, id):
    for i in range(4):
        if i == id:
            continue
        if code[i] == '0':
            print("Machine %d didn't receive the message." % i)

ipAddresses = []
ports = []

with open('config.txt', 'r') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0:
            numPlayers = int(line)
        else:
            ip, port = line.split(':')
            ipAddresses.append(ip)
            ports.append(int(port))

machine_ip = socket.gethostbyname(socket.gethostname())
id = ipAddresses.index(machine_ip)
print("ID: %s" % id)
print("Machine IP: %s" % ipAddresses[id])
print("Receive port: %s" % ports[id])

UDP_CURRENT_IP = ipAddresses[id]
UDP_CURRENT_PORT = ports[id]
UDP_TARGET_IP = ipAddresses[(id + 1) % 4]
UDP_TARGET_PORT = ports[(id + 1) % 4]

print("Target IP: %s" % UDP_TARGET_IP)
print("Target port: %s" % UDP_TARGET_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_CURRENT_IP, UDP_CURRENT_PORT))

hasLead = False
hasToken = False
state = classes.State.LISTENING
receivedData = classes.Data(0, 0, 0, 0, 0, 0, "0000")

if id == 0:
    sock.settimeout(1)
    while True:
        MESSAGE = str(random.randint(0, 5000)).encode()
        sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
        received = False
        try:
            data, addr = sock.recvfrom(1024)
            received = True
        except socket.timeout as e:
            continue
        if received and data.decode() == MESSAGE.decode():
            sock.settimeout(None)
            break

if id == 0:
    deck = dk.createDeck()
    state = classes.State.LISTENING
    hasToken = True
    hasLead = True
    MESSAGE = dk.dealCards(deck)
    sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))

myCards = []

while True:
    if state == classes.State.SENDING:
        if hasToken:
            print("My cards: ", end="")
            print(myCards)
            playInfo = game.makePlay(myCards, receivedData, hasLead)
            if playInfo == None:
                continue
            elif playInfo.willPlay == 0:
                receivedData.sequenceSkipped += 1
                MESSAGE = ("@" + str(id) + "2" + str(receivedData.sequenceSkipped) + "0000@").encode()
            elif game.isPlayValid(myCards, receivedData, playInfo, hasLead):
                receivedData.sequenceSkipped = 0
                MESSAGE = ("@" + str(id) + "1" + str(receivedData.sequenceSkipped) + chr(playInfo.numberOfCards + 48) + chr(playInfo.typeOfCard + 48) + chr(playInfo.numberOfJokers + 48) + "0000" + "@").encode()
            else:
                print("Invalid play.")
                continue
            hasToken = False
            hasLead = False
        #print("Sending message: %s" % MESSAGE.decode())
        sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
        state = classes.State.LISTENING
    elif state == classes.State.LISTENING:
        # Receives data and decodes it
        data, addr = sock.recvfrom(1024)
        decodedMessage = data.decode()
        MESSAGE = decodedMessage.encode()
        #print("Received message: %s" % decodedMessage)
        # If receives the token, set it to true
        if decodedMessage == "@@":
            hasToken = True
        # Else, just reads the message and sends to next player
        elif decodedMessage[0] == '@' and decodedMessage[-1] == '@':
            package.unpackMessage(receivedData, decodedMessage)
            # Player marks the confirmation of the message
            MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()
            if receivedData.origin == id:
                checkConfirmation(receivedData.confirmation, id)
                # checks if players won
                if len(myCards) == 0:
                    MESSAGE = ("@" + str(id) + "3" + str(receivedData.sequenceSkipped) + "0000" + "0000" + "0000" + "0000" + "@").encode()
                else:
                    MESSAGE = package.passToken()
            # Player is receiving cards
            if receivedData.play == 0:
                dk.receiveCards(myCards, decodedMessage, id) 
            # Last player did a play
            elif receivedData.play == 1:
                # Player is the origin of the play
                if receivedData.origin != id:
                    if receivedData.jokersPlayed == 0:
                        print("Player %s threw %s cards of type %s." % (receivedData.origin+1, receivedData.numberOfCardsPlayed, receivedData.typeOfCardPlayed))    
                    else:
                        print("Player %s threw %s cards of type %s and %s jokers." % (receivedData.origin+1, receivedData.numberOfCardsPlayed, receivedData.typeOfCardPlayed, receivedData.jokersPlayed))
            # Last player skipped
            elif receivedData.play == 2:
                if receivedData.origin != id:
                    if receivedData.sequenceSkipped == 4:
                        print("Player %s passed. Hand restarted." % (receivedData.origin+1))
                    else:
                        print("Player %s passed" % (receivedData.origin+1))
                else:
                    if receivedData.sequenceSkipped == 4:
                        print("All players passed. Hand restarted.")
                        hasLead = True
                        hasToken = True
            # Last player won
            elif receivedData.play == 3:
                if receivedData.origin == id:
                    print("Congratulations! You won the game.")
                else:
                    print("Player %s won the game." % (receivedData.origin+1))
                    sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
                break
        state = classes.State.SENDING
