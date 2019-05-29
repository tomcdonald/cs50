# Questions

## What's `stdint.h`?

`stdint.h` is a header file in the C standard library which contains a number of exact width integer types.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

Using integers of specified length is useful for memory management and also to ensure that code runs smoothly across different systems which may have a different interpretation of how many bits `int` should contain, for example. Unsigned integers are useful if negative numbers will not be necessary as they increase the possible range of values the integer can take; i.e. `−32,768 <= int16_t <= +32,767` whereas `0 <= uint16_t <= +65,536`.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4 and 2.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

"BM" in ASCII encoding, or "0x42 0x4D" in hexadecimal.

## What's the difference between `bfSize` and `biSize`?

The former is the size, in bytes, of the bitmap file, whilst the latter is the size, in bytes, of the `BITMAPINFOHEADER` structure.

## What does it mean if `biHeight` is negative?

It indicates a 'top-down' DIB (device independent bitmap), so the origin/beginning of file is in the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount`

## Why might `fopen` return `NULL` in `copy.c`?

If an incorrect filepath has been passed as a command-line argument, so `fopen` isn't able to open a file.

## Why is the third argument to `fread` always `1` in our code?

This argument specifies how many elements of "size = second argument" should be read from the file and stored in memory. As we always specify exactly the amount of bytes we want to read (e.g. `sizeof(BITMAPINFOHEADER)`), the third argument can stay as `1` as we only need to read this number of elements once.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

`int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;`, therefore padding = (4 - (3*3)%4) % 4 = 3.

## What does `fseek` do?

`fseek` sets the current position to be a specific number of elements from a given position through the file. In `copy.c`, `fseek` moves a number of elements `padding` past the current position `SEEK_CUR` in order to skip over any padding. 

## What is `SEEK_CUR`?

`SEEK_CUR` simply finds the current position of the file pointer.
