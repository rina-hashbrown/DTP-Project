from flask import Flask, render_template, redirect, request
import sqlite3   #for the database stuff

app = Flask(__name__)

#the path and filename for the database
DATABASE = "database.db"

#cool function to automatcally connect and query
def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results


#routes go here
@app.route('/')
def index():
    results = query_db("SELECT * FROM item")  
    return render_template('index.html',results=results)

#Its common practice to have a post route that just adds stuff to the database and redirects to home
@app.post('/add_item')
def add_item():
    #get the form data from the request object like this
    item = request.form['item_name']
    sql = "INSERT INTO item (item) VALUES (?);"   #create a query to insert ther data
    query_db(sql,(item,))  #execute the query
    return redirect('/') #redirect back to the home page (will display them all)


#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)