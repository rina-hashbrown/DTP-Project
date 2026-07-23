from flask import Flask, render_template
import sqlite3

DATABASE = 'database.db'
app = Flask(__name__)

@app.route('/')
def home():
    # Looks inside the 'templates' folder for 'home.html'
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
