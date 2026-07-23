import os
from typing import Optional
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, Column, select

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

# Force SQLAlchemy to read these columns as plain text strings
    time = Column(Text)
    date = Column(Text)
    price = Column(Text)
    
# Define Model inheriting from db.Model

@app.route('/')
def home():
    return render_template('home.html', results=any)

@app.route('/rockets')
def get_rockets():
    rockets = db.session.execute(select(Rocket)).scalars().all()
    return render_template('rockets.html', rockets=rockets)

# Route for the Missions page
@app.route('/missions')
def get_missions():
    missions = db.session.execute(select(Mission)).scalars().all()
    return render_template('missions.html', missions=missions)

if __name__ == "__main__":
    app.run(debug=True)
