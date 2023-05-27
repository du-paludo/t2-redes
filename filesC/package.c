#include <stdio.h>
#include "package.h"

void unpackMessage(unsigned char* message) {
    int i = 0;
    while (message[i] != '\0') {
        printf("%d ", i);
        printf("%u\n", message[i]);
        i++;
    }
}