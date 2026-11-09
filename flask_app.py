from flask import Flask, json
import os
import json

app = Flask(__name__)
@app.route("/")
def Home():
    return "Welcome to the Bank Management System!"

if __name__ == "__main__":
    app.run(debug=True) 