import os
from typing import Optional
from flask import Flask, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, Column, select
import sqlite3
import re

# Create the app
app = Flask(__name__)

# Configure SQLite database path explicitly
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy extension
db = SQLAlchemy(app)

with app.app_context():
    db.reflect()

# From the default bind key
class Rocket(db.Model):
    __table__ = db.metadata.tables["rocket"]

class Mission(db.Model):
    __table__ = db.metadata.tables["mission"]

class Location(db.Model):
    __table__ = db.metadata.tables["location"]

class Joint(db.Model):
  __table__ = db.metadata.tables['joint']
  __mapper_args__ = {
      'primary_key': [
          db.metadata.tables['joint'].c.rocket_ID,
          db.metadata.tables['joint'].c.location_ID,
      ]
  }


@app.route('/')
def home():
    return render_template('home.html', results=None)

@app.route('/about')
def about():
    return render_template('about.html', results=None)

@app.route('/credits')
def credits():
    return render_template('credits.html', results=None)

@app.route('/form')
def form():
    return render_template('form.html', results=None)
    
@app.route('/rockets')
def get_rockets():
    stmt = select(Rocket)
    rockets = db.session.scalars(stmt).all()
    return render_template('rockets.html', rockets=rockets)

@app.route("/rocket/<int:id>")
def single_rocket(id):
    stmt = select(Rocket).where(Rocket.rocket_ID == id)
    rocket_item = db.session.execute(stmt).scalar_one_or_none()
    if rocket_item is None:
        abort(404)
    return render_template('rocket_detail.html', rocket=rocket_item)

@app.route('/missions')
def get_missions():
    missions = db.session.execute(select(Mission)).scalars().all()
    return render_template('missions.html', missions=missions)

@app.route("/mission/<int:id>")
def single_mission(id):
    stmt = select(Mission).where(Mission.mission_ID == id)
    mission_item = db.session.execute(stmt).scalar_one_or_none()
    if mission_item is None:
        abort(404)
    return render_template('mission_detail.html', mission=mission_item)

@app.route('/locations')
def get_locations():
    locations = db.session.execute(select(Location)).scalars().all()
    return render_template('location.html', locations=locations)

@app.route("/location/<int:id>")
def single_location(id):
    stmt = select(Location).where(Location.location_ID == id)
    location_item = db.session.execute(stmt).scalar_one_or_none()
    if location_item is None:
        abort(404)
    return render_template('location_detail.html', location=location_item)

@app.route('/joints')
def get_joints():
  joints = db.session.execute(select(Joint)).scalars().all()
  return render_template('joint.html', joints=joints)

def test_input(data):
    """Equivalent to PHP's trim() / sanitization logic."""
    return data.strip() if data else ""

@app.route("/submit", methods=["GET", "POST"])
def submit_form():
    errors = {
        "firstNameErr": "",
        "lastNameErr": "",
        "emailErr": "",
        "commentErr": "",
    }
    form_data = {"firstName": "", "lastName": "", "email": "", "comment": ""}

    if request.method == "POST":
        first_name_input = request.form.get("first_name", "")
        if not first_name_input:
            errors["firstNameErr"] = "First Name is Required"
        else:
            form_data["firstName"] = test_input(first_name_input)
        if not re.match(
             r"^[a-zA-Z\-' ]*$", form_data["firstName"]
            ):
                errors["firstNameErr"] = "Only letters and white space allowed"

            # Validate the last name
        last_name_input = request.form.get("last_name", "")
        if not last_name_input:
            errors["lastNameErr"] = "Last Name is Required"
        else:
            form_data["lastName"] = test_input(last_name_input)
            if not re.match(r"^[a-zA-Z\-' ]*$", form_data["lastName"]):
                errors["lastNameErr"] = "Only letters and white space allowed"

                # Validate the email
        email_input = request.form.get("email", "")
        if not email_input:
            errors["emailErr"] = "Email Address is Required"
        else:
            form_data["email"] = test_input(email_input)
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, form_data["email"]):
                errors["emailErr"] = "Invalid Email format"

        comment_input = request.form.get("comment", "")
        if not comment_input:
            errors["commentErr"] = "Comments are Required"
        else:
            form_data["comment"] = test_input(comment_input)

        if not any(errors.values()):
                    return render_template("form.html", form_data=form_data)

    return render_template("result.html", errors=errors, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)
