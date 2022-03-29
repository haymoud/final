import os

import stripe
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, abort
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# config app
app = Flask(__name__)

#config the payment
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51KfRapEfTM98bLzdV4Nyz0c8l1tNq99vY8pvuatlqiPkK3F2MqvDiDgJYYRfgst3wznFtaH6eBxDXedbLvHFWfkb00cY0A7le0'

app.config['STRIPE_SECRET_KEY'] = 'sk_test_51KfRapEfTM98bLzdyeB6jNHmWR2SJoZs9afhx9gLEeDXtuPq6EeQ8OSDXGfadVmBDaYwHT4h4ZmtzUQrkRheNaR300JzFJIcQq'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#style heroku
app.config.serve_static_assets = True
#gem 'rails_12factor', group: :production

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)




# login route
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
        return render_template("log.html")


# log out route
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # if request is via post
    if request.method == "POST":

        # user input
        user_name = request.form.get("username")
        pass_word = request.form.get("password")
        confirmation_pass = request.form.get("confirmation")


        if not user_name or not pass_word or not confirmation_pass:
            return apology("must have username and password")

        # check for duplicate usernames or dissimilarities passwords
        user_match = db.execute("SELECT * FROM users WHERE username = ?", user_name)

        if len(user_match) != 0:
            return apology("username exist")

        if pass_word != confirmation_pass:
            return apology("password not confirmed")

        # encrypt password
        hash_password = generate_password_hash(pass_word)

        # insert user to database
        db.execute("INSERT INTO  users (username, hash) VALUES(?, ?)", user_name, hash_password)

        # log the user in
        row = db.execute("SELECT * FROM users WHERE username = ?", user_name)
        session["user_id"] = row[0]["id"]
        return redirect("/")



    # if request is via get
    return render_template("register.html")



# main page
@app.route("/")
@login_required
def index():
    depart = db.execute("SELECT * FROM departement")
    return render_template("index.html", depart=depart)

# enter route
@app.route("/enter", methods=["POST"])
@login_required
def enter():
    id = request.form.get("id")
    departement = db.execute("SELECT name, empty_classroom FROM departement WHERE id = ?", id)
    emptyroom = int(departement[0]["empty_classroom"])
    return render_template("rooms.html", departement=departement, id=id, emptyroom=emptyroom)


# take a classroom
@app.route("/take_room", methods=["POST"])
def take_room():
    iddepartement = request.form.get("iddepartement")

    return render_template("reservation.html", iddepartement=iddepartement)


# reservation
@app.route("/reservation", methods=["POST"])
@login_required
def reservation():
    # make sure the user type a room name
    if not request.form.get("salle"):
        return apology("you must enter a name")

    # user form
    nameroom = request.form.get("salle")
    iddepartement = request.form.get("iddepartement")

    # date of reservation
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # update number of empty class room and insert room information to data base
    number_empty_room = int(db.execute("SELECT empty_classroom FROM departement WHERE id = ?", iddepartement)[0]["empty_classroom"])
    if number_empty_room <= 0:
        return apology("there is no room left")

    try:
        db.execute("INSERT INTO classroom (id_depart, name_room, date) VALUES(?, ?, ?)", iddepartement, nameroom, date_now)
    except:
        return apology("name exist")

    db.execute("UPDATE departement SET empty_classroom = ? WHERE id = ? ",number_empty_room - 1, iddepartement)

    rows = db.execute("SELECT name, name_room, date FROM departement INNER JOIN classroom ON id = id_depart")
    return render_template("token_rooms.html", rows=rows,iddepartement=iddepartement)

# delete room
@app.route("/delete", methods=["POST"])
@login_required
def delete():

    # delete the room from token room
    nameroom = request.form.get("nameroom")
    namedepartement = request.form.get("namedepartement")
    if nameroom and namedepartement:
        # delete the room
        db.execute("DELETE FROM classroom WHERE name_room = ?", nameroom)

        #the empty room number
        number_empty_room = int(db.execute("SELECT empty_classroom FROM departement WHERE name = ?", namedepartement)[0]["empty_classroom"])

        #update the empty room number
        db.execute("UPDATE departement SET empty_classroom = ? WHERE name = ? ",number_empty_room + 1, namedepartement)
        return redirect("/")
    else:
        return apology("sorry")


# all room reserved
@app.route("/salles")
@login_required
def salle():
    rows = db.execute("SELECT name, name_room, date FROM departement INNER JOIN classroom ON id = id_depart")
    return render_template("token_rooms.html", rows=rows)


# emphies
@app.route("/emphies")
@login_required
def emphies():
    rows = db.execute("SELECT * FROM emphies")

    return render_template("emphie.html", rows=rows)

#Add an 'amphie'
@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method == "POST":

        name = request.form.get("emphie")
        if not name:
            return apology("must have a name")

        capacity = request.form.get("capacite")
        try:
            capacity = int(capacity)
        except:
            return apology("use an inetger")

        db.execute("INSERT INTO emphies (name, capacity) VALUES(?,?)", name, capacity)

        return redirect("/emphies")

    else:
        return render_template("addemphie.html")

# reserve or free an enphie

@app.route("/libre_reseve", methods=["POST"])
@login_required
def libre_reseve():

    id = request.form.get("id")
    if not id:
        return apology("must have an id")
    # if the state is libre then reserve it else free it
    state = db.execute("SELECT state FROM emphies WHERE id = ?", id)[0]["state"]

    if state == 'libre':
        db.execute("UPDATE emphies SET state = ? WHERE id = ?", 'reservee', id)
    else:
        db.execute("UPDATE emphies SET state = ? WHERE id = ?", 'libre', id)

    return redirect("/emphies")



# delete en emphie
@app.route("/delete_emphie", methods=["POST"])
@login_required
def delete_enphie():

    # delete en emphie from the data base
    id = request.form.get("id")
    if not id:
        return apology("must have an id")

    db.execute("DELETE FROM emphies WHERE id = ?", id)

    return redirect("/emphies")


# menage the trip to the faculty

@app.route("/bus", methods=["GET","POST"])
@login_required
def bus():
    if request.method == "GET":
        rows = db.execute("SELECT name FROM station")
        return render_template("bus.html", rows=rows)

    else:
        s = request.form.get("station")
        if not s:
            return apology("must shoose a station")

        # only two station
        if s == "BMD":

            # the begining and the end of the trip to the faculty
            trips = ["8h_8h.30m","10h_10h.30m","17h_17h.30m"]
            return render_template("bus.html",trips=trips)

        else:
            trips = ["8h_9h","10h_11h","17h_18h"]
            return render_template("bus.html",trips=trips)


# payment route

@app.route("/payment", methods=["POST","GET"])
@login_required
def payment():
    if request.method == "GET":
        return render_template("payment.html")

    else:

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1KflUnEfTM98bLzdJa0NpwPl',
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('bus', _external=True),
        )

        return render_template(
            'payment.html',
            checkout_session_id=session['id'],
            checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
        )


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
