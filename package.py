def unpackMessage(message):
    if message[0] == "@" and message[-1] == "@":
        origin = message[1]
        play = message[2]
        if play == "0":
            