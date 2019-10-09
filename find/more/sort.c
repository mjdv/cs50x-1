/**
 * Prompts user for as many as MAX values until EOF is reached,
 * then prints the values in sorted order. Used to test `sort`.
 *
 * Usage: ./sort
 *
 */

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

#include "helpers.h"

// maximum amount of hay
const int MAX = 1000000;

int main(int argc, string argv[])
{
    fprintf(stderr, "RUNNING SORT\n");
    // fill haystack
    int size = 0;
    int haystack[MAX];
    while(size < MAX && scanf("%d", haystack + size) == 1) {
        size++;
    }
    printf("\n");

    // sort the haystack
    sort(haystack, size);

    // print the haystack, one item per line
    for (int i = 0; i < size; i++)
    {
        printf("%i\n", haystack[i]);
    }
}
