#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int valid_string(string input);

int main(int argc, string argv[])
{   
    int key;
    if (argc == 2 && valid_string(argv[1]) == 0)
    {
        key = atoi(argv[1]);
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return(1);
    }
    
    string plaintext = get_string("plaintext: ");
    int pt_len = strlen(plaintext);
    for(int i = 0; i <= pt_len; i++)
    {
        char letter = plaintext[i];
        if(isupper(letter))
        {
            printf("%c" , ((letter - 65 + key) % 26) + 65);
        }
        else if(islower(letter))
        {
            printf("%c" , ((letter - 97 + key) % 26) + 97);
        }
        else
        {
            printf("%c" , letter);
        }
    }
    printf("\n");
}

int valid_string(string input)
{
    int key_length = strlen(input);
    for(int i = 0; i < key_length; i++)
    {
        if(isdigit(input[i]) == 0)
        {
            return(1);
        }
    }
    return(0);
}
