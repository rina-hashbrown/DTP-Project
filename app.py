# FLASK APPLICATION BACKEND (`app.py`)
#Purpose:
    #Serves as the main entry point and backend server for the Space Race Web Archive.
    #Handles database ORM reflection, route mappings, template rendering, and server-side 
    #form validation (migrated from PHP to Python).


import os
import re
import sqlite3
from typing import Optional

from flask import Flask, abort, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column

# 
# 1. APPLICATION & DATABASE CONFIGURATION
# 

# Initialize the Flask application instance
app = Flask(__name__)

# Configure absolute path to the local SQLite database file (`database.db`)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy extension bound to the Flask app
db = SQLAlchemy(app)

# Reflect existing database tables dynamically within the application context
with app.app_context():
    db.reflect()

# 
# 2. SQLALCHEMY ORM MODELS (DATABASE MAPPER)
# 

# Reflects the 'rocket' table from database.db
class Rocket(db.Model):
    __table__ = db.metadata.tables["rocket"]

# Reflects the 'mission' table from database.db
class Mission(db.Model):
    __table__ = db.metadata.tables["mission"]

# Reflects the 'location' table from database.db
class Location(db.Model):
    __table__ = db.metadata.tables["location"]

# Reflects the 'joint' junction table from databse.db.
class Joint(db.Model):
    __table__ = db.metadata.tables['joint']

# 
# 3. STATIC & INFORMATIONAL PAGE ROUTES
# 

@app.errorhandler(404)
def page_not_found(e):
    """Renders the 404 error."""
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Renders the 500 error."""
    return render_template('generror.html'), 500

@app.route('/')
def home():
    """Renders the Home page landing view."""
    return render_template('home.html', results=None)

@app.route('/about')
def about():
    """Renders the About page containing Space Race history & creator info."""
    return render_template('about.html', results=None)

@app.route('/credits')
def credits():
    """Renders Copyright, Legal Attributions, and Dataset references."""
    return render_template('credits.html', results=None)

@app.route('/form')
def form():
    """Renders the empty user question form."""
    return render_template('form.html', results=None)

# 
# 4. DATABASE COLLECTION & DETAIL ROUTES
# 

# --- ROCKET ROUTES ---
@app.route('/rockets')
def get_rockets():
    """Fetches all rocket records and renders the Rockets list view."""
    stmt = select(Rocket)
    rockets = db.session.scalars(stmt).all()
    return render_template('rockets.html', rockets=rockets)

@app.route("/rocket/<int:id>")
def single_rocket(id):
    """Fetches a specific rocket by ID; returns 404 error page if not found."""
    stmt = select(Rocket).where(Rocket.rocket_ID == id)
    rocket_item = db.session.execute(stmt).scalar_one_or_none()
    if rocket_item is None:
        abort(404)
    return render_template('rocket_detail.html', rocket=rocket_item)

# --- MISSION ROUTES ---
@app.route('/missions')
def get_missions():
    """Fetches all mission records and renders the Missions list view."""
    missions = db.session.execute(select(Mission)).scalars().all()
    return render_template('missions.html', missions=missions)

@app.route("/mission/<int:id>")
def single_mission(id):
    """Fetches a specific mission by ID; returns 404 error page if not found."""
    stmt = select(Mission).where(Mission.mission_ID == id)
    mission_item = db.session.execute(stmt).scalar_one_or_none()
    if mission_item is None:
        abort(404)
    return render_template('mission_detail.html', mission=mission_item)

# --- LOCATION ROUTES ---
@app.route('/locations')
def get_locations():
    """Fetches all launch location records and renders the Location list view."""
    locations = db.session.execute(select(Location)).scalars().all()
    return render_template('location.html', locations=locations)

@app.route("/location/<int:id>")
def single_location(id):
    """Fetches a specific location by ID; returns 404 error page if not found."""
    stmt = select(Location).where(Location.location_ID == id)
    location_item = db.session.execute(stmt).scalar_one_or_none()
    if location_item is None:
        abort(404)
    return render_template('location_detail.html', location=location_item)

# --- OVERVIEW / JOINED ROUTE ---
@app.route('/joints')
def get_joints():
    """Fetches joined relational data combining rockets and locations."""
    joints = db.session.execute(select(Joint)).scalars().all()
    return render_template('joint.html', joints=joints)

# 
# 5. FORM SANITIZATION & BACKEND VALIDATION (MIGRATED FROM PHP)
# 

def test_input(data):
    """
    Helper Function: Sanitizes input string data.
    Direct replacement for PHP's custom test_input() function (trim/strip whitespace).
    """
    return data.strip() if data else ""

@app.route("/submit", methods=["GET", "POST"])
def submit_form():
    """
    Handles form submission, validation, error messaging, and dynamic rendering.
    - If POST validation succeeds: Renders 'result.html' displaying submitted data.
    - If POST validation fails: Re-renders 'form.html' showing inline red error messages.
    """
    # Error message dictionary passed to Jinja template
    errors = {
        "firstNameErr": "",
        "lastNameErr": "",
        "emailErr": "",
        "commentErr": "",
    }
    
    # User input value container (retained to refill form on error)
    form_data = {"firstName": "", "lastName": "", "email": "", "comment": ""}

    if request.method == "POST":
        # 1. Validate First Name (Required + Regex check for letters/spaces/hyphens)
        first_name_input = request.form.get("first_name", "")
        if not first_name_input:
            errors["firstNameErr"] = "First Name is Required"
        else:
            form_data["firstName"] = test_input(first_name_input)
            if not re.match(r"^[a-zA-Z\-' ]*$", form_data["firstName"]):
                errors["firstNameErr"] = "Only letters and white space allowed"

        # 2. Validate Last Name (Required + Regex check for letters/spaces/hyphens)
        last_name_input = request.form.get("last_name", "")
        if not last_name_input:
            errors["lastNameErr"] = "Last Name is Required"
        else:
            form_data["lastName"] = test_input(last_name_input)
            if not re.match(r"^[a-zA-Z\-' ]*$", form_data["lastName"]):
                errors["lastNameErr"] = "Only letters and white space allowed"

        # 3. Validate Email Address (Required + Standard RFC Email Regex check)
        email_input = request.form.get("email", "")
        if not email_input:
            errors["emailErr"] = "Email Address is Required"
        else:
            form_data["email"] = test_input(email_input)
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, form_data["email"]):
                errors["emailErr"] = "Invalid Email format"

        # 4. Validate Comment Area (Required check)
        comment_input = request.form.get("comment", "")
        if not comment_input:
            errors["commentErr"] = "Comments are Required"
        else:
            form_data["comment"] = test_input(comment_input)

        # Success Check: If no errors were generated, render result template
        if not any(errors.values()):
            return render_template("result.html", form_data=form_data)

    # Default/Fallback: Return form template with errors and user's inputs prefilled
    return render_template("form.html", errors=errors, form_data=form_data)

# 
# 6. LOCAL DEVELOPMENT SERVER EXECUTION
# 

if __name__ == "__main__":
    # Runs local Flask development server in debug mode
    app.run(debug=True)
