import classes

def isPlayValid(myCards, receivedData, playInfo, hasLead):
    if hasLead == False:
        cardsNeeded = receivedData.numberOfCardsPlayed + receivedData.jokersPlayed
    else:
        cardsNeeded = playInfo.numberOfCards + playInfo.numberOfJokers
        
    if cardsNeeded == 0:
        return True
    
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

    if cardsOwned + playInfo.numberOfJokers < cardsNeeded:
        return False
    
    for _ in range(playInfo.numberOfJokers):
        myCards.remove(13)
        cardsNeeded -= 1
    for _ in range(cardsNeeded):
        myCards.remove(playInfo.typeOfCard)
    return True
    
def makePlay(myCards, receivedData, hasLead):
    # If players has the lead, he can throw any cards
    if hasLead == True:
        print("Enter number of cards to throw: ", end="")
        numberOfCards = int(input())
        if numberOfCards == 0:
            print("You must throw at least one card.")
            return None
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
        print("Type 0 to pass or 1 to throw %s cards smaller than %s: " % (receivedData.numberOfCardsPlayed + receivedData.jokersPlayed, receivedData.typeOfCardPlayed), end="")
        willPlay = int(input())
        if willPlay == 0:
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
        numberOfCards = receivedData.numberOfCardsPlayed + receivedData.jokersPlayed - numberOfJokers
        return classes.PlayInfo(numberOfCards, typeOfCard, numberOfJokers, willPlay)