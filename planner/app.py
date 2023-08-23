from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Import datetime to use for configuring "Week at a glance" weekly calendar
# The time shown, when run on flask in githubs vscode, shows wrong timzone. I think it might be because this vscode is cloudbased.
# I account for the time difference by subtracting 5 hours
import datetime as d

# Adopted code from CS50 finance for implementation of "navbar" layout template, login, logout, apology, and register features
from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database (planner.db)
db = SQL("sqlite:///planner.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Shows a homepage with a To-Do list and a Weekly Calendar for the current week"""
    if request.method == "POST":
        # This form is used to remove items from the To-Do list when finished with the task, button removes task from to-do list
        db.execute("DELETE FROM todo WHERE id = ? AND user_id = ?", request.form.get("remove"), session["user_id"])
        return redirect("/")
    else:
        # The items variable stores a dictionary of tasks from the todo list that is saved in the database for the logged user
        # This variable is passed into render_template so that jinja can display the items on the "To-Do List" table
        items = db.execute("SELECT id,task FROM todo WHERE user_id = ?", session["user_id"])

        # The imported datetime library, imported as d, is used to make date objects
        # In the variable tday, the current date's "date object" is stored
        tday = d.datetime.today() - d.timedelta(hours=5)

        # Weekday stores the day of the given date, tday, as an integer representing mon-0 to sunday-6
        weekday = tday.weekday()

        # Calculate the number of days from the current date to the beginning of the current week and the end of the current week
        # Shift the week from monday-sunday to sunday-saturday by adding +1 to the distance from the start and subtracting from 5 instead of 6
        schange = d.timedelta(days=(weekday + 1))
        echange = d.timedelta(days=(5 - weekday))

        # Calculate the start and end dates of the week and convert to string format yyyy-mm-dd, store in variables start, end
        start = (tday - schange).strftime("%Y-%m-%d")
        end = (tday + echange).strftime("%Y-%m-%d")

        # Run sql query to find all events within the current week, using start and end, and store inside variable wevents
        wevents = db.execute("SELECT * FROM events WHERE user_id = ? AND date BETWEEN ? and ?", session["user_id"], start, end)

        # Variable listDays stores each date of the week from sunday-saturday
        # Variable tclass lists the strings ntday or tday depending on whether the weekday is today's weekday, this is to be used as classes in html
        listDays = []
        tclass = []
        for i in range(7):
            listDays.append(((tday - schange) + d.timedelta(days=i)).strftime("%Y-%m-%d"))
            if i != (weekday + 1):
                tclass.append("ntday")
            else:
                tclass.append("tday")

        # Render the file index.html and pass in the variables [items, wevents, listDays, tclass] for jinja
        return render_template("index.html", items=items, wevents=wevents, listDays=listDays, tclass=tclass)


@app.route("/todo", methods=["GET", "POST"])
def todo():
    """ A form on the index.html page that adds tasks to the todo database and list """

    if request.method == "POST":

        # Form validation, make sure there is a task inputted
        if not request.form.get("task"):
            return apology("must provide task", 403)

        # Insert the task on the form into the todo database
        db.execute("INSERT INTO todo (user_id, task) VALUES (?, ?)", session["user_id"], request.form.get("task"))
        return redirect("/")

    # Render a seperate html page with a todo form
    else:
        return render_template("todo.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """register user"""
    if request.method == "POST":
        # Form validation
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide same password again", 400)

        # Matching passwords
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # SQL query to check if username exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("username already exists", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))

        # Log new user in and send the user to the homepage
        session["user_id"] = (db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")))[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    """Find events within a given range of dates, could just be one date as well"""
    if request.method == "POST":

        #Form validation: make sure that the input fields are filled before submission
        if not request.form.get("date1") or not request.form.get("date2"):
            return apology("must enter both dates", 400)

        # Get a list of events within the range of dates and render eventList page with events passed in
        events = db.execute("SELECT * FROM events WHERE date BETWEEN ? AND ?", request.form.get("date1"), request.form.get("date2"))
        return render_template("eventList.html", events=events)

    # Render the schedule.html page for the get request
    else:
        return render_template("schedule.html")


@app.route("/eventList", methods=["POST"])
@login_required
def eventList():
    """Add a remove button to events on the eventsList page to remove from database"""

    # Run sql command to remove event item from database and redirect to homepage
    db.execute("DELETE FROM events WHERE id = ? AND user_id = ?", request.form.get("remove"), session["user_id"])
    return redirect("/")


@app.route("/addEvent", methods=["GET", "POST"])
@login_required
def addEvent():
    """Form to add an event to the database"""
    if request.method == "POST":

        # Form validation: the title and date must be filled out, description is not neccesary and is optional
        if not request.form.get("title") or not request.form.get("date"):
            return apology("must enter title and date (description optional)", 400)

        # Get values from form fields
        title = request.form.get("title")
        date = request.form.get("date")
        desc = request.form.get("description")

        # Create a date object from the date given in the form using datetime, and store its weekday value in the variable day
        day = d.datetime.strptime(date, '%Y-%m-%d').weekday()

        # Insert the form values and day of the week into the database table events and redirect to homepage
        db.execute("INSERT INTO events (user_id, title, date, details, day) VALUES (?, ?, ?, ?, ?)", session["user_id"], title, date, desc, day)
        return redirect("/")

    # Render the addEvent.html page for get requests
    else:
        return render_template("addEvent.html")


@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():
    """A page to display journal entries and enter journal entries"""
    if request.method == "POST":

        # Form validation: there must be something in the input fields for the joural entry form
        if not request.form.get("entry"):
            return apology("must enter a journal entry", 400)

        # SQL command to store journal entry in database and redirect to journal entries page
        db.execute("INSERT INTO journal (user_id, entry) VALUES (?, ?)", session["user_id"], request.form.get("entry"))
        return redirect("/journal")

    # If the method is get, select all journal entries by user from the database and display them to the user
    else:
        entries = db.execute("SELECT date, entry FROM journal WHERE user_id = ?", session["user_id"])
        return render_template("journal.html", entries=entries)
