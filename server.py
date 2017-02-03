"""Movie Ratings."""

from jinja2 import StrictUndefined

#from flask import Flask, jsonify
from flask import jsonify

from flask_debugtoolbar import DebugToolbarExtension

#from model import connect_to_db, db

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    a = jsonify([1,3])
   
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/registration", methods=["GET"])
def registeration_form():
    """User sign in form"""


    
    return render_template("registration_form.html")

@app.route("/registration", methods=["POST"])
def registeration_process():
    """Add user to database"""

    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    zipcode = request.form["zipcode"]
   
    new_user = User(email=email, password=password,
                    age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("New user is added")

    return redirect("/")

@app.route("/login", methods=["GET"])
def login_form():
    """User login in form"""


    return render_template("login_form.html")

@app.route("/login", methods=["POST"])
def login_form_process():
    """User login in form"""

    email = request.form["email"]
    #print email
    password = request.form["password"]
    #print password

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User doesn't exist")
        return redirect("/login")
    
    if user.password != password:
        flash("Please enter correct password")
        return redirect("/login")

    session["user_id"]=user.user_id
    flash("Logged in")

    return redirect("/user/%s" % user.user_id)

@app.route("/logout", methods=["GET"])
def logout_form():
    """User login in form"""

    del session["user_id"]
    
    flash("You have logged out successfully")

    return redirect("/")

@app.route("/user/<user_id>", methods=["GET"])
def user_info(user_id):
    """User page"""

    user = User.query.get(user_id)
    print "Sri was here"
    return render_template("user.html", user=user)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5001, host='0.0.0.0')
