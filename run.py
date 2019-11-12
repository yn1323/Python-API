from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
  return "Hello, World!\n"


app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
