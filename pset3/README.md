## CS50 Problem Set 3
This week's lecture and pset focused on using tools within an IDE such as 
debuggers and memory leak detection, string operations, further discussion of
pointers and memory allocation using `malloc()` and defining types/structs.

* **Whodunit**
`whodunit.c` is a script which takes a 'clue' in the form of a bitmap file
`clue.bmp` and manipulates the bits in such a way that the image colour changes 
and reveals "whodunit" in `verdict.bmp`.

* **Resize**
`resize.c` is a script which takes a bitmap file as input (`small.bmp` was used
as an example) and dependent on user input at the commmand line, resizes the
image by the given factor, outputting the new file as `resized.bmp`.

* **Recover**
`recover.c` is a script which takes a memory card file such as `card.raw` as
input, parses through the file's bytes and extracts all .jpeg files.