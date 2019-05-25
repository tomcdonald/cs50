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
    long divisor = 1;
    long final_sum = 0;
    long digit;
    long prev_digit;
    for(int i = 0; i < length; i++)
    {    
        prev_digit = digit;
        digit = (number / divisor) % 10;
        divisor *= 10;
        // For every other digit starting from 2nd to last, multiply by two and add digits of product
        if(i % 2)    
        {    
            long product = digit * 2;
            long product_first_digit = product / 10;
            long product_second_digit = product % 10;
            final_sum += product_first_digit;
            final_sum += product_second_digit;
        }
        // For all remaining digits, add them to the total
        else
        {
            final_sum += digit;
        }
    }
    bool valid = (final_sum % 10 == 0);
    if(valid && length == 15 && digit == 3 && (prev_digit == 4 || prev_digit == 7))
    {
        printf("AMEX\n");
    }
    if(valid && length == 16 && digit == 5 && (prev_digit == 1 || prev_digit == 2 || prev_digit ==3 || prev_digit == 4 || prev_digit == 5))
    {
        printf("MASTERCARD\n");
    }
    if(valid && (length == 13 || length == 16) && digit == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
    printf("FINAL SUM: %ld\n", final_sum);
}
