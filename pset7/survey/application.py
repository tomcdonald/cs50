import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    err = 'Please fill out all fields!'
    name = request.form.get('name')
    sport = request.form.get('sport')
    frequency = request.form.get('frequency')

    if not name or not sport or not frequency:
        return render_template("error.html", message=err)
    else:
        with open('answers.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow((name, sport, frequency))
        return redirect('/sheet')
        
        
@app.route("/sheet", methods=["GET"])
def get_sheet():
    try:
        with open('answers.csv', 'r') as file:
            reader = csv.reader(file)
            answers = list(reader)
        return render_template("sheet.html", answers=answers)
    except:
        return render_template("error.html", message='No responses yet.')