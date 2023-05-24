#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include "deck.h"

// Start delimiter: 01011011
// End delimiter: 01011011

struct Machine {
    char* previous_ip;
    char* next_ip;
    int start_port;
    int end_port;
};
typedef struct Machine Machine_t;

int main(int argc, char **argv) {

    char* ipAddresses[4] = {"10.254.223.29", "10.254.223.30", "10.254.223.31", "10.254.223.32"};
    int ports[4] = {2637, 2638, 2639, 2640};
    Machine_t machine;

    int i = atoi(argv[1]);
    int token = (i == 0) ? 1 : 0;

    if (i == 0) {
        int* deck = createsDeck();
        //printDeck(deck);
        shuffleDeck(deck);
        //printDeck(deck);
        dealCards(deck);
    }
    
    machine.previous_ip = ipAddresses[(i + 3) % 4];
    machine.next_ip = ipAddresses[(i + 1) % 4];
    machine.start_port = ports[(i + 3) % 4];
    machine.end_port = ports[(i + 1) % 4];

    int socket_desc;
    struct sockaddr_in current_addr, previous_addr, next_addr; 
    
    /*
    struct sockaddr_in {
	__uint8_t       sin_len;
	sa_family_t     sin_family;
	in_port_t       sin_port;
	struct  in_addr sin_addr;
	char            sin_zero[8];
    };
    */

    char sent_message[2000], received_message[2000];
    int previous_struct_length = sizeof(previous_addr);
    int next_struct_length = sizeof(next_addr);

    // Clean buffers:
    memset(sent_message, '\0', sizeof(sent_message));
    memset(received_message, '\0', sizeof(received_message));
    
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_DGRAM, 0);

    if (socket_desc < 0) {
        printf("Error while creating socket\n");
        return -1;
    }
    printf("Socket created successfully\n");

    current_addr.sin_family = AF_INET;
    current_addr.sin_port = htons(ports[i]);
    // current_addr.sin_addr.s_addr = inet_addr(ipAddresses[i]);
    
    previous_addr.sin_family = AF_INET;
    previous_addr.sin_port = htons(machine.start_port);
    previous_addr.sin_addr.s_addr = inet_addr(machine.previous_ip);

    // Set port and IP:
    next_addr.sin_family = AF_INET;
    next_addr.sin_port = htons(machine.end_port);
    next_addr.sin_addr.s_addr = inet_addr(machine.next_ip);

    /* if (bind(socket_desc, (struct sockaddr*)&previous_addr, sizeof(previous_addr)) < 0) {
        printf("Couldn't bind to the port\n");
        return -1;
    } */

    if (bind(socket_desc, (struct sockaddr*)&current_addr, sizeof(current_addr)) < 0) {
        printf("Couldn't bind to the port\n");
        return -1;
    }

    printf("Done with binding\n");

    // Get input from the user:
    while (1) {
        if (token) {
            // Machine has the token, so it can send a message
            printf("Enter message: ");
            gets(sent_message);
            
            // Send the message to the next machine
            if (sendto(socket_desc, sent_message, strlen(sent_message), 0,
                (struct sockaddr*)&next_addr, next_struct_length) < 0) {
                printf("Unable to send message\n");
                return -1;
            }
            
            // Receive the server's response (echoed message)
            // if (recvfrom(socket_desc, received_message, sizeof(received_message), 0,
            //     (struct sockaddr*)&previous_addr, previous_struct_length) < 0) {
            //     printf("Couldn't receive message\n");
            //     return -1;
            // }
            
            // printf("Server's response: %s\n", received_message);
            
            // Pass the token to the next machine
            token = 0;
        } else {
            // Machine doesn't have the token, so it can only receive messages
            
            // Receive a message from the previous machine
            if (recvfrom(socket_desc, received_message, sizeof(received_message), 0,
                (struct sockaddr*)&previous_addr, &previous_struct_length) < 0) {
                printf("Couldn't receive message\n");
                perror("Error: ");
                // return -1;
            } else {
		token = 1;
	    }
            
            printf("Received message: %s\n", received_message);
            
            // // Send the received message back to the previous machine
            // if (sendto(socket_desc, received_message, strlen(received_message), 0,
            //     (struct sockaddr*)&previous_addr, previous_struct_length) < 0) {
            //     printf("Unable to send message\n");
            //     return -1;
            // }
            
            // Pass the token to the next machine
            // token = 1;
        }
    }

        
        // printf("Enter message: ");
        // gets(sent_message);
    
        // Send the message to server
    //     if (recvfrom(socket_desc, received_message, sizeof(received_message), 0,
    //         (struct sockaddr*)&previous_addr, &previous_struct_length) < 0) {
    //         printf("Couldn't receive message\n");
    //         return -1;
    //     }

    //     // implements token passing algorithm
    //     if (strcmp(received_message, "01011011") == 0) {
    //         printf("Token received\n");
    //         printf("Enter message: ");
    //         gets(sent_message);
    //     }
    //     if (sendto(socket_desc, sent_message, strlen(sent_message), 0,
    //         (struct sockaddr*)&next_addr, next_struct_length) < 0) {
    //         printf("Unable to send message\n");
    //         return -1;
    //     }
    // }
        
    // Close the socket:
    // close(socket_desc);

    return 0;
}
