#include the render_template to render tamplates!
from flask import Flask, render_template

app = Flask(__name__)


#routes go here
@app.route('/')
def index():
    #must have a folder called templates in the app folder and you cn render any html in it
    return render_template('index.html')

#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)

