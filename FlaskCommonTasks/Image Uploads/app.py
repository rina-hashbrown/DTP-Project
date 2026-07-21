from flask import Flask, render_template, redirect, request,url_for
import sqlite3   #for the database stuff
#this is to sanitaize the filename so we don;t get hacked!!
from werkzeug.utils import secure_filename


app = Flask(__name__)

#the path and filename for the database
DATABASE = "Image Uploads/database.db"
# the upload folder- relative path from the folder I have open in VSCode
UPLOAD_FOLDER = 'Image Uploads/static/images/'

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
    #now get the filename from the form
    file = request.files['file']
    #should check the file is valid but for simplicity......
    #save the file in the UPLOAD_FOLDER
    filename = secure_filename(file.filename)
    file.save(UPLOAD_FOLDER+filename)
    #now insert into the database
    sql = "INSERT INTO item (name, image_filename) VALUES (?,?);"   #create a query to insert ther data
    query_db(sql,(item,filename))  #execute the query
    return redirect('/') #redirect back to the home page (will display them all)


#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)