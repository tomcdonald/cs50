// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// global counter for number of words loaded
int DICT_SIZE;

// Represents number of buckets in a hash table
#define N 65536

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word using case insensitive version of djb2 hash function
// credit: https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
unsigned int hash(const char *word)
{
     unsigned long hash = 5381;

     for (const char* ptr = word; *ptr != '\0'; ptr++)
     {
         hash = ((hash << 5) + hash) + tolower(*ptr);
     }

     return hash % N;
 }

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }
    
    DICT_SIZE = 0;

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // apply hash to word & initialise node/allocate memory
        unsigned int bucket = hash(word);
        struct node *word_node;
        word_node = malloc(sizeof(node));
        word_node->next = NULL;
        
        // account for memory allocation failing
        if (word_node == NULL)
        {
            return 1;
        }
        
        // assign word to the node
        strcpy(word_node->word, word);
        
        // check if bucket empty, if so, add word
        if (hashtable[bucket] == NULL)
        {
            hashtable[bucket] = word_node;
        }
        
        // otherwise, add word to start of linked list
        else
        {
            // if only one element is in bucket
            if (hashtable[bucket]->next == NULL)
            {
                hashtable[bucket]->next = word_node;        
            }
            
            // if any other number of elements are in bucket
            else
            {
                word_node->next = hashtable[bucket]->next;
                hashtable[bucket]->next = word_node;
            }
            
        }
        
        DICT_SIZE++;
        
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (DICT_SIZE > 0)
    {
        return DICT_SIZE;
    }
    
    else
    {
        return 0;
    }
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    unsigned int bucket = hash(word);
    struct node *current_node = hashtable[bucket];
    char word_lower[LENGTH + 1];
    strcpy(word_lower, word);
    
    // convert word to lowercase
    for (int i = 0; i < strlen(word_lower); i++)
    {
        word_lower[i] = tolower(word_lower[i]);
    }

    while (current_node != NULL)
    {
        // check if word is in current node
        if (strcmp(current_node->word, word_lower) == 0)
        {
            return true;
        }
        
        // else, go to next node in list
        else
        {
            current_node = current_node->next;
        }
    }
    
    // if word not found, return false
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    struct node *cursor, *temp;
    
    // iterate over hastahble entries
    for (int i = 0; i < N; i++)
    {
        cursor = hashtable[i];
        
        // traverse linked list, freeing each node's memory
        while (cursor != NULL)
        {
            temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    
    return true;
}
