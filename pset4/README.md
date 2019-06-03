## CS50 Problem Set 4
This week's lecture and pset focused heavily on data structures and techniques
for dynamically allocating data, such as linked lists, hash tables, trees and
tries, as well as introducing makefiles and diagnosing memory leaks.

* **Speller**

> `speller.c` is a script which when run, will spell-check a .txt file by
implementing various functions defined within `dictionary.c`. `load()` loads 
a dictionary of words into memory, `size()` returns the size of said
dictionary, `unload()` removes the dictionary from memory and finally,
`check()` iterates through a text file and cross references each word with
the dictionary, marking it as misspelled if it is not present in the
dictionary.

> The algorithm is case insensitive as it converts every word in the input text
file to lower case, and the hash table used to store the dictionary in memory
uses a modified djb2 hash function (sourced from [here](https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c)) with $2^{16}$ buckets, 
resulting in good performance compared to the basic 27 bucket hash function 
originally provided.

> Within this folder are a sample dictionary (`large`) and text file
(`lalaland.txt`).
