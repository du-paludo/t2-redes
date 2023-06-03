import classes

def isPlayValid(myCards, receivedData, playInfo):
    cardsNeeded = receivedData.numberOfCardsPlayed + receivedData.jokersPlayed
    if cardsNeeded == 0:
        return True
    else:
        cardsOwned = 0
        for card in myCards:
            if card == playInfo.typeOfCard:
                cardsOwned += 1
        
        jokersOwned = 0
        for card in myCards:
            if card == 13:
                jokersOwned += 1
        if jokersOwned < playInfo.numberOfJokers:
            return False
        
        if cardsOwned + jokersOwned < cardsNeeded:
            return False
        
        for _ in range(playInfo.numberOfCards):
            myCards.remove(playInfo.typeOfCard)
        for _ in range(playInfo.numberOfJokers):
            myCards.remove(13)
        return True
    
def makePlay(myCards, receivedData, hasLead):
    # If players has the lead, he can throw any cards
    if hasLead == True:
        print("Enter number of cards to throw: ", end="")
        numberOfCards = int(input())
        print("Enter type of card to throw: ", end="")
        typeOfCard = int(input())
        numberOfJokers = 0
        willPlay = 1
        if 13 in myCards:
            print("Enter number of jokers to throw: ", end="")
            numberOfJokers = int(input())
        return classes.PlayInfo(numberOfCards, typeOfCard, numberOfJokers, willPlay)
    # Otherwise, he must throw the same number of cards of better value
    else:
        print("Type 0 to pass or 1 to throw %s cards: " % (receivedData.numberOfCardsPlayed + receivedData.jokersPlayed), end="")
        willPlay = int(input())
        if willPlay == 0:
            print(receivedData.origin)
            if receivedData.origin == id and receivedData.sequenceSkipped == 3:
                hasLead = True
            return classes.PlayInfo(0, 0, 0, 0)
        else:
            print("Enter type of card of value smaller than %s to throw: " % receivedData.typeOfCardPlayed, end="")
            typeOfCard = int(input())
            if typeOfCard >= receivedData.typeOfCardPlayed:
                print("Value of card must be smaller than %s." % receivedData.typeOfCardPlayed)
                return None
            if 13 in myCards:
                print("Enter number of jokers to throw: ", end="")
                numberOfJokers = int(input())
            else:
                numberOfJokers = 0
        return classes.PlayInfo(receivedData.numberOfCardsPlayed, typeOfCard, numberOfJokers, willPlay)