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

void dealCards(unsigned char* deck) {
    //unsigned char* mensagem = malloc(100000 * sizeof(unsigned char));
    // unsigned char* charDeck = malloc(80 * sizeof(unsigned char));
    // snprintf(charDeck, sizeof(charDeck), "%d", deck);
    // printf("%s\n", deck);
    // printf("%s\n", charDeck);
    // strcat(mensagem, charDeck);
    for (int i = 0; i < 80; i++) {
        printf("%u ", deck[i]);
    }
    printf("\n");
    //printf("%s\n", mensagem);
}