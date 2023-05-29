import socket
import classes
import deck as dk
import game as gm
import package as pk

# @ = 64
# 0 = 48

def checkConfirmation(code, id):
    for i in range(4):
        if i == id:
            continue
        if code[i] == '0':
            print("Machine %d didn't receive the message." % i)


id = int(input())
ipAddresses = ["10.254.223.30", "10.254.223.32", "10.254.223.33", "10.254.223.34"];
ports = [2637, 2638, 2639, 2640];

UDP_CURRENT_IP = ipAddresses[id]
UDP_CURRENT_PORT = ports[id]
UDP_TARGET_IP = ipAddresses[(id + 1) % 4]
UDP_TARGET_PORT = ports[(id + 1) % 4]

print("UDP target IP: %s" % UDP_TARGET_IP)
print("UDP target port: %s" % UDP_TARGET_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_CURRENT_IP, UDP_CURRENT_PORT))

hasLead = False
hasToken = False
state = classes.State.LISTENING

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
            playInfo = gm.makePlay(receivedData, hasLead)
            if playInfo == None:
                continue
            elif playInfo.willPlay == 0:
                receivedData.sequenceSkipped += 1
                MESSAGE = ("@" + str(id) + "2" + str(receivedData.sequenceSkipped) + "@").encode()
            elif gm.isPlayValid(playInfo):
                playInfo.sequenceSkipped = 0
                MESSAGE = ("@" + str(id) + "1" + str(playInfo.sequenceSkipped) + chr(playInfo.numberOfCards + 48) + chr(playInfo.typeOfCard + 48) + chr(playInfo.jokersWanted + 4) + "0000" + "@").encode()
            else:
                print("Invalid play.")
                continue
            hasToken = False
            hasLead = False
        sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
        state = classes.State.LISTENING
    elif state == classes.State.LISTENING:
        # Receives data and decodes it
        data, addr = sock.recvfrom(1024)
        decodedMessage = data.decode()
        # If receives the token, set it to true
        if decodedMessage == "@@":
            hasToken = True
        # Else, just reads the message and sends to next player
        elif decodedMessage[0] == '@' and decodedMessage[-1] == '@':
            # Unpack message
            receivedData = pk.unpackMessage(decodedMessage)
            # Player is receiving cards
            if receivedData.play == 0:
                dk.receiveCards(myCards, decodedMessage)
                # Player marks the confirmation of the message
                MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()
            # Player received a play
            elif receivedData.play == 1:
                # Player is the origin of the play
                if (receivedData.origin == id):
                    checkConfirmation(receivedData.confirmation, id)
                    MESSAGE = pk.passToken()
                else:
                    print("Player %s threw %s cards of type %s." % (receivedData.origin, receivedData.numberOfCardsPlayed, receivedData.typeOfCardPlayed))
                    MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()
            # Last player skipped
            elif receivedData.play == '2':
                if receivedData.origin == id:
                    checkConfirmation(receivedData.confirmation, id)
                    if receivedData.sequenceSkipped == 3:
                        print("All the players skipped. Restart the hand.")
                        hasToken = True
                        hasLead = True
        state = classes.State.SENDING