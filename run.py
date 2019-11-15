from dotenv import load_dotenv
from os.path import join, dirname
import urllib.request
import os,json
from flask import Flask, request
# パッケージ
from scraping.pog import Pog
from common.msg import Msg

# Flask
app = Flask(__name__)
# .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# JSON Convert
def conv(req):
  return json.loads(req.data.decode('utf-8'))
# check URL
def urlChecker(url):
  try:
    f = urllib.request.urlopen(url)
    f.close()
    return True
  except:
    return False

@app.route('/')
def hello_world():
  return pog.Pog(os.environ.get('URL')).top()

@app.route('/pogTop', methods=['POST'])
def pogTop():
  data = conv(request)
  url = data['url']
  print(urlChecker(url))
  if not urlChecker(url):
    return {'ERROR': Msg.common('URL_NOT_FOUND')}
  return Pog(url).top()

# このif文が重要
if __name__ == '__main__':
  # debug=Trueだと自動でリロードする
  # threadeddで並列処理を有効化
  app.run(debug=True, threaded=True, host="0.0.0.0")
