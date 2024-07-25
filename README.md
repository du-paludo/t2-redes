# The Great Damulti Game

This project implements a multiplayer card game using UDP sockets for communication between machines. The game involves dealing cards, making plays, and passing tokens between players.

## Files

- `main.py`: The main script that sets up the game and handles communication between players.
- `classes.py`: Contains the class definitions for `State`, `Data`, and `PlayInfo`.
- `deck.py`: Contains functions for creating and dealing a deck of cards.
- `game.py`: Contains functions for validating plays and making plays.
- `package.py`: Contains functions for passing tokens and unpacking messages.
- `config.txt`: Configuration file with the number of players and their IP addresses and ports.

## Usage

### Configuration

1. **config.txt**:
    - The first line specifies the number of players.
    - Each subsequent line specifies the IP address and port of each player in the format `IP:PORT`.

    Example:
    ```txt
    4
    192.168.1.2:5000
    192.168.1.3:5001
    192.168.1.4:5002
    192.168.1.5:5003
    ```

### Execution

1. Ensure all players have their IP addresses and ports correctly specified in `config.txt`.
2. Run the main script on each machine:

    ```sh
    python main.py
    ```

### Game Flow

1. **Initialization**:
    - Each machine reads its IP address and port from `config.txt` and identifies its ID.
    - The first player (ID 0) starts the game by generating a random message and sending it to the next player.
    - Once the message is confirmed, the deck is created and cards are dealt.

2. **Gameplay**:
    - Players take turns based on the token passing mechanism.
    - Each player makes a play based on the current game state.
    - Messages are sent between players to update the game state and confirm actions.
    - Players can either play cards or pass their turn based on the game rules.

3. **Winning**:
    - The game continues until a player wins by playing all their cards.
    - The winning player is announced, and the game ends.

### Functions

#### Main Script (`main.py`)

- **checkConfirmation(code, id)**:
    Checks if all players have received the message.

#### Deck Management (`deck.py`)

- **createDeck()**:
    Creates and shuffles a deck of cards.

- **dealCards(deck)**:
    Deals cards to players and returns the initial message.

- **receiveCards(myCards, message, id)**:
    Receives and sorts cards for a player.

#### Game Logic (`game.py`)

- **isPlayValid(myCards, receivedData, playInfo, hasLead)**:
    Validates if a play is allowed based on the current game state.

- **makePlay(myCards, receivedData, hasLead)**:
    Prompts the player to make a play and returns the play information.

#### Message Handling (`package.py`)

- **passToken()**:
    Passes the token to the next player.

- **unpackMessage(receivedData, message)**:
    Unpacks a received message and updates the game state.

## Classes

#### `State` (in `classes.py`)

- **LISTENING**: The state where the player is waiting for a message.
- **SENDING**: The state where the player is sending a message.

#### `Data` (in `classes.py`)

- **Attributes**:
    - `origin`: ID of the originating player.
    - `play`: Type of play (0: receiving cards, 1: play, 2: skip, 3: win).
    - `sequenceSkipped`: Number of consecutive skips.
    - `numberOfCardsPlayed`: Number of cards played.
    - `typeOfCardPlayed`: Type of card played.
    - `jokersPlayed`: Number of jokers played.
    - `confirmation`: Confirmation string for message receipt.

#### `PlayInfo` (in `classes.py`)

- **Attributes**:
    - `numberOfCards`: Number of cards to play.
    - `typeOfCard`: Type of card to play.
    - `numberOfJokers`: Number of jokers to play.
    - `willPlay`: Indicates if the player will play or pass.
