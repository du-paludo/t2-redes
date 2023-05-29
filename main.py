import deck as dk
# import package as pk
import socket
from enum import Enum

# @ = 64
# 0 = 48

class State(Enum):
    LISTENING = 1
    SENDING = 2

class Data:
    def __init__(self, origin, play, sequenceSkipped, confirmation):
        self.origin = origin
        self.play = play
        self.sequenceSkipped = sequenceSkipped
        self.confirmation = confirmation

class PlayInfo:
    def __init__(self, numberOfCards, typeOfCard, jokersWanted, willPlay):
        self.numberOfCards = numberOfCards
        self.typeOfCard = typeOfCard
        self.jokersWanted = jokersWanted
        self.willPlay = willPlay

def checkConfirmation(code, id):
    for i in range(4):
        if i == id:
            continue
        if code[i] == '0':
            print("Machine %d didn't receive the message." % i)

def isPlayValid(playInfo):
    if playInfo.cardsNeeded == '0':
        return True
    else:
        cardsOwned = 0
        for card in myCards:
            if card == playInfo.typeOfCard:
                cardsOwned += 1
        if cardsOwned < cardsNeeded:
            return False
        
        jokersOwned = 0

        for card in myCards:
            if card == 13:
                jokersOwned += 1
        if jokersOwned < playInfo.jokersWanted:
            return False
        
        for _ in range(playInfo.cardsNeeded):
            myCards.remove(playInfo.typeOfCard)
        for _ in range(playInfo.jokersWanted):
            myCards.remove(13)
        return True

def passToken():
    return ("@@").encode()

def unpackMessage(message):
    origin = int(message[1])
    play = int(message[2])
    sequenceSkipped = int(message[3])
    confirmation = message[-5:-1]
    return Data(origin, play, sequenceSkipped, confirmation)

def receiveCards(myCards, message):
    startIndex = 3 + 20 * id
    endIndex = startIndex + 20
    for card in message[startIndex: endIndex]:
        myCards.append(ord(card) - 48)
    myCards.sort()
    MESSAGE = (message[0:-5 + id] + "1" + message[-4 + id:]).encode()

def makePlay():
    # If players has the lead, he can throw any cards
    if hasLead == True:
        print("Enter number of cards to throw: ", end="")
        numberOfCards = int(input())
        print("Enter type of card to throw: ", end="")
        typeOfCard = int(input())
        jokersWanted = 0
        willPlay = 1
        if 13 in myCards:
            print("Enter number of jokers to throw: ", end="")
            jokersWanted = int(input())
    # Otherwise, he must throw the same number of cards of better value
    else:
        print("Type 0 to pass or 1 to throw %s cards: " % numberOfCards, end="")
        willPlay = int(input())
        if willPlay == 0:
            if receivedData.origin == id and receivedData.sequenceSkipped == 3:
                hasLead = True
            return PlayInfo(0, 0, 0, 0)
        else:
            print("Enter type of card of value smaller than %s to throw: " % typeOfCardPlayed, end="")
            typeOfCard = int(input())
            if typeOfCard >= typeOfCardPlayed:
                print("Value of card must be smaller than %s." % typeOfCardPlayed)
                return None
            if 13 in myCards:
                print("Enter number of jokers to throw: ", end="")
                jokersWanted = int(input())
    return PlayInfo(numberOfCards, typeOfCard, jokersWanted, willPlay)
    


id = int(input())
ipAddresses = ["10.254.223.31", "10.254.223.38", "10.254.223.39", "10.254.223.40"];
ports = [2637, 2638, 2639, 2640];

UDP_CURRENT_IP = ipAddresses[id]
UDP_CURRENT_PORT = ports[id]
UDP_TARGET_IP = ipAddresses[(id + 1) % 4]
UDP_TARGET_PORT = ports[(id + 1) % 4]

print("UDP target IP: %s" % UDP_TARGET_IP)
print("UDP target port: %s" % UDP_TARGET_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_CURRENT_IP, UDP_CURRENT_PORT))

dealingCards = True
if id == 0:
    deck = dk.createDeck()
    state = State.SENDING
    hasToken = True
    hasLead = True
    MESSAGE = dk.dealCards(deck)
    sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
else:
    state = State.LISTENING
    hasToken = False
    hasLead = False

myCards = []

while True:
    match state:
        case State.SENDING:
            if hasToken:   
                print("My cards: ", end="")
                print(myCards)
                playInfo = makePlay()
                if playInfo == None:
                    continue
                elif playInfo.willPlay == 0:
                    playInfo.sequenceSkipped += 1
                    MESSAGE = ("@" + str(id) + "2" + str(playInfo.sequenceSkipped) + "@").encode()
                elif isPlayValid(playInfo):
                    playInfo.sequenceSkipped = 0
                    MESSAGE = ("@" + str(id) + "1" + str(playInfo.sequenceSkipped) + chr(numberOfCards + 48) + chr(typeOfCard + 48) + chr(jokersWanted + 4) + "0000" + "@").encode()
                else:
                    print("Invalid play.")
                    continue
                playing = False
                hasLead = False
            state = State.LISTENING
            sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
        case State.LISTENING:
            # Receives data and decodes it
            data, addr = sock.recvfrom(1024)
            decodedMessage = data.decode()
            # If receives the token, set it to true
            if decodedMessage == "@@":
                hasToken = True
            # Else, just reads the message and sends to next player
            elif decodedMessage[0] == '@' and decodedMessage[-1] == '@':
                # Unpack message
                receivedData = unpackMessage(decodedMessage)
                # Player is receiving cards
                if receivedData.play == 0:
                    receiveCards(myCards, decodedMessage)
                    # Player marks the confirmation of the message
                    MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()
                # Player received a play
                elif receivedData.play == 1:
                    # Player is the origin of the play
                    if (receivedData.origin == id):
                        checkConfirmation(receivedData.confirmation, id)
                        MESSAGE = passToken()
                    else:
                        numberOfCards = ord(decodedMessage[4]) - 48
                        if (numberOfCards != 0):
                            cardsNeeded = numberOfCards
                        typeOfCardPlayed = ord(decodedMessage[5]) - 48
                        print("Player %s threw %s cards of type %s." % (receivedData.origin, numberOfCards, typeOfCardPlayed))
                        MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()
                # Last player skipped
                elif receivedData.play == '2':
                    if receivedData.origin == id:
                        checkConfirmation(receivedData.confirmation, id)
                        if receivedData.sequenceSkipped == 3:
                            print("All the players skipped. Restart the hand.")
                            playing = True
                            hasLead = True
            state = State.SENDING