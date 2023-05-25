#include <stdio.h>
#include "package.h"

void unpackMessage(unsigned char* message) {
    int i = 0;
    while (message[i] != 0) {
        if (message[i] == 91) {
            printf("ok\n");
        }
    }
}