#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "deck.h"

unsigned char* createsDeck() {
    // int* deck = malloc(80 * sizeof(int));
    // int count = 0;

    // for (int i = 1; i <= 12; i++) {
    //     for (int j = 0; j < i; j++) {
    //         deck[count] = i;
    //         count++;
    //     }
    // }
    // deck[count] = 13;
    // deck[count+1] = 13;

    unsigned char* deck = malloc(80 * sizeof(unsigned char));
    int count = 0;

    for (int i = 1; i <= 12; i++) {
        for (int j = 0; j < i; j++) {
            deck[count] = (unsigned char) i;
            count++;
        }
    }

    return deck;
}

void shuffleDeck(unsigned char* deck) {
    srand(time(NULL));
    int chosenPosition = 0;
    for (int i = 0; i < 80; i++) {
        int chosenPosition = rand() % 80;
        swap(deck, chosenPosition, i);
    }
}

void swap(unsigned char* deck, int a, int b) {
    int temp = deck[a];
    deck[a] = deck[b];
    deck[b] = temp;
}

void printDeck(unsigned char* deck) {
    for (int i = 0; i < 80; i++) {
        printf("%d ", deck[i]);
    }
    printf("\n");
}

unsigned char* dealCards(unsigned char* deck) {
    unsigned char* mensagem = malloc(85 * sizeof(unsigned char));
    const char* delimiter = "01011011";
    const char* confirmation = "00000000";

    mensagem[0] = strtol(delimiter, NULL, 2); // Start delimiter
    mensagem[1] = '0'; // Origin
    mensagem[2] = '0'; // Type of message
    for (int i = 3; i <= 82; i++) {
        mensagem[i] = deck[i-3]; // Cards
    }
    mensagem[83] = strtol(confirmation, NULL, 2); // Received confirmation
    mensagem[84] = strtol(delimiter, NULL, 2); // End delimiter
    mensagem[85] = '\0';

    return mensagem;
    // unsigned char* charDeck = malloc(80 * sizeof(unsigned char));
    // snprintf(charDeck, sizeof(charDeck), "%d", deck);
    // printf("%s\n", deck);
    // printf("%s\n", charDeck);
    // strcat(mensagem, charDeck);
    // for (int i = 0; i < 85; i++) {
    //     printf("%u ", mensagem[i]);
    // }
    // printf("\n");
    // printf("%s\n", mensagem);
}