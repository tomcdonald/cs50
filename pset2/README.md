## CS50 Problem Set 2
This problem set and lecture introduced compiling & debugging, handling
memory and arrays, the concept of strings simply being a pointer to an
address, command line arguments, exit codes and sorting.

* **Caesar**
`caesar.c` is a script which takes a plaintext string as input and converts
it to ciphertext using a simple 'Caesar' cipher whereby each letter in the
string is shifted along by one place in the alphabet. Punctuation and special
characters are unchanged and case is preserved.

* **Mario**
`crack.c` is a script which takes a hashed password as input, which has been
hashed using the `crypt()` function from `<crypt.h>`, and then implements
a brute force algorithm to iterate through possible passwords and crack the
hashed password. It supports a maximum password length of 5 characters.