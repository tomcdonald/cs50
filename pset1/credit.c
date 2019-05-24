#include <stdio.h>
#include <cs50.h>

void luhn_algo(long number);

int main(void)
{
    long number = get_long("Enter credit card number: ");
    luhn_algo(number);
}

void luhn_algo(long number)
{    
    // Get length of number
    int length = 0;
    long number_copy = number;
    while(number_copy > 0)
    {
        number_copy /= 10;
        length++;
    }
    // Iterate through digits from the end of the number
    for(int i = 0; i < length; i++)
    {    
        long divisor = 1;
        long digit = (number / divisor) % 10;
        divisor *= 10;
        if(i % 2)    
        {    
            long product = digit * 2;
            printf("%ld\n", product);
        }
    }
}
