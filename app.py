import os
from typing import Optional
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, Column, select
import sqlite3

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

if __name__ == "__main__":
    app.run(debug=True)
