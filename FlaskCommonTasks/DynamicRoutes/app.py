from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

#the path and filename for the database
DATABASE = "DynamicRoutes/images.db"

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

#Now the cool dynamic route- each image that you click is an anchor tag that 
#passes an id to this route- we then query for THIS item and send just that 
#data to a template.
@app.route('/item/<int:id>')
def item(id):
    sql = "SELECT * FROM item WHERE id=?"
    item = query_db(sql,args=(id,),one=True)
    return render_template('item.html', item=item)


#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)