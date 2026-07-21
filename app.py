from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

#initialise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv      

@app.route('/')
def home(): 
    #home page - just the location_id, station and country from location.
    sql = "SELECT location_id, station, country, rocket_status, rocket_name FROM location, rocket;"
    results = query_db(sql)
    return str(results)

@app.route("/rocket/<int:id>")
def rocket(id):
    #just a singular rocket based on id
    sql = """SELECT * FROM rocket INNER JOIN rocket_location ON rocket_location.rocket_ID = rocket.rocket_ID
            WHERE rocket.rocket_ID =?;"""
    result = query_db(sql,(id,),True)
    return str(result)

if __name__ == "__main__":
    app.run(debug=True) 

    
