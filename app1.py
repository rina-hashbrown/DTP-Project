from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    
    return "Main Page pls work" <h1>Hello<h1>

if __name__ == "__main__":
    app.run()