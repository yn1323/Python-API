import urllib.request
import os,json
from flask import Flask, request
from flask_cors import CORS
# パッケージ
from scraping.pog import Pog
from common.msg import Msg


# Flask
app = Flask(__name__)
# 戻りのJSONをasciiにしない
app.config['JSON_AS_ASCII'] = False
CORS(app)

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
def root():
  return "Hello"

@app.route('/pogTop', methods=['POST'])
def pogTop():
  data = conv(request)
  url = data['url']
  if not urlChecker(url):
    return {'ERROR': Msg.common('URL_NOT_FOUND')}
  return Pog(url).top()


@app.route('/pogEachP', methods=['POST'])
def pogEachP():
  data = conv(request)
  url = data['url']
  if not urlChecker(url):
    return {'ERROR': Msg.common('URL_NOT_FOUND')}
  return Pog(url).eachP()


@app.route('/pogHorse', methods=['POST'])
def pogHorse():
  data = conv(request)
  url = data['url']
  if not urlChecker(url):
    return {'ERROR': Msg.common('URL_NOT_FOUND')}
  return Pog(url).horse()


@app.route('/pogRace', methods=['POST'])
def pogRace():
  data = conv(request)
  url = data['url']
  if not urlChecker(url):
    return {'ERROR': Msg.common('URL_NOT_FOUND')}
  return Pog(url).race()


@app.route('/pogRaceEach', methods=['POST'])
def pogRaceEach():
  data = conv(request)
  url = data['url']
  horse = data['horse']
  return Pog(url).raceEach(horse)

# このif文が重要
if __name__ == '__main__':
  # debug=Trueだと自動でリロードする
  # threadeddで並列処理を有効化
  app.run(debug=True, threaded=True, host="0.0.0.0")
