## CS50 Problem Set 8
The final problem set builds on pset7, diving deeper into web development with 
Flask, covering topics such as using SQLite3 databases to store user data 
on the backend of the site. Various SQL queries to access this data were 
covered, as well as well-known issues with databases such as race conditions 
and SQL injection attacks, and how to guard against them.

* **Finance**
`finance/` contains a web application built using Flask which simulates an 
online stock trading platform. Users can register for an account and purchase 
stocks in real time based on stock prices pulled from an API. Users can then 
sell their stocks at a later time to turn a profit. All of this functionality 
is fleshed out within `application.py`, with a small number of helper 
functions in `helpers.py`. Typically when working with money, decimals should 
be used instead of floats due to the imprecision of floats (using the 
`decimal` module for example), however the CS50 helper function `usd()` 
takes floats as it's argument, therefore I had to use floats. In practice, 
I'd take the former approach. One other point of note is that the API 
suggested by the course docs was shutdown on 15/06/2019, therefore I sourced 
an alternative API which similarly didn't require a token, which can be 
found [here](https://financialmodelingprep.com).