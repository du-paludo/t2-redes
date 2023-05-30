from enum import Enum

class State(Enum):
    LISTENING = 1
    SENDING = 2

class Data:
    def __init__(self, origin, play, sequenceSkipped, numberOfCardsPlayed, typeOfCardPlayed, jokersPlayed, confirmation):
        self.origin = origin
        self.play = play
        self.sequenceSkipped = sequenceSkipped
        self.numberOfCardsPlayed = numberOfCardsPlayed
        self.typeOfCardPlayed = typeOfCardPlayed
        self.jokersPlayed = jokersPlayed
        self.confirmation = confirmation

class PlayInfo:
    def __init__(self, numberOfCards, typeOfCard, numberOfJokers, willPlay):
        self.numberOfCards = numberOfCards
        self.typeOfCard = typeOfCard
        self.numberOfJokers = numberOfJokers
        self.willPlay = willPlay