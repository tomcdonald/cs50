#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;
int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // check for valid input
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image");
        return 1;
    }
    
    FILE *file = fopen(argv[1], "r");
    FILE *img = NULL;
    
    // get file size
    fseek(file, 0L, SEEK_END);
    int size = ftell(file);
    rewind(file);
    
    int num_jpegs = 0;

    for (int i = 0; i < size / BLOCK_SIZE; i++)
    {
        BYTE buffer[BLOCK_SIZE];
        fread(&buffer, BLOCK_SIZE, 1, file);

        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            // close current file if open
            if (img != NULL)
            {
                fclose(img);
            }
            num_jpegs++;
            
            // format new output file
            char filename[8];
            sprintf(filename, "%03i.jpg", num_jpegs);
            img = fopen(filename, "w");
            fwrite(&buffer, sizeof(buffer), 1, img);
        }
        
        else if (num_jpegs > 0)
        {
            fwrite(&buffer, sizeof(buffer), 1, img);
        }

    }
    printf("%i .jpeg files present.\n", num_jpegs);
    
    fclose(file);
    fclose(img);
    return 0;
}
