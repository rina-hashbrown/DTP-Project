from flask import Flask

app = Flask(__name__)


#routes go here
@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)

