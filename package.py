import classes

def passToken():
    return ("@@").encode()

def unpackMessage(receivedData, message):
    receivedData.origin = int(message[1])
    receivedData.play = int(message[2])
    receivedData.confirmation = message[-5:-1]
    if receivedData.play == 1:
        receivedData.sequenceSkipped = int(message[3])
        receivedData.numberOfCardsPlayed = ord(message[4]) - 48
        receivedData.typeOfCardPlayed = ord(message[5]) - 48
        receivedData.jokersPlayed = ord(message[6]) - 48
    elif receivedData.play == 2:
        receivedData.sequenceSkipped = int(message[3])
    
def checkConfirmation(code, id):
    for i in range(4):
        if i == id:
            continue
        if code[i] == '0':
            print("Machine %d didn't receive the message." % i)