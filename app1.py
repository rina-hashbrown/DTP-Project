from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

#initialise app
app = Flask(__name__)

@app.route('/')
def home():
    rocket_list = ["Atlas-D Able", "Soyuz"]
    return render_template('home.html', rockets=rocket_list)