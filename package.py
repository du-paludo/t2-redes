import classes

def passToken():
    return ("@@").encode()

def unpackMessage(message):
    origin = int(message[1])
    play = int(message[2])
    confirmation = message[-5:-1]
    if play == 0:
        return classes.Data(origin, play, None, None, None, confirmation)
    elif play == 1:
        sequenceSkipped = int(message[3])
        numberOfCardsPlayed = ord(message[4]) - 48
        typeOfCardPlayed = ord(message[5]) - 48
        return classes.Data(origin, play, sequenceSkipped, numberOfCardsPlayed, typeOfCardPlayed, confirmation)
    elif play == 2:
        sequenceSkipped = int(message[3])
        return classes.Data(origin, play, sequenceSkipped, None, None, confirmation)
    
def checkConfirmation(code, id):
    for i in range(4):
        if i == id:
            continue
        if code[i] == '0':
            print("Machine %d didn't receive the message." % i)