from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)

#using sessions rquire we set a random secret key
app.config['SECRET_KEY'] = "MySecretKey"

# these are stored server side when hosted. But this is the LEAST secure login method
# hard coded username and passwords to access the 'admin" part of the site 
USERNAME = "admin"
PASSWORD = "admin"

#routes go here
#this is the route taken if we GET from the home page
@app.get('/')
def index():
    return render_template('index.html')

#this route acccepts get AND posts
@app.route('/', methods=["GET","POST"])
def index_post():
    #if we are posting to the route do this stuff
    if request.method == "POST":
        #get the username from the form
        username = request.form['username']
        password = request.form['password']
        #check them here
        if username == USERNAME and password == PASSWORD:
            #we successfully logged in
            #store the username in the session- it's a dictionary that is visible everywhere
            #for the entire time this user has the app open in browser- clears wehn the close the browser
            session['username'] = username
            return redirect("admin")
        #it can be used in the route without having to send it as it is visible in the session
    #regardless of whether we get OR post we render a template
    return render_template('index.html')

@app.route("/admin")
def admin():
    return render_template("admin.html")



#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)