// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize f infile outfile\n");
        return 1;
    }

    // remember filenames
    int f = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];
    
    if (f < 1 || f > 100)
    {
        fprintf(stderr, "Invalid factor, f must be in (0.00, 100.0]");
        return 2;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf_in, bf_out;
    fread(&bf_in, sizeof(BITMAPFILEHEADER), 1, inptr);
    bf_out = bf_in;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi_in, bi_out;
    fread(&bi_in, sizeof(BITMAPINFOHEADER), 1, inptr);
    bi_out = bi_in;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf_in.bfType != 0x4d42 || bf_in.bfOffBits != 54 || bi_in.biSize != 40 ||
        bi_in.biBitCount != 24 || bi_in.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }

    // modify BITMAPFILEHEADER AND BITMAPFILEINFO and determine padding
    bi_out.biWidth = floor(bi_in.biWidth * f);
    bi_out.biHeight = floor(bi_in.biHeight * f);
    int input_padding = (4 - (bi_in.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int output_padding = (4 - (bi_out.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    bi_out.biSizeImage = ((bi_out.biWidth * sizeof(RGBTRIPLE)) + output_padding) * abs(bi_out.biHeight);
    bf_out.bfSize = bf_in.bfSize - bi_in.biSizeImage + bi_out.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_out, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_out, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    // define some useful variables
    int input_width = bi_in.biWidth;
    int input_height = abs(bi_in.biHeight);
    int output_width = bi_out.biWidth;
    int output_height = abs(bi_out.biHeight);
    
    // iterate over infile's scanlines
    for (int in_row = 0; in_row < input_height; in_row++)
    {
        // temporary storage
        RGBTRIPLE triple;

        for (int i = 0; i < (output_width / input_width); i++)
        {
            fseek(inptr, 54 + ((in_row * input_width * sizeof(triple)) + (input_padding * in_row)), SEEK_SET);
        
            // iterate over pixels in scanline
            for (int in_col = 0; in_col < input_width; in_col++)
            {
                // read triple from input file
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                
                // write RGB triple to outfile
                for (int k = 0; k < (output_height / input_height); k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr); 
                }       
            }
            
            // add padding to line
            for (int m = 0; m < output_padding; m++)
            {
                fputc(0x00, outptr);
            }
        }
    }
        
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
