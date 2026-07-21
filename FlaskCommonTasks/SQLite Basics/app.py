from flask import Flask, render_template
import sqlite3   #for the database stuff

app = Flask(__name__)

#the path and filename for the database
DATABASE = "database.db"

#routes go here
@app.route('/')
def index():
    #Connect to the datavase file
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()#create the cursor
    sql = "SELECT * FROM item" #store a query as a string variable
    cursor.execute(sql) # execute the query
    results = cursor.fetchall() #fetch all the results of the query (can use fetchone too)
    db.close()    #closr the database now we are done- no need to commit this time with db.commit()
    return render_template('index.html',results=results)  #send the data to the template

#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)
