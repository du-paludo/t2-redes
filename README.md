# Real-time data transmission using UDP

The goal of this project was to implement a UDP connection to transmit real-time data. In the project, we implemented both the client and the server in Python, and for data collection, we used the Open Meteo API, which provides the temperature of a location in real-time based on latitude and longitude provided in the source code.

## Server

The server was built with the entire logic for storing and distributing data collected by the API. To communicate with multiple clients, threads were implemented to send and receive data simultaneously.

There are three threads on the server. One is responsible for listening on the designated port (5968) to see if any client wants to subscribe to the broadcast list. The second thread is responsible for sending packets to clients registered on the broadcast list. The third thread is responsible for receiving user input in case they wish to terminate the program.

The packets sent are the same for each client. They contain only two fields: the sequence number of that packet in the stream and the temperature in Curitiba.

To terminate the server, simply type "exit" or "quit" in the command line. If the user wishes to change the interval between each sent packet, they can type "setinterval x", where x is the duration in seconds of the interval.

At the end of the server's execution, some statistics are displayed in the standard output, such as the total number of packets sent and the total number of connected clients.

## Client

When running the client program, the server's IP address is requested. After that, a subscription request message is automatically sent to the server. Upon receiving the message, the server adds the client to the broadcast list, and the client starts receiving data sent by the server. These data (sequence number and temperature) are displayed in the standard output with each received packet.

The client checks the sequence number to determine if any packets were lost or if they arrived out of order.

When the client wishes to unsubscribe, they should type "unsubscribe" in the command line. Upon typing this command, a message is sent to the server, which removes the client from the broadcast list. Then, a report is displayed on the screen containing data about the received packets.

The concept of threading was also used on the client side, to receive data from the server and read keyboard input simultaneously.
