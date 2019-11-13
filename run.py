from dotenv import load_dotenv
from os.path import join, dirname
import os
from flask import Flask
# パッケージ
from scraping import pog
# Flask
app = Flask(__name__)
# .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# URL = os.environ.get("URL") 

@app.route("/")
def hello_world():
  return pog.Pog(os.environ.get("URL")).top()

# このif文が重要
if __name__ == "__main__":
  # debug=Trueだと自動でリロードする
  app.run(debug=True)
