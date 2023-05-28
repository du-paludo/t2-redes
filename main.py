import deck as dk
# import package as pk
import socket

# @ = 64
# 0 = 48

def checkConfirmation(code, id):
    for i in range(4):
        if i == id:
            continue
        if code[i] == '0':
            print("Machine %d didn't receive the message." % i)

def isPlayValid(myCards, cardsNeeded, typeOfCard, jokersWanted):
    if cardsNeeded == '0':
        return True
    else:
        cardsOwned = 0
        for card in myCards:
            if card == typeOfCard:
                cardsOwned += 1
        if cardsOwned < cardsNeeded:
            return False
        
        jokersOwned = 0

        for card in myCards:
            if card == 13:
                jokersOwned += 1
        if jokersOwned < jokersWanted:
            return False
        
        for _ in range(cardsNeeded):
            myCards.remove(typeOfCard)
        for _ in range(jokersWanted):
            myCards.remove(13)
        return True

def passToken():
    return ("@@").encode()


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
    playing = True
    hasLead = True
    MESSAGE = dk.dealCards(deck)
else:
    token = 0
    playing = False
    hasLead = False

print("UDP target IP: %s" % UDP_TARGET_IP)
print("UDP target port: %s" % UDP_TARGET_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_CURRENT_IP, UDP_CURRENT_PORT))

myCards = []

while True:
    if token == 1:
        if dealingCards:
            dealingCards = False
        elif not dealingCards and playing:
            print("My cards: ", end="")
            print(myCards)
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
            else:
                print("Type 0 to pass or 1 to throw %s cards: " % numberOfCards, end="")
                willPlay = int(input())
                if willPlay == 0:
                    if int(origin) == id and sequenceSkipped == 3:
                        print("All players passed. Player %s has the lead." % id)
                        hasLead = True
                        continue
                    numberOfCards = 0
                    typeOfCard = 0
                    jokersWanted = 0
                else:
                    print("Enter type of card of value smaller than %s to throw: " % typeOfCardPlayed, end="")
                    typeOfCard = int(input())
                    if typeOfCard >= typeOfCardPlayed:
                        print("Value of card must be smaller than %s." % typeOfCardPlayed)
                        continue
                    if 13 in myCards:
                        print("Enter number of jokers to throw: ", end="")
                        jokersWanted = int(input())

            if isPlayValid(myCards, numberOfCards, typeOfCard, jokersWanted):
                if willPlay == 0:
                    sequenceSkipped += 1
                    MESSAGE = ("@" + str(id) + "2" + str(sequenceSkipped) + "@").encode()
                else:
                    sequenceSkipped = 0
                    MESSAGE = ("@" + str(id) + "1" + str(sequenceSkipped) + chr(numberOfCards + 48) + chr(typeOfCard + 48) + chr(jokersWanted + 4) + "0000" + "@").encode()
                playing = False
                hasLead = False
            else:
                print("Invalid play.")
                continue
        token = 0
        sock.sendto(MESSAGE, (UDP_TARGET_IP, UDP_TARGET_PORT))
    else:
        data, addr = sock.recvfrom(1024)
        # print("Received message: %s" % data)
        decodedMessage = data.decode()
        # print(decodedMessage)
        if decodedMessage == "@@": # has the token
            playing = True
        elif decodedMessage[0] == '@' and decodedMessage[-1] == '@':
            origin = decodedMessage[1]
            play = decodedMessage[2]
            sequenceSkipped = int(decodedMessage[3])
            confirmation = decodedMessage[-5:-1]
            
            # Player is receiving cards
            if play == '0':
                startIndex = 3 + 20 * id
                endIndex = startIndex + 20
                for card in decodedMessage[startIndex: endIndex]:
                    myCards.append(ord(card) - 48)
                myCards.sort()
                MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()

            # Player received a play
            elif play == '1':
                # Player is the origin of the play
                if (int(origin) == id):
                    checkConfirmation(confirmation, id)
                    MESSAGE = passToken()
                else:
                    numberOfCards = ord(decodedMessage[4]) - 48
                    if (numberOfCards != 0):
                        cardsNeeded = numberOfCards
                    typeOfCardPlayed = ord(decodedMessage[5]) - 48
                    print("Player %s threw %s cards of type %s." % (origin, numberOfCards, typeOfCardPlayed))
                    MESSAGE = (decodedMessage[0:-5 + id] + "1" + decodedMessage[-4 + id:]).encode()

            # Last player skipped
            elif play == '2':
                if int(origin) == id:
                    checkConfirmation(confirmation, id)
                    if sequenceSkipped == 3:
                        print("All the players skipped. Restart the hand.")
                        playing = True
                        hasLead = True
        token = 1