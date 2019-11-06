import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class Scraping:
  def __init__(self, url):
    self.url = url
    self.parsedUrl = urlparse(url)
    self.html = requests.get(self.url)
    self.soup = BeautifulSoup(self.html.content, "html.parser")
  # セレクタで指定した文字を取得
  def getString(self, selector):
    return [item.text.strip() for item in self.soup.select(selector)]
  # セレクタで指定したタグにあるURLを取得
  def getUrl(self, selector):
    path = '{uri.scheme}://{uri.netloc}/'.format(uri = self.parsedUrl)
    return [path + item.get("href") for item in self.soup.select(selector)]
