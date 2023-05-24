#ifndef _DECK_
#define _DECK_

unsigned char* createsDeck();

void shuffleDeck(unsigned char* deck);

void swap(unsigned char* deck, int a, int b);

void printDeck(unsigned char* deck);

void dealCards(unsigned char* deck);

#endif