#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <string.h>

const string LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\0";
const int NUM_LETTERS = 53;

int main(int argc, string argv[])
{    // Checking command-line argument given and retrieving length
    string hash;
    int hash_len = strlen(argv[1]);
    if(argc == 2)
    {
        hash = argv[1];
    }
    else
    {
        printf("Usage: ./crack hashed-password\n");
        return(1);
    }
    // Copying first two characters of hash to 'salt' variable
    char salt[3];
    memcpy(salt, hash, 2);
    salt[2] = '\0'; 
    // Brute force algorithm to search for password 
    char password[6] = "\0\0\0\0\0\0";
    for(int i = 0; i < NUM_LETTERS; i++)
    {
        for(int j = 0; j < NUM_LETTERS; j++)
        {
            for(int k = 0; k < NUM_LETTERS; k++)
            {
                for(int l = 0; l < NUM_LETTERS; l++)
                {
                    for(int m = 0; m < NUM_LETTERS; m++)
                    {
                        password[0] = LETTERS[m];
                        password[1] = LETTERS[l];
                        password[2] = LETTERS[k];
                        password[3] = LETTERS[j];
                        password[4] = LETTERS[i];
                        
                        if(strcmp(crypt(password, salt), hash) == 0)
                        {
                            printf("%s\n", password);
                            return(0);
                        }
                    }
                }
            }
        }
    }
}
