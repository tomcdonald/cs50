## CS50 Problem Set 7
This problem set focused on using Python for web development, using the 
popular Flask framework. It introduced the MCV (Model-Controller-View) 
methodology, using Flask to render layout templates and generate HTML, 
working with variables from HTML forms in Python and JavaScript and ended 
with a discussion of the pros and cons of running code client and server-side.

* **Similarities**
`similarities/` contains a web application built using Flask which prompts the 
user to upload two files and select a comparison algorithm, and then returns 
a side-by-side output of the two files with similarities highlighted. The 
logic for the algorithms is contained within `helpers.py` (`lines` and 
`substrings` use just built in Python, whereas `sentences` uses NLTK), the 
application Flask code is held within `application.py` and all the HTML is 
stored in `templates/`.

* **Survey**
TODO
