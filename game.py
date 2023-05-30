import classes

def isPlayValid(myCards, playInfo):
    cardsNeeded = playInfo.numberOfCards
    if cardsNeeded == '0':
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
        
        for _ in range(cardsNeeded):
            myCards.remove(playInfo.typeOfCard)
        for _ in range(playInfo.jokersWanted):
            myCards.remove(13)
        return True
    
def makePlay(myCards, receivedData, hasLead):
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
        return classes.PlayInfo(numberOfCards+jokersWanted, typeOfCard, jokersWanted, willPlay)
    # Otherwise, he must throw the same number of cards of better value
    else:
        print("Type 0 to pass or 1 to throw %s cards: " % receivedData.numberOfCardsPlayed, end="")
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
                jokersWanted = int(input())
            else:
                jokersWanted = 0
        return classes.PlayInfo(receivedData.numberOfCardsPlayed, typeOfCard, jokersWanted, willPlay)