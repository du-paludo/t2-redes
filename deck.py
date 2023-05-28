import random

def createDeck():
    deck = []

    for i in range(1, 13):
        for _ in range(i):
            deck.append(i)
    deck.append(13)
    deck.append(13)
    random.shuffle(deck)

    return deck

def dealCards(deck):
    message = "@" + "0" + "0"
    for card in deck:
        message += chr(card + 48)
    message += "0000" + "@"
    message = message.encode()
    return message