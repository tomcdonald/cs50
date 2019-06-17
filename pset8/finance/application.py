import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from collections import Counter

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    query_str = ('SELECT symbol, SUM(num_stocks) FROM transactions '
                 'WHERE id = :id GROUP BY symbol HAVING SUM(num_stocks) > 0')
    stocks_list = db.execute(query_str, id=session.get("user_id"))
    stocks = []
    
    # Creating lookup list of dicts for HTML table on homepage
    for stock in stocks_list:
        num_stocks = stock['SUM(num_stocks)']
        symbol = stock['symbol']
        price = lookup(symbol)['price']
        value = lookup(symbol)['price'] * float(num_stocks)
        stock_dict = {'symbol': symbol, 
                      'num_stocks': num_stocks,
                      'price': price,
                      'value': value}
        stocks.append(stock_dict)
    
    # Getting current balance from user's account
    balance_query = 'SELECT cash FROM users WHERE id = :id'
    balance = db.execute(balance_query, id=session.get("user_id"))
    balance = balance[0]['cash']
    
    # Using counter to sum total value across all the stock dicts
    c = Counter()
    for d in stocks:
        c.update(d)
    total_value = c['value'] + balance
    
    ##:( buy handles valid purchase
    # application raised an exception (see log for details) 
    #
    # Log 
    # sending POST request to /login 
    # sending POST request to /buy 
    # exception raised in application: TypeError: unsupported format string passed to Undefined.__format__ ########################################
    
    return render_template("index.html", stocks=stocks, balance=balance,
                           total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    
    # User reached route via GET
    if request.method == 'GET':
        return render_template('buy.html')
     
    # Error checking on inputs
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        if not symbol or not shares:
            return apology('enter a symbol and number of shares', 400)
            
        if lookup(symbol) == None:
            return apology('invalid stock symbol', 400)
            
        try:
            shares = int(shares)
            if shares < 0:
                return apology('enter a positive number of shares', 400)
        except:
            return apology('invalid shares input', 400)
            
        # Calculate cost of order
        price = lookup(symbol)['price']
        cost = shares*price
        
        # Queries for checking funds and logging transaction/updating balance
        funds_query = 'SELECT cash FROM users WHERE id = :id;'
        transaction_query = ('INSERT INTO transactions(id, symbol, num_stocks, '
                             'stock_price, total_cost, timestamp) VALUES(:id, '
                             ':symbol, :num_stocks, :stock_price, :total_cost, '
                             ':timestamp);') 
        withdrawal_query = ('UPDATE users SET cash = :cash WHERE '
                            'id = :id;')
        cash = db.execute(funds_query, id=session.get("user_id"))
        new_balance = list(cash[0].values())[0] - cost
        
        # Only completing the purchase if funds available
        if new_balance > 0:
            db.execute(withdrawal_query, cash=new_balance, 
                       id=session.get("user_id"))
            db.execute(transaction_query, id=session.get("user_id"),
                       symbol=symbol, num_stocks=shares, stock_price=price, 
                       total_cost=cost, timestamp=datetime.now())
                       
        else:
            return(apology('insufficient funds', 400))
            
        return redirect("/")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    
    # Accept via GET, a username
    username = request.args.get('username')
    
    # Return this username if it's already in the DB
    check_str = 'SELECT username FROM users WHERE username = :username'
    usernames = db.execute(check_str, username=username)

    # If username present and not in DB, return true, else return false
    if username and not usernames:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    
    # Getting transaction data
    query_str = ('SELECT symbol, num_stocks, stock_price, timestamp FROM '
                 'transactions WHERE id = :id')
    transactions = db.execute(query_str, id=session.get("user_id"))

    return render_template('history.html', transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # User reached route via GET
    if request.method == 'GET':
        return render_template('quote.html')
    
    # User reached route via POST (i.e. submitting the form)
    else:
        symbol = request.form.get("symbol")
        
        # Ensure a symbol was specified
        if not symbol or not lookup(symbol):
            return apology("must provide a valid stock symbol", 400)
        
        quote = lookup(symbol)
        price = usd(quote['price'])
        return render_template("quoted.html", quote=quote, price=price)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # User reached route via POST (i.e. submitting the form)
    if request.method == 'POST':
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = request.form.get("username")
        
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)
    
        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password", 400)
            
        # Ensure password and re-entered password match
        elif password != confirmation:
            return apology("passwords do not match", 400)
        
        # Server-side checking if username exists
        check_str = 'SELECT username FROM users WHERE username = :username'
        usernames = db.execute(check_str, username=username)
        
        if not usernames:
            register_str = ('INSERT INTO users(username, hash) '
                            'VALUES(:username, :hash);')
            db.execute(register_str, username=username, 
                       hash=generate_password_hash(password))
            return redirect('/')
        else:
            return apology("username already exists", 400)
    
    # User reached route via GET
    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    
    # Get stocks owned by user
    stock_query = 'SELECT DISTINCT symbol FROM transactions WHERE id = :id;'
    available_stocks = db.execute(stock_query, id=session.get("user_id"))
    stocks_held = [d['symbol'] for d in available_stocks]
    
    # User reached route via GET
    if request.method == 'GET':
        return render_template("sell.html", stocks_held=stocks_held)
        
    # Else, user submitting POST form to sell stock
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        if not symbol or not shares:
            return apology('enter a symbol and number of shares', 400)
            
        if lookup(symbol) == None:
            return apology('invalid stock symbol', 400)
            
        try:
            shares = int(shares)
            if shares < 0:
                return apology('enter a positive number of shares', 400)
        except:
            return apology('invalid shares input', 400)
            
        # Calculate value of stocks
        price = lookup(symbol)['price']
        value = shares*price
        
        # Queries for checking funds, stocks & updating transactions/balance
        funds_query = 'SELECT cash FROM users WHERE id = :id;'
        stocks_query = ('SELECT SUM(num_stocks) FROM transactions WHERE '
                        'id = :id AND symbol = :symbol GROUP BY symbol;')
        transaction_query = ('INSERT INTO transactions(id, symbol, num_stocks, '
                             'stock_price, total_cost, timestamp) VALUES(:id, '
                             ':symbol, :num_stocks, :stock_price, :total_cost, '
                             ':timestamp);') 
        deposit_query = ('UPDATE users SET cash = :cash WHERE id = :id;')
                     
        stocks = db.execute(stocks_query, id=session.get("user_id"), 
                            symbol=symbol)
        new_stocks = list(stocks[0].values())[0] - shares
        cash = db.execute(funds_query, id=session.get("user_id"))
        new_balance = list(cash[0].values())[0] + value
        
        # Only completing the purchase if stocks available
        if new_stocks >= 0:
            db.execute(deposit_query, cash=new_balance, 
                       id=session.get("user_id"))
            db.execute(transaction_query, id=session.get("user_id"),
                       symbol=symbol, num_stocks=(- shares), stock_price=price,
                       total_cost=value, timestamp=datetime.now())
                       
        else:
            return(apology('insufficient stocks', 400))
            
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
