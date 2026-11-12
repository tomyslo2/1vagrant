from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Najboljša spletna stran"
