import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///job.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username", "yellow")
            return redirect('/login')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", "yellow")
            return redirect('/login')

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password", "yellow")
            return redirect('/login')
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
        # return redirect('/here')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # get data through post
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        acc_type = request.form.get("acc_type")
        hash = generate_password_hash(password)
        # empty username, password,confirmation
        if not request.form.get("username"):
            flash("must provide username", "yellow")
            return redirect('/register')

        elif not request.form.get("password"):
            flash("must provide password", "yellow")
            return redirect('/register')

        elif not request.form.get("confirmation"):
            flash("must provide confirmation", "yellow")
            return redirect('/register')

        if password != confirmation:
            flash("must provide username", "yellow")
            return redirect('/register')

        rows=db.execute("SELECT * FROM users WHERE username=?",username)
        session["user_id"]=rows[0]["id"]
        
        try:
            db.execute("INSERT INTO users (username,hash, acc_type) VALUES (? ,? ,?)",
                       username, hash, acc_type)
            if acc_type=="worker":
                return redirect("/worker")
            elif acc_type=="client":
                return redirect("/client")
        except:
            flash("Username already exists", "yellow")
            return redirect('/register')
        
        return render_template("admin.html")
    else:
        # User reached route via POST (as by submitting a form via GET)
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# @app.route("/admin", methods=["GET", "POST"])
# @login_required
# def admin():
#     answer = request.args.get("answer")
#     if answer == "clientdetails":
#         return render_template("clientdetails.html")
#     elif answer == "workerdetails":
#         return render_template("workerdetails.html")
#     elif answer == "approve":
#         return render_template("approve.html")
    # else:
    #     return render_template("admin.html")

@app.route("/worker")
def worker():
    return render_template("worker.html")

@app.route("/client" , methods=["GET", "POST"] )
# @login_required
def client():
    
    if request.method == "POST":
        # id=session["user_id"]
        name=request.form.get("name")
        email=request.form.get("email")
        contact=request.form.get("contact")
        location=request.form.get("location")
        db.execute("INSERT INTO client (name, email, contact, location) VALUES (?, ? ,? ,?)",
                       name, email, contact, location)
        return render_template("index.html")
    else :            
        return render_template("client.html")   